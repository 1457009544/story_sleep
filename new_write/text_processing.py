import re
from pypinyin import pinyin, Style
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(
    temperature=0.95,
    model="glm-4",
    openai_api_key="a333cb3d1944d5724bb20a4d180d780f.KBZQf8ttUYoyWJZl",
    openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
)

def translate_chinese_to_english(chinese_text, llm, max_retries=10, length_threshold=200):
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
            chain = prompt_tr | glm4

            result = chain.invoke(
                {
                    "input": chinese_text,
                }
            )

            translated_text = result.content.strip()
            print(translated_text)

            if translated_text and translated_text != chinese_text and len(translated_text) <= length_threshold:
                return translated_text
            else:
                print(f"Invalid translation: {translated_text}")

        except Exception as e:
            print(f"Error: {e}")

        retries += 1
        print(f"Retrying... ({retries}/{max_retries})")

    return None

def chinese_to_pinyin(chinese):
    """
    将中文转换为拼音，并以连字符连接
    参数:
    chinese (str): 中文文本。
    返回:
    str: 转换后的拼音字符串。
    """
    pinyin_list = pinyin(chinese, style=Style.NORMAL, strict=False)
    pinyin_str = ''.join([item[0] for item in pinyin_list])
    pinyin_str = re.sub(r'\W+', '-', pinyin_str).strip('-')
    return pinyin_str[:10]

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
        lower_key = key.lower()
        lower_sentence = sentence.lower()

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
    with open('./style_description/descriptions.json', 'r', encoding='utf-8') as json_file:
        descriptions = json.load(json_file)

    with open('./style_description/style.json', 'r', encoding='utf-8') as json_file:
        style = json.load(json_file)

    segments_list_out = []
    segments = segments_str.split('\n\n')

    for pre_segment in segments:
        lines = pre_segment.strip().split('\n')
        if len(lines) >= 3:
            try:
                hint = lines[1].split(': ', 1)[1].strip()
                narration = lines[2].split(': ', 1)[1].strip()
                translated_document = translate_chinese_to_english(hint, llm)
                enrich_f_document = enrich_sentence(translated_document, descriptions)

                enrich_s_document = "Cartoon graphics." + enrich_f_document

                segments_list_out.append([enrich_s_document, narration])
            except IndexError:
                print(f"解析段落时出错: {pre_segment}")
                continue

    return segments_list_out
