<template>
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-6">
      <div class="row justify-between q-mb-lg">
        <div class="col-6 q-pr-md">
          <q-card class="my-card bg-secondary" flat bordered>
            <q-card-section class="bg-secondary text-white">
              <div class="row items-center">
                <div class="col-2">
                  <q-icon name="swap_horiz" size="3em" />
                </div>
                <div class="col-10">
                  <div class="text-h5 q-ml-md">{{ totalTransactions || "..." }}</div>
                  <div class="text-caption q-ml-md">Total Transactions</div>
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
                  <div class="text-h5 q-ml-md">{{ totalAmountTransferred || "..." }}</div>
                  <div class="text-caption q-ml-md">Total Transferred</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <q-table flat bordered title="My Transactions" :rows="rows" :columns="columns" color="primary" row-key="name"
        :loading="loading" :rows-per-page-options="[10, 20, 40, 80, 0]" :filter="filter">
        <template v-slot:body="props">
          <q-tr :props="props">
            <q-td key="timestamp" :props="props">{{ new Date(props.row.timestamp).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' }) }}</q-td>
            <q-td key="from_account_id" :props="props">{{ props.row.from_account_id }}</q-td>
            <q-td key="to_account_id" :props="props">{{ props.row.to_account_id }}</q-td>
            <q-td key="crdr" :props="props">
              <q-badge :color="props.row.crdr === 'cr' ? 'green' : 'red'">
                {{ props.row.crdr }}
              </q-badge>
            </q-td>
            <q-td key="amount" :props="props">{{ props.row.amount }}</q-td>
            <q-td key="description" :props="props">{{ props.row.description }}</q-td>
          </q-tr>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted, toRaw } from 'vue'
import { api } from 'src/boot/axios';
import { useAuthStore } from '../stores/auth';

export default {
  setup() {
    const columns = [
      {
        name: 'timestamp',
        required: true,
        label: 'Timestamp',
        align: 'left',
        field: row => row.timestamp,
        format: (val) => new Date(val).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' }),
        sortable: true,
      },
      { name: 'from_account_id', align: 'left', label: 'From Account', field: 'from_account_id' },
      { name: 'to_account_id', align: 'left', label: 'To Account', field: 'to_account_id' },
      { name: 'crdr', align: 'left', label: 'CR/DR', field: 'crdr', sortable: true },
      { name: 'amount', align: 'right', label: 'Amount', field: 'amount', sortable: true, format: (val) => `$${val.toFixed(2)}` },
      { name: 'description', align: 'left', label: 'Description', field: 'description' }
    ]
    const rows = ref([])
    const totalTransactions = ref(0)
    const totalAmountTransferred = ref(0)

    onMounted(async () => {
      try {
        const transactionsResponse = await api.get('/api/v1/transactions/me')
        rows.value = transactionsResponse.data.data.reverse()

        totalTransactions.value = transactionsResponse.data.data.length
        totalAmountTransferred.value = transactionsResponse.data.data.reduce((acc, transaction) => acc + transaction.amount, 0)

        const accountsResponse = await api.get('/api/v1/accounts/' + useAuthStore().username);
        const accountsList = toRaw(accountsResponse.data.data);

        // if to_account_id in the transaction is one of account id from accounts response, it is a deposit
        rows.value.forEach(transaction => {
          if (accountsList.some(account => account.id === transaction.to_account_id)) {
            rows.value[rows.value.indexOf(transaction)].crdr = 'cr'
          } else {
            rows.value[rows.value.indexOf(transaction)].crdr = 'dr'
          }
        }


        );

      } catch (error) {
        console.error(error)
      }
    })

    return {
      columns,
      rows,
      totalTransactions,
      totalAmountTransferred
    }
  },

  computed: {
    totalBalance() {
      let total = 0;
      const accountsList = toRaw(this.accounts.data)
      if (accountsList && accountsList.length > 0) {
        accountsList.forEach(account => {
          total += account.balance
        })
      }
      return total
    },
  }
}
</script>
