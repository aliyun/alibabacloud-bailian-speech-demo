[comment]: # (title and brief introduction of the sample)
## 批量音视频文件语音识别（实时模式）
批量音视频文件语音识别（实时模式）是指并发的将多个音视频文件通过实时的方式将语音数据发送给语音识别服务，并实时地将语音转换为文字的过程。


## Python

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### 安装Python依赖

    阿里云百炼SDK运行环境需要Python 3.8及以上版本。您可以使用以下命令来安装本示例的依赖：
    ```commandline
    pip install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: 运行示例
- 您可以使用以下命令运行本示例：

```commandline
python3 run.py
```

   示例使用了multiprocessing实现并发运行。在示例运行时，程序会并发的读取您输入的多个音视频文件，将其独立的转为实时识别结果并分别以callback的方式回调识别结果。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/groups.png" width="400"/>