# Rscript sat_sensing_dt.R "2021-01-01" "2021-01-10" Walnut-Gulch.geojson 2> /dev/null

args <- commandArgs(trailingOnly = TRUE)
start_dt = args[1] # yyyy-mm-dd
end_dt   = args[2] # yyyy-mm-dd
geojson  = args[3]

time_window <- as.Date(c(start_dt, end_dt))
gj.sf = geojsonsf::geojson_sfc(geojson)
results = sen2r::s2_list(gj.sf, time_interval = time_window)

sensing_dt <- sen2r::safe_getMetadata(results, "sensing_datetime")
sensing_dt
