<template>
  <div class="fullscreen bg-grey text-white text-center q-pa-md flex flex-center">
    <div>
      <div class="text-h1">
        Logout
      </div>

      <div class="text-h4" style="opacity:.4">
        You have been successfully logged out.
      </div>

      <q-btn class="q-mt-xl" color="white" text-color="blue" unelevated to="/login" label="Login" no-caps />
    </div>
  </div>
</template>

<script lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth';

export default {
  setup() {

    onMounted(async () => {
      try {
        useAuthStore().logout()
      } catch (error) {
        console.error(error)
      }
    })

    return {}
  },
}
</script>
