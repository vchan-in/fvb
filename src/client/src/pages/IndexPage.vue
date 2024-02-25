<template>
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-6">
      <div class="col">
        <!-- Account Balance -->
        <div class="q-pa-md">
          <q-card class="my-card" flat bordered>
            <q-img src="https://cdn.quasar.dev/img/parallax2.jpg" style="height: 100px" />

            <q-card-section>
              <div class="text-overline text-orange-9">Total Balance</div>
              <div class="text-h2 q-mt-sm q-mb-xs">$ {{ totalBalance }}</div>
            </q-card-section>

            <q-card-actions>
              <q-btn flat color="primary" label="All accounts" to="/accounts" />
              <q-btn flat color="secondary" label="Transactions" to="/transactions" />

              <q-space />

              <q-btn color="grey" round flat dense :icon="expanded ? 'keyboard_arrow_up' : 'keyboard_arrow_down'"
                @click="expanded = !expanded" />
            </q-card-actions>

            <q-slide-transition>
              <div v-show="expanded">
                <q-separator />
                <q-card-section class="text-subtitle2">
                  {{ lorem }}
                </q-card-section>
              </div>
            </q-slide-transition>
          </q-card>
        </div>

        <!-- 4 Column Layout with 1 row -->
        <div class="q-pa-md">
          <div class="row">
            <div class="col-6">
              <q-card class="my-card bg-red-1" flat bordered>
                <q-btn flat class="full-width" to="/topup">
                  <q-card-section>
                    <div class="icon text-h5 q-mt-sm q-mb-xs">
                      <q-icon name="account_balance" />
                    </div>
                    <div class="text-h5 q-mt-sm q-mb-xs">TopUp</div>
                    <div class="text-caption text-grey">
                      All networks available
                    </div>
                  </q-card-section>
                </q-btn>
              </q-card>
            </div>

            <div class="col-6">
              <q-card class="my-card bg-blue-1" flat bordered>
                <q-btn flat class="full-width" to="/transfer">
                  <q-card-section>
                    <div class="icon text-h5 q-mt-sm q-mb-xs">
                      <q-icon name="swap_horiz" />
                    </div>
                    <div class="text-h5 q-mt-sm q-mb-xs">Send</div>
                    <div class="text-caption text-grey">
                      Send money to anyone
                    </div>
                  </q-card-section>
                </q-btn>
              </q-card>
            </div>

            <div class="col-6">
              <q-card class="my-card bg-green-1" flat bordered>
                <q-btn flat class="full-width" to="/loan">
                  <q-card-section>
                    <div class="icon text-h5 q-mt-sm q-mb-xs">
                      <q-icon name="local_atm" />
                    </div>
                    <div class="text-h5 q-mt-sm q-mb-xs">Loan</div>
                    <div class="text-caption text-grey">
                      Request for a loan
                    </div>
                  </q-card-section>
                </q-btn>
              </q-card>
            </div>

            <div class="col-6">
              <q-card class="my-card bg-lime-1" flat bordered to="/bills">
                <q-btn flat class="full-width" to="/bills">
                  <q-card-section>
                    <div class="icon text-h5 q-mt-sm q-mb-xs">
                      <q-icon name="receipt" />
                    </div>
                    <div class="text-h5 q-mt-sm q-mb-xs">Bills</div>
                    <div class="text-caption text-grey">
                      Pay your utility bills
                    </div>
                  </q-card-section>
                </q-btn>
              </q-card>
            </div>
          </div>
        </div>

        <!-- Last 5 Transactions -->
        <div class="q-pa-md">
          <q-card class="my-card" flat bordered>
            <q-card-section>
              <div class="text-h6">Last 5 Transactions</div>
            </q-card-section>

            <q-markup-table>
              <thead>
                <tr>
                  <th class="text-left">Timestamp</th>
                  <th class="text-left">From Account</th>
                  <th class="text-left">To Account</th>
                  <th class="text-right">Amount</th>
                  <th class="text-left">Description</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="transaction in transactions" :key="transaction.id">
                  <td class="text-left">{{ transaction.timestamp }}</td>
                  <td class="text-left">{{ transaction.from_account_id }}</td>
                  <td class="text-left">{{ transaction.to_account_id }}</td>
                  <td class="text-right">{{ transaction.amount }}</td>
                  <td class="text-left">{{ transaction.description }}</td>
                </tr>
              </tbody>
            </q-markup-table>
            <q-separator />

            <q-card-actions>
              <q-btn flat color="primary" to="/transactions">
                View all
              </q-btn>
            </q-card-actions>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted, toRaw } from 'vue'
import { api } from 'src/boot/axios';

export default {
  setup() {
    const expanded = ref(false)
    const lorem = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    const accounts = ref({})
    const transactions = ref([])

    onMounted(async () => {
      try {
        const accountsResponse = await api.get('/api/v1/accounts/me')
        accounts.value = accountsResponse.data

        const transactionsResponse = await api.get('/api/v1/transactions/me')
        // Reverse the array and slice to get the last 5 transactions
        let computeLastFiveTransactions = transactionsResponse.data.data.reverse().slice(0, 5)
        // Convert the timestamp to a human readable format
        computeLastFiveTransactions = computeLastFiveTransactions.map(transaction => {
          transaction.timestamp = new Date(transaction.timestamp).toLocaleString('en-US', { dateStyle: 'medium', timeStyle: 'short' })
          return transaction
        })
        transactions.value = computeLastFiveTransactions

      } catch (error) {
        console.error(error)
      }
    })

    return {
      expanded,
      lorem,
      accounts,
      transactions
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

    // Create data for the last 5 transactions table
    lastFiveTransactions(data) {
      ''`
      This is a sample data
      [
        {
          "timestamp": "2024-02-17T17:07:38",
          "id": 6,
          "to_account_id": "VBANK127120240217081416",
          "amount": 0,
          "description": "test",
          "from_account_id": "VBANK101720240217081023"
        },
        {
          "timestamp": "2024-02-17T17:11:08",
          "id": 7,
          "to_account_id": "VBANK127120240217081416",
          "amount": 0,
          "description": "test",
          "from_account_id": "VBANK101720240217081023"
        },
      ]
    ```
      return data.slice(0, 5)
    }
  }
}
</script>
