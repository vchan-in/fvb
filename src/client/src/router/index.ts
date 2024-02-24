import { route } from 'quasar/wrappers';
import {
  createMemoryHistory,
  createRouter,
  createWebHashHistory,
  createWebHistory,
} from 'vue-router';

import routes from './routes';
import { useAuthStore } from 'src/stores/auth';
import { Cookies } from 'quasar';
import { api } from 'src/boot/axios';
import { au } from 'app/dist/spa/assets/index.f8127df2';

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory;

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  });

  // Navigation guard to check if authentication is required for a route
  Router.beforeEach(async (to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      try {
        // Check if user is authenticated
        const token = Cookies.get('access_token');
        if (!token) {
          console.log('User is not authenticated!');
          // User is not authenticated, redirect to login page
          next('/login');
        }

        // if token is present, verify it
        if (token) {
          const is_valid = await useAuthStore().verify_token();
          if (!is_valid) {
            console.log('Token is not valid!');
          } else {
            // Add the token to the axios header
            api.defaults.headers.common = { Authorization: `Bearer ${token}` };
          }
        }

        // User is authenticated, then get the user info from the server
        const current_user_info = await useAuthStore().current_user_info();
        if (current_user_info) {
          // Set a global variable
          window.currentUser = currentUsername = useAuthStore().username;
        }

      } catch (error) {
        console.error('Error:', error);
      }
    }
    next();
  });

  return Router;
});
