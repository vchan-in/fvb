<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="leftDrawerOpen = !leftDrawerOpen" />
        <q-toolbar-title>
            {{ currentUser ? 'Hi, ' + currentUser : 'vBank' }}
        </q-toolbar-title>
        <div class="text-subtitle2">{{ todaysDate }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above :width="250" :breakpoint="600">
      <q-scroll-area style="height: calc(100% - 10em); margin-top: 10em; border-right: 1px solid #ddd">
        <q-list padding>
          <q-item clickable v-ripple to="/" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>

            <q-item-section>
              Dashboard
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/accounts" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="account_balance" />
            </q-item-section>

            <q-item-section>
              Accounts
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/transfer" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="send" />
            </q-item-section>

            <q-item-section>
              Send Money
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/transactions" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="swap_horiz" />
            </q-item-section>

            <q-item-section>
              Transactions
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/topup" exact disable v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="add" />
            </q-item-section>

            <q-item-section>
              Top Up
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/cards" exact disable v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="credit_card" />
            </q-item-section>

            <q-item-section>
              Cards
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/loan" exact disable v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="credit_card" />
            </q-item-section>

            <q-item-section>
              Loan
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/bills" exact disable v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="receipt" />
            </q-item-section>

            <q-item-section>
              Bills
            </q-item-section>
          </q-item>

          <q-separator class="q-mb-sm" v-if="currentUser"/>

          <q-item clickable class="bg-red-1 text-red" v-ripple to="/logout" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="logout" />
            </q-item-section>

            <q-item-section>
              Logout
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/login" exact v-if="!currentUser">
            <q-item-section avatar>
              <q-icon name="login" />
            </q-item-section>

            <q-item-section>
              Login
            </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/signup" exact v-if="!currentUser">
            <q-item-section avatar>
              <q-icon name="person_add" />
            </q-item-section>

            <q-item-section>
              Sign Up
            </q-item-section>
          </q-item>

        </q-list>
      </q-scroll-area>

      <q-img class="absolute-top" src="mountains.jpg" style="height: 10em">
        <div class="absolute-bottom bg-primary">
          <q-icon name="account_balance" size="4em" />
          <div class="text-h5 text-weight-bold">vBank</div>
          <div class="text-italic">Bank with Confidence</div>
        </div>
      </q-img>
    </q-drawer>

    <q-page-container>
        <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { date, Notify } from 'quasar'
import { defineComponent, ref, onMounted } from 'vue'
import { api } from 'src/boot/axios';
import { useAuthStore } from '../stores/auth';

export default defineComponent({
  name: 'MainLayout',

  data() {
    return {
      leftDrawerOpen: false,
    }
  },

  // setup() {
  //   let currentUsername = useAuthStore().username

  //   onMounted(async () => {
  //     try {
  //       const userResponse = await api.get('/api/v1/users/me');
  //       currentUsername.value = userResponse.data.data.username;
  //       if (userResponse.status === 200) {
  //         Notify.create({
  //           message: 'Welcome back, ' + userResponse.data.data.username,
  //           color: 'positive',
  //           icon: 'check',
  //         });
  //       }
  //     } catch (error) {
  //       console.error(error);
  //     }
  //   });

  //   return {
  //     currentUsername,
  //   }
  // },

  computed: {
    todaysDate() {
      let timeStamp = Date.now()
      return date.formatDate(timeStamp, 'dddd D MMMM')
    },
    currentUser() {
      return useAuthStore().username
    },
  },

});
</script>
