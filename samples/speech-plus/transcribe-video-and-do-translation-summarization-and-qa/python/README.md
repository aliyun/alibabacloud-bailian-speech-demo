[comment]: # (title and brief introduction of the sample)
## 会议视频转写并进行翻译摘要和问答

简体中文 | [English](./README_EN.md)

[comment]: # (prerequisites)
### :point_right: 前提条件

1. #### 配置阿里云百炼API-KEY

    在运行本示例之前，您需要开通阿里云账号、获得阿里云百炼API_KEY，并进行必要的环境配置。有关API-KEY的详细配置步骤请参考：[PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### 安装Python依赖

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
提交需要处理的视频文件。控制台会依次输出：
```text
============ transcribe and translate === START ===
transcribe==> 一百多年前，电灯第一次进入了人类的生活世界，迎来了新的时代。
translate ==> More than a hundred years ago, electric lights entered human life for the first time, ushering in a new era.
transcribe==> 有了电，人类才发明了电视机，才有了夜生活。
translate ==> With electricity, humans were able to invent television and thus, nightlife came into existence.
transcribe==> 现代工业和交通的出现，创造了现代的城市。
translate ==> The emergence of modern industry and transportation gave rise to modern cities.
transcribe==> 人类社会发展的速度超过了历史上任何时候，进入了伟大的电气化时代。
translate ==> Human society has developed at a faster pace than ever before in history, ushering in the grand era of electrification.
transcribe==> 今天，我们又迎来了一轮百年未遇的科技变局。
translate ==> Today, we are witnessing another round of technological transformations unprecedented in a century.
============= transcribe and translate ===  END  ===


============= summary === START ===
1. 电气化时代：电灯的发明引领人类进入电气化时代，促进工业、交通发展，加速社会发展进程。
2. 数字化时代变革：当前正处于百年未遇的科技变局，数字化转型改变人类生活、生产方式及生存状态。
3. 云计算新时代：阿里云推动云计算成为新计算时代基础，让计算资源普及，如同电一般无处不在，重塑世界，激发无限想象力。

总结：从电气化到数字化，云计算正如同电一样，深刻改变世界格局，开启创新纪元。
============= summary ===  END  ===


============= QA === START ===
question is: 人类什么时候发明的电灯
result is: 人类发明电灯大约在一百多年前，这标志着电灯首次进入了人类的生活，开启了新的时代。
============= QA ===  END  ===
```

[comment]: # (technical support of the sample)
### :point_right: 技术支持
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group.png" width="400"/>

