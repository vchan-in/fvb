import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'IndexPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/IndexPage.vue') }],
    meta: {
      requiresAuth: true,
      title: 'Home',
    },
  },

  // Accounts page
  {
    path: '/accounts',
    name: 'AccountsPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/AccountsPage.vue') }],
    meta: {
      requiresAuth: true,
      title: 'Accounts',
    },
  },

  // Transaction page
  {
    path: '/transactions',
    name: 'TransactionsPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/TransactionsPage.vue') }],
    meta: {
      requiresAuth: true,
      title: 'Transactions',
    },
  },

  // Transfer page
  {
    path: '/transfer',
    name: 'TransferPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/TransferPage.vue') }],
    meta: {
      requiresAuth: true,
      title: 'Transfer',
    },
  },

  // Profile page
  {
    path: '/profile',
    name: 'ProfilePage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/ProfilePage.vue') }],
    meta: {
      requiresAuth: true,
      title: 'Profile',
    },
  },

  {
    path: '/login',
    name: 'LoginPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/LoginPage.vue') }],
    meta: {
      title: 'Account Login',
    },
  },

  // Logout page
  {
    path: '/logout',
    name: 'LogoutPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/LogoutPage.vue') }],
    meta: {
      title: 'Account Logout',
    },
  },

  // Sign up page
  {
    path: '/signup',
    name: 'SignupPage',
    component: () => import('layouts/MainLayout.vue'),
    children: [{ path: '', component: () => import('pages/SignupPage.vue') }],
    meta: {
      title: 'Account Signup',
    },
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
