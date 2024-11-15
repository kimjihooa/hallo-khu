import os
import random

directory = "/local_datasets/HDTF/videos/"

for i in range(1, 100):
    file_name = f"{i:05}.mp4"
    file_path = os.path.join(directory, file_name)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    else:
        print(f"File not found: {file_path}")

all_files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

files_to_delete = random.sample(all_files, 90)

for file_path in files_to_delete:
    try:
        os.remove(file_path)
        print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

print("Deletion complete.")
