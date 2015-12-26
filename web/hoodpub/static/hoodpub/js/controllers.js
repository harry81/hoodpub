angular.module('hoodpubControllers', []).
  controller('authControllers', [
    '$scope', '$http', '$window', 'Users',
    function ($scope, $http, $window, Users) {

      function try_facebook_auth() {
        localStorage.setItem('id_token', $scope.token_objects.access_token);

        Users.query().$promise.then(function(res) {
          $window.location.href = '/#';
        });
      }

      $scope.$watch('$viewContentLoaded', function() {
        try_facebook_auth();
      });
    }]).

controller('userControllers', [
  '$rootScope', '$scope', '$http', '$window',
  function($rootScope, $scope, $http, $window){

    function init(){
      if (localStorage.getItem('id_token') == null)
        return ;

      $http.get('/api-user/').
        then(function(res) {
          $rootScope.userprofile = res.data;
        }, function(res) {
          if (res.status == 401){
            console.log('api-user fail', res.status, res.data);
            if (res.data.detail.indexOf( 'expired' ) > -1){
              $window.location.href = '/hoodpub-auth/facebook';
              console.log('expired');
            }
          }
        });
    }

    $scope.try_auth = function() {
      $http.post('/api-token-auth/', {"username":$scope.userprofile.username, "password":$scope.userprofile.password}).
        then(function(res) {
          localStorage.setItem('id_token', res.data.token);
          console.log('save new authenticated',  localStorage.getItem('id_token'));

          $rootScope.userprofile = res.data;
          $window.location.href = '/#/';
          init();

        }, function(res) {
          console.log(res);
          $scope.form = res.data;
          console.log('fail');

        });
    }

    $scope.logout = function (){
      localStorage.removeItem('id_token');
      delete $rootScope.userprofile;
      $window.location.href = '/#/';
    }
    init();

  }])
  .controller('hoodpubControllers', [
    '$rootScope', '$scope', '$window', '$routeParams' ,'$http',
    'Books', 'UserBooks', 'Analytics', '$uibModal', '$location', 'usSpinnerService',
    function($rootScope, $scope, $window, $routeParams, $http,
             Books, UserBooks, Analytics, $uibModal, $location, usSpinnerService){
      // scope functions

      $scope.search = function(keyword) {
        if ($scope.keyword)
          keyword = $scope.keyword;
        usSpinnerService.spin('spinner');
        Books.query({'search': keyword }).$promise.then(function(res) {
          delete $scope.items;
          $scope.items = res.results;
          next = res['next'];

          Analytics.trackEvent('search', 'keyword', $scope.keyword);
          usSpinnerService.stop('spinner');
        });
      };

      $scope.search_users = function(sns_id) {
        usSpinnerService.spin('spinner');
        UserBooks.query({'sns_id': sns_id }).$promise.then(function(res) {
          delete $scope.items;
          $scope.items = res.results;
          next = res['next'];
          $location.path('/user/'+ sns_id, false);
          Analytics.trackEvent('user', 'sns_id', sns_id);
          usSpinnerService.stop('spinner');

        });
      };

      $scope.book = function(id){
        $window.location.href = '/#/book?id='+id;
      };

      $scope.get_book = function(id){
        usSpinnerService.spin('spinner');
        Analytics.trackEvent('book', 'isbn', id);
        Books.get({'id': id}).$promise.then(function(res){
          delete $scope.item;
          $scope.item = res;
          $location.path('/book/'+ id);
        });
        usSpinnerService.stop('spinner');
      };

      $scope.read_book = function(item){

        if (typeof $rootScope.userprofile == 'undefined'){

          var modalInstance = $uibModal.open({
            animation: $scope.animationsEnabled,
            templateUrl: "myModalContent.html",
            resolve: {
              items: function () {
                return $scope.items;
              }
            }
          });

          console.log('please login', $rootScope.userprofile);
          return ;
        }
        isbn = item.isbn;
        var req = {
          method: 'POST',
          url: '/api-hoodpub/read/',
          data: { 'isbn': isbn }
        };
        $http(req).then(function()
                        {
                          item.is_read = true;
                          item.total_read++;
                          item.reads.push([
                            {'sns_id': $rootScope.userprofile.sns_id,
                             'name': $rootScope.userprofile.name}]);
                          Analytics.trackEvent('read', 'isbn', isbn);
                        },
                        function()
                        {
                          console.log('fail');
                        });

      };

      $scope.get_next = function(){
        if (typeof next == 'undefined'){
          return ;
        }
        $http.get(next)
          .success(function(res) {
            items = res['results'];

            for (var i = 0, len = items.length; i < len; i++) {
              $scope.items.push(items[i]);
            }
            next = res['next'];
          }
                  );
      };

      $scope.goto_list = function(id){
        $window.location.href = '/#/';
      };

      $scope.go_back = function(){
        if ($window.history.length > 1){
          $window.history.back(-1);
        }
        else{
          $scope.goto_list();
        }
      };

      $scope.postComment = function(book, comment){
        console.log(book, comment);

        isbn = book.isbn;
        var req = {
          method: 'POST',
          url: '/api-comment/onesentense/',
          data: { 'isbn': isbn,
                  'comment': comment}
        };
        $http(req).then(function()
                        {
                          $scope.onesentense='';
                          Analytics.trackEvent('comment', 'isbn', isbn);
                        },
                        function()
                        {
                          console.log('fail');
                        });
      };

      if ($window.location.hash.indexOf('book') > -1){
        console.log('before detail in get_book: ');
        $scope.get_book($routeParams.book_id);
      }
      else if ($window.location.hash.indexOf('user') > -1){
        $scope.search_users($routeParams.user_id);
      }
      else if ($window.location.hash.indexOf('/') > -1){
        $scope.search();
      }
    }])
;
