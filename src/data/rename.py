import os

# Define the path to the directory containing the city_code directories
base_directory = 'src\data'

# Iterate over each city_code directory
for city_code in os.listdir(base_directory):
    city_code_path = os.path.join(base_directory, city_code)
    
    # Check if it is a directory
    if os.path.isdir(city_code_path):
        # Iterate over each file in the city_code directory
        for filename in os.listdir(city_code_path):
            if filename.startswith('merged_') and filename.endswith('.csv'):
                # Extract the emission part of the filename
                emission = filename[len('merged_'):-len('.csv')]
                
                # Define the new filename
                new_filename = f'{emission}.csv'
                
                # Define the full paths for the old and new filenames
                old_file_path = os.path.join(city_code_path, filename)
                new_file_path = os.path.join(city_code_path, new_filename)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed {old_file_path} to {new_file_path}')