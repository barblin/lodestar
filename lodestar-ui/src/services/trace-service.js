import {highlight, invisible} from "./colors";
import {store} from '../store/cluster-state-store'
import {symbol_map} from "../config/symbols";


export function createTwoDimensionalTraces(PANE_NAME, solution, colorLabels, traces) {
    let data = createData(solution, colorLabels)
    data[0].type = 'scatter'
    data[1].type = 'scatter'
    return rerender(PANE_NAME, data, traces)
}

export function createSpaceTraces(PANE_NAME, solution, colorLabels, traces) {
    let data = createData(solution, colorLabels)
    return rerender(PANE_NAME, data, traces)
}

function rerender(PANE_NAME, data, traces){
    let new_traces = [0, 1]

    if(traces.length > 0) {
        Plotly.deleteTraces(PANE_NAME, traces)
    }

    Plotly.addTraces(PANE_NAME, data);
    return new_traces;
}

function createData(solution, colorLabels){
    let data = []

    let bucketX = []
    let bucketY = []
    let bucketZ = []
    let labels = []
    let colors = []

    let highlightedX = []
    let highlightedY = []
    let highlightedZ = []
    let highlightedLabels = []
    let highlightedColors = []

    for (let i = 0; i < colorLabels.length; i++) {
        if (colorLabels[i] != invisible) {
            if (i < solution.length) {
                if (store.getters.labels[i] != store.getters.highlightCluster) {
                    bucketX.push(solution[i].x)
                    bucketY.push(solution[i].y)
                    bucketZ.push(solution[i].z)
                    labels.push(store.getters.labels[i])
                    colors.push(colorLabels[i])
                } else {
                    highlightedX.push(solution[i].x)
                    highlightedY.push(solution[i].y)
                    highlightedZ.push(solution[i].z)
                    highlightedLabels.push(store.getters.labels[i])
                    highlightedColors.push(highlight)
                }
            }
        }
    }

    data.push({
        x: bucketX,
        y: bucketY,
        z: bucketZ,
        labels: labels,
        mode: 'markers',
        type: 'scatter3d',
        showlegend: false,
        marker: {
            color: colors,
            size: 2,
            symbol: symbol_map[0]
        }
    })

    data.push({
        x: highlightedX,
        y: highlightedY,
        z: highlightedZ,
        labels: highlightedColors,
        showlegend: false,
        mode: 'markers',
        type: 'scatter3d',
        marker: {
            color: highlightedColors,
            symbol: symbol_map[1],
            size: 4
        }
    })

    return data
}