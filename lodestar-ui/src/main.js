import {createApp} from 'vue'
import App from './App.vue'
import {store} from './store/cluster-state-store'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {library} from "@fortawesome/fontawesome-svg-core";
import {faChartArea, faUser} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import VueNextSelect from 'vue-next-select';
import 'vue-next-select/dist/index.min.css';


library.add(faUser);
library.add(faChartArea);

const app = createApp(App)

app.use(store)
app.component("font-awesome-icon", FontAwesomeIcon)
app.component("vue-select", VueNextSelect)
app.mount('#app')