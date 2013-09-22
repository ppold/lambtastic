function initialize(latitude, longitude) {
	var mapOptions = {
		center: new google.maps.LatLng(latitude, longitude),
		zoom: 14,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.querySelector(".map-canvas"), mapOptions);
}

var response = function response(position) {
	var latitude = position.coords.latitude;
	var longitude = position.coords.longitude;


	initialize(latitude, longitude);
}

var get_location = function get_location() {
	navigator.geolocation.getCurrentPosition(response);
}

get_location();


