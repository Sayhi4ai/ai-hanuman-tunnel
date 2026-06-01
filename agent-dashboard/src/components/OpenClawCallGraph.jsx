import { useEffect, useRef } from "react";
import * as d3 from "d3";
import API from "../api/api";

export default function OpenClawCallGraph() {
  const ref = useRef(null);

  useEffect(() => {
    API.get("/system/agent-call-graph").then(res => {
      const { nodes, links } = res.data;

      const width = 600;
      const height = 300;

      d3.select(ref.current).selectAll("*").remove();
      const svg = d3.select(ref.current)
        .attr("width", width)
        .attr("height", height);

      const simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links).id(d => d.id).distance(120))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));

      const link = svg.append("g")
        .selectAll("line")
        .data(links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-width", 1.5);

      const node = svg.append("g")
        .selectAll("circle")
        .data(nodes)
        .enter().append("circle")
        .attr("r", 12)
        .attr("fill", "#4a90e2")
        .call(d3.drag()
          .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
        );

      const labels = svg.append("g")
        .selectAll("text")
        .data(nodes)
        .enter().append("text")
        .text(d => d.id)
        .attr("font-size", 12)
        .attr("fill", "#000");

      simulation.on("tick", () => {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);

        labels
          .attr("x", d => d.x + 14)
          .attr("y", d => d.y + 4);
      });
    });
  }, []);

  return (
    <div style={{ padding: "1rem", background: "#eef7ff", borderRadius: "8px", marginTop: "1rem" }}>
      <h2>Agent Call Graph</h2>
      <svg ref={ref}></svg>
    </div>
  );
}
