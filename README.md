# OPTRAM

![Screenshot_20220222_012713](https://user-images.githubusercontent.com/16523144/155042062-d74f38a0-6004-446a-83d6-0fc55506c40c.png)

## Python set-up 

I recommend to use a python env to avoid messing up your gdal configs

```{bash}
conda create --name spatial python=3.8
conda activate spatial
python -m ipykernel install --user --name=spatial

conda install pandas
conda install -y -c conda-forge utm
conda install -y rasterio
conda install -y -c conda-forge gdal
conda install -y -c conda-forge folium
conda install -y --channel conda-forge geopandas
conda install -y haversine
```



## Data

### Sensor

### SWRC Soil Hydrology Data

- Sensor Doc: https://www.tucson.ars.ag.gov/dap/dap_docs/soil.html
- Data: 
  - https://www.tucson.ars.ag.gov/dap/
  - https://www.tucson.ars.ag.gov/metDAP/


**SWRC 2 main Vegetative Covers**
- Lucky Hills (LH) subwatershed:
  - LHMet
  - LHTrench 
  - **TDRL1** -> 30 min UTM NAD83 EAST 589567 NORTH 3512290 ELEV 1366
    - https://www.tucson.ars.ag.gov/metDAP/SoilProfileSiteData/l1tdr17.out
    - https://www.tucson.ars.ag.gov/metDAP/SoilProfileSiteData/l1tdr18.out
  - **TDRL2** -> 30 min UTM NAD83 EAST 589793 NORTH 3512420 ELEV 1373
    - https://www.tucson.ars.ag.gov/metDAP/SoilProfileSiteData/l2tdr17.out
    - https://www.tucson.ars.ag.gov/metDAP/SoilProfileSiteData/l2tdr18.out   
- Grass dominated Kendall(KEN) subwatershed:
  - KNMet
  - KNTrench 
  - KSTrench
  - TDRK1
  - TDRK2 
- RAINGAGE SITES
  - **RG13** -> 30 min, 2008-present, UTM NAD83 EAST 586110 NORTH 3510185 ELEV 1334
    - https://www.tucson.ars.ag.gov/metDAP/RaingageSiteData/rg13vt17.out 
    - https://www.tucson.ars.ag.gov/metDAP/RaingageSiteData/rg13vt18.out 
  - **RG18** -> 30 min, 2008-present, UTM NAD83 EAST 586710 NORTH 3508098 ELEV 1365
    - https://www.tucson.ars.ag.gov/metDAP/RaingageSiteData/rg18vt17.out
    - https://www.tucson.ars.ag.gov/metDAP/RaingageSiteData/rg18vt18.out   -> NO SOIL DATA

  - **RG28** -> 30 min, 2008-present, UTM NAD83 EAST 590624 NORTH 3509990 ELEV 1369
    - https://www.tucson.ars.ag.gov/metDAP/RaingageSiteData/rg28vt17.out
    - https://www.tucson.ars.ag.gov/metDAP/RaingageSiteData/rg28vt18.out

  TDR = Time Domain Reflectometer.

### Satellite 

```{bash}
Rscript s2.R ./inputs-config.json ./Walnut-Gulch.geojson 'Walnut-Gulch' '2017-01-01' '2018-01-01'
./runSentinel.sh ./inputs-config.json ./Walnut-Gulch.geojson 'Walnut-Gulch' '2017-01-01' '2018-02-01'
```

## DATASOURCES

- https://nsidc.org/sites/nsidc.org/files/files/data/amsre-validation/nsidc0383-smex04-walnut-gulch-soil-moisture-az.pdf
- https://nsidc.org/data/search/#keywords=soil+moisture/sortKeys=score,,desc/facetFilters=%257B%257D/pageNumber=1/itemsPerPage=25


### Soil & precip data
- https://www.tucson.ars.ag.gov/dap/
- https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2006WR005702
- https://ameriflux.lbl.gov/sites/siteinfo/US-Wkg#overview

Locations: 
- https://usdaars.maps.arcgis.com/home/item.html?id=fe4ac74f13484a169899b166159e0bb5












