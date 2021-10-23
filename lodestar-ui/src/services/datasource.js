import {store} from '../store/cluster-state-store'
import axios from "axios";
import * as d3 from "d3";
import * as data from './mock-data.json';
import {buildSpaceBody, buildVelocityBody} from "./dimension-util";

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

export function updateResourceHeaders(filename) {
    fetchData("resources/" + filename + "/headers",
        resp => {
            console.log(resp.data)
            store.commit('updateResourceHeaders', resp.data)
        }, () => {
        })
}

export function updateNetwork(id) {
    store.commit('updateLoadingNetwork', true)
    store.commit('updateErroredNetwork', false)
    store.commit('updateNetworkData', {id: null})

    store.commit('updateNetworkData', data)
    store.commit('updateLoadingNetwork', false);

    /*fetchData("networks/" + id,
        resp => {
            store.commit('updateNetwork', resp.data)
        },
        () => {
            store.commit('updateLoadingNetwork', false);
        })*/
}

export function updateSpace(id) {
    store.commit('updateLoadingSpace', true)
    store.commit('updateErroredSpace', false)

    postData("space/" + id,
        resp => {
            store.commit('updateSpace', resp.data)
        },
        () => {
            store.commit('updateLoadingSpace', false);
        }, buildSpaceBody())
}

export function updateVelocityScatter(id) {
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