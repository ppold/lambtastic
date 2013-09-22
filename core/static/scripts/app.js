require(['./xhr'], function(xhr) {
	var initialize = function initialize(latitude, longitude) {
		var mapOptions = {
			center: new google.maps.LatLng(latitude, longitude),
			zoom: 14,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var map = new google.maps.Map(document.querySelector(".map-canvas"), mapOptions);

		xhr.get("/landmarks/museums").then(function result (data) {
			JSON.parse(data).forEach(function add_landmark (landmark) {
				var myLatlng = new google.maps.LatLng(landmark.latitude, landmark.longitude);
				console.log(landmark);
				var marker = new google.maps.Marker({
				    position: myLatlng,
				    title: landmark.name
				});

				marker.setMap(map);
			});
		});
	}

	var response = function response(position) {
		var latitude = position.coords.latitude;
		var longitude = position.coords.longitude;

		initialize(latitude, longitude);
	}

	var get_location = function get_location() {
		// navigator.geolocation.getCurrentPosition(response, function errorHandler (error) {
		// 	console.log('error', error);
		// });

		response({coords:{
			latitude: -12.0639788,
			longitude: -77.03694980000002
		}});
	}

	get_location();
})
