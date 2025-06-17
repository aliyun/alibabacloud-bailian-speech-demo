[comment]: # (title and brief introduction of the sample)

简体中文 | [English](./README_EN.md)

## 并发调用语音合成
## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

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

示例运行时，将使用三种不同的音色并发合成 “我是XXX，欢迎体验阿里云百炼大模型语音合成服务！” 并保存在 `results/result_v<音色名>_p<线程号>.mp3` 文件中。

您可以通过修改`task_list`中增加/删除任务合成指定数量的文本。通过修改`multiprocessing.Pool`中的`processes`参数修改最大进程数。建议不超过机器的cpu核心数。

在Python的调用示例中，由于Python存在全局解释器，因此使用了多进程的方式实现并发。

:information_source: **注意**：个人账号的appkey当前仅支持 3 并发，如需开通多并发请联系我们。



[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>
