// See post: http://asmaloney.com/2015/06/code/clustering-markers-on-leaflet-maps

var map = L.map( 'map', {
  center: [23.7106169, 90.3632993],
  minZoom: 3,
  zoom: 5
});

L.tileLayer( 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
 attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
 subdomains: ['a','b','c']
}).addTo( map );

var myURL = jQuery( 'script[src$="leaf-demo.js"]' ).attr( 'src' ).replace( 'leaf-demo.js', '' );

var myIcon_hospital = L.icon({
  iconUrl: myURL + 'images/hospital_24_24.png',
  iconRetinaUrl: myURL + 'images/hospital_32_32.png',
  iconSize: [29, 24],
  iconAnchor: [9, 21],
  popupAnchor: [0, -14]
});

var myIcon_diagnostic = L.icon({
  iconUrl: myURL + 'images/diagnostic_24_24.png',
  iconRetinaUrl: myURL + 'images/diagnostic_32_32.png',
  iconSize: [29, 24],
  iconAnchor: [9, 21],
  popupAnchor: [0, -14]
});

var myIcon_pharmacy = L.icon({
  iconUrl: myURL + 'images/pharmacy_24_24.png',
  iconRetinaUrl: myURL + 'images/pharmacy_32_32.png',
  iconSize: [29, 24],
  iconAnchor: [9, 21],
  popupAnchor: [0, -14]
});

var markerClusters = L.markerClusterGroup();

// hospital
for ( var i = 0; i < markers_hospital.length; ++i )
{
  var popup = markers_hospital[i].name +
              '<br/>' + markers_hospital[i].city +
              '<br/><b>Phone:</b> ' + markers_hospital[i].phone +
              '<br/><b>PartnerCode:</b> ' + markers_hospital[i].partnercode +
              '<br/><b>Address:</b> ' + markers_hospital[i].address +
              '<br/><b>Discount:</b> ' + markers_hospital[i].discount_info +
              '<br/><b>Timezone:</b> ' + markers_hospital[i].tz;
  var m = L.marker( [markers_hospital[i].lat, markers_hospital[i].lng], {icon: myIcon_hospital} )
                  .bindPopup( popup );
  markerClusters.addLayer( m );
}

// diagnostic
for ( var i = 0; i < markers_diagnostic.length; ++i )
{
  var popup = markers_diagnostic[i].name +
              '<br/>' + markers_diagnostic[i].city +
              '<br/><b>Phone:</b> ' + markers_diagnostic[i].phone +
              '<br/><b>PartnerCode:</b> ' + markers_diagnostic[i].partnercode +
              '<br/><b>Address:</b> ' + markers_diagnostic[i].address +
              '<br/><b>Discount:</b> ' + markers_diagnostic[i].discount_info +
              '<br/><b>Timezone:</b> ' + markers_diagnostic[i].tz;
  var m = L.marker( [markers_diagnostic[i].lat, markers_diagnostic[i].lng], {icon: myIcon_diagnostic} )
                  .bindPopup( popup );
  markerClusters.addLayer( m );
}

map.addLayer( markerClusters );


// pharmacy
for ( var i = 0; i < markers_pharmacy.length; ++i )
{
  var popup = markers_pharmacy[i].name +
              '<br/>' + markers_pharmacy[i].city +
              '<br/><b>Phone:</b> ' + markers_pharmacy[i].phone +
              '<br/><b>PartnerCode:</b> ' + markers_pharmacy[i].partnercode +
              '<br/><b>Address:</b> ' + markers_pharmacy[i].address +
              '<br/><b>Discount:</b> ' + markers_pharmacy[i].discount_info +
              '<br/><b>Timezone:</b> ' + markers_pharmacy[i].tz;
  var m = L.marker( [markers_pharmacy[i].lat, markers_pharmacy[i].lng], {icon: myIcon_pharmacy} )
                  .bindPopup( popup );
  markerClusters.addLayer( m );
}

map.addLayer( markerClusters );
