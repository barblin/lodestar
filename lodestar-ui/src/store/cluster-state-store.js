import {createStore} from 'vuex'
import {modes} from "../services/modes"

export const store = createStore({
    state: {
        currentViewSelection: null,
        currentResource: "Choose resource file",
        currentMode: modes.DEFAULT,

        loadingScatter: false,
        erroredScatter: false,
        loadingNetwork: false,
        erroredNetwork: false,
        loadingSpace: false,
        erroredSpace: false,
        loadingVelocity: false,
        erroredVelocity: false,

        plotData: {},
        spaceData: {},
        velocityScatterData: {},
        velocityNetworkData: {},
        network: 0,
        resources: [],
        overallTime: 0,

        width: 600,
        height: 440,


        // space controls
        drawSpaceNet: false,
        drawSpaceScatter: true,

        drawVelocityNet: false,
        drawVelocityScatter: true,
    },
    mutations: {
        updateCurrentViewSelection(state, selection) {
            state.currentViewSelection = selection
        },
        updateCurrentMode(state, mode) {
            state.currentMode = mode
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
        updateSpace(state, data) {
            state.spaceData = data
        },
        updateVelocityScatter(state, data) {
            state.velocityScatterData = data
        },
        updateVelocityNetwork(state, data) {
            state.velocityNetworkData = data
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
        updateDrawSpaceNet(state, data) {
            state.drawSpaceNet = data
        },
        updateDrawSpaceScatter(state, data) {
            state.drawSpaceScatter = data
        },
        updateDrawVelocityNet(state, data) {
            state.drawVelocityNet = data
        },
        updateDrawVelocityScatter(state, data) {
            state.drawVelocityScatter = data
        },
        updateLoadingSpace(state, isLoading) {
            state.loadingSpace = isLoading
        },
        updateErroredSpace(state, hadError) {
            state.erroredSpace = hadError
        },
        updateLoadingVelocity(state, isLoading) {
            state.loadingVelocity = isLoading
        },
        updateErroredVelocity(state, hadError) {
            state.erroredVelocity = hadError
        },
    },
    getters: {
        currentViewSelection: state => state.currentViewSelection,
        currentMode: state => state.currentMode,

        loadingScatter: state => state.loadingScatter,
        erroredScatter: state => state.erroredScatter,
        loadingNetwork: state => state.loadingNetwork,
        erroredNetwork: state => state.erroredNetwork,
        loadingSpace: state => state.loadingSpace,
        erroredSpace: state => state.erroredSpace,
        loadingVelocity: state => state.loadingVelocity,
        erroredVelocity: state => state.erroredVelocity,

        loadingAny: state => state.loadingScatter || state.loadingNetwork,

        plotData: state => state.plotData,
        network: state => state.network,
        spaceData: state => state.spaceData,
        velocityNetworkData: state => state.velocityNetworkData,
        velocityScatterData: state => state.velocityScatterData,

        overallTime: state => state.overallTime,

        width: state => state.width,
        height: state => state.height,

        resources: state => state.resources,
        currentResource: state => state.currentResource,

        drawSpaceNet: state => state.drawSpaceNet,
        drawSpaceScatter: state => state.drawSpaceScatter,

        drawVelocityNet: state => state.drawVelocityNet,
        drawVelocityScatter: state => state.drawVelocityScatter,
    }
})