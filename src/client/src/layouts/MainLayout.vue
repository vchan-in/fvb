<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-primary text-white">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <q-toolbar-title>
          {{ currentUser ? 'Hi, ' + currentUser : 'vBank' }}
        </q-toolbar-title>
        <div class="text-subtitle2">{{ todaysDate }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      :width="250"
      :breakpoint="600"
    >
      <q-scroll-area
        style="
          height: calc(100% - 10em);
          margin-top: 10em;
          border-right: 1px solid #ddd;
        "
      >
        <q-list padding>
          <q-item clickable v-ripple to="/" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="home" />
            </q-item-section>

            <q-item-section> Dashboard </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/accounts" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="account_balance" />
            </q-item-section>

            <q-item-section> Accounts </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/transfer" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="send" />
            </q-item-section>

            <q-item-section> Send Money </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/transactions"
            exact
            v-if="currentUser"
          >
            <q-item-section avatar>
              <q-icon name="swap_horiz" />
            </q-item-section>

            <q-item-section> Transactions </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/deposit"
            exact
            disable
            v-if="currentUser"
          >
            <q-item-section avatar>
              <q-icon name="add" />
            </q-item-section>

            <q-item-section> Deposit </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/cards"
            exact
            disable
            v-if="currentUser"
          >
            <q-item-section avatar>
              <q-icon name="credit_card" />
            </q-item-section>

            <q-item-section> Cards </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/loan"
            exact
            disable
            v-if="currentUser"
          >
            <q-item-section avatar>
              <q-icon name="credit_card" />
            </q-item-section>

            <q-item-section> Loan </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/bills"
            exact
            disable
            v-if="currentUser"
          >
            <q-item-section avatar>
              <q-icon name="receipt" />
            </q-item-section>

            <q-item-section> Bills </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/profile" exact v-if="currentUser">
            <q-item-section avatar>
              <q-icon name="person" />
            </q-item-section>

            <q-item-section> My Profile </q-item-section>
          </q-item>

          <q-item
            clickable
            v-ripple
            to="/admin"
            exact
            v-if="currentUser && isAdmin"
          >
            <q-item-section avatar>
              <q-icon name="admin_panel_settings" />
            </q-item-section>

            <q-item-section> Admin </q-item-section>
          </q-item>

          <q-separator class="q-mb-sm" v-if="currentUser" />

          <q-item
            clickable
            class="bg-red-1 text-red"
            v-ripple
            to="/logout"
            exact
            v-if="currentUser"
          >
            <q-item-section avatar>
              <q-icon name="logout" />
            </q-item-section>

            <q-item-section> Logout </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/login" exact v-if="!currentUser">
            <q-item-section avatar>
              <q-icon name="login" />
            </q-item-section>

            <q-item-section> Login </q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/signup" exact v-if="!currentUser">
            <q-item-section avatar>
              <q-icon name="person_add" />
            </q-item-section>

            <q-item-section> Sign Up </q-item-section>
          </q-item>
        </q-list>

        <q-item class="absolute-bottom">
          <q-item-section avatar>
            <q-icon name="info" />
          </q-item-section>

          <q-item-section>
            <q-item-label>
              vBank &copy; 2024
            </q-item-label>
            <q-item-label caption v-if="checkPing">
              <q-icon name="check" color="green" />
              <span>Server Online</span>
            </q-item-label>
          </q-item-section>
        </q-item>
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
      <q-pull-to-refresh @refresh="refresh">
        <router-view />
      </q-pull-to-refresh>
    </q-page-container>
  </q-layout>
</template>

<script>
import { date } from 'quasar';
import { defineComponent } from 'vue';
import { useAuthStore } from '../stores/auth';
import { api } from 'src/boot/axios';

export default defineComponent({
  name: 'MainLayout',

  data() {
    return {
      leftDrawerOpen: false,
    };
  },

  setup() {
    return {
      refresh (done) {
        setTimeout(() => {
            location.reload();
          done()
        }, 1000)
      }
    }
  },

  computed: {
    todaysDate() {
      let timeStamp = Date.now();
      return date.formatDate(timeStamp, 'dddd D MMMM');
    },
    currentUser() {
      return useAuthStore().username;
    },
    isAdmin() {
      return useAuthStore().admin;
    },
    checkPing() {
      return async () => {
        const pingResponse = await api.get('/api/v1/ping');
        return pingResponse.status === 200;
      };
    },
  },
});
</script>
