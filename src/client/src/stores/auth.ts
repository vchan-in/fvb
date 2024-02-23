// Pinia Store for Authentication and Authorization

import { defineStore } from 'pinia';
import { Cookies } from 'quasar';
import { api } from 'src/boot/axios';

/*
POST /api/v1/auth/token

Request
 {
    "username": "vaishno",
    "password":"qwerty"
 }

Response
  {
    "access_token": access_token,
    "token_type": "bearer"
  }
*/


export const useAuthStore = defineStore('auth', {
  state: () => ({
    access_token: '',
  }),
  getters: {
    get_access_token: (state) => state.access_token,
  },
  actions: {
    set_access_token(token: string) {
      this.access_token = token;
      // Set the token in the Authorization header
      api.defaults.headers.common.Authorization = `Bearer ${token}`;
    },

    async login(username: string, password: string): Promise<boolean> {
      const response = await api.post('/api/v1/auth/token', {
        username: username,
        password: password,
      });
      if (response.status === 200) {
        // Set the token in the cookie with a 1 day expiry
        Cookies.set('access_token', response.data.access_token, { expires: 1 });
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
      // Remove the token from the store
      this.set_access_token('');
    },
  },
});
