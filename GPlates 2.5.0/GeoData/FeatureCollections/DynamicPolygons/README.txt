1 December 2023

This directory contains the Zahirovic et al. (2022) topological plate polygon and plate boundary dataset. 

Note: The mantle reference frame has been recomputed in this version. 

Directory contains one file:

- Zahirovic_etal_2022_Plate_Boundaries.gpml - contains the topologies that reference the individual lines and features 
- Zahirovic_etal_2022_Feature_Geometries.gpml - contains the individual lines and features 

To load these datasets in GPlates do the following:

1.  Open GPlates
2.  Pull down the GPlates File menu and select the operation Open Feature Collection
3.  Click the file you want to load
4.  Click Open 

Alternatively, drag and drop the file onto the globe.
                   
In order to reconstruct these features, you will need to load in the underlying rotation model (.rot file) which can be found in the GeoData or downloaded from http://www.earthbyte.org/gplates-2-4-software-and-data-sets/.  

The topological plate polygon file is different to the standard data files released with GPlates. This file includes both the plate polygons and the intersecting lines that make up the plate polygons.  When you load the gpml file into GPlates, the plate polygons and the intersecting lines will be displayed.  However, for the purpose of visualization, you may want to only display the plate polygon data. To do this, go to the Layers toolbar on the right hand side of the screen. Click on the eye next to green tab. This will make all the lines that make up the plate polygons invisible, allowing only the plate polygons to be displayed. To switch the lines back on, just click the eye again. Note: Not all the topologies or topological features are stored in this file - you will need to also load in the FeatureCollections/DeformingLithosphere active and inactive deformation topologies. 

For more information on using topological data, see the GPlates tutorials.

Please use the following citation for this dataset:

Zahirovic, S., Eleish, A., Doss, S., Pall, J., Cannon, J., Pistone, M., and Fox, P., 2022, Subduction kinematics and carbonate platform interactions: Geoscience Data Journal, doi: 10.1002/gdj3.146

Müller, RD, Zahirovic, S, Williams, SE, Cannon, J, Seton, M, Bower, DJ, Tetley, MG, Heine, C, Le Breton, E, Liu, S, Russell, SHJ, Yang, T, Leonard, J & Gurnis, M 2019, 'A global plate model including lithospheric deformation along major rifts and orogens since the Triassic', Tectonics, vol. 38, no. Fifty Years of Plate Tectonics: Then, Now, and Beyond, doi: 10.1029/2018TC005462

Cao, X, Zahirovic, S, Li, S, Suo, Y, Wang, P, Liu, J & Muller, RD 2020, 'A deforming plate tectonic model of the South China Block since the Jurassic', Gondwana Research, doi: 10.1016/j.gr.2020.11.010

Young, A, Flament, N, Maloney, K, Williams, S, Matthews, K, Zahirovic, S & Müller, RD 2019, 'Global kinematics of tectonic plates and subduction zones since the late Paleozoic Era', Geoscience Frontiers, doi: 10.1016/j.gsf.2018.05.011

Torsvik, TH, Steinberger, B, Shephard, GE, Doubrovine, PV, Gaina, C, Domeier, M, Conrad, CP & Sager, WW 2019, 'Pacific‐Panthalassic reconstructions: Overview, errata and the way forward', Geochemistry, Geophysics, Geosystems, vol. 20, no. 7, pp. 3659-89, doi: 10.1029/2019GC008402

Any questions, please email:            
                                        Dietmar Müller dietmar.muller@sydney.edu.au
                                        Sabin Zahirovic sabin.zahirovic@sydney.edu.au
                                        Maria Seton maria.seton@sydney.edu.au

