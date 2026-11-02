[comment]: # (title and brief introduction of the sample)
## 批量音视频文件转写（SDK v2 兼容模式）
## Python

本示例使用 DashScope SDK 2.0.2 的 `Client`/v2 接口和 `qwen-audio-3.1-asr-flash-filetrans` 模型。由于 v2 批量转写端点当前不提供 `sensevoice-v1`，示例为每个 URL 分别提交一个任务，主要展示文件转写流程。

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

运行示例后，录音文件识别服务会为每个 URL 分别执行后台转写。转写成功后，示例下载结果，通过 `parse_sensevoice_result` 清理文本及结果中可能存在的标签，并打印到终端。

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="../../../../docs/image/group.png" width="400"/>

