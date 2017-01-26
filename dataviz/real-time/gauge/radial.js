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

var Radial = function(ele, attr)
{
	var _this = this;

	this.ele = ele;
	this.attr = attr || {
		'weight' : 3,
		'size' : 80,
		'cx' : 50,
		'cy' : 50
	};
	
	this.arcs = [];
	this.raph = attr.raph;

	//init
	(function(ele){	
		if(!_this.raph) _this.raph = Raphael(ele);

		_this.raph.customAttributes.arc = function (xloc, yloc, value, total, R) {
			var alpha = 360 / total * value,
				a = (90 - alpha) * Math.PI / 180,
				x = xloc + R * Math.cos(a),
				y = yloc - R * Math.sin(a),
				path;

			if (total == value) 
			{
				path = [
					["M", xloc, yloc - R],
					["A", R, R, 0, 1, 1, xloc - 0.01, yloc - R]
				]
			}
			else
			{
				path = [
					["M", xloc, yloc - R],
					["A", R, R, 0, +(alpha > 180), 1, x, y]
				]
			}
			return { 'path' : path }
		}
	})(ele)

	this.update = function(arcs, duration)
	{
		if(typeOf(arcs) != 'array') arcs = [arcs];
		arcs.each(function(arc, i){
			var data_end,
				a;
		
			if(!arc.total) arc.total = 100;
			if(arc.value > arc.total) arc.value = arc.total;
		
			if(_this.arcs.length > i && _this.arcs[i] && _this.arcs[i].a)
			{
				data_end = [_this.attr.cx, _this.attr.cy, arc.value, arc.total || 100, _this.attr.size/2];
				a = _this.arcs[i].a;
			}
			else
			{
				var data_start = [_this.attr.cx, _this.attr.cy, 0, arc.total || 100, _this.attr.size/2];

				data_end = [_this.attr.cx, _this.attr.cy, arc.value, arc.total || 100, _this.attr.size/2];
				a = _this.raph.path()
					.toFront()
					.attr({
						'stroke-linecap' : 'round',
						'stroke' : arc.color || "#f00",
						'stroke-width' : arc.weight || _this.attr.weight,
						'arc' : data_start
					})
					.rotate(-180, _this.attr.cx, _this.attr.cy);

				arc.a = a;
				_this.arcs[i] = arc;
			}
		
			a.animate({
				'arc' : data_end, 
				'stroke' : arc.color || a.attr('stroke') || '#f00'
			}, duration || 250, "ease-in-out");
		})
	}

	if(_this.attr.arcs) _this.update(_this.attr.arcs)
}