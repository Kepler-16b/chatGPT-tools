import re
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import NullFormatter
from pygments.util import ClassNotFound

exclusion_keywords = ['代码', '编程', '脚本', '程序', '编写', '错误', '终端', '要求', '实现', '效果', '目的', '如何修复', '如何改正', '？', 'example code', 'code example', 'program', 'snippet']
included_keywords = ['if', 'else', 'while', 'for', 'def', 'class', 'import', '# 我:', '# GPT:']
possible_language = ['bash', 'python', 'js', 'javascript', 'java', 'golang', 'c', 'cpp', 'c#', 'html', 'css', 'html', 'css', 'ruby', 'go', 'php', 'swift']
invalid_language = ['CBM BASIC V2', 'Text only', 'scdoc', 'verilog']

'''----------------代码语言检测函数，用于检测用户给出的代码片段 | 使用pygments----------------'''
def language_auto_detect(snippet_in_question):

    try:
        lexer = guess_lexer(snippet_in_question)
        language_deteced = lexer.name
    except ClassNotFound:
        language_deteced = ''
    
    return language_deteced


'''----------------从文本中找出可能为代码的行，并添加注释符号----------------'''
def is_code_line(line, languages=None):
    # 检查缩进（至少有一个制表符或四个空格）
    if re.match(r'^(\t| {4})', line):
        return True

    # 如果包含排除列表中的单词，则不是代码行
    if any(keyword in line for keyword in exclusion_keywords):
        return False

    # 使用正则表达式匹配常见的编程关键字
    keywords = included_keywords
    if any(re.search(r'\b' + keyword + r'\b', line) for keyword in keywords):
        return True

    # 使用Pygments库检测代码行
    if languages is None:
        languages = possible_language

    for lang in languages:
        try:
            lexer = get_lexer_by_name(lang)
            highlighted = highlight(line, lexer, NullFormatter())
            if highlighted.strip():
                return True
        except:
            pass

    return False


def add_code_annotations(text, code_language='NONE'):
    lines = text.split('\n\n')
    in_code_block = False
    annotated_lines = []

    for i, line in enumerate(lines):
        # 检查当前行是否在两个代码块之间
        between_code_blocks = False
        if i > 0 and i < len(lines) - 1:
            between_code_blocks = is_code_line(lines[i - 1]) and is_code_line(lines[i + 1])

        if is_code_line(line) or (in_code_block and line.strip() == '') or between_code_blocks:
            if not in_code_block:
                in_code_block = True
                # 如果未传入code_language参数，则进行自动判断
                if code_language == 'NONE':
                    code_language = language_auto_detect(line)
                    if code_language not in invalid_lang:
                        annotated_lines.append(f'```{code_language}')
            annotated_lines.append(line)
        else:
            if in_code_block:
                if code_language not in invalid_lang:
                    annotated_lines.append('```')
                in_code_block = False
            annotated_lines.append(line)
            
    if in_code_block and code_language not in invalid_lang:
        annotated_lines.append('```')

    return '\n'.join(annotated_lines)