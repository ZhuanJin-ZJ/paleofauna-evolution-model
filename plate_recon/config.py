import pygplates
import os

BASE_PATH = r'C:\Users\acer\paleofauna-model\GPlates 2.5.0\GeoData\FeatureCollections\AltPlateReconstructions\Muller_etal_2022'
ROTATION_PATH = os.path.join(BASE_PATH, '1000_0_rotfile.rot')

rotation_model = pygplates.RotationModel(ROTATION_PATH)
