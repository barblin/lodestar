import {createStore} from 'vuex'

export const store = createStore({
    state: {
        currentViewSelection: null,
        currentResource: "Choose resource file",

        loadingScatter: false,
        erroredScatter: false,
        loadingNetwork: false,
        erroredNetwork: false,

        plotData: 0,
        network: 0,
        resources: [],
        overallTime: 0,

        width: 600,
        height: 440,
    },
    mutations: {
        updateCurrentViewSelection(state, selection) {
            state.currentViewSelection = selection
        },
        updateLoadingScatter(state, isLoading) {
            state.loadingScatter = isLoading
        },
        updateErroredScatter(state, hadError) {
            state.erroredScatter = hadError
        },
        updateLoadingNetwork(state, isLoading) {
            state.loadingNetwork = isLoading
        },
        updateErroredNetwork(state, hadError) {
            state.erroredNetwork = hadError
        },
        updatePlot(state, data) {
            state.plotData = data
        },
        updateNetwork(state, data) {
            state.network = data
        },
        overallTime(state, time) {
            state.overallTime = time.toFixed(9)
        },
        height(state, height) {
            state.height = height
        },
        width(state, width) {
            state.width = width
        },
        updateResources(state, data) {
            state.resources = data
        },
        updateCurrentResource(state, data) {
            state.currentResource = data
        },
    },
    getters: {
        currentViewSelection: state => state.currentViewSelection,

        loadingScatter: state => state.loadingScatter,
        erroredScatter: state => state.erroredScatter,
        loadingNetwork: state => state.loadingNetwork,
        erroredNetwork: state => state.erroredNetwork,

        loadingAny: state => state.loadingScatter || state.loadingNetwork,

        plotData: state => state.plotData,
        network: state => state.network,

        overallTime: state => state.overallTime,

        width: state => state.width,
        height: state => state.height,

        resources: state => state.resources,
        currentResource: state => state.currentResource
    }
})