<template>
  <!-- Login Page -->
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-4">
      <div class="col">
        <q-card class="my-card" flat bordered>
          <q-card-section>
            <div class="text-h6 q-my-lg">
              Welcome back! Please login to continue.
            </div>

            <q-card-section>
              <q-form @submit="login">
                <q-input filled v-model="username" label="Username" lazy-rules
                  :rules="[val => !!val || 'Please enter your username']" type="text" autocomplete="username" />

                <q-input filled v-model="password" label="Password" lazy-rules
                  :rules="[val => !!val || 'Please enter your password']" type="password"
                  autocomplete="current-password" />

                <!-- Forget Password -->
                <q-item clickable v-ripple to="/forgetpassword" exact disable>
                  <q-item-section avatar>
                    <q-icon name="help" />
                  </q-item-section>

                  <q-item-section>
                    Forget Password
                  </q-item-section>
                </q-item>

                <div class="justify-center row">
                  <q-btn class="q-mt-md q-mb-md col-12" color="primary" label="Login" type="submit"
                    :disable="!username || !password" />
                  <div class="text-caption text-center">
                    Don't have an account? <router-link to="/signup">Sign Up here</router-link>.
                  </div>
                </div>
              </q-form>
            </q-card-section>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { Notify } from 'quasar'
import { useRouter } from 'vue-router'


export default {
  name: 'LoginPage',

  setup() {
    const router = useRouter()

    const authStore = useAuthStore();

    const username = ref('');
    const password = ref('');

    // Login user, if successful redirect to home page
    const login = async () => {
      try {
        console.log('FVB_BACKEND_BASEURL:', process.env.FVB_BACKEND_BASEURL);
        console.log('FVB_BACKEND_PORT:', process.env.FVB_BACKEND_PORT);
        if (await authStore.login(username.value, password.value)) {
          Notify.create({
            message: 'Login successful.',
            color: 'positive',
            icon: 'check',
          });

          // Redirect to home page
          router.push('/');
        } else {
          Notify.create({
            message: 'Invalid username or password.',
            color: 'negative',
            icon: 'warning',
          });
        }

      } catch (error) {
        Notify.create({
          message: 'An error occurred while logging in.' + error,
          color: 'negative',
          icon: 'warning',
        });
      }
    };

    return {
      login,
      router,
      authStore,

      username,
      password,
    };
  },


};
</script>
