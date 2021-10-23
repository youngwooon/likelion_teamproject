function initMap() {
    let org_lat = origin_lat
    let org_lng = origin_lng
    const directionsRenderer = new google.maps.DirectionsRenderer();
    const directionsService = new google.maps.DirectionsService();
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 14,
      center: { lat: parseFloat(org_lat), lng: parseFloat(org_lng) },
    });
  
    directionsRenderer.setMap(map);
    calculateAndDisplayRoute(directionsService, directionsRenderer);
    document.getElementById("mode").addEventListener("change", () => {
      calculateAndDisplayRoute(directionsService, directionsRenderer);
    });
  }
  
  function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    const selectedMode = document.getElementById("mode").value;
    let org_lat = origin_lat
    let org_lng = origin_lng
    let des_lat = destination_lat
    let des_lng = destination_lng
    directionsService
      .route({
        origin: { lat: parseFloat(org_lat), lng: parseFloat(org_lng) },
        destination: { lat: parseFloat(des_lat), lng: parseFloat(des_lng) },
        // Note that Javascript allows us to access the constant
        // using square brackets and a string value as its
        // "property."
        travelMode: google.maps.TravelMode[selectedMode],
      })
      .then((response) => {
        directionsRenderer.setDirections(response);
      })
      .catch((e) => window.alert("Directions request failed due to " + status));
  }