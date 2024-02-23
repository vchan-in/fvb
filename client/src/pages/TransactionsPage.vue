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
        :loading="loading" :rows-per-page-options="[10, 20, 40, 80, 0]" :filter="filter" column-sort-order="ad" />
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted, toRaw } from 'vue'
import { api } from 'src/boot/axios';

export default {
  setup() {
    const columns = [
      {
        name: 'timestamp',
        required: true,
        label: 'Timestamp',
        align: 'left',
        field: 'timestamp',
        format: (val) => new Date(val).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' }),
        sortable: true,
        sort: (a, b) => new Date(b).getTime() - new Date(a).getTime(), // Modified sort function
        sortOrder: 'ad'
      },
      { name: 'from_account_id', align: 'left', label: 'From Account', field: 'from_account_id' },
      { name: 'to_account_id', align: 'left', label: 'To Account', field: 'to_account_id' },
      { name: 'amount', align: 'right', label: 'Amount', field: 'amount', sortable: true },
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
