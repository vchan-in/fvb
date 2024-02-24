// Pinia Store for Authentication and Authorization

import { defineStore } from 'pinia';
import { Cookies } from 'quasar';
import { api } from 'src/boot/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: '',
    admin: false,
  }),
  getters: {},
  actions: {
    async login(username: string, password: string): Promise<boolean> {
      const response = await api.post('/api/v1/auth/token', {
        username: username,
        password: password,
      });
      if (response.status === 200) {
        // Set the token in the cookie with a 1 day expiry and secure flag
        Cookies.set('access_token', response.data.access_token, { expires: 1, secure: true, sameSite: 'Strict' });
        return true;
      }

      return false;
    },

    async verify_token(): Promise<boolean> {
      const token = Cookies.get('access_token');
      if (token) {
        try {
          const response = await api.post('/api/v1/auth/token/verify', {
            access_token: token,
            token_type: 'bearer',
          });
          if (response.data.status === 'success') {
            return true;
          }
        } catch (error) {
          console.error('Error:', error);
          return false;
        }
      }
      return false;
    },

    logout() {
      // Remove the token from the cookie
      Cookies.remove('access_token');
      // Clear the entire store
      this.username = '';
      this.admin = false;
    },

    async current_user_info() {
      try {
        const response = await api.get('/api/v1/users/me');
        if (response.status === 200) {
          this.username = response.data.data.username;
          if (response.data.data.admin == 1) {
            this.admin = true;
          }
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
});
