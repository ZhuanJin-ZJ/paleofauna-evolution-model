6 December 2023

This directory contains sample palaeomagnetic data sets from the IAGA Global Paleomagnetic Database.

Please use the following citation for this dataset:

Pisarevsky, S. A., Li, Z. X., Tetley, M. G., Liu, Y., & Beardmore, J. P. (2022). An updated internet-based Global Paleomagnetic Database. Earth-Science Reviews, 104258, doi:10.1016/j.earscirev.2022.104258

The data was downloaded on 5 December 2023 from the Global Paleomagnetic Database (https://gpmdb.net/). 

The directory contains three files; two in the native GPlates compressed GPML format (gpmlz), and one raw csv file downloaded from the database. 

- vgp_features_gplates_default.gpmlz - cookie-cut with the QuickStart Deforming model
- vgp_features_muller2022.gpmlz - cookie-cut with the QuickStart Rigid model
- gpmdb-pmag-result-20231206.csv - raw CSV data downloaded from the database 

It is important that the files are loaded with their respective models from the GeoData, as the paleomagnetic data is sensitive to the suture locations (static polygons) and Plate IDs. You would need to activate a paleomagnetic reference frame to be evaluating these data. The NAME field contains the Resultnumber, which is a reference to the relevant row in the database.

To load these datasets in GPlates do the following:

1.  Open GPlates
2.  Pull down the GPlates File menu and select the operation Open Feature Collection
3.  Click all the files while holding down the shift key to select all files. All the GPMLZ files should be highlighted.
4.  Click Open 

Alternatively, drag and drop the files onto the globe.

Once loaded, the 
                 
In order to reconstruct these features, you will need to load in the underlying rotation model (.rot file) which can be found in the GeoData or downloaded from http://www.earthbyte.org/gplates-2-4-software-and-data-sets/.  

Play around with the GPlates buttons to make an animation, select features, draw features, etc.  For more information, read the GPlates manual which can be downloaded from www.gplates.org.
 

               
Any questions, please email:            
                                        Dietmar Müller dietmar.muller@sydney.edu.au
                                        Sabin Zahirovic sabin.zahirovic@sydney.edu.au

