[comment]: # (title and brief introduction of the sample)
## 语音合成实时LLM输出并播放（流式模式）
## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装ffmpeg

    示例需要用到ffmpeg进行音视频解码。推荐从官方网站下载安装，并将ffmpeg安装路径配置进环境变量：[ffmpeg官方网站下载](https://www.ffmpeg.org/download.html)。也可以参考文档[如何安装ffmpeg](../../../docs/QA/ffmpeg.md)。

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

示例运行时，将会调用阿里云百炼平台大语言模型千问（qwen-turbo）回答提问：“番茄炒鸡蛋怎么做？”，并使用 longmiao 音色，按照流式方式发送大模型回答的文本并合成，将音频按照流式方式下发并通过扬声器播放。

运行示例如下：
```
>>>提问：番茄炒鸡蛋怎么做？
>>>回答：做番茄炒鸡蛋挺简单的，你先准备好材料：几个新鲜的番茄和几个鸡蛋。先把鸡蛋打在碗里，加一点点盐，然后用筷子搅匀。
接着热锅凉油，油温上来后就把鸡蛋液倒进去，等它稍微凝固一点就可以用铲子翻炒几下，鸡蛋变金黄色就可以盛出来备用。
                                                            
然后锅里再加点油，把切好的番茄块放进去翻炒，番茄会出一些汁水，你可以根据口味加点糖中和酸味。等番茄差不多了，就把刚才炒好
的鸡蛋倒回去一起翻炒均匀，最后尝尝味道，如果需要可以再调一下味，撒点葱花就可以出锅啦！

试试看吧，记得注意火候哦！                                                                                              synthesize and play over with requestId:  09690564096a47a5b7fae07dbb615117 
```

您可以通过修改`query_to_llm`更改提问内容。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
