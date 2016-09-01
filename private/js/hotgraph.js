var ctx = $("#myChart");
var getData = function() {
    $.get('/private/result_data', function(data, status) {
        if (status == 'success') {                     
            linedata = {
                labels: data.labels,
                datasets: [{
                    label: "Hot " + data.title,
                    fill: false,
                    //lineTension: 0.1,
                    backgroundColor: "rgba(75,192,192,0.4)",
                    borderColor: "rgba(75,192,192,1)",
                    borderCapStyle: 'butt',
                    //borderDash: [],
                    //borderDashOffset: 0.0,
                    //borderJoinStyle: 'miter',
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    bezierCurve : true,   //////
                    bezierCurveTension : 0.4,   ///////////
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 1,
                    pointHitRadius: 10,
                    data: data.data,
                    spanGaps: false,
                }]
            };      
            $("#myChart").remove();
            $("#main").append('<canvas id="myChart"></canvas>');
            ctx = $("#myChart");
            myLineChart = new Chart(ctx, {
                type: 'line',
                data: linedata
            });            
        }
    });
}
//getData();
var endIt=function(){
    var addkey ='<form action="/private/makesearch_add" method="post">   <div class="form-group"> <label for="hotkey"  class="control-label">关键字:</label>            <input type="text" class="form-control" name="keyword" required id="hotkey" placeholder="请输入关键词，多于一个词的用$连接"></div></div> </form>';
    $("#main").append(addkey);  
    clearInterval(inter);
}
getData();
inter = setInterval("getData()", 4000);
setTimeout("endIt()",40000);