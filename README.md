
![WG-nologo.png](https://github.com/VicenteYago/OPTRAM/blob/main/WalnutGulch/img/WG-nologo.png)

# Implementation of Optical Trapezoid Model (OPTRAM) with Sentinel 2 

The Optical Trapezoid Model (OPTRAM) was developed to overcome the limitations of the Thermal-Optical Trapezoid Model (TOTRAM), i.e., non aplicability to satellites that do not provide thermal data, and the requirement of parametrization for each individual date. Based on Short Wave Infrared Reflectance (SWIR), Normalized Difference Vegetation Index (NDVI) and in situ measurements at surface level, the OPTRAM has demostrated to be a significant advance for remote sensing of soil moisture with great importance to undestand seasonal dynamics, water resource planning and agricultural production.

The present work its a implementation of the OPTRAM based on the paper [sadegui et al 2017](https://www.sciencedirect.com/science/article/abs/pii/S0034425717302493), however some differences are worth mentioning: 

- Only the Walnut Gulch Watershed area has been modelized, leaving aside Little Washita.
- 71 Sentinel2 BOA (Level 2A) images corresponding to 2019 TOA (Level 1C) have been used, in contrast to the 17 images corresponding to the year 2015 used in the article. Because of BOA level, radiometric, atmospheric and geometric corrections were not needed.

- The Sentinel2 [SCL](https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm) band was used as a single mask to filter water bodies, clouds, saturated pixels, etc, as a consequence, the clustering and water body classification models of the original article were not necessary.

- Both methods for the estimation of the 𝜃𝑑, 𝜃𝑤 coefficients, corresponding to the two scenarios presented in the original article have been implemented, although only the first scenario is fully developed.

Adittionaly in some parts, the implementation makes advantage of parallel computations to process the tens of millions of data to be computed in a single computer.

# Data
The OPTRAM models needs intensive data from surface soil moisture sensors and satellite images. In the following subsections both sources will be detailed. This graphs summarizes the process of data processing: 

<p align="center">
  <img src="https://github.com/VicenteYago/OPTRAM/blob/main/WalnutGulch/img/scheme_full.png/"  width="400">
</p>

- **1-3** : Sensor processing, the filtering of incomplete sensors will be performed here.
- **4-8** : Very complex but made easy by [sen2r](http://sen2r.ranghetti.info/index.html) library in R, rasterio and gdal in python.
- **9**   : This data fusion is key to obtain a full implementation of the OPTRAM model. The sensor readings of each station are matched with the nearest pixels of each image at the acqusition time, allowing for volumetric content water (%) predictions once the model is validated. Aditionally a big speed up is achieved using the parallel library [Dask](https://dask.org/). 
- **10**  : The Scheme Classification Layer ([SCL](https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm)) already computed by Copernicus is used to mask the defective pixels, i.e., clouds, snow, shadows, etc.
- **11**  : Finally, with the filtered data and inSitu fusion observations the OPTRAM can be fitted.

## NDVI-STR space

The wet and dry edges are fitted by visual matching as recomended by the authors.
![NDVI_STR.png](https://github.com/VicenteYago/OPTRAM/blob/main/WalnutGulch/img/NDVI_STR.png)

`inSitu_obs` are the images pixels corresponing to the soil moisture stations al the time of the acquisition by the sentinel2 satellites.

## Results 

![scenario_comparison](https://github.com/VicenteYago/OPTRAM/blob/main/WalnutGulch/img/scenario1_2_comparison.png)

More detailed insight about the heavy scatter can be found in the notebook, section __Model parametrization__.

## W maps
Normalized soil moisture content were also computed for all images.
<p align="center">
  <img src=https://github.com/VicenteYago/OPTRAM/blob/main/WalnutGulch/img/example_W_2.png/>
</p>

The SCL band is applied at each image, masking diferent pixels at each date.

## Reproduce it 
1. Clone the repo
```{python}
git lfs install
git clone https://github.com/VicenteYago/OPTRAM.git
```
2. Set up the enviroment
```{python}
conda env create -f environment.yml
conda activate optram
# make the env available as kernel inside jupyter notebook
python -m ipykernel install --user --name=optram
```

Also you can view it in [nbviewer](https://nbviewer.org/github/VicenteYago/OPTRAM/blob/main/OPTRAM.ipynb).

## Q&A 

#### Its your code fully reproducible ? 
Yes, the repo has all the files, and time consuming objects are already computed and ready to be load inside the notebook. But if you want to build it from the scratch you will have to download the original Sentinel2 SAFE products. 

#### Why units differ from the original paper, I mean why the estimate soil moisture is in % an not in cm3/cm3^-1? 
The article has 𝜃 in gravimetric units while the implementation has it in volumetric units. The reason is the South Watershed Reseach Center has the SM5 or 𝜃 in the former unit, and I have not been able to find a direct conversion between them.

#### Are your results different from the original paper ? 
In some extent yes, this may be due to the fact that its not a exact replica i.e., it is not the same sampling year the volume of images used are very different etc. Anyways my results are a bit worse, but I think the notebook provides a good insight about why may be the reason. And of course there may be mistakes about the implementation.

#### W maps are great but what about 𝜃 maps ? 
W maps has the disadvantage that they are no different from a water index such as NDWI in that they are a normalized measure. The OPTRAM solves this as its able to provide actually physical predictions about the soil moisture in volumetric/gravimetric units. The 𝜃 maps are built by applying the 𝜃 ~ W regression model but its not cover in the original paper, however in a coming notebook several alternatives to obtain the volumetric 𝜃 maps will be implemented.

#### I spotted an error/optimization in your code, how can I proceed ? 
In both situations I would be very grateful, you can open an issue and report your findings. I am aware that there may be errors, but that is why I made this repository, so that we can improve our understanding of this great model.

