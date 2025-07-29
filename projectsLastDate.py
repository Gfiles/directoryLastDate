import os
import pandas as pd
from datetime import datetime

def get_last_modified_files(working_directory):
    # List to hold file information
    file_info = {
        'project': [],
        'solution': [],
        'filename': [],
        'modified': []
    }

    # Walk through the directory and its subdirectories
    last_modified_time = 0
    last_solution = ""
    for root, dirs, files in os.walk(working_directory):
        #print(f"Processing directory: {dirs}")
        #check if 'deploy' in directory name
        #print(f"files: {files}")
        # check if file has .log
        log_file_list = dict()
        #if any(file.endswith('.log') for file in files):
        for file in files:
            if file.endswith('.log'):
                # get Solution Name
                root_parts = root.split(os.sep)
                solution_name = root_parts[-3]
                file_info['project'].append(root_parts[-4])
                file_info['solution'].append(solution_name)
                file_info['filename'].append(file)
                modified_time = os.path.getmtime(os.path.join(root, file))
                
                file_info['modified'].append(datetime.fromtimestamp(modified_time).date())
                continue
  
    return file_info

    
def display_table(file_info):
    # Create a DataFrame
    df = pd.DataFrame(file_info)
    # Display the DataFrame as a table
    print(df)

if __name__ == "__main__":
    # get working directory
    working_directory = os.getcwd()

    logs_directory = 'logs'  # Change this to your logs directory
    file_info = get_last_modified_files(working_directory)
    #display_table(file_info)
    df = pd.DataFrame(file_info)
    # group by solution and get the max modified date
    df['modified'] = pd.to_datetime(df['modified'])
    print(df.groupby(["project", "solution"])["modified"].max())
    input("Press Enter to exit...")