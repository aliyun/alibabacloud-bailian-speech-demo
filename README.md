# Sample Repository for the AlibabaCloud Bailian Speech SDK

## 关于
---

本仓库提供了阿里云百炼语音大模型服务在一些常用场景的集成示例代码。示例展示了如何通过阿里云百炼的语音大模型服务开发工具包（SDK），实现语音识别（语音转文字）、语音合成（文字转语音）、语音交互等各类AI功能。
您可以将本文档中的这些示例集成进自己的项目中进行二次开发。如有任何疑问还可以通过我们的钉钉 / 微信群进行沟通交流。

### 联系我们

<img src="docs/image/groups.png" width="400"/>


## 最新动态
----
- 2024/07/19：更新文档结构。增加VoiceChat示例、增加语音质检示例。
- 2024/07/17：更新说明文档。
- 2024/07/05：补充QA文档。
- 2024/06/25：发布初始版本，分别支持从麦克风/文件输入识别，以及语音合成到扬声器和文件的 python/java 示例。


## 示例获取和准备
----

- 您可以通过 `git clone` 克隆示例工程，或者通过 `Download Zip` 下载完整工程，并在本地解压到文件。

- 在执行示例代码之前，您需要申请阿里云账号并开通**API\_KEY,** 并进行必要的**环境配置**。 请参考文档[PREREQUISITES.md](./PREREQUISITES.md).
- 有些示例的场景还需要导入必要的依赖，如mp3播放的示例需要导入mp3编解码和播放的依赖库。您可以在示例代码所在目录下的README.md文件中查看依赖条件。

##  应用场景与开发示例
----
### 快速开始

<div style="display: flex;">
  <div style="flex: 1; padding: 10px;">
    <h3>电话客服中心场景</h3>
    <p>呼叫语音转文字 | 客服回复转语音 | 批量通话录音转文字 | 电话录音质检</p>
    <h3>语音对话场景</h3>
    <p>语音助手 | 智能音箱 | 智能机器人 </p>
    <h3>会议场景</h3>
    <p>线下&音视频会议语音识别与分析 | 销售对话分析</p>
  </div>
  
  <div style="flex: 1; padding: 10px;">
    <h3>语音播报场景</h3>
    <p>视频配音  | 角色扮演配音 | 有声读物  | 信息播报 | 分角色的有声书配音</p>
    <h3>音视频场景</h3>
    <p>Voice Chat | 音视频语音识别 </p>
  </div>
</div>

### 场景详情

#### 电话客服中心场景

<table>
    <tr>
        <th style="background-color: gray; font-weight: bold;">应用场景</th>    
        <th style="background-color: gray; font-weight: bold;">典型用法</th>
        <th style="background-color: gray; font-weight: bold;">开发示例</th>
    <tr>
    <tr>
        <td rowspan="6">呼叫中心<br/> 电话内外呼 <br/> Virtual Call</td>
        <td>
           <p><i>呼叫语音转文字</i></p>
            <span style="font-size: 12px; color: grey;">将用户或客服人员的语音通话实时转为文字 </span>
        </td>
        <td>
            实时语音识别 <a href="samples/speech-recognition/from-file/java/realtime-recognition">java </a> <a href="samples/speech-recognition/from-file/python/realtime-recognition">python </a> </td>
    <tr>
    <tr>
        <td>
           <p><i>客服回复转语音</i> </p>
            <span style="font-size: 12px; color: grey;">使用文字转语音对客服机器人回复进行实时语音播报 </span>
        <td>实时语音播报 <a target="_blank" rel="noopener noreferrer" href="samples/speech-synthesizer/play-by-speaker/java/single-line-input/">java </a> <a target="_blank" rel="noopener noreferrer" href="samples/speech-synthesizer/play-by-speaker/python/single-line-input">python</a> </td>
    </tr>
    <tr>
        <td>
            <p><i>批量通话录音转文字</i> </p>
            <span style="font-size: 12px; color: grey;">将用户或客服人员的语音通话录音批量转为文字 </span>
        </td>
        <td>录音文件识别 <a href="samples/speech-recognition/from-file/java/transcription">java </a> <a href="samples/speech-recognition/from-file/python/transcription">python </a> </td>
    </tr>
    <tr>
        <td>
            <p><i>电话录音质检</i> </p>
            <span style="font-size: 12px; color: grey;">对于电话录音进行语义转写。在获取结果后，调用大模型能力，配合prompt定义质检规则对识别文本进行质检。</span>
        </td>
        <td>电话录音质检 <a href="https://tongyi.aliyun.com/"><img src="docs/image/logo.svg" width="15"/>  <a href="samples/speech-plus/call-quality-assurance">python </a> </td>
    </tr>
</table>


#### 语音播报场景

<table>
    <tr>
        <th style="background-color: gray; font-weight: bold;">应用场景</th>    
        <th style="background-color: gray; font-weight: bold;">典型用法</th>
        <th style="background-color: gray; font-weight: bold;">开发示例</th>
    <tr>
    <tr>
        <td>视频配音 <br/> 角色扮演配音 <br/>
        AIGC视频生成 </td>
        <td>
            <p><i>配音</i></p>
            <span style="font-size: 12px; color: grey;">根据场景、人设、情绪选择适合的发音人，合成设计文案生成配音</span>
        </td>
        <td rowspan="4">
            实时语音播报 <a href="samples/speech-synthesizer/play-by-speaker/java/single-line-input">java </a> <a href="samples/speech-synthesizer/play-by-speaker/python/single-line-input">python </a> 
            <br/> 离线语音合成 <a href="samples/speech-synthesizer/save-to-file/java">java </a> <a href="samples/speech-synthesizer/save-to-file/python">python </a>
        </td>
    <tr>
    <tr>
        <td>新闻<br/>数字人</td>
        <td>
            <p><i>信息播报</i></p>
            <span style="font-size: 12px; color: grey;">新闻等场景，通过语音合成进行文本信息的播报</span>
        </td>
    <tr>
    <tr>
        <td rowspan="4">有声读物</td>
        <td>
            <p><i>分角色的有声书配音</i></p>
            <span style="font-size: 12px; color: grey;">将绘本、小说等文字内容转换为有声读物。推荐结合大模型能力，将内容分角色格式化输出。</span>
        </td>
        <td>分角色的语音合成 <a href="https://tongyi.aliyun.com/"><img src="docs/image/logo.svg" width="15"/> 
        <br/> <a href="samples/speech-synthesizer/play-by-speaker/python/multi-roles-input">python </a>
        </td>
    <tr>
</table>

#### 语音对话场景
<table>
    <tr>
        <th style="background-color: gray; font-weight: bold;">应用场景</th>    
        <th style="background-color: gray; font-weight: bold;">典型用法</th>
        <th style="background-color: gray; font-weight: bold;">开发示例</th>
    <tr>
    <tr>
        <td rowspan="4">语音助手 <br> 智能音箱 <br> 智能机器人 </td>
        <td>
            <p><i>语音交互</i></p>
            <span style="font-size: 12px; color: grey;">
            适用于手机、车机、智能音箱、机器人包括IOT设备等场景下的语音对话。用户通过语音输入问题，通过语音合成获取结果
            </span>
        </td>
        <td>实时语音识别 <a href="">java </a> <a href="samples/speech-recognition/from-file/python/realtime-recognition">python </a><br>
            实时语音合成 <a href="samples/speech-synthesizer/play-by-speaker/java/single-line-input">java </a> <a href="samples/speech-synthesizer/play-by-speaker/python/single-line-input">python </a> 
        </td>
    <tr>
    <tr>
        <td>
            <p><i>语音对话聊天（大模型结合）</i></p>
            <span style="font-size: 12px; color: grey;">
            适用于手机、车机、智能音箱、机器人包括IOT设备等场景下开放域聊天，以及Agent等LLM等深度定制场景
            </span>
        </td>
        <td>实时语音识别 <a href="">java </a> <a href="samples/speech-recognition/from-file/python/realtime-recognition">python </a><br>
        结合大模型的语音播报 <a href="https://tongyi.aliyun.com/"><img src="docs/image/logo.svg" width="15"/> <br/> <a href="samples/speech-synthesizer/play-by-speaker/java/streaming-input">java </a> <a href="samples/speech-synthesizer/play-by-speaker/python/streaming-input">python </a>
    <tr>
</table>

#### 音视频场景
<table>
    <tr>
        <th style="background-color: gray; font-weight: bold;">应用场景</th>    
        <th style="background-color: gray; font-weight: bold;">典型用法</th>
        <th style="background-color: gray; font-weight: bold;">开发示例</th>
    <tr>
    <tr>
        <td >Voice Chat 🔥</td>
        <td>
            <p><i>Voice Chat</i></p>
            <span style="font-size: 12px; color: grey;">适用于数字人、在线教育、智能客服等语音进语音出的交互场景</span>
        </td>
        <td>
            Voice Chat <a href="https://tongyi.aliyun.com/"><img src="docs/image/logo.svg" width="15"/> <a href="samples/speech-plus/voice-chat">python </a> </td>
    <tr>
    <tr>
        <td rowspan="3">视频会议<br/>直播</td>
        <td>
            <p><i>音视频语音识别</i> </p>
            <span style="font-size: 12px; color: grey;"> 适用于音视频会议、直播等场景下的通过流式调用的语音识别</span>
        </td>
        <td>实时语音识别 <a href="samples/speech-recognition/from-file/java/realtime-recognition">java </a> <a href="samples/speech-recognition/from-file/python/realtime-recognition">python </a> </td>
    <tr>
</table>

#### 会议及对话场景
<table>
    <tr>
        <th style="background-color: gray; font-weight: bold;">应用场景</th>    
        <th style="background-color: gray; font-weight: bold;">典型用法</th>
        <th style="background-color: gray; font-weight: bold;">开发示例</th>
    <tr>
    <tr>
        <td>    
            线下会议<br/>
            音视频会议 <br/>
            现场访谈
        </td>
        <td>
            <p><i>音视频语音识别与分析</i></p>
            <span style="font-size: 12px; color: grey;"> 适用于线下会议、音视频会议等场景，会议结束后对会议音视频进行转写，对会议对话内容的总结</span>
        </td>
        <td rowspan="2">
            录音文件识别 <a href="https://tongyi.aliyun.com/"><img src="docs/image/logo.svg" width="15"/><a href="samples/speech-recognition/from-file/java/transcription">java </a> <a href="samples/speech-recognition/from-file/python/transcription">python </a> 
        </td>
    </tr>
</table>

## 常见问题

常见问题请参考[QA文档](docs/QA/qa.md)

## 许可协议

本项目遵循[The MIT License](https://opensource.org/license/MIT)开源协议