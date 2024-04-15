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

    // Function to add a layer to the map
    function addLayer(name, source) {
        const layer = new ol.layer.Image({
            title: name,
            source: new ol.source.ImageStatic({
                url: source,
                projection: 'EPSG:3857', // Assuming the projection of the uploaded files is EPSG:3857 (Web Mercator)
                imageExtent: [-20037508.34, -20037508.34, 20037508.34, 20037508.34] // Full extent of EPSG:3857
            })
        });
        map.addLayer(layer);
    }

    // Add layers for testing
    addLayer("Open Street Map", "https://a.tile.openstreetmap.org/")
    addLayer("ESRI World Imagery", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}");

    // Add Layers widget
    const layerSwitcher = new ol.control.LayerSwitcher({
        reverse: true,
        groupSelectStyle: 'children',
        showOpacity: true,
        showLabels: true,
        collapsed: false
    });
    map.addControl(layerSwitcher);
});
