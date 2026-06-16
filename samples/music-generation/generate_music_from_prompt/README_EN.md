[comment]: # (title and brief introduction of the sample)
## Generate Music from Prompt

English | [简体中文](./README.md)

This example demonstrates how to generate a complete song using the Fun-Music large model by providing a prompt that describes the music style and scene. The generated audio is saved as a file.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions |
| ----- | ----- | ----- |
| **Entry-level Scenario** | Generate music from description | *Input a description of music style, mood, and scene to automatically generate and sing a song* |
| **Video Soundtrack Scenario** | Vlog/short video background music | *Generate matching background music based on video theme and mood* |
| **Creative Assistance Scenario** | Music creation inspiration | *Quickly generate demos through AI to get creative inspiration* |

[comment]: # (supported programming languages of the sample)
### :point_right: Programming Languages
- [Python](./python)
- [Java](./java)

[comment]: # (model and interface of the sample)
### :point_right: Reference Details
| Recommended Model | API Details |
| --- | --- |
| **fun-music-v1** | [Fun-Music Music Generation API Details](https://help.aliyun.com/zh/model-studio/fun-music) |
| **fun-music-preview** | [Fun-Music Music Generation API Details](https://help.aliyun.com/zh/model-studio/fun-music) |

### :point_right: Expected Results

When running the example, it will generate a song sung by a female voice based on the prompt "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐" and save it to the `result.mp3` file.

### :point_right: Parameter Description

- **prompt**: A natural language prompt describing the music style, scene, and mood. It is recommended to be specific, e.g., "sad piano music, rainy night longing" rather than vague descriptions like "sad music".
- **gender**: Singer gender,可选 `male` or `female`.
- **model**: Music generation model,可选 `fun-music-v1` or `fun-music-preview`.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
