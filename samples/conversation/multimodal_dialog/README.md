# DashScope Multimodal Dialog API 集成指南
简体中文 | [English](./README_EN.md)

## 概述

DashScope 多模对话 API 提供强大的多模对话能力。多模对话服务提供了Speech-to-Speech的的实时交互能力，同时支持图片和视频等多模态数据对话的能力，多模对话服务同时支持使用百炼生态中的插件、官方应用和三方应用。

## 功能特性

- 🎤 **语音对话**: 实时语音识别和合成
- 🖼️ **图像问答**: 基于图像内容的智能问答
- 💬 **多种交互模式**: Push2Talk、Tap2Talk、Duplex
- 🔄 **流式处理**: 实时音频流传输和处理
- 🌐 **WebSocket 连接**: 低延迟实时通信
- 🧩 **Agent支持**: 百炼官方和三方Agent集成

## 前置条件

### 1. 获取 API 凭证
请登录多模态对话控制台，激活服务并创建应用，然后您可以获得以下参数：
- **API Key**: 用于身份验证
- **Workspace ID**: 工作空间标识符
- **App ID**: 应用标识符

### 2. 环境要求

#### Java 环境
- Java 8 或更高版本
- Maven 3.6+

#### Python 环境
- Python 3.9 或更高版本
- pip 包管理器

### 其他
更多 API 详情，请参考官方文档 [Python](https://help.aliyun.com/zh/model-studio/multimodal-sdk-python) 和 [Java](https://help.aliyun.com/zh/model-studio/multimodal-sdk-java)。