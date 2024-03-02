/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'
import vue3GoogleLogin from 'vue3-google-login'
const app = createApp(App)
app.use(vue3GoogleLogin, {
    clientId: '456578524163-nte2rni7bdabpi600mr4nnm9q2rjp9co.apps.googleusercontent.com'
})


registerPlugins(app)

app.mount('#app')
