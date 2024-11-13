import os
import subprocess
import shutil

local_dataset_dir = "/local_datasets"
root_dir = '/data/kimjihooa/repos/hallo'

# Step 3: Prepare paths for image and audio directories
image_dir = os.path.join(local_dataset_dir, "Images")  # Adjust as needed after extraction
audio_dir = os.path.join(local_dataset_dir, "Audios")  # Adjust as needed after extraction
output_dir = os.path.join(root_dir, "outputs")

# Ensure output directory exists
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# Get all image files
image_files = sorted([f for f in os.listdir(image_dir) if f.endswith(".jpg")])

# Step 4: Run Hallo inference for each image-audio pair
for img in image_files:
    audio_filename = os.path.splitext(img)[0] + ".wav"
    audio_path = os.path.join(audio_dir, audio_filename)

    # Check if the audio file exists
    if not os.path.exists(audio_path):
        print(f"Audio file for {img} not found, skipping...")
        continue

    # Define paths
    img_path = os.path.join(image_dir, img)
    output_path = os.path.join(output_dir, f"{os.path.splitext(img)[0]}.mp4")

    # Run the hallo inference command
    command = f"python scripts/inference.py --source_image {img_path} --driving_audio {audio_path} --output {output_path}"
    subprocess.call(command, shell=True)

    print(f"Processed {img} with {audio_filename}")

print("All videos processed successfully.")
