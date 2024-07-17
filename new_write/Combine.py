import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, TextClip
import time
from concurrent.futures import ThreadPoolExecutor

def numeric_sort_key(value):
    """从文件名中提取数字进行排序"""
    return int(os.path.splitext(value)[0])

def process_clip(image_path, audio_path, text_path, font_path):
    """
    处理单个视频剪辑，合成图像、音频和字幕

    参数:
    image_path (str): 图片文件路径。
    audio_path (str): 音频文件路径。
    text_path (str): 字幕文本文件路径。
    font_path (str): 字体文件路径。

    返回:
    final_clip (CompositeVideoClip): 包含图像、音频和字幕的最终视频剪辑。
    """
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path, duration=audio_clip.duration)

    with open(text_path, 'r', encoding='utf-8') as file:
        subtitle_text = file.read()

    subtitle_clip = (
        TextClip(subtitle_text, fontsize=36, color='white', font=font_path, stroke_color='black', stroke_width=1, size=(950, None))
        .set_duration(audio_clip.duration)
        .set_position(('center', lambda t: image_clip.size[1] - 50))
    )

    final_clip = CompositeVideoClip([image_clip, subtitle_clip]).set_audio(audio_clip)
    final_clip.fps = 24
    return final_clip

def get_sorted_files(folder, extensions):
    """
    获取排序后的指定类型文件列表

    参数:
    folder (str): 文件夹路径。
    extensions (tuple): 文件扩展名元组。

    返回:
    list: 排序后的文件名列表。
    """
    return sorted([f for f in os.listdir(folder) if f.endswith(extensions)], key=numeric_sort_key)

def merge_images_audio_with_subtitles(image_folder, audio_folder, text_folder, output_path, font_path='style_description/msyh.ttc'):
    """
    合成图片、音频和字幕，生成最终视频

    参数:
    image_folder (str): 图片文件夹路径。
    audio_folder (str): 音频文件夹路径。
    text_folder (str): 字幕文本文件夹路径。
    output_path (str): 输出视频文件路径。
    font_path (str): 字体文件路径。

    返回:
    None
    """
    image_files = get_sorted_files(image_folder, ('.png', '.jpg', '.jpeg'))
    audio_files = get_sorted_files(audio_folder, ('.wav',))
    text_files = get_sorted_files(text_folder, ('.txt',))

    with ThreadPoolExecutor() as executor:
        video_clips = list(executor.map(
            process_clip,
            [os.path.join(image_folder, f) for f in image_files],
            [os.path.join(audio_folder, f) for f in audio_files],
            [os.path.join(text_folder, f) for f in text_files],
            [font_path] * len(image_files)
        ))

    if video_clips:
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
    else:
        print("No video clips to concatenate.")

def main():
    """
    主函数，定义视频和音频文件夹路径，以及输出文件夹路径，调用合成视频函数

    返回:
    None
    """
    story_name = "xiaobaituy"

    # 定义视频和音频文件夹路径，以及输出文件夹路径
    base_dir = os.path.abspath('./save_dir')
    image_folder = os.path.join(base_dir, 'images', story_name)
    audio_folder = os.path.join(base_dir, 'audios', story_name)
    text_folder = os.path.join(base_dir, 'texts', story_name)
    output_folder = os.path.join(base_dir, 'Combine')

    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    output_path = os.path.join(output_folder, f"final_video_{timestamp}.mp4")

    # 合成视频
    merge_images_audio_with_subtitles(image_folder, audio_folder, text_folder, output_path, font_path='style_description/msyh.ttc')

if __name__ == "__main__":
    main()
