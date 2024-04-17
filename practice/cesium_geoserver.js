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

/** 
 // Event handler for "Add Path" button click
document.querySelector('.nav-link[href="#"]').addEventListener('click', function(event) {
  // Add path drawing functionality here
  drawPath();
});

// Function to draw a path on the Cesium map
function drawPath() {
  // Example: Drawing a path from New York to Los Angeles
  const newYork = Cesium.Cartesian3.fromDegrees(-74.0, 40.0);
  const losAngeles = Cesium.Cartesian3.fromDegrees(-118.0, 34.0);

  viewer.entities.add({
    name: 'Path',
    polyline: {
      positions: [newYork, losAngeles],
      width: 5,
      material: Cesium.Color.RED
    }
  });

  // Calculate the length of the path (straight-line distance)
  const length = Cesium.Cartesian3.distance(newYork, losAngeles);

  // Output length and other information as needed
  console.log('Length of the path:', length);
}*/



try {
  document.querySelector('.nav-link[href="#"]').addEventListener('click', function(event) {
    console.log("Button clicked");
    // Other functionality here
    let selectedPoints = [];

// Event handler for "Add Path" button click
document.querySelector('.nav-link[href="#"]').addEventListener('click', function(event) {
  // Clear previously selected points
  selectedPoints = [];
  // Activate point selection mode
  activatePointSelection();
});

// Function to activate point selection mode
// Function to activate point selection mode
function activatePointSelection() {
  // Disable default camera controls
  viewer.scene.screenSpaceCameraController.enableRotate = false;
  viewer.scene.screenSpaceCameraController.enableTranslate = false;
  viewer.scene.screenSpaceCameraController.enableZoom = false;
  viewer.scene.screenSpaceCameraController.enableTilt = false;
  viewer.scene.screenSpaceCameraController.enableLook = false;
  
  // Listen for clicks on the Cesium viewer
  const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
  handler.setInputAction(function(movement) {
    if (movement && movement.endPosition) {
      const cartesian = viewer.camera.pickEllipsoid(movement.endPosition, viewer.scene.globe.ellipsoid);
      if (cartesian) {
        selectedPoints.push(cartesian);
        if (selectedPoints.length === 2) {
          // Two points selected, draw the path
          drawPath(selectedPoints[0], selectedPoints[1]);
          // Reset selected points array
          selectedPoints = [];
          // Remove point selection mode
          handler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK);
          // Re-enable default camera controls
          viewer.scene.screenSpaceCameraController.enableRotate = true;
          viewer.scene.screenSpaceCameraController.enableTranslate = true;
          viewer.scene.screenSpaceCameraController.enableZoom = true;
          viewer.scene.screenSpaceCameraController.enableTilt = true;
          viewer.scene.screenSpaceCameraController.enableLook = true;
        }
      }
    }
  }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
}

// Function to draw a path between two points on the Cesium map
function drawPath(point1, point2) {
  viewer.entities.add({
    name: 'Path',
    polyline: {
      positions: [point1, point2],
      width: 5,
      material: Cesium.Color.RED
    }
  });

  // Calculate the length of the path (straight-line distance)
  const length = Cesium.Cartesian3.distance(point1, point2);

  // Output length and other information as needed
  console.log('Length of the path:', length);
}
  });
} catch (error) {
  console.error("Error occurred:", error);
}


const dynamicDataContainer = document.getElementById('dynamicDataContainer');
dynamicDataContainer.innerHTML = '<p>This is some dynamic data.</p>';