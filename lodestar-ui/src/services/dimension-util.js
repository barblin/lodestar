import {store} from '../store/cluster-state-store'

export function includeFirstSpaceDimension() {
    return 0 < store.getters.resourceHeaders.length;
}

export function includeSecondSpaceDimension() {
    return 1 < store.getters.resourceHeaders.length;
}

export function includeThirdSpaceDimension() {
    return 2 < store.getters.resourceHeaders.length;
}

export function includeFirstVelocityDimension() {
    return 3 < store.getters.resourceHeaders.length;
}

export function includeSecondVelocityDimension() {
    return 4 < store.getters.resourceHeaders.length;
}

export function includeThirdVelocityDimension() {
    return store.getters.resourceHeaders.length > 5;
}

export function includeThirdVelocityDimensionForBody() {
    return store.getters.resourceHeaders.length > 5;
}


export function buildAll() {
    let space = buildSpaceBody()
    let velocity = buildVelocityBody()

    return {
        s1: space.s1,
        s2: space.s2,
        s3: space.s3,
        v1: velocity.v1,
        v2: velocity.v2,
        v3: velocity.v3,
        rad_error: store.getters.resourceHeaders[store.getters.currentColumnSelection.rad_error],
        level: store.getters.level,
        alpha: store.getters.alpha
    }
}

export function buildSpaceBody(current_cluster) {
    let spaceBody = {s1: null, s2: null, s3: null, current_cluster: current_cluster, level: store.getters.level}

    if (includeFirstSpaceDimension()) {
        spaceBody.s1 = store.getters.resourceHeaders[store.getters.currentColumnSelection.s1]
    }

    if (includeSecondSpaceDimension()) {
        spaceBody.s2 = store.getters.resourceHeaders[store.getters.currentColumnSelection.s2]
    }

    if (includeThirdSpaceDimension()) {
        spaceBody.s3 = store.getters.resourceHeaders[store.getters.currentColumnSelection.s3]
    }

    return spaceBody
}

export function buildVelocityBody() {
    let velocityBody = {v1: null, v2: null, v3: null}

    if (includeFirstVelocityDimension()) {
        velocityBody.v1 = store.getters.resourceHeaders[store.getters.currentColumnSelection.v1]
    }

    if (includeSecondVelocityDimension()) {
        velocityBody.v2 = store.getters.resourceHeaders[store.getters.currentColumnSelection.v2]
    }

    if (includeThirdVelocityDimensionForBody()) {
        velocityBody.v3 = store.getters.resourceHeaders[store.getters.currentColumnSelection.v3]
    }

    return velocityBody
}