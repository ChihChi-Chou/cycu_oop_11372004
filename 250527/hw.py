<!DOCTYPE html>
<html>
<head>
    
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css"/>
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css"/>
    
            <meta name="viewport" content="width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
            <style>
                #map_003c3ce3f8131ea5ca7e78a5dae15bc6 {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
                .leaflet-container { font-size: 1rem; }
            </style>

            <style>html, body {
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
            }
            </style>

            <style>#map {
                position:absolute;
                top:0;
                bottom:0;
                right:0;
                left:0;
                }
            </style>

            <script>
                L_NO_TOUCH = false;
                L_DISABLE_3D = false;
            </script>

        
</head>
<body>
    
    
            <div class="folium-map" id="map_003c3ce3f8131ea5ca7e78a5dae15bc6" ></div>
        
</body>
<script>
    
    
            var map_003c3ce3f8131ea5ca7e78a5dae15bc6 = L.map(
                "map_003c3ce3f8131ea5ca7e78a5dae15bc6",
                {
                    center: [25.033, 121.5654],
                    crs: L.CRS.EPSG3857,
                    ...{
  "zoom": 13,
  "zoomControl": true,
  "preferCanvas": false,
}

                }
            );

            

        
    
            var tile_layer_63effc8fff147db96594cc20f4f55b11 = L.tileLayer(
                "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                {
  "minZoom": 0,
  "maxZoom": 19,
  "maxNativeZoom": 19,
  "noWrap": false,
  "attribution": "\u0026copy; \u003ca href=\"https://www.openstreetmap.org/copyright\"\u003eOpenStreetMap\u003c/a\u003e contributors",
  "subdomains": "abc",
  "detectRetina": false,
  "tms": false,
  "opacity": 1,
}

            );
        
    
            tile_layer_63effc8fff147db96594cc20f4f55b11.addTo(map_003c3ce3f8131ea5ca7e78a5dae15bc6);
        
    
            var marker_1e0f02deddb023679fcd46d3d0097588 = L.marker(
                [25.033, 121.5654],
                {
}
            ).addTo(map_003c3ce3f8131ea5ca7e78a5dae15bc6);
        
    
            var icon_ef70e7d5e68bcaae67cbd30f0e7416bc = L.AwesomeMarkers.icon(
                {
  "markerColor": "green",
  "iconColor": "white",
  "icon": "info-sign",
  "prefix": "glyphicon",
  "extraClasses": "fa-rotate-0",
}
            );
        
    
        var popup_d9ebe5bbbf6ea0f216007898fed8e223 = L.popup({
  "maxWidth": "100%",
});

        
            
                var html_097376e129eea7d70d682408012604dc = $(`<div id="html_097376e129eea7d70d682408012604dc" style="width: 100.0%; height: 100.0%;">站牌1 (ID: 2315202960)</div>`)[0];
                popup_d9ebe5bbbf6ea0f216007898fed8e223.setContent(html_097376e129eea7d70d682408012604dc);
            
        

        marker_1e0f02deddb023679fcd46d3d0097588.bindPopup(popup_d9ebe5bbbf6ea0f216007898fed8e223)
        ;

        
    
    
                marker_1e0f02deddb023679fcd46d3d0097588.setIcon(icon_ef70e7d5e68bcaae67cbd30f0e7416bc);
            
    
            var marker_0f3dbe599ead2ca7fcf01b4a815d5818 = L.marker(
                [25.037, 121.563],
                {
}
            ).addTo(map_003c3ce3f8131ea5ca7e78a5dae15bc6);
        
    
            var icon_8f87b4558cb1930f8e3591a92686e7a4 = L.AwesomeMarkers.icon(
                {
  "markerColor": "orange",
  "iconColor": "white",
  "icon": "info-sign",
  "prefix": "glyphicon",
  "extraClasses": "fa-rotate-0",
}
            );
        
    
        var popup_9eaade42af080942144348999891545d = L.popup({
  "maxWidth": "100%",
});

        
            
                var html_63144e6f5be85f29254f34fe99db9bda = $(`<div id="html_63144e6f5be85f29254f34fe99db9bda" style="width: 100.0%; height: 100.0%;">站牌2 (ID: 2314301700)</div>`)[0];
                popup_9eaade42af080942144348999891545d.setContent(html_63144e6f5be85f29254f34fe99db9bda);
            
        

        marker_0f3dbe599ead2ca7fcf01b4a815d5818.bindPopup(popup_9eaade42af080942144348999891545d)
        ;

        
    
    
                marker_0f3dbe599ead2ca7fcf01b4a815d5818.setIcon(icon_8f87b4558cb1930f8e3591a92686e7a4);
            
</script>
</html>