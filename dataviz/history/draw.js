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

var	aSpeed = [],
	maxSpeed = 200,
	aMaf = [],
	maxMaf = 300,
	aRpm = [],
	maxRpm = 5000;

window.addEvent('domready', function(){

	obdData.each(function(frame){
		console.log(frame.SPEED);
		aSpeed.push(frame.SPEED);
		aMaf.push(frame.MAF);
		aRpm.push(frame.RPM);
	});

	var speed = $$('div.speed')[0],
		maf = $$('div.maf')[0],
		rpm = $$('div.rpm')[0];

	drawSparkline(speed, aSpeed, maxSpeed, 1000, 100);
	drawSparkline(maf, aMaf, maxMaf, 1000, 100);
	drawSparkline(rpm, aRpm, maxRpm, 1000, 100);
});

function drawSparkline(ele, data, max, width, height) 
{
	var graph = d3.select(ele).append("svg:svg").attr("width", "100%").attr("height", "100%"),

		x = d3.scale.linear().domain([0, data.length]).range([0, width]),
		y = d3.scale.linear().domain([0, max]).range([0, height]),

		line = d3.svg.line()
			.x(function(d, i) { return x(i); })
			.y(function(d) { return y(d); })
			.interpolate("basis");

	graph.selectAll("path")
		.data([data])
		.enter()
		.append("svg:path")
		.attr("d", line);
}