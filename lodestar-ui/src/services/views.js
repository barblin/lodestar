export let views = {
    SCATTER: "scatter",
    NETWORK: "network",
    SPACE: "space",
    VELOCITY: "velocity",
    HRD: "hrd",
    DISTRIBUTION: "distribution",
    ALPHA: "alpha",
    CLUSTER_DETAIL: "cluster_detail",
    HISTOGRAMS: "histograms",
    HEAT_MAP: "heat_map",
    STABILITY: "stability",
}

export function percentChange(solution, screen) {
    if (solution < screen) {
        return screen / solution
    } else if (screen < solution) {
        return screen / solution;
    }

    return -1
}