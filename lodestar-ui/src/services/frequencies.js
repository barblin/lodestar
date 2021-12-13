export function frequencyFromNodes(nodes) {
    let frequs = []

    for (const [key, value] of Object.entries(nodes)) {
        frequs.push(value[2])
    }

    return frequs
}

export function sortByFrequency(array) {
    let frequency = {};

    array.forEach(function (value) {
        frequency[value] = 0;
    });

    let uniques = array.filter(function (value) {
        return ++frequency[value] == 1;
    });

    return uniques.sort(function (a, b) {
        return frequency[b] - frequency[a];
    });
}