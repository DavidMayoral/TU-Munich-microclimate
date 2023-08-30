# -*- coding: utf-8 -*-

import requests
import io
import zipfile
import os

from dwd_data_info import dwd_data_info

##################################
# DEFINITIONS
##################################

output_folder = "downloaded_data_files"

##################################
# INITIALIZE DATA LISTS
##################################

urls = [dwd_data_info[ddi]["url"] for ddi in dwd_data_info]
file_names = [dwd_data_info[ddi]["file_name"] for ddi in dwd_data_info]

##################################
# HTTPS RETRIEVE
##################################

response = [None] * len(urls)   # this will store the response of the server for each url
errorcount = 0

print("\nStarting downloading")
for i, url in enumerate(urls):
    response[i] = requests.get(url)
    
    if response[i].status_code == 404:
        print("Error: File not found")
    elif response[i].status_code == 503:
        print("Error: Service unavailable")
    elif response[i].status_code == 401:
        print("Error: Unauthorised (Authentication required)")
    elif response[i].status_code == 403:
        print("Error: Forbidden")
    elif response[i].status_code == 200:
        print("\tDownload successful for: " + url)
        pass
    else:
        print("\tDownload failed for: " + url)
        errorcount += 1
print("Request terminated with", errorcount, "errors.")
print("Finished downloading.")

##################################
# ZIP EXTRACT AND WRITE
##################################

print("\nStarting extracting and writing")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i, file_name in enumerate(file_names):
    with zipfile.ZipFile(io.BytesIO(response[i].content)) as z:
        print("\tExtracting file: " + file_name)
        z.extract(file_name, path=output_folder)
print("Finished extracting and writing")