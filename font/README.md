主要使用的字体为[霞鹜文楷](https://github.com/lxgw/LxgwWenKai)的 Regular 字重。

字体文件并没有上传到仓库中，需要自行从 [Release](https://github.com/lxgw/LxgwWenKai/releases) 下载 `LXGWWenKai-Regular.ttf`，保存到这个目录。

打包时使用的的是经过字体子集化处理、只保留了实际使用的字形的文件。如果需要生成这个文件，可以在下载字体到任意位置后在项目根目录运行 `python tool/generate-font-subset.py /path/to/LXGWWenKai-Regular.ttf font/LXGWWenKai-Regular.ttf "**/*.py" "scriptfiles/**/*.txt"`。