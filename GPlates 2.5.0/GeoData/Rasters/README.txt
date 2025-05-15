25 June 2021

######### RASTERS #########

This directory contains several folders with global raster files in them. [Note: the resolution of the provided rasters has been limited to reduce the file size of the GPlates package. The original data sets are available in higher resolutions.]

Each raster has at least two associated files, a .jpg/.png/.tif image file AND also a GPlates .gpml file. For easiest results, open the .gpml file in GPlates. GPlates will then generate some cache files that help it display the raster. Generating the cache files takes up some hard drive space and can take a minute to generate them the first time the rasters are loaded. Each subsequent loading of the raster using the .gpml file will be quicker, as GPlates will use the already-generated cache files. The Seafloor_Age_Grid contains a third .gproj file which is the best one to load this raster. Also contained in each of these folders is a Legend image which gives an indication what the colours refer to.

Seafloor_Age_Grid - Seafloor_Age_Grid.grd, Seafloor_Age_Grid.gpml and Seafloor_Age_Grid_Project.gproj
NetCDF numerical grid of seafloor age consistent with the Seton et al. (2020) produced by the EarthByte group with 6 arc minute resolution. It is best to open the Project (.gproj), as this will import the correct colour palette settings. As this is a grid file (.grd) no legend is required, however, this is accessible from the GPlates Layers dialog. 

Suggested citations:
Seton, M., Müller, R. D., Zahirovic, S., Williams, S., Wright, N. M., Cannon, J., Whittaker, J. M., Matthews, K. J., and McGirr, R., 2020, A Global Data Set of Present-Day Oceanic Crustal Age and Seafloor Spreading Parameters: Geochemistry, Geophysics, Geosystems, v. 21, no. 10, p. e2020GC009214, doi: 10.1029/2020GC009214

Topography - Topography.jpg and Topography.gpml
Colour grid of present-day 1 arc minute resolution topography (ETOPO1) from Amante et al. (2009), with white regions representing ice sheets. This is available from the National Geophysical Data Center (NGDC). More information, and the original data in a variety of grid formats, can be found at http://www.ngdc.noaa.gov/mgg/global/global.html
Suggested citation:
Amante, C., Eakins, B., & Boulder, C. (2009). ETOPO1 1 arc-minute global relief model: Procedures, data sources and analysis. NOAA Technical Memorandum. 

Free_Air_Gravity_Anomalies - Free_Air_Gravity_Anomalies.jpg and Free_Air_Gravity_Anomalies.gpml
Colour grid of free air gravity anomalies from Sandwell and Smith (2014).
Suggested citation:
Sandwell, D. T., R. D. Müller, W. H. F. Smith, E. Garcia, R. Francis, New global marine gravity model from CryoSat-2 and Jason-1 reveals buried tectonic structure, Science, Vol. 346, no. 6205, pp. 65-67, doi: 10.1126/science.1258213, 2014.

Vertical_Gravity_Gradient - Vertical_Gravity_Gradient.jpg and Vertical_Gravity_Gradient.gpml
Colour grid of the vertical gravity gradient from Sandwell and Smith (2014). 
Suggested citation:
Sandwell, D. T., R. D. Müller, W. H. F. Smith, E. Garcia, R. Francis, New global marine gravity model from CryoSat-2 and Jason-1 reveals buried tectonic structure, Science, Vol. 346, no. 6205, pp. 65-67, doi: 10.1126/science.1258213, 2014.

Bouguer_Gravity_Anomalies - Bouguer_Gravity_Anomalies_WGM.jpg ad Bouguer_Gravity_Anomalies_WGM.gpml
Bouguer gravity anomalies from the World Gravity Map (Balmino et al., 2012). 
Suggested citation:
Balmino, G., Vales, N., Bonvalot, S. and Briais, A., 2012. Spherical harmonic modeling to ultra-high degree of Bouguer and isostatic anomalies. Journal of Geodesy. July 2012, Volume 86, Issue 7, pp 499-520 , doi: 10.1007/s00190-011-0533-4

Isostatic_Gravity_Anomalies - Isostatic_Gravity_Anomalies_WGM.png and Isostatic_Gravity_Anomalies_WGM.gpml
Isostatic gravity anomalies from the World Gravity Map (Balmino et al., 2012).
Suggested citation:
Balmino, G., Vales, N., Bonvalot, S., and Briais, A., 2012, Spherical harmonic modelling to ultra-high degree of Bouguer and isostatic anomalies: Journal of Geodesy, v. 86, no. 7, p. 499-520, doi:10.1007/s00190-011-0533-4.

Magnetic_Anomalies_EMAG2 - Magnetic_Anomalies_EMAG2.jpg and Magnetic_Anomalies_EMAG2.gpml
Colour grid of magnetic anomalies from EMAG2 (Maus et al., 2009). This raster does not use the directional gridding to fill gaps, and so better represents the raw magnetic data. More information, as well as the original data sets in their full resolution, can be found at http://www.geomag.org/models/emag2.html
Suggested citation:
Maus, S., Barckhausen, U., Berkenbosch, H., Bournas, N., Brozena, J., Childers, V., Dostaler, F., Fairhead, J., Finn, C., and von Frese, R., 2009, EMAG2: A 2-arc min resolution Earth Magnetic Anomaly Grid compiled from satellite, airborne, and marine magnetic measurements: Geochemistry, Geophysics, Geosystems, v. 10, no. 8, p. Q08005, doi:10.1029/2009GC002471.

Global_Geology - Global_Geology.png and Global_Geology.gpml
World geological map from Bouysse (2014) published by the UNESCO CGMW program. 
Suggested citation:
Bouysse, P., 2014, Geological Map of the World at 1:35 000 000.

Crustal_Thickness - Crustal_Thickness.png and Crustal_Thickness.gmpl
Crustal thickness model (CRUST 2.0) from Laske et al. (2000). 
Suggested citation:
Laske, G., Masters, G., and Reif, C., 2000, CRUST 2.0: A new global crustal model at 2x2 degrees, Institute of Geophysics and Planetary Physics, The University of California, San Diego, website: http://igppweb.ucsd.edu/~gabi/crust2.html.

Crustal_StrainRate - Crustal_StrainRate.png and Crustal_StrainRate.gpml
Second invariant of strain rate from Kreemer et al. (2014). 
Suggested citation:
Kreemer, C., Blewitt, G., and Klein, E. C., 2014, A geodetic plate motion and global strain rate model: Geochemistry, Geophysics, Geosystems, v. 15, https://doi.org/10.1002/2014GC005407

The quickest way to load these rasters in GPlates is to use the File > Open Feature Collection and point to the .gpml file on your machine. Alternatively, you can also click and drag the .gpml file onto the globe in the GPlates main window. The general approach to loading your own rasters in GPlates is to do the following:
1.  Open GPlates
2.  Pull down the GPlates File menu, select Import and then select Import Raster
3.  Navigate to and click on the appropriate file 
4.  Leave the default to be "band_1" and click Continue
5.  Specify the geographic extent (unless it is a NETCDF numerical grid where that information is automatically detected) and click Continue
6.  Click Done to create a new feature collection, and GPlates will create a .gpml file following the name of the raster

Note: When importing your own raster, GPlates will automatically generate a GPML file. To save time, next time you can just load the GPML file, and thus skip the import raster step. When loading rasters for the first time, GPlates may take a few minutes to generate the cache files that will enable efficient viewing. These only need to be generated once, however, if they are deleted, they will be re-generated.
                   
In order to reconstruct these features, you will need to load in the underlying rotation model (.rot file) which can be found in the GeoData or downloaded from http://www.earthbyte.org/gplates-2-4-software-and-data-sets/ and cookie-cut the data using the Static Polygon files, which can be found in the FeatureCollections directory.

Play around with the GPlates buttons to make an animation, select features, draw features, etc. For more information, read the GPlates manual which can be downloaded from www.gplates.org.

######### TIME-DEPENDENT RASTER #########

GPlates also has the ability to display time-dependent rasters. These rasters can be global or regional, and the suffix to the filename is a dash or underscore followed by an integer age in millions of years before present. In the GeoData we include a time-dependent raster of slabs age-coded from the MIT-P P-wave seismic tomography (Li et al., 2008), where slabs are assumed (on the first order) to sink vertically with a constant sinking rate. The sinking rate applied here is 3 cm/yr in the upper mantle, and 1.2 cm/yr in the lower mantle. The quickest way to visualise this dataset in GPlates is to load the .gpml file (MIT-P08-Asia-UM30-LM12.gpml) as described above. However, the first time the time-dependent rasters are loaded, GPlates will need to generate cache files for each depth/time layer. This process will take some minutes, and will take up a total of about 350 Mb of hard disk space. GPlates requires that the rasters follow the same filenaming format, and that they are all exactly the same dimensions (pixel width and height).
Suggested citation:
Li, C., van der Hilst, R., Engdahl, E., and Burdick, S., 2008, A new global model for P wave speed variations in Earth's mantle: Geochemistry, Geophysics, Geosystems, v. 9, no. 5, p. 21, doi:10.1029/2007GC001806.


The general approach to loading your own time-dependent rasters in GPlates is to do the following:
1.  Open GPlates
2.  Pull down the GPlates File menu, select Import and then select Import Time-Dependent Raster
3.  You can select an entire folder by clicking the "Add directory" button, or add files by clicking the "Add files" button
4.  GPlates will take some time to generate the cache files, after which you need to click Continue
5. 	Leave the default to be "band_1" and click Continue
7.  Specify the geographic extent (unless it is a NETCDF numerical grid where that information is automatically detected) and click Continue
8.  Click Done to create a new feature collection, and GPlates will create a .gpml file following the name of the time-dependent raster. You will only need to load the GPML the next time you need to use the time-dependent raster, which allows you to bypass the re-import process. 
          
               
Any questions, please email:            
                                        Dietmar Müller dietmar.muller@sydney.edu.au
                                        Sabin Zahirovic sabin.zahirovic@sydney.edu.au
                                        Maria Seton maria.seton@sydney.edu.au
