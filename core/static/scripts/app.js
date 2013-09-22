function initialize() {
	var mapOptions = {
		center: new google.maps.LatLng(-34.397, 150.644),
		zoom: 8,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	var map = new google.maps.Map(document.querySelector(".map-canvas"), mapOptions);
}
initialize();
// google.maps.event.addDomListener(window, 'load', initialize);
