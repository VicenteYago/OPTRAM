# Rscript sat_sensing_dt.R "2021-01-01" "2021-01-10" Walnut-Gulch.geojson

library(magrittr)

args <- commandArgs(trailingOnly = TRUE)
print(args)
start_dt = args[1] # yyyy-mm-dd
end_dt   = args[2]
geojson  = args[3]

#files <- list.files(folder.BOA, full.names = T)
time_window <- as.Date(c(start_dt, end_dt))
print(geojson)
gj.sf = geojsonsf::geojson_sfc(geojson)
results = sen2r::s2_list(gj.sf, time_interval = time_window)

sensing_dt <- sen2r::safe_getMetadata(results, "sensing_datetime")
sensing_dt
