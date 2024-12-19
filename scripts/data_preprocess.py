# pylint: disable=W1203,W0718
"""
This module is used to process videos to prepare data for training. It utilizes various libraries and models
to perform tasks such as video frame extraction, audio extraction, face mask generation, and face embedding extraction.
The script takes in command-line arguments to specify the input and output directories, GPU status, level of parallelism,
and rank for distributed processing.

Usage:
    python -m scripts.data_preprocess --input_dir /path/to/video_dir --dataset_name dataset_name --gpu_status --parallelism 4 --rank 0

Example:
    python -m scripts.data_preprocess -i data/videos -o data/output -g -p 4 -r 0
"""
import argparse
import logging
import os
from pathlib import Path
from typing import List

import cv2
import torch
from tqdm import tqdm

from hallo.datasets.audio_processor import AudioProcessor
from hallo.datasets.image_processor import ImageProcessorForDataProcessing
from hallo.utils.util import convert_video_to_images, extract_audio_from_videos
import subprocess


# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def setup_directories(video_path: Path) -> dict:
    """
    Setup directories for storing processed files.

    Args:
        video_path (Path): Path to the video file.

    Returns:
        dict: A dictionary containing paths for various directories.
    """
    base_dir = video_path.parent.parent
    dirs = {
        "face_mask": base_dir / "face_mask",
        "sep_pose_mask": base_dir / "sep_pose_mask",
        "sep_face_mask": base_dir / "sep_face_mask",
        "sep_lip_mask": base_dir / "sep_lip_mask",
        "face_emb": base_dir / "face_emb",
        "audio_emb": base_dir / "audio_emb"
    }

    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    return dirs

def convert_25fps(video_path):

    if not os.path.isfile(video_path):
        print(f"Error: {video_path} File does not exist.")
        return

    dir_name = os.path.dirname(video_path)
    file_name = os.path.basename(video_path)
    temp_path = os.path.join(dir_name, "temp_" + file_name)

    command = [
        "ffmpeg",
        "-i", video_path,          # 입력 파일
        "-filter:v", "fps=fps=25", # FPS를 25로 설정
        "-c:v", "libx264",         # 비디오 코덱 설정
        "-preset", "fast",         # 인코딩 속도
        "-c:a", "aac",             # 오디오 코덱 설정
        "-b:a", "192k",            # 오디오 비트레이트 설정
        "-y",                      # 출력 파일 덮어쓰기
        temp_path                  # 임시 출력 파일
    ]

    print(f"Processing {video_path}...")
    subprocess.run(command, check=True)

    os.remove(video_path)
    os.rename(temp_path, video_path)
    print(f"Converted {video_path} to 25 FPS.")

def process_single_video(video_path: Path,
                         output_dir: Path,
                         image_processor: ImageProcessorForDataProcessing,
                         audio_processor: AudioProcessor,
                         step: int) -> None:
    """
    Process a single video file.

    Args:
        video_path (Path): Path to the video file.
        output_dir (Path): Directory to save the output.
        image_processor (ImageProcessorForDataProcessing): Image processor object.
        audio_processor (AudioProcessor): Audio processor object.
        gpu_status (bool): Whether to use GPU for processing.
    """
    assert video_path.exists(), f"Video path {video_path} does not exist"
    dirs = setup_directories(video_path)
    logging.info(f"Processing video: {video_path}")

    try:
        if step == 1:
            #convert_25fps(video_path)

            images_output_dir = output_dir / 'images' / video_path.stem
            images_output_dir.mkdir(parents=True, exist_ok=True)
            images_output_dir = convert_video_to_images(
                video_path, images_output_dir)
            logging.info(f"Images saved to: {images_output_dir}")

            audio_output_dir = output_dir / 'audios'
            audio_output_dir.mkdir(parents=True, exist_ok=True)
            audio_output_path = audio_output_dir / f'{video_path.stem}.wav'
            audio_output_path = extract_audio_from_videos(
                video_path, audio_output_path)
            logging.info(f"Audio extracted to: {audio_output_path}")

            face_mask, _, sep_pose_mask, sep_face_mask, sep_lip_mask = image_processor.preprocess(
                images_output_dir)
            cv2.imwrite(
                str(dirs["face_mask"] / f"{video_path.stem}.png"), face_mask)
            cv2.imwrite(str(dirs["sep_pose_mask"] /
                        f"{video_path.stem}.png"), sep_pose_mask)
            cv2.imwrite(str(dirs["sep_face_mask"] /
                        f"{video_path.stem}.png"), sep_face_mask)
            cv2.imwrite(str(dirs["sep_lip_mask"] /
                        f"{video_path.stem}.png"), sep_lip_mask)
            #!!!!!
            return True
        else:
            images_dir = output_dir / "images" / video_path.stem
            audio_path = output_dir / "audios" / f"{video_path.stem}.wav"
            _, face_emb, _, _, _ = image_processor.preprocess(images_dir)
            torch.save(face_emb, str(
                dirs["face_emb"] / f"{video_path.stem}.pt"))
            audio_emb, _ = audio_processor.preprocess(audio_path)
            torch.save(audio_emb, str(
                dirs["audio_emb"] / f"{video_path.stem}.pt"))
            #!!!!!
            return True
        
    except Exception as e:
        logging.error(f"Failed to process video {video_path}: {e}")
        #!!!!!
        return False


def process_all_videos(input_video_list: List[Path], output_dir: Path, step: int) -> None:
    """
    Process all videos in the input list.

    Args:
        input_video_list (List[Path]): List of video paths to process.
        output_dir (Path): Directory to save the output.
        gpu_status (bool): Whether to use GPU for processing.
    """
    face_analysis_model_path = "pretrained_models/face_analysis"
    landmark_model_path = "pretrained_models/face_analysis/models/face_landmarker_v2_with_blendshapes.task"
    audio_separator_model_file = "pretrained_models/audio_separator/Kim_Vocal_2.onnx"
    wav2vec_model_path = 'pretrained_models/wav2vec/wav2vec2-base-960h'

    audio_processor = AudioProcessor(
        16000,
        25,
        wav2vec_model_path,
        False,
        os.path.dirname(audio_separator_model_file),
        os.path.basename(audio_separator_model_file),
        os.path.join(output_dir, "vocals"),
    ) if step==2 else None

    image_processor = ImageProcessorForDataProcessing(
        face_analysis_model_path, landmark_model_path, step)

    #!!!!!
    preprocessed_num = 0
    for video_path in tqdm(input_video_list, desc="Processing videos"):
        if preprocessed_num != 2000:
            successed = process_single_video(video_path, output_dir,
                                 image_processor, audio_processor, step)
            if successed:
                preprocessed_num += 1
            else:
                os.remove(video_path)
                logging.info(f"Preprocess Filed. Deleting: {video_path}")
            logging.info(f"Processing video: {preprocessed_num} / 2000")
        else:
            os.remove(video_path)
            logging.info(f"Deleted: {video_path}")



def get_video_paths(source_dir: Path, parallelism: int, rank: int) -> List[Path]:
    """
    Get paths of videos to process, partitioned for parallel processing.

    Args:
        source_dir (Path): Source directory containing videos.
        parallelism (int): Level of parallelism.
        rank (int): Rank for distributed processing.

    Returns:
        List[Path]: List of video paths to process.
    """
    video_paths = [item for item in sorted(
        source_dir.iterdir()) if item.is_file() and item.suffix == '.mp4']
    return [video_paths[i] for i in range(len(video_paths)) if i % parallelism == rank]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process videos to prepare data for training. Run this script twice with different GPU status parameters."
    )
    parser.add_argument("-i", "--input_dir", type=Path,
                        required=True, help="Directory containing videos")
    parser.add_argument("-o", "--output_dir", type=Path,
                        help="Directory to save results, default is parent dir of input dir")
    parser.add_argument("-s", "--step", type=int, default=1,
                        help="Specify data processing step 1 or 2, you should run 1 and 2 sequently")
    parser.add_argument("-p", "--parallelism", default=1,
                        type=int, help="Level of parallelism")
    parser.add_argument("-r", "--rank", default=0, type=int,
                        help="Rank for distributed processing")

    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = args.input_dir.parent

    video_path_list = get_video_paths(
        args.input_dir, args.parallelism, args.rank)

    if not video_path_list:
        logging.warning("No videos to process.")
    else:
        process_all_videos(video_path_list, args.output_dir, args.step)
