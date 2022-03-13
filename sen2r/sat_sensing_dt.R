# Rscript sat_sensing_dt "2021-01-01" "2021-01-10" Walnut-Gulch.geojson

library(magrittr)

args <- commandArgs(trailingOnly = TRUE)
geojson  = args[0]
start_dt = args[1] # yyyy-mm-dd
end_dt   = args[2]

#files <- list.files(folder.BOA, full.names = T)

time_window <- as.Date(c(start_dt, end_dt))
results <- geojsonsf::geojson_sfc(parcela.json) %>% 
  sen2r::s2_list(time_interval = time_window)

sensing_dt <- sen2r::safe_getMetadata(results, "sensing_datetime")
sensing_dt