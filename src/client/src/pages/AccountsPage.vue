<template>
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-6">
      <div class="row justify-between q-mb-lg">
        <div class="col-6 q-pr-md">
          <q-card class="my-card bg-secondary" flat bordered>
            <q-card-section class="bg-secondary text-white">
              <div class="row items-center">
                <div class="col-2">
                  <q-icon name="account_balance" size="3em" />
                </div>
                <div class="col-10">
                  <div class="text-h5 q-ml-md">{{ totalAccounts || "..." }}/5</div>
                  <div class="text-caption q-ml-md">Total Accounts</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-6 q-pl-xs">
          <q-card class="my-card bg-secondary" flat bordered>
            <q-card-section class="bg-secondary text-white">
              <div class="row items-center">
                <div class="col-2">
                  <q-icon name="account_balance_wallet" size="3em" />
                </div>
                <div class="col-10">
                  <div class="text-h5 q-ml-md">{{ totalBalance || "..." }}</div>
                  <div class="text-caption q-ml-md">Total Balance</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <div class="row justify-center q-mb-lg">
        <div class="col-12">
          <q-card class="my-card bg-cyan-6" flat bordered>
            <q-card-section class="bg-cyan-6 text-white">
              <div class="row items-center">
                <div class="col-1">
                  <q-icon name="local_offer" size="3em" />
                </div>
                <div class="col-10">
                  <div class="text-h5 q-ml-md">Welcome Bonus</div>
                  <div class="text-caption q-ml-md">The first account automatically gets a $1000 welcome bonus.</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <q-table flat bordered title="My Accounts" :rows="rows" :columns="columns" color="primary" row-key="name"
        :loading="loading" :rows-per-page-options="[10, 20, 40, 80, 0]" :filter="filter">
        <template v-slot:top>
          <q-btn color="primary" icon="account_balance" :disable="disableAddAccount" label="Add Account" @click="prompt">
            <q-tooltip transition-show="scale" transition-hide="scale">
              You can add up to 5 accounts.
            </q-tooltip>
          </q-btn>
          <q-space />
          <q-btn class="q-ml-sm" color="primary" icon="refresh" :disable="loading" @click="refreshData" />
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { useQuasar, Notify } from 'quasar'
import { ref, onMounted } from 'vue'
import { api } from 'src/boot/axios';
import { useAuthStore } from '../stores/auth';

export default {
  setup() {
    const $q = useQuasar()
    const columns = [
      {
        name: 'id',
        required: true,
        label: 'Account ID',
        align: 'left',
        field: 'id',
        sortable: true
      },
      { name: 'balance', align: 'right', label: 'Balance', field: 'balance', sortable: true },
    ]
    const rows = ref([])
    const totalAccounts = ref(0)
    const totalBalance = ref(0)
    const disableAddAccount = ref(false)

    const refreshData = async () => {
      console.log('Refreshing data...')
      try {
        const accountsResponse = await api.get('/api/v1/accounts/'+useAuthStore().username);
        rows.value = accountsResponse.data.data.reverse()

        totalAccounts.value = accountsResponse.data.data.length
        totalBalance.value = accountsResponse.data.data.reduce((acc, account) => acc + account.balance, 0)

        if (totalAccounts.value >= 5) {
          disableAddAccount.value = true
        }
      } catch (error) {
        console.error(error)
      }
    }


    onMounted(async () => {
      try {
        await refreshData()
      } catch (error) {
        console.error(error)
      }
    })

    return {
      prompt() {
        $q.dialog({
          title: 'Create Account',
          message: 'Are you sure you want to create a new account?',
          confirm: true,
          label: 'Create',
          cancel: true,
          persistent: true
        }).onOk(async () => {
          const accountsCreateResponse = await api.post('/api/v1/account/create');
          if (accountsCreateResponse.status === 201) {
            Notify.create({
              message: 'Account created successfully.',
              color: 'positive',
              icon: 'check',
            });

            refreshData()
          }
        }).onCancel(() => {
          Notify.create({
            message: 'Account creation cancelled.',
            color: 'warning',
            icon: 'warning',
          });
          refreshData()
        })
      },
      refreshData,
      columns,
      rows,
      totalAccounts,
      totalBalance,
      disableAddAccount,
    }
  }
}
</script>
