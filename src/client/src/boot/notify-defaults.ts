import { boot } from 'quasar/wrappers';
import { Notify } from 'quasar';

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async (/* { app, router, ... } */) => {
  // something to do
  Notify.setDefaults({
    position: 'bottom',
    timeout: 2500,
    textColor: 'white',
    actions: [{ icon: 'close', color: 'white' }],
  });
});
