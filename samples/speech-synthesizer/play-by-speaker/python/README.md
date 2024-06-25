## 前提条件
### 安装 Python 依赖

阿里云百炼SDK运行环境需要Python3.8及以上版本。
运行本场景DEMO依赖的环境可以通过[PyPI](https://pypi.org/)安装。
- FFMPEG


- 三方SDK
```commandline
pip3 install pyglet //用于播放mp3音频
pip3 install pyaudio //用于实时播放音频
pip3 install ffmpeg-python //python的ffmpeg绑定，用于实时解码mp3音频。
```
在安装ffmpeg-python时请参考对应[官方文档](https://github.com/kkroening/ffmpeg-python)安装ffmpeg

- 百炼SDK
```commandline
pip3 install dashscope //安装阿里云百炼SDK
```