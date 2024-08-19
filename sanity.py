import os

def sanitise(folder_path, target_pattern,target_string):

# Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):
        if target_pattern.casefold() in filename.casefold():
            file_path = os.path.join(folder_path, filename)
            
            # Read the content of the file
            with open(file_path, 'r', encoding='utf8', errors='ignore') as file:
                content = file.read()
            
            # Find the index of the target string
            index = content.find(target_string)
            if index != -1:
                # Truncate the content after the target string
                truncated_content = content[:index + len(target_string)]
                
                # Save the modified content back to the file
                with open(file_path, 'w') as file:
                    file.write(truncated_content)
                print(f"Processed and saved: {filename}")


sanitise("./data/depth_2", "https___www_mayoclinic_org","There is a problem with information submitted for this request")
