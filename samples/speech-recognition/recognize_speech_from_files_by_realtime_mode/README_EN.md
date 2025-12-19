[comment]: # (title and brief introduction of the sample)
## Batch Audio/Video File Speech Recognition (Real-time Mode)
This example demonstrates how to batch call the real-time speech recognition API to process multiple file streams and return recognition results for each file in real-time.

The **real-time mode** of audio/video file speech recognition is more suitable for processing local files with immediate result returns, or building streaming audio services that collect frontend audio streams and return recognition results instantly.

If you use Java to build a speech service, refer to the [high-concurrency example documentation](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-in-high-concurrency-scenarios) for optimal performance.

If you need to process large volumes of cloud files for production tasks without requiring immediate results, please refer to the example: [Batch Audio/Video File Speech Recognition (Batch Mode)](../recognize_speech_from_files_by_batch_mode//).

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario    | Typical Use    | Usage Description              |
|---------|---------|-------------------|
| **Getting Started Scenario**| Audio/Video File Speech Recognition	 | *Perform batch speech recognition on audio/video files*  |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details

| Recommended Model | API Details |
| ----- | ----- |
| **fun-asr-realtime** | [Fun-ASR Real-time Speech Recognition API Details](https://help.aliyun.com/zh/model-studio/fun-asr-real-time-speech-recognition-api-reference/) |
| **paraformer-realtime-v2**<br>paraformer-realtime-v1<br>paraformer-realtime-8k-v1 | [Paraformer Real-time Speech Recognition API Details](https://help.aliyun.com/zh/model-studio/developer-reference/paraformer-real-time-speech-recognition-api) |


### :point_right: Expected Results

Running the example will output streaming recognition results in the console. Each file's recognition corresponds to a [process id], and incremental results will be returned continuously. For example:

```
    //process 51389 corresponds to recognition result 1 of sample_audio.mp3
    [process 51389]RecognitionCallback text:  那河畔的金柳是夕阳中的

    //process 51392 corresponds to recognition result of sample_video_story.mp4
    [process 51392]RecognitionCallback text:  在一个阳光明媚的早晨，鸭妈妈决定带着小鸭子们

    //process 51389 corresponds to recognition result 2 of sample_audio.mp3
    [process 51389]RecognitionCallback text:  那河畔的金柳是夕阳中的新娘。
```

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>