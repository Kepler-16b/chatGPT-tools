# chatGPT-tools
Simple tools that enhance chatGPT experience, made by chatGPT.

-----------------------------------------------------------------------------------
|                                    脚本简介                                      |
-----------------------------------------------------------------------------------

convert2Markdown.py 是使用chatGPT辅助编写的文本转换脚本。
其主要功能是将chatGPT的聊天记录通过html转markdown的方式，转换为可在本地阅读的文档版本。
由于openAI目前尚未对公众发布官方的插件接口，chatGPT仍在持续优化中，可能未来还会面临聊天记录丢失等情况;
另外，储存与云端的聊天记录也不太方便随时浏览，这两点是我制作此脚本的原因。

实现的功能：将chatGPT聊天记录保存为html文档后，通过本脚本可批量转换为markdown格式。
    Markdown语法是一种轻量级标记语言，通过特定符号进行写作，通常用于编写简单的文档，例如README文件、博客文章、论坛帖子等等。Markdown语法简单易懂，可以快速创建格式良好的文档。每种符号都具有特定含义，例如：
        **文本1** —— 会将文本1加粗显示；
        _文本2_ —— 会将文本2用斜体显示；
        以下三个要点将显示为无序列表
            - 要点1
            - 要点2
            - 要点3
    md文件需要使用特定的笔记应用查看才能正确渲染格式，如果以记事本打开，会将格式符号直接显示出来。

缺陷：暂不支持代码块的识别。如果聊天中包含代码，可能产生不正确的格式。

可在/source 和/output文件夹中查看提供的示例。


-----------------------------------------------------------------------------------
|                                    使用方法                                      |
-----------------------------------------------------------------------------------


0. 您需要先自行安装python，版本为3.10.4或以上即可，
    下载链接：https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe
    在下载完成后，运行exe文件并以默认的设置选项安装即可，建议勾选Add to PATH选项，来让python被注册至windows系统的环境变量中；


1. python安装完成后，双击运行“安装依赖库.bat”，缺少必要的python库，该脚本将无法正常工作；
    若出于某些原因，无法通过“安装依赖库.bat”安装相应的依赖，您可以执行以下操作来手动安装：
        1. 首先，按下win + R 键盘，唤出运行窗口，输入powershell并按下回车，这将打开windows系统的终端；
        2. 在终端内，首先输入 python --version 来查看当前系统默认的python版本。终端应该会返回类似如下信息：
            Python 3.10.4
        3. 然后，依次输入以下两条指令：
            pip install -i https://pypi.tuna.tsinghua.edu.cn/simple beautifulsoup4
            注意在两次输入之间，应该等待终端提示下载完成，才可继续执行下一条指令；
        4. 若正常运行，两个依赖库应该都已经被正确安装，您可以通过以下指令来确认：
            pip show pygments beautifulsoup4

            这将打印出类似下面的信息：
            Name: beautifulsoup4
            Version: 4.11.2
            Summary: Screen-scraping library
            ...


4. 安装完运行库即可正常使用该脚本。以下是具体使用方法：
    - 在chatGPT的任意聊天窗口中，右键-另存为，将整个页面保存为html文档。建议您建立一个专门的文件夹用于存放chatGPT的聊天记录；

    - 将下载的html文件放置于：
            ~\chatGPT聊天记录转换\source\聊天记录XXXX.html
        你的文件夹层级结构应该看上去类似这样：
            |----chatGPT聊天记录转换
                |----output
                |----source
                    |----聊天记录1.html
                    |----聊天记录2.html
                    |----聊天记录n.html
                |----convert2Markdown.py
                |----requirements.txt
                |----安装依赖库.bat
                |----运行批量转换.bat

    - 双击运行“运行批量转换.bat”，会将source下的所有html文件批量转换为markdown文本，并储存至“output”文件夹内。


5. 请注意，如果一次对非常多html文件执行批量转换，可能会消耗较多时间才能完成。


6. 转换完成的.md文件是使用markdown格式编写的文档，您可以将它们导入任意支持markdown语法的笔记应用中进行浏览，
    例如：我来Wolai、Typora、MarkText以及VS Code等。
