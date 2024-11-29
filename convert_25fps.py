import os
import subprocess

# 경로 설정
input_dir = "/local_datasets/imsi/CelebV/videos/"
output_dir = "/local_datasets/CelebV/videos/"
os.makedirs(output_dir, exist_ok=True)

# 모든 파일 처리
for filename in os.listdir(input_dir):
    if filename.endswith((".mp4", ".avi", ".mkv", ".mov")):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        command = [
            "ffmpeg",
            "-i", input_path,
            "-vf", "fps=25",  # FPS 변경
            "-c:v", "libx264",  # 비디오 코덱 설정
            "-preset", "fast",  # 인코딩 속도 설정
            "-crf", "23",  # 품질 설정
            "-c:a", "aac",  # 오디오 코덱 설정
            "-b:a", "192k",  # 오디오 비트레이트
            output_path
        ]

        # FFmpeg 실행
        print(f"Processing: {filename}")
        subprocess.run(command, check=True)
