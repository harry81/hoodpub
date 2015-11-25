describe('Unit: MainController', function() {
    // Load the module with MainController
    beforeEach(module('app'));
    console.log('hi3');

    var ctrl, scope;
    // inject the $controller and $rootScope services
    // in the beforeEach block
    beforeEach(inject(function($controller, $rootScope) {
        // Create a new scope that's a child of the $rootScope
        scope = $rootScope.$new();
        // Create the controller
        ctrl = $controller('hoodpubControllers', {
            $scope: scope
        });
    }));

    it('should create $scope.greeting when calling sayHello',
       
       function() {
       });
})
