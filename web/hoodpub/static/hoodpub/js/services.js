angular.module('hoodpubServices', []).
    factory('Auth', [
        '$resource', function($resource){
            return $resource('/api-token-auth/', {
                query: {method:'POST'}
            });
    }]).
    factory('Users', [
        '$resource', function($resource){
            return $resource('/api-user/', {}, {
                query: {method:'GET'}
            });
    }]).
    factory('Books', [
        '$resource', function($resource){
            return $resource('/api-book/:id/', {}, {
                get: {method:'GET', params:{id:'id'}},
                query: {method:'GET'}
            });
    }])
;
