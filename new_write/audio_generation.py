import os
import subprocess
from text_processing import chinese_to_pinyin

def text2audio(text_list, dir_name):
    """
    将文本列表转换为音频文件并保存在指定目录中。

    参数:
    text_list (list): 包含要转换为音频的文本帧列表，每个文本帧为一个字符串。
    dir_name (str): 保存音频文件的目录名称。

    功能:
    1. 将目录名称转换为拼音。
    2. 在指定路径创建保存音频文件的目录。
    3. 设置所需的模型路径、参考音频和其他参数。
    4. 进入指定的工作目录。
    5. 遍历文本列表，将每个文本帧转换为音频文件并保存在指定目录中。

    使用示例:
    text_list = ["你好", "世界"]
    dir_name = "音频目录"
    text2audio(text_list, dir_name)
    """
    pinyin_dir_name = chinese_to_pinyin(dir_name)
    save_dir = os.path.join("E:\\python\\pycharm_code\\pythonProject\\story_write\\save_dir\\audios", pinyin_dir_name)
    os.makedirs(save_dir, exist_ok=True)

    gpt_model = "D:/voice_clone/GPT-SoVITS-beta0306fix2/GPT_weights/DingZhen-e10.ckpt"
    sovits_model = "D:/voice_clone/GPT-SoVITS-beta0306fix2/SoVITS_weights/DingZhen_e8_s288.pth"
    ref_audio = "D:/voice_clone/Audio/dingzhen/raw/dingzhen_8.wav"
    prompt_language = "中文"
    text_language = "中文"
    how_to_cut = "不切"

    os.chdir("D:/voice_clone/GPT-SoVITS-beta0306fix2")

    for index, text_frame in enumerate(text_list):
        output = os.path.join(save_dir, f"{index}.wav")
        text = text_frame[-1]
        command = [
            "runtime\\python", "GPT_SoVITS\\your_script.py",
            "--gpt_model", gpt_model,
            "--sovits_model", sovits_model,
            "--ref_audio", ref_audio,
            "--prompt_language", prompt_language,
            "--text", text,
            "--text_language", text_language,
            "--how_to_cut", how_to_cut,
            "--output", output
        ]
        subprocess.run(command)
