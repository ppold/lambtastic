require(['./xhr'], function(xhr) {
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
			console.log(landmark);
		}

		xhr.get("/landmarks/museums").then(function result (data) {
			jsonResult = JSON.parse(data);
			jsonResult.forEach(add_landmark);
			template = Handlebars.compile(document.querySelector('#results_template').innerHTML);
			results = document.querySelector('#results');
			results.innerHTML = template({landmarks:jsonResult});
		});

		xhr.get("/landmarks/historic").then(function result (data) {
			jsonResult = JSON.parse(data);
			jsonResult.forEach(add_landmark);
			template = Handlebars.compile(document.querySelector('#results_template').innerHTML);
			results = document.querySelector('#results');
			results.innerHTML = template({landmarks:jsonResult});
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
