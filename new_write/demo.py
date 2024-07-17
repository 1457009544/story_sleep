from story_generator import generate_story_and_frames
from text_processing import parse_segments_to_list
from file_operations import save_subtitles, feature_choice, style_choice
from image_generation import text2images
from audio_generation import text2audio
import json
from story_generator import llm_initialization




# 示例用法，输入剧情相关的
prompt = "小马和小鹿"
word_count = 200  # 用户输入的字数，可以调整

# 初始化大模型
llm = llm_initialization()

# 生成故事和分镜
story, frames = generate_story_and_frames(prompt, word_count, llm)

print("生成的故事:")
print(story)

# 转换为列表输出并翻译
segments_list = parse_segments_to_list(story, llm)

# 输出分镜列表
print("\nModified segments_list:")
for segment in segments_list:
    print(segment)

# 保存文本
save_subtitles(segments_list, prompt)

# 生成图片
text2images(segments_list, prompt)

# 生成音频
text2audio(segments_list, prompt)
