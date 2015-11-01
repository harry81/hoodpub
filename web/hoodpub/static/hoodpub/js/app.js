'use strict';

angular.module('app', ['ngRoute', 'ngResource', 'angular-jwt',
                       'relativeDate',
                       'infinite-scroll', 'hoodpubServices', 'hoodpubControllers']).
    config(['$routeProvider', '$httpProvider', 'jwtInterceptorProvider', '$resourceProvider',
            function($routeProvider, $httpProvider, jwtInterceptorProvider, $resourceProvider) {
                $resourceProvider.defaults.stripTrailingSlashes = false;

                $routeProvider.
                    when('/list', {
                        templateUrl: '/static/hoodpub/templates/list.html',
                        controller: 'hoodpubControllers'
                    }).
                    when('/my', {
                        templateUrl: '/static/hoodpub/templates/my.html',
                        controller: 'myControllers'
                    }).
                    when('/login', {
                        templateUrl: '/static/hoodpub/templates/login.html',
                        controller: 'userControllers'
                    }).
                    when('/books', {
                        templateUrl: '/static/hoodpub/templates/books.html',
                        controller: 'hoodpubControllers'
                    }).
                    when('/book_search', {
                        templateUrl: '/static/hoodpub/templates/book_search.html',
                        controller: 'hoodpubControllers'
                    }).
                    when('/book_detail', {
                        templateUrl: '/static/hoodpub/templates/book_detail.html',
                        controller: 'hoodpubControllers'
                    }).
                    when('/order_complete', {
                        templateUrl: '/static/hoodpub/templates/order_complete.html',
                        controller: 'hoodpubControllers'
                    }).
                    otherwise({redirectTo: '/book_search'});

                $httpProvider.defaults.xsrfCookieName = 'csrftoken';
                $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

                $httpProvider.defaults.useXDomain = true;
                $httpProvider.defaults.withCredentials = true;
                delete $httpProvider.defaults.headers.common["X-Requested-With"];

                jwtInterceptorProvider.tokenGetter = ['jwtHelper', '$http', function(jwtHelper, $http) {
                    var idToken = localStorage.getItem('id_token');
                    if (! idToken) {
                        return ;
                    }

                    return idToken;
                }];
                $httpProvider.interceptors.push('jwtInterceptor');

            }])
;

