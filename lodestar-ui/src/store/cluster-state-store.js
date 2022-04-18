import {createStore} from 'vuex'
import {modes} from "../services/modes"

export const store = createStore({
    state: {
        currentViewSelection: null,
        currentResource: "Choose resource file",
        currentColumnSelection: {
            s1: 5,
            s2: 7,
            s3: 9,
            v1: 12,
            v2: 14,
            v3: 66,
            rad_error: 67
        },
        hrdSelection: {
            x: "ra",
            y: "dec"
        },
        level: 44,
        alpha: 0.05,
        maxLevel: 0,
        noise: false,
        labels: [],
        colorLabels: [],
        colorMap: {},
        alphaColorMap: {},
        allLabels: {},
        currentMode: modes.INPUT,
        currentCluster: {level: null, label: null, user_label: null, name: null, size: 0},
        temporaryClusterName: null,
        levelSet: {},
        densityLevels: [],
        alphas: [],
        significantRoots: [],

        loadingScatter: false,
        erroredScatter: false,
        loadingMain: false,
        erroredMain: false,
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
        heatmap: []
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
        updateLoadingMain(state, isLoading) {
            state.loadingMain = isLoading
        },
        updateErroredMain(state, hadError) {
            state.erroredMain = hadError
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
        updateAlphaColorMap(state, map) {
            state.alphaColorMap = map
        },
        updateAllLabels(state, map) {
            state.allLabels = map
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
        updateCurrentClusterSize(state, size) {
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
        addNode(state, node) {
            if (!(node.level in state.levelSet)) {
                state.levelSet[node.level] = {}
            }
            state.levelSet[node.level][node.label] = node
        },
        updateName(state, node) {
            state.levelSet[node.level][node.label].name = node.name
        },
        updateDensityLevels(state, data) {
            state.densityLevels = data
        },
        updateAlpha(state, data) {
            state.alpha = data
        },
        updateAlphas(state, data) {
            state.alphas = data
        },
        updateSignificantRoots(state, data) {
            state.significantRoots = data
        },
        updateTemporaryClusterName(state, data) {
            state.temporaryClusterName = data
        },
        updateHeatmap(state, data) {
            state.heatmap = data
        },
    },
    getters: {
        currentViewSelection: state => state.currentViewSelection,
        currentMode: state => state.currentMode,
        currentColumnSelection: state => state.currentColumnSelection,
        hrdSelection: state => state.hrdSelection,

        loadingMain: state => state.loadingMain,
        erroredMain: state => state.erroredMain,
        loadingSpace: state => state.loadingSpace,
        erroredSpace: state => state.erroredSpace,
        loadingVelocity: state => state.loadingVelocity,
        erroredVelocity: state => state.erroredVelocity,
        loadingHrd: state => state.loadingHrd,
        erroredHrd: state => state.erroredHrd,

        loadingAny: state => state.loadingSpace || state.loadingMain || state.loadingVelocity || state.loadingHrd,

        networkData: state => state.networkData,
        spaceData: state => state.spaceData,
        velocityNetworkData: state => state.velocityNetworkData,
        velocityScatterData: state => state.velocityScatterData,
        hrd: state => state.hrd,

        overallTime: state => state.overallTime,

        width: state => state.width,
        height: state => state.height,
        level: state => state.level,
        alpha: state => state.alpha,
        alphas: state => state.alphas,
        maxLevel: state => state.maxLevel,
        noise: state => state.noise,
        labels: state => state.labels,
        colorLabels: state => state.colorLabels,
        colorMap: state => state.colorMap,
        alphaColorMap: state => state.alphaColorMap,
        allLabels: state => state.allLabels,
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
        levelSet: state => state.levelSet,
        significantRoots: state => state.significantRoots,
        temporaryClusterName: state => state.temporaryClusterName,
        heatmap: state => state.heatmap
    }
})