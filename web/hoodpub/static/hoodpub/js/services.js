angular.module('hoodpubServices', []).
    factory('Users', [
        '$resource', function($resource){
            return $resource('/api-user/', {}, {
                query: {method:'GET'}
            });
    }]).
    factory('Books', [
        '$resource', function($resource){
            return $resource('/api-book/:id/', {}, {
                get: {method:'GET', params:{id:'isbn'}},
                query: {method:'GET'}
            });
    }])
;
