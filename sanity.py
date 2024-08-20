import os
import unicodedata

def sanitise(folder_path, target_pattern,target_string):

# Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):
        if target_pattern.casefold() in filename.casefold():
            file_path = os.path.join(folder_path, filename)
            
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.read()

                # first sanitise - remove exotic bytes like 0xa0 or 0x97
                clean_content = unicodedata.normalize("NFKD",content)
                print(f"sanitising file: {filename}")

                # Find the the target string
                index = clean_content.find(target_string)
                if index != -1:
                    # Truncate the content after the target string
                  #  clean_content = clean_content[:index + len(target_string)]
                    print (f"trunkated file: {filename}")
                    
                # Save the modified content back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(clean_content)
                print(f"Processed and saved: {filename}")
            

sanitise("./data/depth_2", "https___www_mayoclinic_org","There is a problem with information submitted for this request")
