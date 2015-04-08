var app = angular.module('PollApp', ['ngMaterial']).config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .accentPalette('blue');
});

function share(url) {
    window.location = url;
}

app.config(function($mdIconProvider) {
    $mdIconProvider
    .icon('facebook', 'http://upload.wikimedia.org/wikipedia/commons/c/c2/F_icon.svg', 24)
    .icon('twitter', 'https://upload.wikimedia.org/wikipedia/commons/a/af/Twitter_circle.svg', 24)
    .icon('gplus', 'http://upload.wikimedia.org/wikipedia/commons/5/5c/Google_plus.svg', 24);
});

app.controller('GridBottomSheetCtrl', function($scope, $mdBottomSheet, $location) {
	var currentUrl = $location.absUrl();
	var str = encodeURIComponent(currentUrl);
	var template_F = 'https://www.facebook.com/dialog/share?app_id=690937737684299&display=popup&href=[URL]&redirect_uri=[REDIR_URL]';
	var withUrl_F = template_F.replace('[URL]', str);
	withUrl_F = withUrl_F.replace('[REDIR_URL]', str);
	var template_T = 'https://twitter.com/intent/tweet?hashtags=PollPortal&text=Poll%20Portal&url=[URL]';
	var withUrl_T = template_T.replace('[URL]', str);
	var template_G = 'https://plus.google.com/share?url=[URL]';
	var withUrl_G = template_G.replace('[URL]', str);
	$scope.items = [ {
		name : 'Facebook',
		icon : 'facebook',
		href : withUrl_F
	}, {
		name : 'Tweet',
		icon : 'twitter',
		href : withUrl_T
	}, {
		name : 'Google+',
		icon : 'gplus',
		href : withUrl_G
	}, ];
	$scope.listItemClick = function($index) {
		var clickedItem = $scope.items[$index];
		$mdBottomSheet.hide(clickedItem);
	};
});

app.controller('AppCtrl', function($scope, $timeout, $mdBottomSheet) {
	  $scope.alert = '';
	  $scope.showGridBottomSheet = function($event) {
	    $scope.alert = '';
	    $mdBottomSheet.show({
	      templateUrl: '/sheet/',
	      controller: 'GridBottomSheetCtrl',
	      targetEvent: $event
	    }).then(function(clickedItem) {
	      $scope.alert = clickedItem.name + ' clicked!';
	    });
	  };
	})