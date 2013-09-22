require(['./xhr', './promise'], function(xhr, Promise) {
	var initialize = function initialize(latitude, longitude) {
		var mapOptions = {
			center: new google.maps.LatLng(latitude, longitude),
			zoom: 14,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		var directionsDisplay = new google.maps.DirectionsRenderer();
		var map = new google.maps.Map(document.querySelector(".map-canvas"), mapOptions);
		var directionsService = new google.maps.DirectionsService();
		directionsDisplay.setMap(map);

		var myLatlng = new google.maps.LatLng(latitude, longitude);
		var from = new google.maps.Marker({
				position: myLatlng,
				title: 'Posición actual',
				map: map,
				icon: '/static/img/current.png'
		});

		var markers = [];

		function add_landmark (landmark) {
			var icon = null;

			if (landmark.kind == 'urban') {
				icon = '/static/img/town-hall-24.png';
			} else if (landmark.kind == 'historic') {
				icon = '/static/img/monument-24.png';
			} else if (landmark.kind == 'museo') {
				icon = '/static/img/museum-24.png';
			}

			var myLatlng = new google.maps.LatLng(landmark.latitude, landmark.longitude);
			var marker = new google.maps.Marker({
					position: myLatlng,
					title: landmark.name,
					map: map,
					icon: icon
			});

			markers.push(marker);
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

			function show_route (from, to) {
				var request = {
					origin:from.position,
					destination:to.position,
					travelMode: google.maps.TravelMode.DRIVING
				};
				directionsService.route(request, function(result, status) {
					if (status == google.maps.DirectionsStatus.OK) {
						console.log(result);
						directionsDisplay.setDirections(result);
					}
				});
			}


			var wholeListing = document.querySelector("#results");

			Array.prototype.forEach.call(document.querySelectorAll("li", wholeListing), function (elem) {
				elem.addEventListener('click', function (event) {
					var index = Array.prototype.indexOf.call(wholeListing.children, event.currentTarget);
					show_route(from, markers[index]);
				});
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
