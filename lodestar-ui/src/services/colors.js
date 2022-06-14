import {sortByFrequency, frequencyFromNodes} from "./frequencies.js"
import {store} from '../store/cluster-state-store'

export let invisible = 'rgba(162,162,162,0)'

export let highlight = '#ccac00'
export let selected_el = "rgba(0,255,0,0.67)"
export let density_max = "#0223ad"

export let col_map = {
    0: 'rgba(84,84,84,0.5)',
    1: '#FF0000',
    2: '#00FF00',
    3: '#0000FF',
    5: '#00FFFF',
    6: '#800080',
    7: '#FF00FF',
    9: '#FF8080',
    10: '#80FF80',
    11: '#8080FF',
    12: '#808000'
}

export function createAllLabelsMap(alphasProxy, labels){
    let alphas = Array.from(alphasProxy)
    let allLabels = {}

    for(let i = 0; i < alphas.length; i++){
        allLabels[alphas[i]] = labels[alphas[i]]
    }
    return allLabels
}

export function createAlphaColorMap(alphasProxy, alphaNodes){
    let alphas = Array.from(alphasProxy)
    let alphaColorMap = {}

    for(let i = 0; i < alphas.length; i++){
        alphaColorMap[alphas[i]] = createColorMap(alphaNodes[alphas[i]])
    }
    return alphaColorMap
}

export function createColorMap(nodes){
    let frequencies = frequencyFromNodes(nodes)

    let labels = sortByFrequency(frequencies)
    labels = Array.from(labels)

    let colorMap = {}
    let index = 1
    for(let i = 0; i < labels.length; i++){

        if(index < Object.keys(col_map).length) {
            colorMap[labels[i]] = col_map[index]
            index += 1
        } else {
            colorMap[labels[i]] = 'rgb(0,0,0)'
        }
    }

    store.commit("updateSortedLabels", labels)
    return colorMap
}

export function computeColorLabels(labels, colorMap, includeNoise) {
    labels = Array.from(labels)

    let colorLabels = []
    for (let i = 0; i < labels.length; i++) {
        if (!includeNoise) {
            if (labels[i] == -1) {
                colorLabels.push(invisible)
                continue
            }
        }

        if (labels[i] == -1) {
            colorLabels.push('rgba(84,84,84,0.5)')
            continue
        } else {
            colorLabels.push(colorMap[labels[i]])
        }
    }

    return colorLabels
}