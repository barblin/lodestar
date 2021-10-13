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
    return store.getters.resourceHeaders.length > 5 && store.getters.plotRadial;
}

export function buildSpaceBody() {
    let spaceBody = {s1: null, s2: null, s3: null}

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

    if (includeThirdVelocityDimension()) {
        velocityBody.v3 = store.getters.resourceHeaders[store.getters.currentColumnSelection.v3]
    }

    return velocityBody
}
