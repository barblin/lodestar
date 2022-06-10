import {store} from '../../store/cluster-state-store'

export function correctedWidth(posX, widthFactor) {
    return (posX) * widthFactor + 20
}

export function correctedHeight(posY, heightFactor) {
    return (posY) * heightFactor + 10
}

export function positionMapOf(nodes, fullWidth, cluster_level_info) {
    let clusterMap = {}

    let levelOccs = {}
    let max_nodes = 0
    nodes.forEach(node => {
        let node_index = node[0]
        let cluster = Object.entries(cluster_level_info[node_index][1])
        let level = cluster[0][1], label = cluster[2][1]

        if(store.getters.maxLevel < level){
            store.commit("updateMaxLevel", level)
        }

        if(level in levelOccs){
            let curOccs = levelOccs[level]
            curOccs++
            levelOccs[level] = curOccs
        } else {
            levelOccs[level] = 1
        }

        if(max_nodes < levelOccs[level]){
            max_nodes = levelOccs[level]
        }

        if(!(level in clusterMap)){
            clusterMap[level] = {}
        }

        let cur_level_map = clusterMap[level]
        if(!(label in cur_level_map)){
            cur_level_map[label] = {index: node_index, posX: 0, posY: 0, label: label}
        }
        clusterMap[level] = cur_level_map
    })

    let maxLevels = store.getters.maxLevel
    let sortedLabels = store.getters.sortedLabels;

    console.log(store.getters.maxLevel)
    console.log(store.getters.sortedLabels)

    let clusterLookup = {}
    let positionMap = []
    let slice = fullWidth / (max_nodes + 1)

    console.log("We currently have this amount of max nodes: " + new String(max_nodes));
    console.log("A slice is this wide: " + new String(slice));

    console.log(clusterMap)

    for(let i = 0; i < maxLevels; i++){
        let row = []
        let cur_level = clusterMap[i]

        for(let j = 0; j < sortedLabels.length; j++){
            let label = sortedLabels[j]

            if(label in cur_level) {
                let cluster = cur_level[label]
                cluster.posX = slice * (j + 1)
                clusterLookup[cluster.index] = cluster
                row.push(cluster)
            }
        }

        positionMap.push(row);
    }

    console.log("Position Map looks like this: ")
    console.log(positionMap)
    console.log("Cluster lookup looks like this: ")
    console.log(clusterLookup)

    store.commit("updateClusterLookup", clusterLookup)

    return positionMap
}
