 args <- commandArgs(TRUE)	
 json_model <- args[1]
 AOI        <- args[2]
 name       <- args[3]
 start_d    <- args[4]
 end_d      <- args[5]

 print(args) 
 sen2r::check_gcloud('/home/rstudio/google-cloud-sdk')
 sen2r::write_scihub_login("your_account", "your_password")
 inputs<- jsonlite::fromJSON(json_model)
 inputs$extent <- AOI
 inputs$extent_name <- name

 if (is.null(start_d) && is.null(end_d)){
   inputs$timewindow <- diffdate
 } else{
   inputs$timewindow[1] <- toString(start_d)  
   inputs$timewindow[2] <- toString(end_d)    
 }
 print(inputs)
 file_arg <- tempfile(pattern = name, tmpdir = "./tmp", fileext = ".json")
 write(jsonlite::toJSON(inputs), file_arg)
 res<-sen2r::sen2r(param_list = file_arg)
 unlink(file_arg)

