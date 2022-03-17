export function createLevelLabels(svg, heights, half) {
    return svg.append('g')
        .selectAll("text")
        .data(heights)
        .enter()
        .append("text")
        .attr("x", 1)
        .attr("y", (d) => (d[0] - half))
        .attr("dy", ".45em")
        .attr("font-size", "11px")
        .attr("pointer-events", "none")
        .text(function (d) {
            return d[1]
        })
}