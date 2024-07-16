import json
import os
from langchain_community.llms import Tongyi
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# from character_initialization import feature_choice, style_choice


def llm_initialization():
    """
    初始化大语言模型。

    :return: llm
    """
    # Qwen model

    # llm = Tongyi(
    #     api_key=os.getenv("DASHSCOPE_API_KEY"),
    #     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # )

    # zhipu model

    llm = ChatOpenAI(
        temperature=0.6,
        model="glm-4-0520",
        openai_api_key="a333cb3d1944d5724bb20a4d180d780f.KBZQf8ttUYoyWJZl",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
        max_tokens=4096
    )

    return llm


def select_person():
    """
    选择故事对应的主角。待修改。

    :return: 返回故事的主角，组成字符船，如：白雪公主、七个小矮人
    """
    persons = ['功夫熊猫', '小兔子']

    person_out = persons[0] + '、' + persons[1]

    return person_out


def generate_story(prompt, word_count, llm):
    """
    生成一个儿童睡前故事视频脚本。

    :param prompt: 故事的主题
    :param word_count: 期望的故事字数（不包括额外添加的提示字数）
    :param llm：大语言模型
    :return: 生成的故事脚本，如果生成失败则返回空字符串
    """
    # 验证参数
    if not prompt or not isinstance(word_count, int) or word_count <= 0:
        return "输入参数无效"

    # 增加字数要求以适应可能的提示词长度
    number_of_shots = word_count // 10

    # 选择故事的主角
    person = select_person()

    # 智谱API使用
    while True:
        prompt_te = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "你现在是一名儿童睡前故事创作专家和以为视频脚本创作专家。请帮我生成一个儿童睡前故事视频脚本。场景需要{number_of_shots}个,包含画面和旁白。\n"
                    "故事内容积极向上，充满乐趣，有教育意义。\n"
                    "请确保生成的分镜数量不少于20段，每个分镜都是独立的，之间没有连续性。\n"
                    "同时你也是一名分镜画面专家。按照生成的故事设计对应的分镜，请为每个分镜生成具体的画面和旁白，画面中包含天气，地点和大概时间等元素，画面格式："
                    "人物，地点，动作，时间，天气。\n"
                    "请根据的每个分镜内容，生成每个画面的提示词，以便用于AI绘画，同时优化提示词。\n"
                    "只保留对应的画面和旁白即可。\n"
                    "请注意，每个分镜都是独立的，不要有连续性。请确保每个分镜生成一一对应的画面提示和旁白，并且每个画面提示和旁白具体且详细。\n"
                    "场景提示请保证每个分镜所需的关键元素都包含在内，如：天气，地点和大概时间等元素。旁白是解释当前的情节发展，提供情感和细节描述。\n"
                    "所有分镜中画面中的人物请使用主角名称，不能使用任何代称，如：他、她、他们、它们、它等代称。\n"
                    "请按以下格式生成脚本：\n"
                    "分镜1:\n"
                    "画面: [详细描述分镜1的场景和元素，确保包含所有关键元素，例如：小白兔，森林边缘的一片花丛中，手拿着一张古老的地图，晚上，小雨。]\n"
                    "旁白: [分镜1的旁白，例如：小白兔发现了一张古老的地图，地图上标注着一个神秘的宝藏]\n"
                    "分镜2:\n"
                    "画面: [详细描述分镜2的场景和元素，确保包含所有关键元素，例如：小白兔，森林深处的一条小路上，手握地图四处张望，早上，晴天。]\n"
                    "旁白: [分镜2的旁白，例如：小白兔心中充满了期待，它一步一步地按照地图上的指示前进]\n"
                    "...\n"
                    "分镜{number_of_shots}:画面:[详细描述分镜{number_of_shots}的场景和元素，确保包含所有关键元素，"
                    "例如：小白兔，洞穴前，拿着地图看着洞穴，中午，阴天。]\n"
                    "旁白:[分镜{number_of_shots}的旁白，例如：小白兔鼓起勇气，决定进入洞穴寻找宝藏]\n"
                    "请确保每个分镜的画面提示和旁白都是具体的，不要省略。请确保所有画面中的人物请使用主角名称，不能使用任何代称。\n"
                    "请确保画面格式：人物，地点，动作，时间，天气。",
                ),
                ("human", "主题是：{human_input_topic}，主角是：{human_input_person}"),
            ]
        )

        chain = prompt_te | llm

        try:
            result = chain.invoke(
                {
                    "number_of_shots": number_of_shots,
                    "human_input_topic": prompt,
                    "human_input_person": person
                }
            )

            story_content = result.content.strip()

            story_content = clean_story(story_content)

            segments = story_content.split('\n\n')

            if len(segments) >= 20:
                # 如果分镜数符合要求，结束循环
                return story_content
            else:
                print(f"生成的分镜数不符合要求: {len(segments)}，重新生成...")
                continue  # 重新生成故事

        except Exception as e:
            print(f"生成故事时出错: {e}")
            return ""

    # while True:
    #     # 动态生成提示词，包含字数控制的指示
    #     full_prompt = (f"你现在是一名儿童睡前故事创作专家。请帮我生成一个主题为{prompt}的儿童睡前故事视频脚本。\n"
    #                    f"故事内容积极向上，充满乐趣，有教育意义。\n"
    #                    f"请确保生成的分镜数量不少于20段，每个分镜都是独立的，之间没有连续性。\n"
    #                    f"同时你也是一名分镜画面专家。按照生成的故事设计对应的分镜，请为每个分镜生成具体的画面提示和旁白。\n"
    #                    f"请根据的每个分镜内容，生成每个画面的提示词，以便用于AI绘画，同时优化提示词。\n"
    #                    f"只保留对应的画面和旁白即可。\n"
    #                    f"请注意，每个分镜都是独立的，不要有连续性。请确保每个分镜生成一一对应的画面提示和旁白，并且每个画面提示和旁白具体且详细。\n"
    #                    f"场景提示请保证每个分镜所需的关键元素都包含在内。旁白是解释当前的情节发展，提供情感和细节描述。\n"
    #                    f"所有分镜中画面提示中的人物请保持一致。不能使用任何代称。\n"
    #                    f"请按以下格式生成脚本：\n"
    #                    f"分镜1:\n"
    #                    f"画面提示: [详细描述分镜1的场景和元素，确保包含所有关键元素，例如：小白兔在森林边缘的一片花丛中，手里拿着一张古老的地图]\n"
    #                    f"旁白: [分镜1的旁白，例如：小白兔发现了一张古老的地图，地图上标注着一个神秘的宝藏]\n"
    #                    f"分镜2:\n"
    #                    f"画面提示: [详细描述分镜2的场景和元素，确保包含所有关键元素，例如：小白兔在森林深处的一条小路上，四处张望寻找线索，手中紧握着那张地图]\n"
    #                    f"旁白: [分镜2的旁白，例如：小白兔心中充满了期待，它一步一步地按照地图上的指示前进]\n"
    #                    f"...\n"
    #                    f"分镜20:\n"
    #                    f"画面提示:[详细描述分镜20的场景和元素，确保包含所有关键元素，例如：小白兔在一个神秘的洞穴前，洞口隐约闪着光芒，小白兔依然拿着地图]\n"
    #                    f"旁白:[分镜20的旁白，例如：小白兔鼓起勇气，决定进入洞穴寻找宝藏]\n"
    #                    f"请确保每个分镜的画面提示和旁白都是具体的，不要省略。"
    #                    )
    #
    #     try:
    #         response = llm.generate(prompts=[full_prompt], max_tokens=total_word_count * 4)
    #         print(f"完整响应: {response}")
    #
    #         if not response or not response.generations or not response.generations[0]:
    #             raise ValueError("响应格式不正确或为空")
    #
    #         # 提取生成的文本
    #         story_content = response.generations[0][0].text.strip()
    #
    #         # 清理故事文本
    #         story_content = clean_story(story_content)
    #         segments = story_content.split('\n\n')
    #
    #         if len(segments) >= 20:
    #             # 如果分镜数符合要求，结束循环
    #             return story_content
    #         else:
    #             print(f"生成的分镜数不符合要求: {len(segments)}，重新生成...")
    #             continue  # 重新生成故事
    #
    #     except Exception as e:
    #         print(f"生成故事时出错: {e}")
    #         return ""

    return story_content


def clean_story(story_clean):
    """
    清理故事文本，移除不必要的引号等字符。

    :param story_clean: 原始的故事文本
    :return: 清理后的故事文本
    """

    # 千问用这个
    # return story_clean.replace('”', '').replace("'", '').replace("“", '')

    # 智谱用这个
    return story_clean.replace('”', '').replace("'", '').replace("“", '').replace('[', '').replace(']', '')


def generate_story_and_frames(prompt_user, word_count_limit, llm):
    """
    根据用户提供的主题和字数，生成对应的故事和分镜。

    :param word_count_limit: 用户输入的字数
    :param prompt_user: 用户输入的主题
    :param llm：大语言模型
    :return: 整体故事和分镜
    """

    # 初始化llm

    glm4 = llm

    # 确保用户输入字数在200到300之间
    word_count_max = max(200, min(word_count_limit, 300))

    while True:
        try:
            # 生成故事
            story_output = generate_story(prompt_user, word_count_max, glm4)

            print(story_output)

            # 将故事分成若干分镜
            segments = story_output.split('\n\n')

            pre_frames = []

            for segment in segments:
                lines = segment.strip().split('\n')  # 使用strip()去除可能的前后空白
                if len(lines) >= 3 and lines[0].startswith('分镜'):  # 确保是有效的分镜
                    hint = lines[1].split(': ', 1)[1].strip()
                    narration = lines[2].split(': ', 1)[1].strip()
                    pre_frames.append([hint, narration])

            # 如果没有发生异常，返回结果
            return story_output, pre_frames

        except (IndexError, ValueError) as e:
            # 处理可能的错误并重试
            print(f"Error processing segment: {e}")
            continue


def enrich_sentence(sentence, f_descriptions):
    """
    检查句子中是否包含描述的键，并生成新的句子

    参数：
    sentence (str)：翻译后的句子。
    descriptions （json）：json文件格式，特征。

    返回：
    str：加入新描述后的句子。
    """
    for key, description in f_descriptions.items():
        # 将key和sentence转换为全小写
        lower_key = key.lower()
        lower_sentence = sentence.lower()

        # 检查key是否在sentence中，并且之前没有添加过description
        if lower_key in lower_sentence and description not in sentence:
            sentence = f"{description} {sentence}"
    return sentence


def parse_segments_to_list(segments_str, llm):
    """
    解析分镜内容，并将其存储为列表格式，每个分镜内容以 [画面提示, 旁白] 的形式存储。

    参数:
    segments_str (str): 多个分镜内容的字符串，格式如示例所示。
    llm：大语言模型
    返回:
    list: 分镜内容列表，每个元素是一个 [画面提示, 旁白] 的列表。
    """
    # 读取人物特征
    with open('descriptions.json', 'r', encoding='utf-8') as json_file:
        descriptions = json.load(json_file)

    with open('style.json', 'r', encoding='utf-8') as json_file:
        style = json.load(json_file)

    # 初始化分镜列表
    segments_list_out = []

    # 分割每个分镜
    segments = segments_str.split('\n\n')

    # 处理每个分镜
    for pre_segment in segments:
        lines = pre_segment.strip().split('\n')
        if len(lines) >= 3:
            try:
                hint = lines[1].split(': ', 1)[1].strip()
                narration = lines[2].split(': ', 1)[1].strip()
                translated_document = translate_chinese_to_english(hint, llm)
                enrich_f_document = enrich_sentence(translated_document, descriptions)

                # 风格还需要修改
                enrich_s_document = "Cartoon graphics." + enrich_f_document

                segments_list_out.append([enrich_s_document, narration])
            except IndexError:
                print(f"解析段落时出错: {pre_segment}")
                continue

    return segments_list_out


def translate_chinese_to_english(chinese_text, llm, max_retries=10, length_threshold=200):
    # 千问
    # full_prompt = f"Translate the above Chinese text into English.{chinese_text}"
    # try:
    #     # 调用OpenAI的GPT-3.5模型进行翻译
    #     response = llm.generate(prompts=[full_prompt])
    #
    #     # 解析翻译后的英文文本
    #     translated_text = response.generations[0][0].text.strip()
    # 
    #     return translated_text
    #
    # except Exception as e:
    #     print(f"Error: {e}")
    #     return None

    # 智谱
    glm4 = llm
    prompt_tr = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "我想让您担任英语翻译、拼写纠正和改进员。我将用中文与您交谈，您将检测语言、翻译语言，并用经过更正和改进的英语版本回答我的问题。"
                "我想让你用更优美、更优雅、更高级别的英语单词和句子替换我简化的 A0 级单词和句子。意思不变，但要更有文采。"
                "我希望您只回复翻译后的文字，不要写解释或其他的内容。",
            ),
            ("human", "{input}"),
        ]
    )

    retries = 0

    while retries < max_retries:
        try:
            # 调用OpenAI的模型进行翻译
            chain = prompt_tr | glm4

            result = chain.invoke(
                {
                    "input": chinese_text,
                }
            )

            # 解析翻译后的英文文本
            translated_text = result.content.strip()
            print(translated_text)

            # 检查翻译结果是否为空、与原文相同或包含多余的内容（句子长度过长）
            if translated_text and translated_text != chinese_text and len(translated_text) <= length_threshold:
                return translated_text
            else:
                print(f"Invalid translation: {translated_text}")

        except Exception as e:
            print(f"Error: {e}")

        retries += 1
        print(f"Retrying... ({retries}/{max_retries})")

    return None


# feature_choice()
# style_choice()

# 示例用法，输入剧情相关的
prompt = "冒险故事"
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
