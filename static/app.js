$(document).ready(function() {
	$("#getStat").on("click",function(){
		Ext.getBody().mask("Loading data...");
		$.post('/getStatistics', {
		user1: $("#user1").val(),
		user2: $("#user2").val(),
		duration: $("#duration").val()
	    	}).done(function(response) {
			generateChart(response);
	    	}).fail(function(error) {
			console.log(error);
			Ext.getBody().unmask();
	    	});
	});
	
});


getTickSteps=function(jsData){
	var majorTickSteps=0;
	var user1=jsData['user1'];
  	var user2=jsData['user2'];
	var tweetData=jsData['data'];
	for(i=0;i<tweetData.length;i++){
		if((tweetData[i])[user1]>majorTickSteps)
			majorTickSteps=(tweetData[i])[user1];
		if((tweetData[i])[user2]>majorTickSteps)
			majorTickSteps=(tweetData[i])[user2];
	}
	/*Due to bug in extJS library, majorTickSteps value of chart 
	is changed for lower values to display data properly, depending on maximum value. Following is the correction.
	Maximum value		majorTickSteps
	   1-9			  maximum-1
	   others	       no change or 10
	*/
	if(majorTickSteps>0 && majorTickSteps<=9)
		majorTickSteps-=1;
	else if(majorTickSteps>9)
		majorTickSteps=10;
	return majorTickSteps;

}


function generateChart(jsData){
	var majorTickSteps= getTickSteps(jsData);
	var user1=jsData['user1'];
  	var user2=jsData['user2'];
	$("#tweetGraph").remove();
	var store = Ext.create('Ext.data.JsonStore', {
		fields: ['period', user1,user2],
		data:  jsData['data']
	});

	
	
Ext.create('Ext.chart.Chart', {
    renderTo: Ext.get("graph"),   
    animate: true,
	width:800,
	height:300,
	legend: {
                position: 'bottom',
		boxStrokeWidth: 0,
		fields : ['period'],
		width : 300
    }, 
    store: store,
	id:'tweetGraph',
    axes: [
        {
            type: 'Numeric',
            position: 'left',
            fields: [user1, user2],
            label: {
                renderer: Ext.util.Format.numberRenderer('0,0')
				
            },
            grid: true,
            minimum: 0,
			majorTickSteps : majorTickSteps
        },
        {
            type: 'Category',
            position: 'bottom',
            fields: 'period',
			label: {
									field: 'period',
									rotate: {
										degrees: 315
									},
									font: '12px Arial'
			}
        }
    ],
    series: [
        {
            type: 'line',
            highlight: {
                size: 7,
                radius: 7
            },
            axis: 'left',
            xField: 'period',
            yField: user1,			
			label: {							
				fill:'#fff'
			},
            markerConfig: {
                type: 'cross',
                size: 4,
                radius: 4,
                'stroke-width': 0
            }
        },
        {
            type: 'line',
            highlight: {
                size: 7,
                radius: 7
            },
            axis: 'left',           
            xField: 'period',
            yField: user2,
			label: {										
				fill:'#fff'				
			},
            markerConfig: {
                type: 'circle',
                size: 4,
                radius: 4,
                'stroke-width': 0
            }
        }
    ]
});
Ext.getBody().unmask();
}
