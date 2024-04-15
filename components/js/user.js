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

    // Add event listener for form submission
    const form = document.getElementById('user-input-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        // Get uploaded files
        const soilMoistureFile = document.getElementById('soil-moisture').files[0];
        const ndviFile = document.getElementById('ndvi').files[0];
        const spiFile = document.getElementById('spi').files[0];
        const stiFile = document.getElementById('sti').files[0];
        const lithologyFile = document.getElementById('lithology').files[0];

        // Add layers to the map
        addLayer('Soil Moisture', soilMoistureFile);
        addLayer('NDVI', ndviFile);
        addLayer('SPI', spiFile);
        addLayer('STI', stiFile);
        addLayer('Lithology', lithologyFile);
    });
});

// Function to add a layer to the map
function addLayer(name, file) {
    const reader = new FileReader();
    reader.onload = function (event) {
        const url = event.target.result;
        const layer = new ol.layer.Image({
            title: name,
            source: new ol.source.ImageStatic({
                url: url,
                projection: 'EPSG:3857', // Assuming the projection of the uploaded files is EPSG:3857 (Web Mercator)
                imageExtent: [-20037508.34, -20037508.34, 20037508.34, 20037508.34] // Full extent of EPSG:3857
            })
        });
        map.addLayer(layer);
    };
    reader.readAsDataURL(file);
}
