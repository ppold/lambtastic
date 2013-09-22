require(['./xhr', './promise'], function(xhr, Promise) {
	var initialize = function initialize(latitude, longitude) {
		var mapOptions = {
			center: new google.maps.LatLng(latitude, longitude),
			zoom: 14,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var map = new google.maps.Map(document.querySelector(".map-canvas"), mapOptions);

		function add_landmark (landmark) {
			var myLatlng = new google.maps.LatLng(landmark.latitude, landmark.longitude);
			var marker = new google.maps.Marker({
					position: myLatlng,
					title: landmark.name,
					map: map
			});
		}

		Promise.all(["historic", "museums", "sites"].map(function (resource) {
			return xhr.get("/landmarks/"+resource);
		})).then(function (resultList) {
			landmarks = [];

			resultList.forEach(function (data) {
				landmarks = landmarks.concat(JSON.parse(data[0]));
			});

			landmarks.forEach(add_landmark);
			template = Handlebars.compile(document.querySelector('#results_template').innerHTML);
			results = document.querySelector('#results');
			results.innerHTML = template({landmarks:landmarks});
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
