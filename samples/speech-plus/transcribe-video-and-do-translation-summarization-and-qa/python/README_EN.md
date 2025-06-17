[comment]: # (title and brief introduction of the sample)
## Meeting Video Transcription with Translation, Summary, and Q&A

English | [简体中文](./README.md)

[comment]: # (prerequisites)
### :point_right: Prerequisites

1. #### Configure Alibaba Cloud Bailian API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

2. #### Install Python Dependencies

    The Alibaba Cloud Bailian SDK requires Python 3.8 or higher. You can install the dependencies for this example using the following command:
    ```commandline
    pip3 install -r requirements.txt
    ```

[comment]: # (how to run the sample and expected results)
### :point_right: Run Example
You can run this example using the following command:

```commandline
python3 run.py
```

Submit the video file to be processed. The console will sequentially output:

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
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>