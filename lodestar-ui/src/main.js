import {createApp} from 'vue'
import router from './router'
import App from './App.vue'
import {store} from './store/cluster-state-store'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'
import {library} from "@fortawesome/fontawesome-svg-core";
import {
    faBraille,
    faChartArea,
    faCompressArrowsAlt,
    faDisease,
    faFileExport,
    faDrawPolygon,
    faExpandArrowsAlt,
    faLevelDownAlt,
    faSearchPlus,
    faTrash,
    faUser,
    faVectorSquare,
    faCheckSquare,
    faBackward,
    faFloppyDisk,
    faArrowsUpDown
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
library.add(faFileExport);
library.add(faCheckSquare);
library.add(faBackward);
library.add(faFloppyDisk);
library.add(faArrowsUpDown);

const app = createApp(App)

app.use(store)
app.use(router)
app.use(VueNumerals, {
    locale: 'en'
});
app.component("font-awesome-icon", FontAwesomeIcon)
app.component("vue-select", VueNextSelect)
app.mount('#app')