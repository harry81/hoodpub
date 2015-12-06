angular.module('hoodpubDirective', []).
  directive('myEnter', function () {
    return function (scope, element, attrs) {
      element.bind("keydown keypress", function (event) {
        if(event.which === 13) {
          scope.$apply(function (){
            scope.$eval(attrs.myEnter);
            element = '';
          });
          event.preventDefault();
        }
      });
    };
  });
