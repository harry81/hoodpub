'use strict';

angular.module('app', ['ngRoute', 'ngResource', 'angular-jwt',
                       'relativeDate',
                       'infinite-scroll', 'hoodpubServices', 'hoodpubControllers', 'angular-google-analytics', 'ui.bootstrap']).
    config(['$routeProvider', '$httpProvider', 'jwtInterceptorProvider', '$resourceProvider', 'AnalyticsProvider',
            function($routeProvider, $httpProvider, jwtInterceptorProvider, $resourceProvider, AnalyticsProvider) {
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

                AnalyticsProvider.setAccount('UA-35673137-1');
                AnalyticsProvider
                    .logAllCalls(true);

                // Track all routes (default is true).
                AnalyticsProvider.trackPages(true);

                // Track all URL query params (default is false).
                AnalyticsProvider.trackUrlParams(true);

                // Ignore first page view (default is false).
                // Helpful when using hashes and whenever your bounce rate looks obscenely low.
                AnalyticsProvider.ignoreFirstPageLoad(true);

                // URL prefix (default is empty).
                // Helpful when the app doesn't run in the root directory.
                AnalyticsProvider.trackPrefix('hoodpub-web');

                // Change the default page event name.
                // Helpful when using ui-router, which fires $stateChangeSuccess instead of $routeChangeSuccess.
                AnalyticsProvider.setPageEvent('$stateChangeSuccess');
            }]).
        app.run(['$route', '$rootScope', '$location', function ($route, $rootScope, $location) {
        var original = $location.path;
        $location.path = function (path, reload) {
            if (reload === false) {
                var lastRoute = $route.current;
                var un = $rootScope.$on('$locationChangeSuccess', function () {
                    $route.current = lastRoute;
                    un();
                });
            }
            return original.apply($location, [path]);
        };
    }])
;

