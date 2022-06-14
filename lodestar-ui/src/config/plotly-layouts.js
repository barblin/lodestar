import {store} from "../store/cluster-state-store";

export function THREE_DIMENSION_LAYOUT(height, width){
    return {
        title: {
            text: 'Space',
                font: {
                family: 'Courier New, monospace',
                    size: 12
            },
            xref: 'paper',
                y: 0.99,
                x: 0.01
        },
        autosize: true,
        height: height,
        margin: {
        l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
    },
        scene: {
            aspectratio: {
                x: 1,
                    y: 1,
                    z: 1
            },
            camera: {
                center: {
                    x: 0,
                        y: 0,
                        z: 0
                },
                eye: {
                    x: 1.25,
                        y: 1.25,
                        z: 1.25
                },
                up: {
                    x: 0,
                        y: 0,
                        z: 1
                }
            },
            xaxis: {
                title: {
                    text: store.getters.resourceHeaders[store.getters.currentColumnSelection.s1],
                },
                type: 'linear',
                    zeroline: false
            },
            yaxis: {
                title: {
                    text: store.getters.resourceHeaders[store.getters.currentColumnSelection.s2],
                },
                type: 'linear',
                    zeroline: false
            },
            zaxis: {
                title: {
                    text: store.getters.resourceHeaders[store.getters.currentColumnSelection.s3],
                },
                type: 'linear',
                    zeroline: false
            }
        },
        width: width
    }
};


export function TWO_DIMENSION_LAYOUT(height, width, header, labelX, labelY, yAutorange = true){
    let layout = {
        title: {
            text: header,
            font: {
                family: 'Courier New, monospace',
                size: 12
            },
            xref: 'paper',
            y: 0.99,
            x: 0.01
        },
        autosize: true,
        height: height,
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },

        xaxis: {
            title: {
                text: labelX,
            },
            zeroline: false
        },
        yaxis: {
            title: {
                text: labelY,
            },
            zeroline: false,
            autorange: 'reversed'
        },
        width: width
    };

    return layout
}