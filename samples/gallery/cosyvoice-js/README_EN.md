# Cosyvoice Text-to-Speech JavaScript Example

English | [简体中文](./README.md)

This example demonstrates how to integrate the Cosyvoice text-to-speech service from Alibaba Cloud's Bailian platform using JavaScript. The example includes a player module that can play streaming audio in the browser.

## Prerequisites

#### Configure Alibaba Cloud Bailian API-KEY

Before running this example, you need to create an Alibaba Cloud account, obtain the Alibaba Cloud Bailian API-KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../PREREQUISITES.md)

## Run Example

This directory demonstrates a frontend integration of Cosyvoice. You need to set up a local HTTP server to support loading local JS scripts in the browser.

Run an HTTP server in this directory:
```bash
python -m http.server 9000
```

You can then open the test page in your browser by entering `http://localhost:9000`. Enter your API key, the text to synthesize, and click the `Send` button to generate and play the audio.

<img src="../../../docs/image/js-cosyvoice.png" width="400"/>

### About Streaming Input

Streaming input can be implemented by calling sendText multiple times. This example does not demonstrate this functionality.

### About the Player Implementation

In `audio_player.js`, we developed a PCMAudioPlayer using Web Audio API to play streaming PCM format audio. It converts 16-bit samples to float values, writes them into audioBuffer for playback, and immediately plays the next audio segment when the previous one ends via the onended callback.

>Note ⚠️:
>1. Using MediaSource for streaming audio is a simpler solution, but it's not supported in: Safari, Safari-based iOS WebView, and WeChat Mini Programs. More compatibility information see MediaSource
>2. Using openai-realtime-console with wavtools may produce noise during playback on mobile devices and Safari browsers.

### Authentication and Account Security

In the Bailian Websockets service, since JavaScript doesn't support adding custom HTTP Headers, the API Key needs to be passed through URL parameters for authentication.

### Security Notes

While adding a long-term API Key via URL is simple, it carries certain security risks:

API Key Exposure Risk: API Keys exposed in frontend code or URLs can be easily obtained by malicious users through browser developer tools, network packet captures, or log records.
Potential Consequences: A leaked API Key could allow attackers to access your services indefinitely, potentially leading to data breaches, resource abuse, or other security issues.

### Disclaimer

Please note that when using this method, you assume full responsibility for any consequences caused by API Key leaks. We strongly recommend implementing the following security measures:

1. Avoid exposing long-term API Keys: Consider using short-lived dynamic tokens (like JWT) instead of permanent API Keys, generating and distributing these tokens through backend services.
2. Enable HTTPS: Ensure all communications use encrypted HTTPS connections to prevent API Key interception during transmission.
Restrict API Key Permissions: Set minimal permissions for API Keys to limit potential damage in case of a leak.

For higher security requirements, we recommend deploying a forwarding service.