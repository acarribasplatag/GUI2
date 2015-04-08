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
    .icon('gplus', 'http://upload.wikimedia.org/wikipedia/commons/5/5c/Google_plus.svg', 24)
    .icon('tumblr', 'https://upload.wikimedia.org/wikipedia/commons/4/43/Tumblr.svg', 24)
    .icon('linkedin', 'https://upload.wikimedia.org/wikipedia/commons/c/ce/Linkedin_circle.svg', 24)
    .icon('email', 'http://upload.wikimedia.org/wikipedia/commons/b/b1/Email_Shiny_Icon.svg', 24);
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
	var template_TU = 'https://www.tumblr.com/widgets/share/tool?posttype=link&title=Poll%20Portal&content=[URL]';
	var withUrl_TU = template_TU.replace('[URL]', str);
	var template_LI = 'https://www.linkedin.com/shareArticle?url=[URL]&mini=true&title=Poll%20Portal';
	var withUrl_LI = template_LI.replace('[URL]', str);
	var template_email = 'mailto:?subject=Check%20out%20Poll%20Portal!&body=Here%27s%20a%20link:%0A[URL]';
	var withUrl_email = template_email.replace('[URL]', str);
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
	}, {
		name: 'Tumblr',
		icon: 'tumblr',
		href: withUrl_TU
	}, {
		name: 'LinkedIn',
		icon: 'linkedin',
		href: withUrl_LI
	}, {
		name: 'Email',
		icon: 'email',
		href: withUrl_email
	} ];
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