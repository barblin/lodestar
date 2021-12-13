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
        hrdSelection: {
            x: "ra",
            y: "dec"
        },
        level: 0,
        maxLevel: 0,
        levelCache: {},
        noise: false,
        labels: [],
        colorLabels: [],
        colorMap: {},
        currentMode: modes.INPUT,
        currentCluster: {level: null, label: null, user_label: null, name: null, size: 0},

        loadingScatter: false,
        erroredScatter: false,
        loadingNetwork: false,
        erroredNetwork: false,
        loadingSpace: false,
        erroredSpace: false,
        loadingVelocity: false,
        erroredVelocity: false,
        loadingHrd: false,
        erroredHrd: false,

        plotData: {},
        spaceData: {},
        velocityScatterData: null,
        velocityNetworkData: {},
        networkData: null,
        hrd: {},

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
        inspectCluster: false,
        selectExclude: false,
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
        updateHrdSelection(state, selection) {
            state.hrdSelection = selection
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
        updateLoadingHrd(state, isLoading) {
            state.loadingHrd = isLoading
        },
        updateErroredHrd(state, hadError) {
            state.erroredHrd = hadError
        },
        updateNetworkData(state, data) {
            state.networkData = data
        },
        updateSpace(state, data) {
            state.spaceData = data
        },
        updateLevel(state, level) {
            state.level = level
        },
        updateMaxLevel(state, max) {
            state.maxLevel = max
        },
        updateNoise(state, noise) {
            state.noise = noise
        },
        updateLabels(state, labels) {
            state.labels = labels
        },
        updateColorMap(state, map) {
            state.colorMap = map
        },
        updateLevelCache(state, cache) {
            state.levelCache = cache
        },
        updateColorLabels(state, colorLabels) {
            state.colorLabels = colorLabels
        },
        updateCurrentClusterLevel(state, level) {
            state.currentCluster.level = level
        },
        updateCurrentClusterLabel(state, label) {
            state.currentCluster.label = label
        },
        updateCurrentClusterUserLabel(state, label) {
            state.currentCluster.user_label = label
        },
        updateCurrentClusterName(state, name) {
            state.currentCluster.name = name
        },
        updateCurrentClusterSize(state, size){
            state.currentCluster.size = size
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
        updateHrd(state, data) {
            state.hrd = data
        },
        updateInspectCluster(state, data) {
            state.inspectCluster = data
        },
        updateSelectExclude(state, data) {
            state.selectExclude = data
        },
    },
    getters: {
        currentViewSelection: state => state.currentViewSelection,
        currentMode: state => state.currentMode,
        currentColumnSelection: state => state.currentColumnSelection,
        hrdSelection: state => state.hrdSelection,

        loadingNetwork: state => state.loadingNetwork,
        erroredNetwork: state => state.erroredNetwork,
        loadingSpace: state => state.loadingSpace,
        erroredSpace: state => state.erroredSpace,
        loadingVelocity: state => state.loadingVelocity,
        erroredVelocity: state => state.erroredVelocity,
        loadingHrd: state => state.loadingHrd,
        erroredHrd: state => state.erroredHrd,

        loadingAny: state => state.loadingSpace || state.loadingNetwork || state.loadingVelocity,

        networkData: state => state.networkData,
        spaceData: state => state.spaceData,
        velocityNetworkData: state => state.velocityNetworkData,
        velocityScatterData: state => state.velocityScatterData,
        hrd: state => state.hrd,

        overallTime: state => state.overallTime,

        width: state => state.width,
        height: state => state.height,
        level: state => state.level,
        maxLevel: state => state.maxLevel,
        noise: state => state.noise,
        labels: state => state.labels,
        levelCache: (state) => (level) => {
            return state.levelCache[level]
        },
        colorLabels: state => state.colorLabels,
        colorMap: state => state.colorMap,
        currentCluster: state => state.currentCluster,

        resources: state => state.resources,
        resourceHeaders: state => state.resourceHeaders,
        currentResource: state => state.currentResource,

        drawSpaceNet: state => state.drawSpaceNet,
        drawSpaceScatter: state => state.drawSpaceScatter,

        drawVelocityNet: state => state.drawVelocityNet,
        drawVelocityScatter: state => state.drawVelocityScatter,

        plotRadial: state => state.plotRadial,
        inspectCluster: state => state.inspectCluster,
        selectExclude: state => state.selectExclude,
    }
})