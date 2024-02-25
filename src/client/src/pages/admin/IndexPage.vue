<template>
  <div class="q-pa-md">
    <div class="q-gutter-y-md">
      <q-tabs
        v-model="tab"
        dense
        class="text-grey"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="overview" label="Overview" />
        <q-tab name="users" label="Users" />
        <q-tab name="accounts" label="Accounts" />
        <q-tab name="transactions" label="Transactions" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="overview">
          <div class="col-12 col-md-8 col-lg-6">
            <q-card-section>
              <div class="text-h6">Overview</div>
              <span class="text-subtitle1">
                Welcome to the admin dashboard. Here you can view and manage
                users, accounts, and transactions.
              </span>
            </q-card-section>
            <div class="col">
              <!-- Info Cards -->
              <div class="q-pa-md">
                <q-card class="my-card" flat bordered>
                  <q-card-section>
                    <div class="row justify-between">
                      <div class="col-auto q-mb-md">
                        <q-icon name="people" size="3em" />
                        <div class="text-h5">Users</div>
                        <div class="text-h3">
                          {{ users.length || 0 }}
                        </div>
                      </div>
                      <div class="col-auto q-mb-md">
                        <q-icon name="account_balance" size="3em" />
                        <div class="text-h5">Accounts</div>
                        <div class="text-h3">
                          {{ accounts.length || 0 }}
                        </div>
                      </div>
                      <div class="col-auto q-mb-md">
                        <q-icon name="swap_horiz" size="3em" />
                        <div class="text-h5">Transactions</div>
                        <div class="text-h3">
                          {{ transactions.length || 0 }}
                        </div>
                      </div>
                      <div class="col-auto q-mb-md">
                        <q-icon name="account_balance_wallet" size="3em" />
                        <div class="text-h5">Holding</div>
                        <div class="text-h3">${{ totalBalance }}</div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
              <!-- End of Info Cards -->
            </div>
          </div>
        </q-tab-panel>

        <q-tab-panel name="users">
          <q-card-section>
              <div class="text-h6">Users</div>
              <span class="text-subtitle1">
                Here you can view all users registered on the platform.
              </span>
            </q-card-section>
          <div class="col-12 col-md-8 col-lg-6">
            <q-table
              flat
              bordered
              :rows="usersRows"
              :columns="usersColumns"
              color="primary"
              row-key="id"
              :loading="loading"
              :rows-per-page-options="[10, 20, 40, 80, 0]"
              :filter="filter"
            />
          </div>
        </q-tab-panel>

        <q-tab-panel name="accounts">
          <q-card-section>
              <div class="text-h6">Accounts</div>
              <span class="text-subtitle1">
                Here you can view all accounts created by users.
              </span>
            </q-card-section>
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
                        <div class="text-h5 q-ml-md">
                          {{ accounts.length || 0 }}
                        </div>
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
                        <div class="text-h5 q-ml-md">
                          {{ totalBalance || 0 }}
                        </div>
                        <div class="text-caption q-ml-md">Total Balance</div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>

            <q-table
              flat
              bordered
              :rows="accountsRows"
              :columns="accountsColumns"
              color="primary"
              row-key="name"
              :loading="loading"
              :rows-per-page-options="[10, 20, 40, 80, 0]"
              :filter="filter"
            >
            </q-table>
          </div>
        </q-tab-panel>

        <q-tab-panel name="transactions">
          <q-card-section>
            <div class="text-h6">Transactions</div>
            <span class="text-subtitle1">
              Here you can view all transactions made by users.
            </span>
          </q-card-section>
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
                        <div class="text-h5 q-ml-md">
                          {{ transactions.length || '...' }}
                        </div>
                        <div class="text-caption q-ml-md">
                          Total Transactions
                        </div>
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
                        <div class="text-h5 q-ml-md">
                          {{ totalAmountTransferred || '...' }}
                        </div>
                        <div class="text-caption q-ml-md">
                          Total Transferred
                        </div>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>

            <q-table
              flat
              bordered
              :rows="transactionsRows"
              :columns="transactionsColumns"
              color="primary"
              row-key="name"
              :loading="loading"
              :rows-per-page-options="[10, 20, 40, 80, 0]"
              :filter="filter"
              column-sort-order="ad"
            />
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import { api } from 'src/boot/axios';

export default {
  setup() {
    const users = ref([]);
    const accounts = ref({});
    const transactions = ref([]);
    const totalAmountTransferred = ref(0);
    const tab = ref('overview');

    const usersColumns = [
      {
        name: 'id',
        required: true,
        label: 'ID',
        align: 'left',
        field: 'id',
        sortable: true,
      },
      {
        name: 'username',
        align: 'left',
        label: 'Username',
        field: 'username',
      },
      {
        name: 'email',
        align: 'left',
        label: 'Email',
        field: 'email',
      },
      {
        name: 'phone',
        align: 'left',
        label: 'Phone',
        field: 'phone',
      },
      {
        name: 'dob',
        align: 'left',
        label: 'DOB',
        field: 'dob',
      },
      {
        name: 'address',
        align: 'left',
        label: 'Address',
        field: 'address',
      },
      {
        name: 'admin',
        align: 'left',
        label: 'Admin',
        field: 'admin',
      },
    ];
    const usersRows = ref([]);

    const accountsColumns = [
      {
        name: 'id',
        required: true,
        label: 'ID',
        align: 'left',
        field: 'id',
        sortable: true,
      },
      {
        name: 'userId',
        align: 'left',
        label: 'User ID',
        field: 'userId',
      },
      {
        name: 'balance',
        align: 'right',
        label: 'Balance',
        field: 'balance',
        sortable: true,
      },
    ];
    const accountsRows = ref([]);

    const transactionsColumns = [
      {
        name: 'timestamp',
        required: true,
        label: 'Timestamp',
        align: 'left',
        field: 'timestamp',
        format: (val) =>
          new Date(val).toLocaleString('en-US', {
            dateStyle: 'medium',
            timeStyle: 'short',
          }),
        sortable: true,
        sort: (a, b) => new Date(b).getTime() - new Date(a).getTime(), // Modified sort function
        sortOrder: 'ad',
      },
      {
        name: 'from_account_id',
        align: 'left',
        label: 'From Account',
        field: 'fromAccount',
      },
      {
        name: 'to_account_id',
        align: 'left',
        label: 'To Account',
        field: 'toAccount',
      },
      {
        name: 'amount',
        align: 'right',
        label: 'Amount',
        field: 'amount',
        sortable: true,
      },
      {
        name: 'description',
        align: 'left',
        label: 'Description',
        field: 'description',
      },
    ];
    const transactionsRows = ref([]);

    onMounted(async () => {
      try {
        const usersResponse = await api.post('/graphql', {
          query: `
            query MyQuery {
              getAllUsers {
                address
                admin
                dob
                email
                id
                phone
                username
              }
            }
          `,
        });
        users.value = usersResponse.data.data.getAllUsers;
        usersRows.value = usersResponse.data.data.getAllUsers;

        const accountsResponse = await api.post('/graphql', {
          query: `
            query MyQuery {
              getAllAccounts {
                balance
                id
                userId
              }
            }
          `,
        });
        accounts.value = accountsResponse.data.data.getAllAccounts;
        accountsRows.value = accountsResponse.data.data.getAllAccounts;

        const transactionsResponse = await api.post('/graphql', {
          query: `
            query MyQuery {
              getAllTransactions {
                amount
                description
                fromAccount
                toAccount
                timestamp
              }
            }
          `,
        });
        transactions.value = transactionsResponse.data.data.getAllTransactions;
        transactionsRows.value =
          transactionsResponse.data.data.getAllTransactions.reverse();
        totalAmountTransferred.value =
          transactionsResponse.data.data.getAllTransactions.reduce(
            (acc, transaction) => acc + transaction.amount,
            0
          );
      } catch (error) {
        console.error(error);
      }
    });

    return {
      tab,
      users,
      usersColumns,
      usersRows,

      accounts,
      accountsColumns,
      accountsRows,

      transactions,
      totalAmountTransferred,
      transactionsColumns,
      transactionsRows,
    };
  },

  computed: {
    totalBalance() {
      let total = 0;
      const accounts = this.accounts;
      if (accounts && accounts.length > 0) {
        accounts.forEach((account) => {
          total += account.balance;
        });
      }
      return total;
    },

    // Create data for the last 5 transactions table
    lastFiveTransactions(data) {
      return data.slice(0, 5);
    },
  },
};
</script>
