import os
import subprocess
import shutil

# 경로 설정
video_dir = "/local_datasets/HDTF/renamed_videos/"
image_dir = "/local_datasets/Images/"
audio_dir = "/local_datasets/Audios/"

# 동영상 길이 가져오기 함수
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

# 모든 동영상의 길이 가져오기
video_lengths = []
for filename in os.listdir(video_dir):
    if filename.endswith((".mp4", ".avi", ".mkv", ".mov")):  # 지원하는 확장자
        video_path = os.path.join(video_dir, filename)
        length = get_video_length(video_path)
        video_lengths.append((filename, length))

# 길이 기준 정렬
video_lengths.sort(key=lambda x: x[1])  # 두 번째 요소(length) 기준으로 정렬

# 가장 짧은 100개의 파일 이름 가져오기
shortest_videos = [name for name, length in video_lengths[:100]]
print(f"Shortest 100 videos: {shortest_videos}")

# 이미지와 오디오 파일 삭제
for video_name in shortest_videos:
    base_name, _ = os.path.splitext(video_name)  # 확장자 제거하여 기본 이름 추출

    # 이미지 삭제
    image_path = os.path.join(image_dir, f"{base_name}.png")  # 예: 이미지 확장자가 .png라고 가정
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Deleted: {image_path}")

    # 오디오 삭제
    audio_path = os.path.join(audio_dir, f"{base_name}.wav")  # 예: 오디오 확장자가 .wav라고 가정
    if os.path.exists(audio_path):
        os.remove(audio_path)
        print(f"Deleted: {audio_path}")
