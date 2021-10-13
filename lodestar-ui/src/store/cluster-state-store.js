import {createStore} from 'vuex'
import {modes} from "../services/modes"

export const store = createStore({
    state: {
        currentViewSelection: null,
        currentResource: "Choose resource file",
        currentColumnSelection: {
            s1: 0,
            s2: 1,
            s3: 2,
            v1: 3,
            v2: 4,
            v3: 5
        },
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
        networkData: {},
        resources: [],
        resourceHeaders: [],
        overallTime: 0,

        width: 600,
        height: 440,


        // space controls
        drawSpaceNet: false,
        drawSpaceScatter: true,

        drawVelocityNet: false,
        drawVelocityScatter: true,

        plotRadial: false,
    },
    mutations: {
        updateCurrentViewSelection(state, selection) {
            state.currentViewSelection = selection
        },
        updateCurrentMode(state, mode) {
            state.currentMode = mode
        },
        updateCurrentColumnSelection(state, selection) {
            state.currentColumnSelection = selection
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
        updateNetworkData(state, data) {
            state.networkData = data
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
        updateResourceHeaders(state, data) {
            state.resourceHeaders = data
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
        updatePlotRadial(state, plotRadial) {
            state.plotRadial = plotRadial
        },
    },
    getters: {
        currentViewSelection: state => state.currentViewSelection,
        currentMode: state => state.currentMode,
        currentColumnSelection: state => state.currentColumnSelection,

        loadingNetwork: state => state.loadingNetwork,
        erroredNetwork: state => state.erroredNetwork,
        loadingSpace: state => state.loadingSpace,
        erroredSpace: state => state.erroredSpace,
        loadingVelocity: state => state.loadingVelocity,
        erroredVelocity: state => state.erroredVelocity,

        loadingAny: state => state.loadingSpace || state.loadingNetwork || state.loadingVelocity,

        networkData: state => state.networkData,
        spaceData: state => state.spaceData,
        velocityNetworkData: state => state.velocityNetworkData,
        velocityScatterData: state => state.velocityScatterData,

        overallTime: state => state.overallTime,

        width: state => state.width,
        height: state => state.height,

        resources: state => state.resources,
        resourceHeaders: state => state.resourceHeaders,
        currentResource: state => state.currentResource,

        drawSpaceNet: state => state.drawSpaceNet,
        drawSpaceScatter: state => state.drawSpaceScatter,

        drawVelocityNet: state => state.drawVelocityNet,
        drawVelocityScatter: state => state.drawVelocityScatter,

        plotRadial: state => state.plotRadial,
    }
})