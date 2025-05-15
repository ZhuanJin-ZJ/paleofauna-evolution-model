25 June 2021

This directory contains both polygon and polyline coastline files. The coastline for Greenland uses the Danish Geological Survey dataset, and the rest of the world uses the World Vector Shoreline from the the Global Self-consistent Hierarchical High-resolution Geography (GSHHG) dataset, Version 2.3.7. The coastline data included here is a simplified version of the "high" resolution GSHHG coastline data - simplified in ArcGIS with simplification tolerance 0.05 decimal degrees (min area: 100 sq km). The coastlines are cookie-cut first using the static polygons, with a second stage applied where oceanic volcanic provinces (Johansson et al., 2018 - see FeatureCollections/IgneousProvinces) are used to assign ages to oceanic islands related to hotspots. 

For more information on the GSHHG see:
http://www.ngdc.noaa.gov/mgg/shorelines/gshhs.html

The simplified GSHHG polygon and polyline coastline have been made consistent with the Muller et al. (2019) model and two file formats are given:
shapefile (ESRI shapefile .shp format): 
- Global_EarthByte_GPlates_PresentDay_Coastlines.shp 
- Global_EarthByte_GPlates_PresentDay_Coastlines_Polyline.shp
gpmlz (native GPlates Markup Language .gpml compressed format): 
- Global_EarthByte_GPlates_PresentDay_Coastlines.gpmlz 
- Global_EarthByte_GPlates_PresentDay_Coastlines_Polyline.gpmlz

To load these datasets in GPlates do the following:

1.  Open GPlates
2.  Pull down the GPlates File menu and select the operation Open Feature Collection
3.  Click all the files while holding down the shift key to select all files.  All the files should be highlighted.
4.  Click Open 

Alternatively, drag and drop the GPMLZ or SHP file onto the globe.

You now have a coastline and polyline coastline file loaded in GPlates. 

Note: When loading a shapefile, GPlates may prompt you to associate shapefile attributes with GPlates model properties. You just need to click OK. However, if loading your own shapefiles, you may need to ensure that the model properties are mapped correctly.
                   
In order to reconstruct these features, you will need to load in the underlying rotation model (.rot file) which can be found in the GeoData or downloaded from http://www.earthbyte.org/gplates-2-4-software-and-data-sets/.

Play around with the GPlates buttons to make an animation, select features, draw features, etc.  For more information, read the GPlates manual which can be downloaded from www.gplates.org.
     


Any questions, please email:            
                                        Sabin Zahirovic sabin.zahirovic@sydney.edu.au
                                        Dietmar Müller dietmar.muller@sydney.edu.au
                                        Maria Seton maria.seton@sydney.edu.au


			