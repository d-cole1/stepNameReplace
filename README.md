## Use
This code processes Bill of Materials (BOM) data from an Excel file and updates STEP files in a specified directory. 
The execute_func function reads the BOM data into a DataFrame, verifies its format, and locates STEP files. It then 
creates an output directory and processes each STEP file by replacing specific strings based on the BOM data. The 
helper functions stp_finder, extract_mre_bom, and check_bom_format assist in locating STEP files, reading the BOM 
data, and verifying its format. The step_name_replace function handles the string replacements in the STEP files, 
ensuring the processed files are correctly updated and saved.
