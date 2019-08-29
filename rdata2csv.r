args = commandArgs(trailingOnly=TRUE)
if (length(args) != 2) {
  print("Usage: Rscript rdata2csv.r --adnimerge.tar.gz --csv_output_folder")
  quit(save = "no", status = 1)
}

Sys.setenv(TAR = "/bin/tar")

adnimerge_file = gsub("--", "", args[1])
adnimerge_tar_data_path = "ADNIMERGE/data/"
output_folder = gsub("--", "", args[2])
untar_folder = gsub("--", "", args[2])
rdata_folder = paste(untar_folder, "/", adnimerge_tar_data_path, sep="")
temp_folder = paste(untar_folder, "/", "./ADNIMERGE/", sep="")

print(adnimerge_file)
print(untar_folder)
print(adnimerge_tar_data_path)

print("Extracting data from ADNIMERGE...")

untar(adnimerge_file, files = adnimerge_tar_data_path, exdir = untar_folder)

files = list.files(path = rdata_folder, pattern = "\\.rdata$")

# Create directory if does not exists
dir.create(file.path(output_folder), showWarnings = FALSE)
setwd(file.path(output_folder))

print("Converting data to csv...")
for (file in files) {
  # tryCatch(
  #   # This is what I want to do...
  #   {
      file_path = paste(rdata_folder, file, sep="")
      object <-load(file_path)
      print(file)
      sprintf("Saving %s", file)


      file_path_save = paste(object, ".csv", sep = "")
      write.csv(eval(as.name(object)), file = file_path_save, row.names = FALSE)
      eval(call("rm", eval(object)))
  #   },
  #   # ... but if an error occurs, tell me what happened:
  #   error=function(error_message) {
  #     sprintf('Error while converting %s', file)
  #     quit(save = "no", status = 1)
  #   },
  #   # ... but if an warning occurs, tell me what happened:
  #   warning=function(warning_condition) {
  #     {}
  #   }
  # )
}
print("Removing temp files")
unlink(temp_folder, recursive = TRUE)
print("Complete")
quit(save = "no", status = 0)
