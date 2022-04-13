![WG-nologo.png](https://github.com/VicenteYago/OPTRAM/blob/main/img/WG-nologo.png)

# Implementation of Optical Trapezoid Model (OPTRAM) with Sentinel 2 

The Optical Trapezoid Model (OPTRAM) was developed to overcome the limitations of the Thermal-Optical Trapezoid Model (TOTRAM), i.e., non aplicability to satellites that do not provide thermal data, and the requirement of parametrization for each individual date. Based on Short Wave Infrared Reflectance (SWIR), Normalized Difference Vegetation Index (NDVI) and in situ measurements at surface level, the OPTRAM has demostrated to be a significant advance for remote sensing of soil moisture with great importance to undestand seasonal dynamics, water resource planning and agricultural production.

The present work its a implementation of the OPTRAM based on the paper [sadegui et al 2017](https://www.sciencedirect.com/science/article/abs/pii/S0034425717302493), however some differences are worth mentioning: 

- Only the Galnut Gulch Watershed area has been modelized, leaving aside Little Washita.
- 71 Sentinel2 BOA (Level 2A) images corresponding to 2019 TOA (Level 1C) have been used, in contrast to the 17 images corresponding to the year 2015 used in the article. Because of BOA level, radiometric, atmospheric and geometric corrections were not needed.

- The Sentinel2 [SCL](https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-2a/algorithm) band was used as a single mask to filter water bodies, clouds, saturated pixels, etc, as a consequence, the clustering and water body classification models of the original article were not necessary.

- Both methods for the estimation of the 𝜃𝑑, 𝜃𝑤 coefficients, corresponding to the two scenarios presented in the original article have been implemented, although only the first scenario is fully developed.


Adittionaly in some parts, the implementation makes advantage of parallel computations to process the tens of millions of data to be computed in a single computer.


## NDVI-STR space

The wet and dry edges are fitted by visual matching as recomended by the authors.
![NDVI_STR.png](https://github.com/VicenteYago/OPTRAM/blob/main/img/NDVI_STR.png)

`inSitu_obs` are the images pixels corresponing to the soil moisture stations al the time of the acquisition by the sentinel2 satellites.

## Results 

![scenario_comparison](https://github.com/VicenteYago/OPTRAM/blob/main/img/scenario1_2_comparison.png)

More detailed insight about the heavy scatter can be found in the notebook, section __Model parametrization__.

## W maps
Normalized soil moisture content were also computed for all images.
<p align="center">
  <img src=https://github.com/VicenteYago/OPTRAM/blob/main/img/example_W_2.png/>
</p>

The SCL band is applied at each image, masking diferent pixels at each date.



## Q&A 

#### Its your code fully reproducible ? 
Yes

#### Why units differ from the original paper, I mean why the estimate soil moisture is in % an not in cm3/cm3^-1? 
Yes

#### Are your results different from the original paper ? 
Yes

#### W maps are great but, how theta maps are built ? 
Yes

#### I spotted an error on your code / I need some aclarations ... 
Yes

