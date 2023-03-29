chcp 65001

@echo 开始安装脚本所需的依赖，若显示连接超时，请尝试关闭网络代理后再次运行bat脚本。

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

@echo 脚本依赖安装完成。

pause