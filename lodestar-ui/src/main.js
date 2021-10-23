import {createApp} from 'vue'
import App from './App.vue'
import {store} from './store/cluster-state-store'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {library} from "@fortawesome/fontawesome-svg-core";
import {
    faChartArea,
    faCompressArrowsAlt,
    faExpandArrowsAlt,
    faLevelDownAlt,
    faTrash,
    faUser,
    faDrawPolygon,
    faDisease,
    faSearchPlus,
    faVectorSquare
} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import VueNextSelect from 'vue-next-select';
import 'vue-next-select/dist/index.min.css';

library.add(faUser);
library.add(faChartArea);
library.add(faTrash);
library.add(faLevelDownAlt);
library.add(faExpandArrowsAlt);
library.add(faCompressArrowsAlt);
library.add(faDrawPolygon);
library.add(faDisease);
library.add(faSearchPlus);
library.add(faVectorSquare);

const app = createApp(App)

app.use(store)
app.component("font-awesome-icon", FontAwesomeIcon)
app.component("vue-select", VueNextSelect)
app.mount('#app')