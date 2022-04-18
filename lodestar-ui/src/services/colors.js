import {sortByFrequency, frequencyFromNodes} from "./frequencies.js"

export let col_map = {
    0: 'rgba(84,84,84,0.5)',
    1: '#1f78b4',
    2: '#33a02c',
    3: '#ff7f00',
    4: '#cab2d6',
    5: '#b2df8a',
    6: '#fdbf6f',
    7: '#fb9a99',
    8: '#a6cee3',
    9: '#af0000',
    10: '#000080',
    11: '#ff2424',
    12: 'rgba(162,162,162,0)'
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

    return colorMap
}

export function computeColorLabels(labels, colorMap, includeNoise) {
    labels = Array.from(labels)

    let colorLabels = []
    for (let i = 0; i < labels.length; i++) {
        if (!includeNoise) {
            if (labels[i] == -1) {
                colorLabels.push(col_map[12])
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