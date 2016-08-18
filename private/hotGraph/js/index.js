window.graphCtrl = ['$scope', '$http', function($scope, $http) {
  $scope.sampleData = [];

  /*for(var i=0;i<73;i++)
    $scope.sampleData[i]=50;*/

  /*$scope.sample = function() {
    for (var i = 0, len = 74; i < len; i++) {
      $scope.sampleData[i] = (90) + 5;
    }
  };*/

  $scope.sample=function() {
    //alert(9);
    $http.get('/private/result_data').success(function(data, status, headers, config) {
      //alert('ss'+data);
      if(data.length>10)
        $scope.sampleData = data;      
    });
  }
  $scope.sample();
  $scope.sampler = setInterval(function() {
    $scope.$apply($scope.sample);
  }, 3000);

  setTimeout(function(){
    clearInterval($scope.sampler);
  },30000);
}];

angular.module('myApp', []).

directive('graph', function() {
  return {
    restrict: 'A',
    link: function(scope, elm, attr) {
      var points = elm[0].querySelectorAll('[data-point]');

      // graph data provided by the "data" attribute.
      // NB: data is interpreted as percentages
      scope.$watch(attr.data, function(data) {
        angular.forEach(data, function(val, i) {
          var pt = points[i],
            psty = pt && pt.style;

          if (psty) {
            var sect = pt.parentNode,
              sectWidth = sect.offsetWidth,
              sectHeight = sect.offsetHeight;

            sect.title = val;
            psty.top = (val * sectHeight / 100) + 'px';

            var next = data[i + 1];
            if (typeof next === 'number') {
              var delta = (next - val) * sectHeight / 100;

              psty.height = Math.sqrt(Math.pow(sectWidth, 2) + Math.pow(delta, 2)) + 'px';
              psty.webkitTransform =
                psty.msTransform =
                psty.transform =
                'rotate(' + (-Math.PI / 2 + Math.atan2(delta, sectWidth)) + 'rad)';
            }
          }
        });
      }, /* deep */ true);

    }
  };
});