import os
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from file_operations import select_person

def llm_initialization():
    """
    初始化大语言模型。
    :return: llm
    """
    llm = ChatOpenAI(
        temperature=0.6,
        model="glm-4-0520",
        openai_api_key="",
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/",
        max_tokens=4096
    )
    return llm

def generate_story(prompt, word_count, llm):
    """
    生成一个儿童睡前故事视频脚本。
    :param prompt: 故事的主题
    :param word_count: 期望的故事字数（不包括额外添加的提示字数）
    :param llm：大语言模型
    :return: 生成的故事脚本，如果生成失败则返回空字符串
    """
    if not prompt or not isinstance(word_count, int) or word_count <= 0:
        return "输入参数无效"

    number_of_shots = word_count // 10
    person = select_person()

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
                return story_content
            else:
                print(f"生成的分镜数不符合要求: {len(segments)}，重新生成...")
                continue

        except Exception as e:
            print(f"生成故事时出错: {e}")
            return ""

    return story_content

def clean_story(story_clean):
    """
    清理故事文本，移除不必要的引号等字符。
    :param story_clean: 原始的故事文本
    :return: 清理后的故事文本
    """
    return story_clean.replace('”', '').replace("'", '').replace("“", '').replace('[', '').replace(']', '')

def generate_story_and_frames(prompt_user, word_count_limit, llm):
    """
    根据用户提供的主题和字数，生成对应的故事和分镜。
    :param word_count_limit: 用户输入的字数
    :param prompt_user: 用户输入的主题
    :param llm：大语言模型
    :return: 整体故事和分镜
    """
    glm4 = llm
    word_count_max = max(200, min(word_count_limit, 300))

    story_output = generate_story(prompt_user, word_count_max, glm4)
    segments = story_output.split('\n\n')
    pre_frames = []

    for segment_frames in segments:
        lines = segment_frames.strip().split('\n')
        if len(lines) >= 3 and lines[0].startswith('分镜'):
            hint = lines[1].split(': ', 1)[1].strip()
            narration = lines[2].split(': ', 1)[1].strip()
            pre_frames.append([hint, narration])

    return story_output, pre_frames
