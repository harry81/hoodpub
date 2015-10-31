angular.module('hoodpubServices', []).
    factory('Users', [
        '$resource', function($resource){
            return $resource('/api-user/', {}, {
                query: {method:'GET'}
            });
    }]).
    factory('UserBooks', [
        '$resource', function($resource){
            return $resource('/api-hoodpub/:sns_id/users/', {}, {
                query: {method:'GET', params:{sns_id:'sns_id'}},
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
