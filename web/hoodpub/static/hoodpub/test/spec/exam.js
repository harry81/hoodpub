describe('Calculator ', function() {

  beforeEach(module('app'));

  var UserController,
      scope;

  beforeEach(inject(function ($rootScope, $controller, $window) {
    scope = $rootScope.$new();
    window = $window;
    UserController = $controller('userControllers', {
      $scope: scope,
      $window: window
    });
  }));

  it('has http in location!', function () {
    expect(window.location.href).toMatch(/http/);
});


});
