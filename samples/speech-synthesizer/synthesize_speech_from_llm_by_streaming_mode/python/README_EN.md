## Real-time LLM Output Synthesis and Playback (Streaming Mode)

English | [简体中文](./README.md)

## Python

### :point_right: Prerequisites

1. #### Configure Alibaba Cloud API-KEY

    Before running this example, you need to create an Alibaba Cloud account, obtain the API-KEY, and complete environment configuration. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../../PREREQUISITES.md)

1. #### Install ffmpeg

    This example requires ffmpeg for audio/video decoding. It is recommended to download and install it from the official website, and configure the ffmpeg installation path in the environment variables: [ffmpeg official website download](https://www.ffmpeg.org/download.html). You can also refer to the document [How to install ffmpeg](../../../docs/QA/ffmpeg_en.md).

1. #### Install Python dependencies

    The Alibaba Cloud SDK requires Python 3.8 or higher. You can use the following command to install dependencies for this example:
    ```commandline
    pip3 install -r requirements.txt
    ```
    Please refer to [documentation](https://github.com/kkroening/ffmpeg-python) for ffmpeg installation

### :point_right: How to Run the Example
You can use the following command to run this example:

```commandline
python3 run.py
```
When the example runs, it will call the Alibaba Cloud Qwen (qwen-turbo) large language model to answer the question: "How to cook tomatoes with eggs?" and use the longanhuan voice to send the model's response text in streaming mode for synthesis, then stream and play the audio through the speaker.

Sample output:
```
>>> Question: How to cook tomatoes with eggs?
>>> Answer: It's quite simple to make tomatoes with eggs. First prepare the ingredients: several fresh tomatoes and eggs. Crack the eggs into a bowl, add a little salt, then stir well with a chopstick.
Next, heat the pan with oil, when the oil is hot enough, pour in the egg liquid. Once it starts to solidify, flip it with a spatula a few times. When the eggs turn golden yellow, remove them and set aside.

Add more oil to the pan, put in the chopped tomatoes and stir-fry. As the tomatoes release some juice, you can add a bit of sugar to balance the sour taste according to your preference. When the tomatoes are almost done, add the previously cooked
eggs back in to stir-fry together. Finally, taste and adjust the seasoning if needed, sprinkle some green onions, and it's ready to serve!

Give it a try, and remember to pay attention to the heat!                                                                                              synthesize and play over with requestId:  09690564096a47a5b7fae07dbb615117
```

You can modify `query_to_llm` to change the question content.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
