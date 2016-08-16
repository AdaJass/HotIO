window.graphCtrl = ['$scope', function($scope) {
  $scope.sampleData = [0, 0, 0, 50, 50, 50, 50, 50, 50, 50];
  
  $scope.sample = function() {
    for (var i=0, len=$scope.sampleData.length; i < len; i++) {
      $scope.sampleData[i] = (Math.random() * 90) + 5;
    }
  };
  
  $scope.sample();
  $scope.sampler = setInterval(function() {
    $scope.$apply($scope.sample);
  }, 2000);
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
          var pt = points[i]
            , psty = pt && pt.style;
          
          if (psty) {
            var sect = pt.parentNode
              , sectWidth = sect.offsetWidth
              , sectHeight = sect.offsetHeight;
          
            sect.title = Math.round(100 - val) + '%';
            psty.top = (val * sectHeight / 100) + 'px';
            
            var next = data[i + 1];
            if (typeof next === 'number') {
              var delta = (next - val) * sectHeight / 100;
              
              psty.height = Math.sqrt(Math.pow(sectWidth, 2) + Math.pow(delta, 2)) + 'px';
              psty.webkitTransform =
                psty.msTransform =
                psty.transform =
                  'rotate('+(-Math.PI / 2 + Math.atan2(delta, sectWidth))+'rad)';
            }
          }
        });
      }, /* deep */ true);
        
    }
  };
});

