<template>
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-6">
      <div class="col">
        <div class="q-pa-md">
          <q-card class="my-card" flat bordered>
            <q-img
              src="mountains.jpg"
              style="height: 200px"
            />

            <q-card-section>
              <div class="text-h2 q-mt-sm q-mb-xs text-center">
                @{{ user.username || 'error' }}
              </div>
            </q-card-section>

            <q-separator class="q-mb-lg" color="q-gray-2" />

            <q-card-section>
              <q-form @submit="topup">
                <q-input
                  filled
                  v-model="user.username"
                  label="Username"
                  lazy-rules
                  :rules="[
                    (val) => !!val || 'Please enter your username',
                    (val) =>
                      val.length >= 5 ||
                      'Username must be at least 5 characters',
                  ]"
                >
                  <template v-slot:prepend>
                    <q-icon name="account_circle" />
                  </template>
                </q-input>

                <q-input
                  filled
                  v-model="user.email"
                  label="Email"
                  lazy-rules
                  :rules="[
                    (val) => !!val || 'Please enter your email',
                    (val) =>
                      /.+@.+\..+/.test(val) || 'Please enter a valid email',
                  ]"
                >
                  <template v-slot:prepend>
                    <q-icon name="email" />
                  </template>
                </q-input>

                <q-input
                  filled
                  v-model="user.password"
                  label="Password"
                  lazy-rules
                  :rules="[
                    (val) => !!val || 'Please enter your password',
                    (val) =>
                      val.length >= 8 ||
                      'Password must be at least 8 characters',
                  ]"
                  type="password"
                >
                  <template v-slot:prepend>
                    <q-icon name="lock" />
                  </template>
                </q-input>

                <q-input
                  filled
                  v-model="user.dob"
                  label="Date of Birth"
                  class="q-mb-lg"
                  lazy-rules
                  :rules="[
                    (val) => !!val || 'Please enter your date of birth',
                    (val) =>
                      /^\d{4}-\d{2}-\d{2}\ \d{2}:\d{2}$/.test(val) ||
                      'Please enter a valid date in the format YYY-MM-DD HH:mm',
                  ]"
                >
                  <template v-slot:prepend>
                    <q-icon name="event" />
                  </template>
                  <template v-slot:append>
                    <q-icon
                      name="touch_app"
                      class="cursor-pointer"
                      color="primary"
                    >
                      <q-popup-proxy
                        cover
                        transition-show="scale"
                        transition-hide="scale"
                      >
                        <q-date v-model="dob" mask="YYYY-MM-DD HH:mm">
                          <div class="row items-center justify-end">
                            <q-btn
                              v-close-popup
                              label="Close"
                              color="primary"
                              flat
                            />
                          </div>
                        </q-date>
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>

                <q-input
                  filled
                  v-model="user.phone"
                  label="Phone"
                  lazy-rules
                  :rules="[
                    (val) => !!val || 'Please enter your phone',
                    (val) =>
                      val.length >= 10 ||
                      'Phone must be at least 10 characters',
                  ]"
                >
                  <template v-slot:prepend>
                    <q-icon name="phone" />
                  </template>
                </q-input>

                <q-input
                  filled
                  v-model="user.address"
                  label="Address"
                  lazy-rules
                  :rules="[(val) => !!val || 'Please enter your address']"
                >
                  <template v-slot:prepend>
                    <q-icon name="location_on" />
                  </template>
                </q-input>

                <!-- <div class="justify-evenly row">
                  <q-btn
                    class="q-mt-md q-mb-md col-12"
                    color="primary"
                    label="Update"
                    @click="update"
                    :disable="
                      !username ||
                      !email ||
                      !password ||
                      !dob ||
                      !phone ||
                      !address
                    "
                  />
                  <q-btn
                    class="q-ml-sm q-mb-md col-12"
                    label="Reset"
                    type="reset"
                    color="primary"
                    flat
                    disable
                  />
                </div> -->
              </q-form>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue';
import { api } from 'src/boot/axios';
import { useAuthStore } from '../stores/auth';

export default {
  setup() {
    const user = ref({});

    onMounted(async () => {
      try {
        const userResponse = await api.get('/api/v1/users/'+useAuthStore().username+'/info');
        user.value = userResponse.data.data;
      } catch (error) {
        console.error(error);
      }
    });

    return {
      user
    };
  },
};
</script>
