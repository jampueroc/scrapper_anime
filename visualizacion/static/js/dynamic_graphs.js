var diameter = 960,
    format = d3.format(",d"),
    color = d3.scale.category20c(); // aquí está la paleta 10, 20 , 20b 20c

var bubble = d3.layout.pack()
    .sort(function(a, b) { return a.value - b.value })// andrea juega con esto como te parezca más bonito, puedes cambiar el orden o comentarlo para quitarlo
    .size([diameter, diameter])
    .padding(1.5);

var svg = d3.select("bubble").append("svg")
    .attr("width", diameter)
    .attr("height", diameter)
    .attr("class", "bubble");

var tooltip = d3.select("body")
    .append("div")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden")
    .style("color", "white")
    .style("padding", "8px")
    .style("background-color", "rgba(0, 0, 0, 0.75)")
    .style("border-radius", "6px")
    .style("font", "12px sans-serif")
    .text("tooltip");

d3.json(url_json_percent, function(error, root) {
  var node = svg.selectAll(".node")
      .data(bubble.nodes({children: root})
      .filter(function(d) { return !d.children; }))
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

  node.append("circle")
      .attr("r", function(d) { return d.r; })
      .style("fill", function(d) { return color(d.name); })
      .on("mouseover", function(d) {
              tooltip.text("Género: "+d.name + ", Cantidad de producciones:" + format(d.total));
              tooltip.style("visibility", "visible");
      })
      .on("mousemove", function() {
          return tooltip.style("top", (d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
      })
      .on("mouseout", function(){return tooltip.style("visibility", "hidden");})
    .on("click",function (d) {
        $("#genres").val(d.name).trigger("change");
        $('#ref_g').click();

    });

  node.append("text")
      .attr("dy", ".3em")
      .style("text-anchor", "middle")
      .style("pointer-events", "none")
      .text(function(d) { return d.name.substring(0, d.r / 3); });
});
