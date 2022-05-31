import {store} from '../store/cluster-state-store'
import axios from "axios";
import * as d3 from "d3";
import {buildAll, buildSpaceBody, buildVelocityBody} from "./dimension-util";
import {computeColorLabels, createAllLabelsMap, createAlphaColorMap, createColorMap} from "../config/colors";
import {cloneDeep} from "lodash/lang";

export const host = "http://localhost:5000/api/v1/"

export function updateBatch() {
    getCurrentTree();
    getSignificantRoots(store.getters.level);
    updateAllLabels();
    updateCurrentLabels({
        level: store.getters.level,
        alpha: store.getters.alpha
    })
}


function fetchData(endpoint, callback, onFinally) {
    axios.get(host + endpoint)
        .then(callback)
        .catch(error => {
            store.commit('updateErroredScatter', true)
            console.error(error);
        })
        .finally(onFinally);
}

const headers = {}

function postData(endpoint, callback, onFinally, data) {
    axios.post(host + endpoint, data, {headers: headers, method: "post"})
        .then(callback)
        .catch(error => {
            store.commit('updateErroredScatter', true)
            console.error(error);
        })
        .finally(onFinally);
}

export function updateResources() {
    fetchData("resources",
        resp => {
            store.commit('updateResources', resp.data)
        }, () => {
        })
}

export function updateHeatmap() {
    fetchData("heatmap",
        resp => {
            store.commit('updateHeatmap', cloneDeep(resp.data))
        }, () => {
            getSignificantRoots(store.getters.level);
        })
}


export function updateAlphas() {
    fetchData("alphas",
        resp => {
            store.commit('updateAlphas', resp.data)
        }, () => {
        })
}

export function getSignificantRoots(level) {
    postData("trees/significant/roots",
        resp => {
            store.commit('updateSignificantRoots', resp.data)
        }, () => {
            updateAllLabels()
        }, {level: level})
}

export function updateDensityLevels() {
    fetchData("density-levels",
        resp => {
            store.commit('updateDensityLevels', resp.data)
        }, () => {
        })
}

export function updateResourceHeaders(filename) {
    fetchData("resources/" + filename + "/headers", resp => {
        store.commit('updateResourceHeaders', resp.data)
    }, () => {
    })
}

export function getCurrentTree() {
    postData("trees/current", resp => {
        let response = cloneDeep(resp.data)
        let cluster_level_info = response.node_level_clusters
        let allPositions = response.pos

        store.commit('updateColorMap',
            createColorMap(cluster_level_info))

        for (const [key, value] of Object.entries(allPositions)) {
            let node = cluster_level_info[key]
            store.commit("addNode", {
                level: node[0],
                label: node[2],
                color: store.getters.colorMap[node[2]],
                name: node[2],
                size: node[1]
            })
        }

        store.commit('updateNetworkData', response)
    }, () => {
    }, buildAll())
}

export function getAllTrees() {
    fetchData("trees", resp => {
        let response = cloneDeep(resp.data)

        store.commit('updateAlphaColorMap',
            createAlphaColorMap(store.getters.alphas, response))
    }, () => {
        updateHeatmap();
    })
}

export function updateAllLabels() {
    postData("labels/all", resp => {
            let response = cloneDeep(resp.data)
            store.commit('updateAllLabels',
                createAllLabelsMap(store.getters.alphas, response))
        }, () => {
            store.commit('updateLoadingMain', false);
            store.commit('updateCalculated', true);
        },
        {
            level: store.getters.level
        })
}

export function updateNetwork(id) {
    store.commit('updateLoadingMain', true)
    store.commit('updateErroredMain', false)
    store.commit('updateNetworkData', {id: null})

    postData("trees/" + id, resp => {
    }, () => {
        getCurrentTree();
        getAllTrees()
    }, buildAll())
}

export function updateSpace(id, current_cluster = null) {
    store.commit('updateLoadingSpace', true)
    store.commit('updateErroredSpace', false)

    postData("space/" + id,
        resp => {
            store.commit('updateSpace', resp.data)
        },
        () => {
            store.commit('updateLoadingSpace', false);
        }, buildSpaceBody(current_cluster))
}

export function updateVelocity(id) {
    store.commit('updateLoadingVelocity', true)
    store.commit('updateErroredVelocity', false)

    d3.select("#velocity_pane").selectAll("div").remove();

    postData("velocity/" + id,
        resp => {
            store.commit('updateVelocityScatter', resp.data)
        },
        () => {
            store.commit('updateLoadingVelocity', false);
        }, buildVelocityBody())
}

export function updateCurrentLabels(params) {
    store.commit('updateLoadingSpace', true)
    store.commit('updateErroredSpace', false)
    store.commit('updateLoadingVelocity', true)
    store.commit('updateErroredVelocity', false)

    postData("labels", resp => {
        let data = Array.from(resp.data)
        store.commit('updateLabels', data)
        store.commit('updateColorLabels',
            computeColorLabels(resp.data, store.getters.colorMap,
                store.getters.noise))
    }, () => {
        store.commit('updateLoadingVelocity', false);
        store.commit('updateLoadingSpace', false);
    }, params)
}

export function updateCurrentCluster() {
    store.commit('updateLoadingSpace', true)
    store.commit('updateErroredSpace', false)
    store.commit('updateLoadingVelocity', true)
    store.commit('updateErroredVelocity', false)

    let cluster = store.getters.levelSet[store.getters.currentCluster.level]
        [store.getters.currentCluster.label]

    postData("levels/" + store.getters.level + "/cluster/"
        + store.getters.currentCluster.label, resp => {
    }, () => {
        store.commit('updateLoadingVelocity', false);
        store.commit('updateLoadingSpace', false);
    }, {
        custom_label: cluster.label,
        custom_label_name: cluster.name,
        alpha: store.getters.alpha
    })
}

export function updateHrd(id) {
    store.commit('updateLoadingHrd', true)
    store.commit('updateErroredHrd', false)

    postData("hrd/" + id,
        resp => {
            store.commit('updateHrd', resp.data)
        },
        () => {
            store.commit('updateLoadingHrd', false);
        }, store.getters.hrdSelection)
}

export function updateSelection(id) {
    //store.commit('updateLoadingHrd', true)
    //store.commit('updateErroredHrd', false)

    postData("hrd/" + id,
        resp => {
            store.commit('updateSelector', resp.data)
        },
        () => {
            //store.commit('updateLoadingHrd', false);
        }, store.getters.selectorSelection)
}

export function downloadResource(url) {
    store.commit('updateUploadFinished', false)

    postData("downloads", resp => {
        store.commit('updateUploadFinished', true)
    }, () => {

    }, {"url": url})
}