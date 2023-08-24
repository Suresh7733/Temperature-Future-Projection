var platform = new H.service.Platform({
    apikey: 'XWqfUKW1OA8uB-1JbSwdMVQAMFrOkFoERDaGXt4y0e4'
  });
  var defaultLayers = platform.createDefaultLayers();
  var map = new H.Map(
    document.getElementById('map'),
    defaultLayers.vector.normal.map,
    {
      zoom: 5,
      center: { lat: 23.3937, lng: 78.9629 }
    }
  );
  var marker;
  var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));
  map.addEventListener('tap', function (evt) {
  var coord = map.screenToGeo(evt.currentPointer.viewportX,
    evt.currentPointer.viewportY);
  addMarker(map,coord.lat,coord.lng)
});

function addMarker(map, latitude, longitude) {
  
  if (marker) {
    map.removeObject(marker);
    
  }

   marker = new H.map.Marker({lat: latitude, lng: longitude});
  map.addObject(marker);
  document.getElementById("lat").value = latitude.toFixed(6);
  document.getElementById("lon").value = longitude.toFixed(6);
}
