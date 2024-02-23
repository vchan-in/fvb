<template>
  <!-- Signup Page -->
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-4">
      <div class="column" style="height: 150px">
        <div class="col">
          <q-card class="my-card" flat bordered>
            <q-card-section>
              <div class="text-h6 q-my-lg">
                Let's get started by filling out the form below.
              </div>

              <q-input filled v-model="username" label="Username" lazy-rules :rules="[
                val => !!val || 'Please enter your username',
                val => val.length >= 5 || 'Username must be at least 5 characters',
              ]">
                <template v-slot:prepend>
                  <q-icon name="account_circle" />
                </template>
              </q-input>

              <q-input filled v-model="email" label="Email" lazy-rules :rules="[
                val => !!val || 'Please enter your email',
                val => /.+@.+\..+/.test(val) || 'Please enter a valid email',
              ]">
                <template v-slot:prepend>
                  <q-icon name="email" />
                </template>
              </q-input>

              <q-input filled v-model="password" label="Password" lazy-rules :rules="[
                val => !!val || 'Please enter your password',
                val => val.length >= 8 || 'Password must be at least 8 characters',
              ]" type="password">
                <template v-slot:prepend>
                  <q-icon name="lock" />
                </template>
              </q-input>

              <q-input filled v-model="dob" label="Date of Birth" class="q-mb-lg" lazy-rules :rules="[
                val => !!val || 'Please enter your date of birth',
                val => /^\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}$/.test(val) || 'Please enter a valid date in the format YYY-MM-DD HH:mm',
              ]">
                <template v-slot:prepend>
                  <q-icon name="event" />
                </template>
                <template v-slot:append>
                  <q-icon name="touch_app" class="cursor-pointer" color="primary">
                    <q-popup-proxy cover transition-show="scale" transition-hide="scale">
                      <q-date v-model="dob" mask="YYYY-MM-DD HH:mm">
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Close" color="primary" flat />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>

              <q-input filled v-model="phone" label="Phone" lazy-rules :rules="[
                val => !!val || 'Please enter your phone',
                val => val.length >= 10 || 'Phone must be at least 10 characters',
              ]">
                <template v-slot:prepend>
                  <q-icon name="phone" />
                </template>
              </q-input>

              <q-input filled v-model="address" label="Address" lazy-rules
                :rules="[val => !!val || 'Please enter your address']">
                <template v-slot:prepend>
                  <q-icon name="location_on" />
                </template>
              </q-input>


              <div class="justify-evenly row">
                <q-btn class="q-mt-md q-mb-md col-12" color="primary" label="Signup" @click="register"
                  :disable="!username || !email || !password || !dob || !phone || !address" />
                <q-btn class="q-ml-sm q-mb-md col-12" label="Reset" type="reset" color="primary" flat disable />
                <div class="text-caption text-center">
                  Already have an account? <router-link to="/login">Login here</router-link>.
                </div>
              </div>

            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref } from 'vue';
import { api } from 'src/boot/axios';
import { Notify } from 'quasar'
import { useRouter } from 'vue-router'

export default {
  name: 'SignupPage',

  setup() {
    const router = useRouter();

    const username = ref('');
    const email = ref('');
    const password = ref('');
    const dob = ref('');
    const phone = ref('');
    const address = ref('');

    // Register user
    const register = async () => {
      try {
        const registerResponse = await api.post('/api/v1/user/create', {
          admin: 0,
          username: username.value,
          email: email.value,
          password: password.value,
          dob: dob.value,
          phone: phone.value,
          address: address.value,
        });

        if (registerResponse.status === 201) {
          Notify.create({
            message: 'Account created successfully. Please login to continue.',
            color: 'positive',
            icon: 'check',
          });

          // Redirect to login page
          router.push('/login');
        }

        if (registerResponse.status === 400) {
          Notify.create({
            message: this.register_response.data.message,
            color: 'negative',
            icon: 'warning',
          });
        }
      } catch (error) {
        Notify.create({
          message: 'Error creating account. Please try again later.',
          color: 'negative',
          icon: 'warning',
        });
      }
    };

    return {
      username,
      email,
      password,
      dob,
      phone,
      address,
      register,
    };
  },
};
</script>
