import os
import cv2

target_path = "/local_datasets/HDTF/renamed_videos/"

video_lengths = []

for file_name in os.listdir(target_path):
    file_path = os.path.join(target_path, file_name)

    if file_name.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.flv')):
        try:
            cap = cv2.VideoCapture(file_path)
            length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = length / fps if fps > 0 else 0
            cap.release()
            video_lengths.append((file_path, duration))
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

video_lengths.sort(key=lambda x: x[1], reverse=True)

# 상위 100개 파일 삭제
for i, (file_path, duration) in enumerate(video_lengths[:290]):
    try:
        os.remove(file_path)
        print(f"Deleted ({i+1}/100): {file_path} - Duration: {duration:.2f} seconds")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

print("Completed deleting top longest videos.")
