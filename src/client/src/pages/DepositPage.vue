<template>
  <q-page class="row justify-evenly q-my-lg">
    <div class="col-12 col-md-8 col-lg-6">
      <q-card flat bordered>
        <q-card-section>
          <section class="q-mb-xl">
            <div class="text-h6">Remote Deposit</div>
            <span class="text-caption">Deposit money from anywhere</span>
          </section>
          <q-tabs v-model="tab" dense class="text-grey" active-color="primary" indicator-color="primary" align="justify"
            narrow-indicator>
            <q-tab name="checkDeposit" label="Check Deposit" />
          </q-tabs>

          <q-separator />

          <q-tab-panels v-model="tab" animated>
            <q-tab-panel name="checkDeposit">
              <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
                <q-select filled v-model="depositData.to_account_id" label="To Account *" lazy-rules
                  :options="accounts.map(account => ({ label: account.id + ' Balance: ' + account.balance, value: account.id }))"
                  :rules="[val => val !== null || 'Please select an account']">
                  <template v-slot:prepend>
                    <q-icon name="account_balance_wallet" />
                  </template>
                </q-select>

                <q-input filled v-model="depositData.amount" label="Amount *" type="number" lazy-rules
                    :rules="[val => val !== null && val !== '' || 'Please enter the amount', val => val <= 10000 || 'Amount should not be greater than 10000']">
                  <template v-slot:prepend>
                    <q-icon name="attach_money" />
                  </template>
                </q-input>

                <q-input filled v-model="depositData.description" label="Description" hint="Enter a description"
                  lazy-rules :rules="[val => val && val.length > 0 || 'Please enter a description']">
                  <template v-slot:prepend>
                    <q-icon name="description" />
                  </template>
                </q-input>

                <q-separator inset />
                <div class="text-uppercase text-subtitle2">Photos of the front and back of the check</div>
                <div class="row justify-between">
                  <div class="col-5">
                    <q-file filled bottom-slots v-model="depositData.check_front" label="Front" counter>
                      <template v-slot:prepend>
                        <q-icon name="cloud_upload" @click.stop.prevent />
                      </template>
                      <template v-slot:append>
                        <q-icon name="close" @click.stop.prevent="depositData.check_front = null" class="cursor-pointer" />
                      </template>

                      <template v-slot:hint>
                        Front page of the check
                      </template>
                    </q-file>
                  </div>
                  <div class="col-5">
                    <q-file filled bottom-slots v-model="depositData.check_back" label="Back" counter>
                      <template v-slot:prepend>
                        <q-icon name="cloud_upload" @click.stop.prevent />
                      </template>
                      <template v-slot:append>
                        <q-icon name="close" @click.stop.prevent="depositData.check_back = null" class="cursor-pointer" />
                      </template>

                      <template v-slot:hint>
                        Back page of the check
                      </template>
                    </q-file>
                  </div>
                </div>


                <div>
                  <q-btn label="Submit" type="submit" color="primary" />
                  <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
                </div>
              </q-form>
            </q-tab-panel>

          </q-tab-panels>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
import { Notify } from 'quasar'
import { api } from 'src/boot/axios';

export default {
  setup() {
    const accounts = ref([])
    const depositData = ref({
      type: 'check',
      amount: '',
      description: 'Remote check deposit',
      to_account_id: '',
      check_front: null,
      check_back: null,

    })

    onMounted(async () => {
      try {
        const accountsResponse = await api.get('/api/v1/accounts/me')
        accounts.value = accountsResponse.data.data.reverse()
      } catch (error) {
        console.error(error)
      }
    })

    return {
      accounts,
      depositData,
      tab: ref('checkDeposit'),
    }
  },

  methods: {
    async onSubmit() {
      try {
        this.depositData.to_account_id = this.depositData.to_account_id.value
        const response = await api.post('/api/v1/deposit/create', this.depositData)
        if (response.status === 201) {
          Notify.create({
            message: 'Deposit successful',
            color: 'positive',
            icon: 'check',
          });
          this.$router.push('/transactions')
        } else {
          throw new Error(response.data.message)
        }
      } catch (error) {
        Notify.create({
          message: 'Deposit failed with error: ' + error,
          color: 'negative',
          icon: 'warning',
        });
      }
    },
    onReset() {
      this.depositData.amount = ''
      this.depositData.description = ''
      this.depositData.to_account_id = ''
    }
  },

  computed: {
  }
}
</script>
