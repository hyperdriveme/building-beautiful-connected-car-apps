//  MIT License
// 
//  Copyright (c) 2017 HyperdriveMe, Inc.
// 
//  Permission is hereby granted, free of charge, to any person obtaining a copy
//  of this software and associated documentation files (the "Software"), to deal
//  in the Software without restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//  copies of the Software, and to permit persons to whom the Software is
//  furnished to do so, subject to the following conditions:
// 
//  The above copyright notice and this permission notice shall be included in all
//  copies or substantial portions of the Software.
// 
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
//  SOFTWARE.

var	periodicals,
	i = 0,
	updates = [3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 3, 6, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 9];

window.addEvent('domready', function(){
	updates.shuffle();

	var brick = $$('li.stat')[0];
	var rps = brick.getElement('div.line.rps'),
		lat = brick.getElement('div.line.lat');
	drawSparkline(rps, 300, 20, 2000, 2000);
	drawSparkline(lat, 300, 20, 2000, 2000);

	periodicals = (updateStats).periodical(3000);
});

function drawSparkline(ele, width, height, updateDelay, transitionDelay, refresh) 
{
	var maxval = 10,
		graph = d3.select(ele).append("svg:svg").attr("width", "100%").attr("height", "100%"),
		data = [3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 3, 6, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 9],

		x = d3.scale.linear().domain([0, 48]).range([-5, width]),
		y = d3.scale.linear().domain([0, 10]).range([0, height]),

		line = d3.svg.line()
			.x(function(d, i) { return x(i); })
			.y(function(d) { return y(d); })
			.interpolate("basis");

	if(ele.hasClass('rps')) data.shuffle();

	graph.selectAll("path")
		.data([data])
		.enter()
		.append("svg:path")
		.attr("d", line);

	function redraw(new_data) 
	{
		if(maxval < new_data)
		{
			var mult = maxval/new_data;
			maxval = new_data;
			data = data.map(function(d){ return 10-Math.round((10-d)*mult,0) } )
		}

		if(maxval > 10) new_data = (new_data*(10/maxval)),0
		new_data = Math.round(new_data,0);

		if(!new_data || new_data < 0) new_data = 0;
		if(new_data > 10) new_data = 10;

		data.push(10-new_data);
		data.shift(); 

		graph.selectAll("path")
			.data([data])
			.attr("transform", "translate(" + x(1) + ")")
			.attr("d", line)
			.transition()
			.ease("linear")
			.duration(transitionDelay)
			.attr("transform", "translate(" + x(0) + ")");
	}
	
	ele.store('redraw', redraw);
}

function updateStats()
{
	if((i+=2) > updates.length)
	{
		updates.shuffle();
		i=0;
	}

	var update = {
		'lat' : updates[i],
		'rps' : updates[i+1]
	}
	console.log(update);

	var brick = $$('li.stat')[0],
		lat = update.lat,
		rps = update.rps,
		rps_val = brick.getElement('div.stat.rps div.val'),
		lat_val = brick.getElement('div.stat.lat div.val'),
		rps_line = brick.getElement('div.line.rps'),
		lat_line = brick.getElement('div.line.lat');
	displayStatsUpdate(lat_val, rps_val, lat_line, rps_line, {'lat' : lat, 'rps' : rps});
}

function uproundNumber(n, k)
{
	if(n == null) n = 0;
	
	var ret,
		sign = '';

	if(k && n > 0) 
		sign = '+';
	else if (k && n < 0) 
		sign = '-';

	if(n>1000000)
	{
		ret = (n/1000000).toInt();
		return sign + ret + 'm';
	}
	else if(k && n>100000)
	{
		ret = (n/1000000).toInt();
		return sign + ret + 'm';
	}
	else if((k && n >10000) || (k && n>1000))
	{
		ret = (n/1000).toInt();
		return sign + ret + 'k'
	}
	return sign + n.toInt();
}

function displayStatsUpdate(lat_val, rps_val, lat_line, rps_line, update)
{
	var setvalue = function(ele)
	{
		var value = ele.retrieve('value');
		ele.set('text', uproundNumber(value, false));
	}

	setvalue(lat_val.store('value', update.lat));
	lat_line.retrieve('redraw')(update.lat) 
	setvalue(rps_val.store('value', update.rps));
	rps_line.retrieve('redraw')(update.rps) 
}
