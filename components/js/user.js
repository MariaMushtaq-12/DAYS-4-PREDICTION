document.addEventListener('DOMContentLoaded', function () {
    // Initialize OpenLayers map with only base layer
    const map = new ol.Map({
        target: 'map-container',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM() // Add OpenStreetMap as the base layer
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([0, 0]),
            zoom: 2
        })
    });
});
