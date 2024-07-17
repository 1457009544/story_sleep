import os
import json
from text_processing import chinese_to_pinyin

test_path = "E:\\python\\pycharm_code\\pythonProject\\story_write\\save_dir\\texts"

def save_subtitles(segments_list, prompt):
    """
    保存字幕文本到指定目录
    参数:
    segments_list (list): 包含字幕段落的列表，每个段落为一个二元组 (index, text)。
    prompt (str): 用于命名目录的提示文本。
    返回:
    None
    """
    pinyin_dir_name = chinese_to_pinyin(prompt)
    subtitles_folder = os.path.join(test_path, pinyin_dir_name)
    os.makedirs(subtitles_folder, exist_ok=True)

    for idx, segment in enumerate(segments_list):
        subtitle_text = segment[1]
        subtitle_filename = os.path.join(subtitles_folder, f"{idx}.txt")
        with open(subtitle_filename, 'w', encoding='utf-8') as f:
            f.write(subtitle_text)
        print(f"Saved subtitle {idx} to {subtitle_filename}")

def select_person():
    """
    选择故事对应的主角。待修改。
    :return: 返回故事的主角，组成字符船，如：白雪公主、七个小矮人
    """
    persons = ['功夫熊猫', '小兔子']

    person_out = persons[0] + '、' + persons[1]

    return person_out

def feature_choice():
    """
    选择特征描述并保存到 JSON 文件
    返回:
    None
    """
    rabbit = ('The white rabbit is white and white, with two ears erect, '
              'a tail like a fluffy ball, and two red eyes, like two rubies.')
    wolf = ('The gray wolf ears are erect perpendicular to each other, and the mouth is relatively wide, '
            'with large lobed teeth, very sharp teeth, and eyes that are slanted upward')

    descriptions = {
        "rabbit": rabbit,
        "wolf": wolf
    }

    with open('./style_description/descriptions.json', 'w', encoding='utf-8') as json_file:
        json.dump(descriptions, json_file, ensure_ascii=False, indent=4)

def style_choice():
    """
    选择风格描述并保存到 JSON 文件
    返回:
    None
    """
    cartoon = 'Cartoon graphics'
    descriptions = {"cartoon": cartoon}

    with open('./style_description/style.json', 'w', encoding='utf-8') as json_file:
        json.dump(descriptions, json_file, ensure_ascii=False, indent=4)
