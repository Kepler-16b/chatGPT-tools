'''
本脚本由chatGPT和它没用的人类助手合作编写
This script was made possible with huge help from chatGPT(Model: GPT3.5).
He's the master, I'm the side kick :)
--------------------------------
实现功能：自动将下载的chatGPT聊天记录（.html）转换为合适的markdown文本，
并提供聊天双方的称谓;
计划实现：聊天中代码自动识别并添加对应的md语法符号
--------------------------------
TODOs:
    1. 需要增加一个功能：当用户提问的文本过长时（>300字 | 中文计算字数，英文计算空格数量），仅显示前两个句子，并将剩余文本放入一个折叠列表中;
    2. 完善代码块检测及转换功能，当前不可用；
    （done）markdown格式转换功能还有缺陷：有序、无序列表不见了；分段不够准确
    （done）代码块检测函数放在detectSnippet.py中；
    （done）文本优化函数放到textOptimize.py中；
    字数限制函数放到foldLongText.py中。
'''


import os
import sys
import re
import glob
import textOptimize as textOp
# import foldLongText as foldText
# import detectSnippet as codeDetect

import warnings
from bs4 import MarkupResemblesLocatorWarning
warnings.filterwarnings('ignore', category=MarkupResemblesLocatorWarning)


'''----------------文件路径处理与html解析缓冲----------------'''
# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# 定义markdown保存路径，若不存在，则创建
html_dir = os.path.join(script_dir, "source")
if not os.path.exists(html_dir):
    os.mkdir(html_dir)

save_dir = os.path.join(script_dir, "output")
if not os.path.exists(save_dir):
    os.mkdir(save_dir)


'''----------------定义非代码块中可能出现的词汇----------------'''
possible_language = ['bash', 'python', 'js', 'javascript', 'java', 'golang', 'c', 'cpp', 'c#', 'html', 'css', 'html', 'css', 'ruby', 'go', 'php', 'swift']

# 未消除的gpt代码块标识——“语言+Copy code”
gpt_code_format = [lang + 'Copy code' for lang in possible_language]


'''----------------主函数 | 执行批量操作----------------'''
def main():
    # 定位至html源文件路径，获取所有html文件
    os.chdir(html_dir)
    html_files = glob.glob('*.html')

    # 循环遍历所有html文件，执行批量处理
    for html_file in html_files:

        # 获取原始html文件名，去掉多余的标点符号和空格，并将空格转换为下划线
        md_filename = os.path.splitext(html_file)[0]
        md_filename = re.sub(r'[^\w\s-]', '', md_filename).strip().replace(' ', '_')
        md_filename += '_extract.md'

        # 以该文件名，创建对应的markdown文档
        extracted_markdown_file = os.path.join(save_dir, md_filename)

        # 提取本文件的主题和模型名称
        extracted_contents = textOp.extract_content(html_file)
        extracted_topic = extracted_contents['chat_topic']
        extracted_model_name = extracted_contents['model_name']
        
        # 获取该html文件中的问答文本
        extracted_chat_history = extracted_contents['messages']

        # 去除chatGPT提供的脚本复制及代码语言标识
        for i in range(1, len(extracted_chat_history), 2):
            for s in gpt_code_format:
                if s in extracted_chat_history[i]:
                    extracted_chat_history[i] = re.sub(s, '', extracted_chat_history[i])

        # markdown转换
        extracted_chat_history = textOp.convert_to_markdown(extracted_chat_history)

        # 添加称谓
        extracted_chat_history = textOp.add_titles(extracted_chat_history)

        '''
        # 为用户提问执行代码检测
        for j in range(0, len(extracted_chat_history), 2):
            extracted_chat_history[j] = codeDetect.add_code_annotations(extracted_chat_history[j])

        # 为chatGPT的回答执行代码检测
        for k in range(1, len(extracted_chat_history), 2):
            for s in gpt_code_format:
                answer_code_lang = ''
                if s in extracted_chat_history[k]:
                    answer_code_lang = s.replace('Copy code', '')
                    s = re.sub('gpt_code_format', '', s)
                else:
                    answer_code_lang = 'INVALID'
            # 将chatGPT的回答中自带的代码标识作为代码块语言标记传入
            extracted_chat_history[k] = codeDetect.add_code_annotations(extracted_chat_history[k], answer_code_lang)
        '''

        # 保存处理的文本至对应md文件
        with open(extracted_markdown_file, 'w', encoding='utf-8') as md_file:
            md_header = '> Chat about ' + '" **' + extracted_topic + '** ", ' + ' using ' + '_' + extracted_model_name + '_'
            md_header += '  \n\n'
            md_file.write(md_header)

            for dialogue in extracted_chat_history:
                md_file.write(dialogue)

if __name__ == '__main__':
    main()