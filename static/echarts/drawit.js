function initstock(id, title, sblist, xlabels) {
	var series = [];
	for (var i = 0; i < sblist.length;i++) {
		series.push({
				name:sblist[i],
				type:'line',
				data:[]
		})
	}
	option = {
		title: {
			text: title
		},
		legend: {
			data:sblist
		},
		toolbox: {
			feature: {
				saveAsImage: {}
			}
		},
        //data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		xAxis : [
			{
				type : 'category'
			}
		],
		yAxis : [
			{
				type : 'value'
			}
		],
		series : series
	};
	var myChart = echarts.init(document.getElementById(id))
	myChart.setOption(option);
		// myChart.setOption({
		// title: {
			// text: '异步数据加载示例'
		// },
		// tooltip: {},
		// legend: {
			// data:['销量']
		// },
		// xAxis: {
			// data: []
		// },
		// yAxis: {},
		// series: [{
			// name: '销量',
			// type: 'bar',
			// data: []
		// }]
	// })
	return myChart;

}

function drawstock(hdl, sb, data) {
	var xvalue = []
	var yvalue = []
	for (var i = 0;i < data.length;i++) {
		xvalue.push(data[i]['x'])
		yvalue.push(data[i]['y'])
	}
		
	option = {
		xAxis :{type : 'category', data : xvalue},
		series : [
			{
				name:sb,
				type:'line',
				data:yvalue
			}
		]
	};
	
	 // hdl.setOption({
        // xAxis: {
            // data: xvalue
        // },
        // series: [{
            //根据名字对应到相应的系列
            // name: sb,
            // data: yvalue
        // }]
    // });
	hdl.setOption(option)
}