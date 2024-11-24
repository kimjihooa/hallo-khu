import os
import subprocess

# 경로 설정
video_dir = "/local_datasets/HDTF/renamed_videos/"
image_dir = "/local_datasets/Images/"
audio_dir = "/local_datasets/Audios/"

def get_video_length(video_path):
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        return float("inf")  # 오류 발생 시 최대값 반환

video_lengths = []
for filename in os.listdir(video_dir):
    if filename.endswith((".mp4", ".avi", ".mkv", ".mov")):  # 지원하는 확장자
        video_path = os.path.join(video_dir, filename)
        length = get_video_length(video_path)
        video_lengths.append((filename, length))

video_lengths.sort(key=lambda x: x[1])  # 두 번째 요소(length) 기준으로 오름차순 정렬

shortest_videos = [name for name, length in video_lengths[:100]]  # 가장 짧은 100개
longest_videos = [name for name, length in video_lengths[-190:]]  # 가장 긴 190개
print(f"Shortest 100 videos: {shortest_videos}")
print(f"Longest 190 videos: {longest_videos}")


def delete_files(video_names, image_dir, audio_dir):
    for video_name in video_names:
        base_name, _ = os.path.splitext(video_name)

        # 이미지 삭제
        image_path = os.path.join(image_dir, f"{base_name}.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted: {image_path}")

        # 오디오 삭제
        audio_path = os.path.join(audio_dir, f"{base_name}.wav")
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"Deleted: {audio_path}")


delete_files(shortest_videos, image_dir, audio_dir)
delete_files(longest_videos, image_dir, audio_dir)
