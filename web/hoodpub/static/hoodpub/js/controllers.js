angular.module('hoodpubControllers', []).
    controller('authControllers', ['$scope', '$http', '$window', 'Users',
                                   function ($scope, $http, $window, Users) {

        function try_facebook_auth() {
            localStorage.setItem('id_token', $scope.token_objects.access_token);

            Users.query().$promise.then(function(res) {
                $window.location.href = '/#/books';
            });
        }

        $scope.$watch('$viewContentLoaded', function() {
            try_facebook_auth();
        });

    }]).

    controller('userControllers', [
        '$scope', '$http', '$window',
        function($scope, $http, $window){

            function init(){
                $http.get('/api-user/').
                    then(function(res) {
                        $scope.user = res.data.user;
                        console.log('after init: ', $scope.user);
                    }, function(res) {
                        console.log('fail');
                    });
            }

            $scope.try_auth = function() {
                $http.post('/api-token-auth/', {"username":$scope.username, "password":$scope.password}).
                    then(function(res) {
                        localStorage.setItem('id_token', res.data.token);
                        console.log('save new authenticated',  localStorage.getItem('id_token'));

                        $scope.user = res.data.user;
                        $window.location.href = '/#/list';
                        init();

                    }, function(res) {
                        console.log(res);
                        $scope.form = res.data;
                        console.log('fail');

                    });
            }

            $scope.logout = function (){
                localStorage.removeItem('id_token');
                delete $scope.user;
                console.log('logout');
            }
            init();
        }])
    .controller('hoodpubControllers', [
        '$scope', '$window', '$routeParams' ,'$http', 'Books', 'UserBooks',
        function($scope, $window, $routeParams, $http, Books, UserBooks){
            // scope functions
            $scope.search = function(keyword) {
                if ($scope.keyword)
                    keyword = $scope.keyword;
                Books.query({'search': keyword }).$promise.then(function(res) {
                    console.log(res);

                    $scope.items = res.results;
                    next = res['next'];
                });
            }

            $scope.search_users = function(sns_id) {
                UserBooks.query({'sns_id': sns_id }).$promise.then(function(res) {
                    console.log(res);

                    $scope.items = res.results;
                    next = res['next'];
                });
            }

            $scope.book_detail = function(id){
                $window.location.href = '/#/book_detail?id='+id;
            }

            $scope.get_book_detail = function(id){
                Books.get({'id': id}).$promise.then(function(res){
                    console.log('detail : ',  res);
                    $scope.item = res;
                });
            }

            $scope.read_book = function(isbn){
                var req = {
                    method: 'POST',
                    url: '/api-hoodpub/read/',
                    data: { 'isbn': isbn }
                }
                $http(req).then(function()
                                {
                                    console.log('sucess');
                                },
                                function()
                                {
                                    console.log('fail');
                                });

            }

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
            }

            $scope.goto_list = function(id){
                $window.location.href = '/#/books';
            }

            if ($window.location.hash.indexOf('book_detail') > -1){
                $scope.get_book_detail($routeParams.id);
            }
            $scope.search();
        }])
;
