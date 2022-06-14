import {modes} from "../config/modes";
import {updateCurrentLabels} from "./data/datasource";
import {store} from "../store/cluster-state-store";

export function inspect (level, label){
    if(store.getters.currentMode != modes.CLUSTER) {
        store.commit('updatePreviousMode', store.getters.currentMode)
    }
    let cluster = store.getters.levelSet[level][label]

    store.commit('updateCurrentMode', modes.CLUSTER)
    store.commit('updateCurrentClusterLabel', cluster.label)
    store.commit('updateCurrentClusterName', cluster.name != null ? cluster.name : cluster.label)
    store.commit('updateCurrentClusterSize', cluster.size)
    store.commit('updateCurrentClusterLevel', cluster.level)
    store.commit('updateLevel', cluster.level)

    updateCurrentLabels({
        level: cluster.level,
        current_cluster: cluster.label,
        alpha: store.getters.alpha
    })
}