/*
 * Inspired by : bl.ocks.org/mbostock/7607535
 * 
 */


function loadArtistViz(){
	jQuery.support.cors = true;
	artist = document.getElementById("SelectArtist").value;;
	url    = "https://hds.iriscouch.com/jazzdisco_albums/_design/albums/_view/collaborators?startkey=%5B%22"+artist+"%22%5D&endkey=%5B%22"+artist+"%22,{},{}%5D";

	var jxhr = $.ajax(
		{
			type:'get',
			dataType:"jsonp",
			crossDomain:true,
			url:url, 
			success: function(data, textStatus) {	
				var 	tree = getD3Tree(data["rows"]);
				constructD3CirclePackZoom(tree);
				}
			})
	.fail(function( jqXHR, textStatus, errorThrown ) {
		alert(textStatus);
		alert(errorThrown);
	});
	
	function getD3Tree(data){
		var root = {name:data[0]['key'][0],children:[]};
		
		data.forEach(function(d) {
			
			var p = d['key'][1]; // player = instrument->child
			var i = d['key'][2]; // instrument = root->child
			
			/* 
			 * 
			 * 1. is the artist already a member of the children and if so add
			 * 
			 */
			if (root.children.map ( function(o) {
					return o.name;
				}).indexOf(i) < 0 ) {
					root.children.push(
						{name:i,
						 parent:root.name,
						 children:
						 	[{name:p,size:1,parent:i}]
						 }
					);
				}
			else {
				
				i_idx = root.children.map ( function(o) {
								return o.name;
							}).indexOf(i);
				
				p_idx =
					root.children[ i_idx ]
						.children.map( function (o) {
								return o.name;
							}).indexOf(p); 
		
				if (p_idx < 0) {
					root.children[i_idx].children.push({name:p,parent:i,size:1});
				} else {
					root.children[i_idx].children[p_idx].size+=1;
				}
			}
		});
		return root;
	}
	
	function constructD3CirclePackZoom(root) {
		d3.select("svg").remove();
		
		var margin = 20,
		diameter = 800;

		var color = d3.scale.linear()
		    .domain([-1, 5])
		    .range(["hsl(52,80%,80%)", "hsl(128,30%,40%)"])
		    .interpolate(d3.interpolateHcl);
		
		var pack = d3.layout.pack()
		    .padding(2)
		    .size([diameter - margin, diameter - margin])
		    .value(function(d) { return d.size; });
		
		var svg = d3.select("body").append("svg")
		    .attr("width", diameter)
		    .attr("height", diameter)
		  .append("g")
		    .attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");
		
		  var focus = root,
		      nodes = pack.nodes(root),
		      view;
		
		  var circle = svg.selectAll("circle")
		      .data(nodes)
		    .enter().append("circle")
		      .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
		      .style("fill", function(d) { return d.children ? color(d.depth) : null; })
		      .on("click", function(d) { if (focus !== d) zoom(d), d3.event.stopPropagation(); });
		
		  var text = svg.selectAll("text")
		      .data(nodes)
		    .enter().append("text")
		      .attr("class", "label")
		      .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
		      .style("display", function(d) { return d.parent === root ? null : "none"; })
		      .text(function(d) { return d.name; });
		
		  var node = svg.selectAll("circle,text");
		
		  d3.select("body")
		      .style("background", color(-1))
		      .on("click", function() { zoom(root); });
		
		  zoomTo([root.x, root.y, root.r * 2 + margin]);
		
		  function zoom(d) {
		    var focus0 = focus; focus = d;
		
		    var transition = d3.transition()
		        .duration(d3.event.altKey ? 7500 : 750)
		        .tween("zoom", function(d) {
		          var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
		          return function(t) { zoomTo(i(t)); };
		        });
		
		    transition.selectAll("text")
		      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
		        .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
		        .each("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
		        .each("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
		  }
		
		  function zoomTo(v) {
		    var k = diameter / v[2]; view = v;
		    node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
		    circle.attr("r", function(d) { return d.r * k; });
		  }
		d3.select(self.frameElement).style("height", diameter + "px");			
		}
	}
