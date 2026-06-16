[comment]: # (title and brief introduction of the sample)
## Generate Music from Lyrics

English | [简体中文](./README.md)

This example demonstrates how to provide custom lyrics and use the Fun-Music large model to compose music and sing based on the lyrics. The generated audio is saved as a file.

[comment]: # (list of scenarios of the sample)
### :point_right: Applicable Scenarios

| Application Scenario | Typical Usage | Usage Instructions |
| ----- | ----- | ----- |
| **Entry-level Scenario** | Generate music from custom lyrics | *Provide your own lyrics and let AI compose and sing* |
| **Music Creation Scenario** | Lyric and melody creation assistance | *Already have lyrics, quickly generate a Demo to preview the effect* |
| **Personalization Scenario** | Custom songs | *Create exclusive songs for specific occasions (birthdays, anniversaries, etc.)* |

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

When running the example, it will generate a song sung by a female voice based on the provided custom lyrics and save it to the `result.mp3` file.

### :point_right: Lyrics Specification

You can use the following structural tags to organize the song structure:

| Tag | Description |
| --- | --- |
| `[intro]` | Introduction, sets the atmosphere |
| `[verse]` | Verse, tells the story |
| `[chorus]` | Chorus, emotional climax |
| `[bridge]` | Bridge, perspective shift |
| `[outro]` | Outro, gradual fade-out |

### :point_right: Parameter Description

- **lyrics**: Custom lyrics content. Supports Chinese or English, must follow originality principles and content safety requirements.
- **gender**: Singer gender,可选 `male` or `female`.
- **model**: Music generation model,可选 `fun-music-v1` or `fun-music-preview`.

**Note**: Either `lyrics` or `prompt` must be provided, and they cannot both be empty. When both are provided, only `lyrics` takes effect, and `prompt` will be ignored.

[comment]: # (technical support of the sample)
### :point_right: Technical Support
<img src="https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/group-en.png" width="400"/>
