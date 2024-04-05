// Your access token can be found at: https://ion.cesium.com/tokens.
Cesium. Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlZTg3MGQ4MC03MTk5LTRkYWEtYjQxMi0xMDVjN2NkMmQxOTciLCJpZCI6MjAxNjk0LCJpYXQiOjE3MTAzNTIyMzd9.SE_vrP6TmeW-jMwWEkvhttlScC-IT0t0N9l842ZPDPg';
// Initialize the Cesium Viewer in the HTML element with the `cesiumContainer` ID.
const viewer = new Cesium.Viewer('cesiumContainer', {
  terrain: Cesium.Terrain.fromWorldTerrain(),
});    

/** const viewer = new Cesium.Viewer("cesiumContainer", {
baseLayer: Cesium.ImageryLayer.fromWorldImagery({
terrain: Cesium.Terrain.fromWorldTerrain(),
style: Cesium.IonWorldImageryStyle.AERIAL_WITH_LABELS,
}),
baseLayerPicker: true,
});*/

//osm 3d building
const tileset = viewer.scene.primitives.add(
await Cesium.Cesium3DTileset.fromIonAssetId(96188),
);
//viewer.scene.primitives.add(Cesium.createOsmBuildingsAsync());
// Fly the camera to astore district at the given longitude, latitude, and height.
viewer.camera.flyTo({
  destination: Cesium.Cartesian3.fromDegrees(74.90, 33.10, 100000),
  orientation: {
    heading: Cesium.Math.toRadians(10.0),
    pitch: Cesium.Math.toRadians(-29.0),
  }
});


// GeoServer WMS URL
const geoserverUrl = "http://localhost:8081/geoserver/fyp/wms";
  var imageryLayers = viewer.imageryLayers;
  imageryLayers.addImageryProvider(
    new Cesium.WebMapServiceImageryProvider({
      url: "http://localhost:8081/geoserver/fyp/wms",
      layers: "	fyp:final_astore_project",
      parameters: {
        transparent: true,
        format: "image/png",
      },
    })
  );

