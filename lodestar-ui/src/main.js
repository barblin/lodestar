import {createApp} from 'vue'
import App from './App.vue'
import {store} from './store/cluster-state-store'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {library} from "@fortawesome/fontawesome-svg-core";
import {
    faBraille,
    faChartArea,
    faCompressArrowsAlt,
    faDisease,
    faDownload,
    faDrawPolygon,
    faExpandArrowsAlt,
    faLevelDownAlt,
    faSearchPlus,
    faTrash,
    faUser,
    faVectorSquare
} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import VueNextSelect from 'vue-next-select';
import 'vue-next-select/dist/index.min.css';
import VueNumerals from 'vue-numerals';

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
library.add(faBraille);
library.add(faDownload);

const app = createApp(App)

app.use(store)
app.use(VueNumerals, {
    locale: 'en'
});
app.component("font-awesome-icon", FontAwesomeIcon)
app.component("vue-select", VueNextSelect)
app.mount('#app')