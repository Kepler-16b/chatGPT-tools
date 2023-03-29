'''
文本优化函数库
包含三个功能：
    extract_content()：用于预处理html文件，剥除无用的html标签
    convert_to_markdown()：用于将文本内必要的html标签替换为markdown语法标识符号
    add_titles()：用于根据消息列表顺序，为聊天双方添加称谓
'''

from bs4 import BeautifulSoup


'''----------------html转markdown函数----------------'''
def convert_to_markdown(html_list):
    markdown_list = []
    for html in html_list:
        soup = BeautifulSoup(html, "html.parser")

        # 加粗
        for strong in soup.find_all("strong"):
            strong.string = f"**{strong.text}**"
        # 斜体
        for em in soup.find_all("em"):
            em.string = f"*{em.text}*"
        # 有序列表
        for ol in soup.find_all("ol"):
            for idx, li in enumerate(ol.find_all("li"), start=1):
                li.string = f"{idx}. {li.text}\n"
        # 无序列表
        for ul in soup.find_all("ul"):
            for li in ul.find_all("li"):
                li.string = f"- {li.text}\n"
        # 段落
        for p in soup.find_all("p"):
            p.string = f"{p.text}\n\n"
        # 换行
        for br in soup.find_all("br"):
            br.replace_with("\n")

        # 移除所有剩余的HTML标签
        markdown_text = soup.get_text()
        markdown_list.append(markdown_text)
    
    return markdown_list


'''----------------剥除无用的html标签 | 使用BeautifulSoup4----------------'''
def extract_content(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = BeautifulSoup(content, 'lxml')

    # 获取对话的主题（自动生成）
    try:
        chat_topic = html_content.title.string.strip()
    except AttributeError:
        chat_topic = 'Unknown'

    # 获取对话中使用的模型
    try:
        model_div = html_content.find('div', {'class': 'flex w-full items-center justify-center gap-1 border-b border-black/10 bg-gray-50 p-3 text-gray-500 dark:border-gray-900/50 dark:bg-gray-700 dark:text-gray-300'})
        model_name = model_div.get_text().strip()
    except AttributeError:
        model_name = 'Unspecified'

    
    # 获取问题和回复
    question_queue = html_content.find_all('div', {'class': 'group w-full text-gray-800 dark:text-gray-100 border-b border-black/10 dark:border-gray-900/50 dark:bg-gray-800'})
    answer_queue = html_content.find_all('div', {'class': 'group w-full text-gray-800 dark:text-gray-100 border-b border-black/10 dark:border-gray-900/50 bg-gray-50 dark:bg-[#444654]'})

    '''
    # 将问题和回复按照位置排序，并将其包装为字符串列表
    question_positions = [(q.get_text().strip(), i) for i, q in enumerate(question_queue)]
    answer_positions = [(a.get_text().strip(), i) for i, a in enumerate(answer_queue)]
    messages = [t[0] for t in sorted(question_positions + answer_positions, key=lambda x: x[1])]
    '''

    question_positions = [(str(q), i) for i, q in enumerate(question_queue)]
    answer_positions = [(str(a), i) for i, a in enumerate(answer_queue)]
    messages = [t[0] for t in sorted(question_positions + answer_positions, key=lambda x: x[1])]

    # 将chat_topic、model_name、question_queue和answer_queue打包为字典并返回
    extraced_content = {
        'chat_topic': chat_topic,
        'model_name': model_name,
        'messages': messages
    }

    return extraced_content


'''----------------添加聊天人称谓----------------'''
def add_titles(given_chat_list):
    for i in range(len(given_chat_list)):
        # 按照段落顺序添加称谓，因为聊天总是由人类发起，因此偶数位的字符串为“我”所说的内容
        prefix = ' --- \n\n## 我: ' if i % 2 == 0 else '## GPT: '
        given_chat_list[i] = '  \n\n' + prefix + '  \n\n' + given_chat_list[i]

    return given_chat_list