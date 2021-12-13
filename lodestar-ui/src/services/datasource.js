import {store} from '../store/cluster-state-store'
import axios from "axios";
import * as d3 from "d3";
import * as data from './mock-data.json';
import {buildAll, buildSpaceBody, buildVelocityBody} from "./dimension-util";
import {modes} from "./modes";
import {computeColorLabels, createColorMap} from "./colors";

export const host = "http://localhost:5000/api/v1/"


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

export function updateDensityLevels() {
    fetchData("density-levels",
        resp => {
            store.commit('updateDensityLevels', resp.data)
        }, () => {
        })
}

export function updateResourceHeaders(filename) {
    fetchData("resources/" + filename + "/headers",
        resp => {
            store.commit('updateResourceHeaders', resp.data)
        }, () => {
        })
}

export function updateNetwork(id) {
    store.commit('updateLoadingNetwork', true)
    store.commit('updateErroredNetwork', false)
    store.commit('updateNetworkData', {id: null})

    store.commit('updateNetworkData', data)
    store.commit('updateColorMap', createColorMap(data.node_level_clusters))
    store.commit('updateLoadingNetwork', false);
    store.commit('updateCurrentMode', modes.DEFAULT)

    /*postData("networks/" + id,
        resp => {
            store.commit('updateNetworkData', resp.data)
            store.commit('updateCurrentMode', modes.DEFAULT)
            store.commit('updateColorMap', createColorMap(resp.data.node_level_clusters))
        },
        () => {
            store.commit('updateLoadingNetwork', false);
        }, buildAll())*/
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

export function updateCurrentLabels(id, coords) {
    store.commit('updateLoadingSpace', true)
    store.commit('updateErroredSpace', false)
    store.commit('updateLoadingVelocity', true)
    store.commit('updateErroredVelocity', false)

    postData("labels/" + id,
        resp => {
            let data = Array.from(resp.data)
            store.commit('updateLabels', data)
            store.commit('updateColorLabels', computeColorLabels(resp.data,
                store.getters.colorMap, store.getters.noise))
            let cache = store.getters.levelCache
            cache[coords] = data
            store.commit('updateLevelCache', cache);
        },
        () => {
            store.commit('updateLoadingVelocity', false);
            store.commit('updateLoadingSpace', false);
        }, coords)
}

export function updateLabels(id, level) {
    postData("labels/" + id,
        resp => {
            let cache = store.getters.levelCache
            cache[level] = Array.from(resp.data)
            store.commit('updateLevelCache', cache);
        },
        () => {
        }, level)
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

export function updateVelocityNet() {
    store.commit('updateLoadingVelocity', true)
    store.commit('updateErroredVelocity', false)

    d3.select("#velocity_pane").selectAll("div").remove();

    d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/2_TwoNum.csv").then(function (data) {
        store.commit('updateVelocityNetwork', data)
        store.commit('updateLoadingVelocity', false);
    });
}