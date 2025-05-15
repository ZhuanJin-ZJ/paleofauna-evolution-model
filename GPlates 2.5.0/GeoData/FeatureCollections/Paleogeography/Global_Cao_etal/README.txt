7 September 2021

This directory contains a global paleogeography model from Cao et al. (2017). 

The folder contains four shapefiles (i: ice sheet, m: mountain, lm: landmass and sm: shallow marine). Each shapefile is a collection of features for all time intervals from 402 to 2 Ma. For instance, the file of "m_402_2.shp" is a conbination of all mountain geometries on all revised paleogeographic maps. Note that the alternative time scale ICS2016 as two new columns named "START_ICS" and "END_ICS" is added to the attributes of the each shapefile.

Since the shapefiles are all at present-day coordinates, to reconstruct them in GPlates, please load them and the relevant rotation files (using the Matthews et al., 2016 model) in GPlates and reconstruct them to geological time. Note that, to avoid artefacts introduced from overlapping paleogeographies, the display order must use the following sequence: ice sheets, mountains, landmasses and finally shallow marine environments (top to bottom layering). 

The project file (.gproj) is a GPlates project file, which loads all of the relevant files. You can download additional data from here:
https://www.biogeosciences.net/14/5425/2017/

If you have any question about GPlates, please see the tutorials on GPlates website (https://www.gplates.org/).

Citations:
Cao, W., Zahirovic, S., Flament, N., Williams, S., Golonka, J., and Müller, R. D., 2017, Improving global paleogeography since the late Paleozoic using paleobiology: Biogeosciences, v. 14, no. 23, p. 5425-5439, DOI:10.5194/bg-14-5425-2017.
Matthews, K. J., Maloney, K. T., Zahirovic, S., Williams, S. E., Seton, M., and Müller, R. D., 2016, Global plate boundary evolution and kinematics since the late Paleozoic: Global and Planetary Change, DOI: 10.1016/j.gloplacha.2016.10.002.

Any other question, please email: Sabin Zahirovic sabin.zahirovic@sydney.edu.au
                                  Wenchao Cao wenchao.cao@sydney.edu.au
                                  Nicolas Flament nflament@uow.edu.au
                                  Simon Williams simon.williams@nwu.edu.cn
                                  Dietmar Müller dietmar.muller@sydney.edu.au
                                  Maria Seton maria.seton@sydney.edu.au
