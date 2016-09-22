var ctx = $("#myChart");
var lineSets = [];
var lineNum = 0;
var getColor=function(){
    var a=parseInt(256*Math.random());
    var b=parseInt(256*Math.random());
    var c=parseInt(192*Math.random());
    return 'rgba('+a+','+b+','+c+',';
}

var getData = function() {
    $.get('/private/result_data', function(data, status) {
        if (status == 'success') {
            var color=getColor();
            //alert(color+'1'+')"');
            lineSets[lineNum] = {
                label: "Hot " + data.title,
                fill: false,
                //lineTension: 0.1,
                backgroundColor: color+'0.6'+')',  //图例
                borderColor: color+'1'+')',         //图例边框以及线条
                borderCapStyle: 'butt',
                //borderDash: [],
                //borderDashOffset: 0.0,
                //borderJoinStyle: 'miter',
                pointBorderColor: color+'1'+')',
                pointBackgroundColor: "#fff",
                pointBorderWidth: 1,
                pointHoverRadius: 5,
                bezierCurve: true, //////
                bezierCurveTension: 0.4, ///////////
                pointHoverBackgroundColor: color+'1'+')',
                pointHoverBorderColor: "rgba(220,220,220,1)",
                pointHoverBorderWidth: 2,
                pointRadius: 1,
                pointHitRadius: 10,
                data: data.data,
                spanGaps: false,
            }

            linedata = {
                labels: data.labels,
                datasets: lineSets
            };
            $("#myChart").remove();
            $("iframe").remove();
            $("#container").append('<canvas id="myChart" width="200" height="100"></canvas>');
            ctx = $("#myChart");
            myLineChart = new Chart(ctx, {
                type: 'line',
                data: linedata
            });            
        }
    });
}

var makeSearch=function(){
    var postdata={
        keyword: $('#keyword').val(),
        andDescript: $('#andDescript').val(),
        orDescript: $('#orDescript').val()
    };
    $.post('/private/makesearch',postdata,function(data,status){
        if(status='success'){
            lineNum++;
            //getData();
            //$('#btn').attr('disabled','true');
            inter = setInterval("getData()", 4000);
            setTimeout("endIt()", 34000);
        }
    });    
}

//getData();
var endIt = function() {
    //$('#btn').removeAttr("disabled");  
    clearInterval(inter);
    //getData();
    //ctx.width=910;
    //ctx.height=455;
}
getData();
var inter = setInterval("getData()", 4000);
setTimeout("endIt()", 34000);