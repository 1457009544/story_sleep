import os
import random
import torch
from diffusers import StableDiffusion3Pipeline
from text_processing import chinese_to_pinyin

def text2images(text_list, dir_name):
    """
    将文本列表转换为图像文件并保存在指定目录中。

    参数:
    text_list (list): 包含要转换为图像的文本帧列表，每个文本帧为一个字符串。
    dir_name (str): 保存图像文件的目录名称。

    返回:
    None
    """
    pinyin_dir_name = chinese_to_pinyin(dir_name)
    save_dir = os.path.join("E:\\python\\pycharm_code\\pythonProject\\story_write\\save_dir\\images", pinyin_dir_name)
    os.makedirs(save_dir, exist_ok=True)

    # 初始化Stable Diffusion模型
    pipe = StableDiffusion3Pipeline.from_pretrained(
        pretrained_model_name_or_path="E:\\python\\pycharm_code\\pythonProject\\stable-diffusion-3-medium",
        local_files_only=True,
        torch_dtype=torch.float16,
        use_safetensors=True,
        text_encoder_3=None,
        tokenizer_3=None,
    )

    # 设置随机种子
    seed = random.randint(0, 10000)
    generator = torch.manual_seed(seed)
    pipe.enable_model_cpu_offload()

    for index, text_frame in enumerate(text_list):
        # 生成图像
        image = pipe(
            text_frame[0],
            negative_prompt="nsfw,bad quality, poor quality, doll, disfigured, jpg, toy, bad anatomy, missing limbs, missing fingers, 3d, cgi",
            num_inference_steps=30,
            guidance_scale=7.0,
            generator=generator,
        ).images[0]

        # 保存图像
        image_path = os.path.join(save_dir, f"{index}.png")
        image.save(image_path)
