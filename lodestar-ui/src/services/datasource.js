import {store} from '../store/cluster-state-store'
import axios from "axios";
import * as d3 from "d3";

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

export function updateResources() {
    fetchData("resources",
        resp => {
            store.commit('updateResources', resp.data)
        }, () => {
        })
}

export function updateScatter(id) {
    store.commit('updateLoadingScatter', true)
    store.commit('updateErroredScatter', false)

    prepareView("#scatter_pane")

    fetchData("scatters/" + id,
        resp => {
            store.commit('updatePlot', resp.data)
        },
        () => {
            store.commit('updateLoadingScatter', false);
        })
}

export function updateNetwork(id) {
    store.commit('updateLoadingNetwork', true)
    store.commit('updateErroredNetwork', false)

    prepareView("#network_pane")

    fetchData("networks/" + id,
        resp => {
            store.commit('updateNetwork', resp.data)
        },
        () => {
            store.commit('updateLoadingNetwork', false);
        })
}

export function prepareView(name) {
    d3.select(name).selectAll("svg").remove();
}