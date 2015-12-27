angular.module('hoodpubControllers', []).
  controller('graphControllers', [
    '$scope', '$http', '$window', 'UserBooks', '$routeParams',
    function ($scope, $http, $window, UserBooks, $routeParams) {
      // Step 1. We create a graph object.
      var hoodpub = new HoodpubGraph();
      console.log('hoodpub obj', hoodpub);

      $scope.get_graph_user = function(user_id){
        UserBooks.query({'sns_id': user_id }).$promise.then(function(res) {
          hoodpub.AddLinkNode(res);
          hoodpub.run();
          next = res['next'];

          if (next != null){
            $http.get(next).
              then(function(res) {
                hoodpub.AddLinkNode(res.data);
              }, function(res) {
                console.error('error');
              });
          }
        });
      };

      if ($window.location.hash.indexOf('graph') > -1){
        $scope.get_graph_user($routeParams.user_id);
      }

    }]).
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
    };

    $scope.logout = function (){
      localStorage.removeItem('id_token');
      delete $rootScope.userprofile;
      $window.location.href = '/#/';
    };
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

var HoodpubGraph = function () {
  var nodeSize = 35,
      book_height = 60,
      book_width = 40,
      user_height = 35,
      user_width = 35,
      self = this;

  this.graph = Viva.Graph.graph();
  this.graphics = Viva.Graph.View.svgGraphics();

  this.layout = Viva.Graph.Layout.forceDirected(this.graph, {
    springLength : 50,
    springCoeff : 0.000008,
    dragCoeff : 0.008,
    gravity : -1.2
  });

  this.graphics.node(function(node) {
    var ui = Viva.Graph.svg('g'),
        svgText = Viva.Graph.svg('text').attr('y', '-4px').text(node.data.label),
        img = Viva.Graph.svg('image')
          .attr('width', node.data.type == 'book' ? book_width : user_width)
          .attr('height', node.data.type == 'book' ? book_height : user_height)
          .link(node.data.url);

    $(ui).hover(function() { // mouse over
      $('#sidebar').show();
      console.log('node :', node.id);
      $('#sidebar>img').attr('src', node.data.url);
      $('span.title').text(node.data.label);
    }, function() { // mouse out
    }).click(function() {
      if (node.data.type == 'book'){
        window.open('https://hoodpub.com/book/'.concat(node.id), '_blank');
      }
      else if (node.data.type == 'user'){
        console.log('node.data.type :', 'user');

        $.ajax({
          url: 'https://www.hoodpub.com/api-hoodpub/'.concat(node.id).concat('/users/'),
          data: {
            format: 'json'
          },
          error: function() {
            console.error('error');
          },
          success: function(data) {
            console.log('good');
            self.AddLinkNode(data);

          },
          type: 'GET'
        });

      }
    });

    // ui.append(svgText);
    ui.append(img);
    return ui;
  })
    .placeNode(function(nodeUI, pos){
      // Shift image to let links go to the center:
      nodeUI.attr('transform',
                  'translate(' +
                  (pos.x - nodeSize/2) + ',' + (pos.y - nodeSize/2) +
                  ')');
    });

  this.renderer = Viva.Graph.View.renderer(
    this.graph,
    {
      graphics : this.graphics,
      layout : this.layout,
      prerender: 20,
      container : document.getElementById('graphDiv')
    });

};

HoodpubGraph.prototype.run = function() {
  this.renderer.run();
};

HoodpubGraph.prototype.AddLinkNode = function(res) {
  console.log('res:', res );
    books = res.results;
    next = res['next'];

    for (var cnt_book = 0, book_len = books.length;
         cnt_book < book_len; cnt_book++) {
      this.graph.addNode(books[cnt_book].isbn, {
        type: 'book',
        url: books[cnt_book].cover_s_url,
        label: books[cnt_book].title,
        size: 70
      });

      reads = books[cnt_book].reads;
      for (var cnt_user = 0, user_len = reads.length;
           cnt_user < user_len; cnt_user++) {
        pic_url = 'https://graph.facebook.com/'.concat(reads[cnt_user].user[0].sns_id).concat('/picture');
        this.graph.addNode(reads[cnt_user].user[0].sns_id, {
          type: 'user',
          url: pic_url,
          label: reads[cnt_user].user[0].sns_id,
          size: 40
        });

        this.graph.addLink(books[cnt_book].isbn, reads[cnt_user].user[0].sns_id);
      }
    }

  };
