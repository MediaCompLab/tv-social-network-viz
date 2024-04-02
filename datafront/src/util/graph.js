const NODE_RADIUS = 5;
const the_graph = {
  "directed": false,
  "multigraph": false,
  "graph": {},
  "nodes": [
    { "count": 1, "x": -50.0, "y": -50.0, "color": 0.1, "id": "Sheldon" },
    { "count": 1, "x": -0.0, "y": -0.0, "color": 0.1, "id": "Leonard" },
    { "count": 1, "x": 50.0, "y": 50.0, "color": 0.1, "id": "Receptionist" }
  ],
  "links": [
    { "weight": 1, "color": 0.1, "source": "Sheldon", "target": "Leonard" },
    { "weight": 1, "color": 0.1, "source": "Sheldon", "target": "Receptionist" }
  ]
};

function json2vNG(json) {
  console.log('received json:',json);
  const nodes = {};
  const edges = {};
  const layouts = { nodes: {} };

  json.nodes.forEach((node) => {
    nodes[node.id] = {
      name: node.id,
      count: node.count,
      size: NODE_RADIUS,
      color: `rgba(255, 0, 0, ${node.color})`,
      label: true,
    };
    layouts.nodes[node.id] = { x: node.x*10, y: node.y*10 };
  });

  json.links.forEach((link, index) => {
    edges[`edge${index + 1}`] = {
      source: link.source,
      target: link.target,
      width: 2,
      count: link.weight,
      color: `rgba(255, 0, 0, ${link.color})`,
    };
  });

  return { nodes, edges, layouts };
}

function vNG2Json(vNetworkGraph) {
  const nodes = [];
  const links = [];

  Object.entries(vNetworkGraph.nodes).forEach(([id, node]) => {
    const [r, g, b, a] = node.color.match(/\d+/g).map(Number);
    nodes.push({
      count: 1,
      x: vNetworkGraph.layouts.nodes[id].x,
      y: vNetworkGraph.layouts.nodes[id].y,
      size: NODE_RADIUS,
      color: a,
      id,
    });
  });

  Object.values(vNetworkGraph.edges).forEach((edge) => {
    const [r, g, b, a] = edge.color.match(/\d+/g).map(Number);
    links.push({
      weight: edge.width,
      color: a,
      source: edge.source,
      target: edge.target,
    });
  });

  return {
    directed: false,
    multigraph: false,
    graph: {},
    nodes,
    links,
  };
}

const graph_info = json2vNG(the_graph);

export { graph_info, NODE_RADIUS, json2vNG, vNG2Json };