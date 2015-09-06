
// SCRIPT FOR D3 FORCE GRAPH - AS OF 9/6/15 NOT IMPLEMENTED IN FRONT END

var width = 960,
    height = 500,
    root;


var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);


d3.json("/shakespeare.json", function(error, json) {
if (error) return console.warn(error);
root = json;
visualizeit(json);
});

function visualizeit(data) {
  var nodes = data.nodes;
  var links = data.links;

  // Restart the force layout.
  debugger
  var force = d3.layout.force()
      .nodes(d3.values(nodes))
      .links(links)
      .size([width, height])
      .on("tick", tick)
      .charge(-200)
      .start();

  var link = svg.selectAll(".link")
                .data(force.links())
                .enter().append("line")
                .attr("class", "link");

  var node = svg.selectAll(".node")
                .data(force.nodes())
                .enter().append("g")
                .attr("class", "node")
                .call(force.drag);


  var color = d3.scale.category20();


  // Enter any new links.
  link
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });


  // Exit any old nodes.


  // Enter any new nodes.
  node.append("circle")
      .attr("class", "node")
      .attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; })
      .attr("r", function(d) { return Math.sqrt(d.size) / 10 || 4.5; })
      .style("fill", color)
      .on("click", click)
      .call(force.drag);
}

function tick() {
  link.attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

  node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
}

// Color leaf nodes orange, and packages white or blue.
function color(d) {
  return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
}

// Toggle children on click.
function click(d) {
  if (!d3.event.defaultPrevented) {
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else {
      d.children = d._children;
      d._children = null;
    }
    // visualizeit();
  }
}
