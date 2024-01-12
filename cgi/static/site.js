function authClick() {
    // fetch("/auth?login=user&password=123") // переводимо на схему Basic
    const cred = btoa( 'user:123' );
    fetch("/auth", {
        headers: {
            'Authorization': `Basic ${cred}`
        }
    })
    .then(response => response.json())
    .then(j => sessionStorage.setItem('token', j.data["token"]))
}

function infoClick() {
    fetch("/auth", { 
        method: 'post', 
        headers: { 
            'Authorization': 'Bearer ' + sessionStorage.getItem('token'),
            'My-Header' : 'my-value'
        } 
    } )
    .then(r => r.json())
    .then(console.log);
}

function publishClick() {
    fetch("/product", { 
        method: 'post', 
        headers: { 
            'Authorization': 'Bearer ' + sessionStorage.getItem('token')
        },
        body: JSON.stringify( {
            name: 'Коробка 10х10х10',
            price: 19.50,
            image: "box2.png"
        } )
    } )
    .then(r => r.json())
    .then(console.log);
}

angular.module('app', [])
  .directive('products', function() {
    return {
      restrict: 'E',
      transclude: true,
      scope: {},
      controller: function($scope, $http) {
        $scope.products = [];
        $http.get('/product').then(r => $scope.products = r.data.data)
      },
      templateUrl: `/static/tpl/product.html`,
      replace: true
    };
  });

function addCartClick(e) {
    const productId = e.target.closest('[data-product-id]').getAttribute('data-product-id');
    const userToken = sessionStorage.getItem('token');
    fetch('/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${userToken}`,
        },
        body: JSON.stringify( { productId } )
    }).then( r => r.text() ).then( console.log );
}