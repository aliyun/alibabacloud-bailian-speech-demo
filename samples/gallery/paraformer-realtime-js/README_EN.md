# Paraformer Real-Time Speech Recognition JavaScript Example

English | [简体中文](./README.md)

This example demonstrates how to integrate the Paraformer real-time speech recognition service on Alibaba Cloud's Model Studio platform using JavaScript. The example includes a built-in audio recorder module that allows recording audio in the browser, calling the speech recognition service, and displaying recognition results.

## Prerequisites

### Configure Alibaba Cloud Model Studio API-KEY
Before running this example, you need to create an Alibaba Cloud account, obtain the Model Studio API_KEY, and complete necessary environment configurations. For detailed API-KEY configuration steps, please refer to: [PREREQUISITES.md](../../../PREREQUISITES.md)

## Run the Example

This directory demonstrates a frontend integration example of Paraformer. You need to set up a local HTTP server to support importing local JS scripts through the browser.

Run an HTTP server in this directory:

```
python -m http.server 9000
```


You can then open the test page in your browser by entering `http://localhost:9000`. Enter the API key and click the `Start Recording` button to begin speaking into the microphone. Click the `Stop Recording` button to end the recording.

<img src="../../../docs/image/js-paraformer.png" width="400"/>

### Audio Recording Notes
In `audio_recorder.js`, we use the Web Audio API to develop PCMAudioRecorder for recording PCM format audio. AudioWorkletNode is used to asynchronously convert sample points from floating-point numbers to 16-bit Int16Array through callbacks. The buffer size defaults to 1600 sample points (100ms).

### Authentication and Account Security

In the Model Studio WebSocket service, since JavaScript doesn't support custom HTTP headers, the API Key needs to be passed through URL parameters for authentication.

#### Security Notes
While adding permanent API Keys directly in URLs is simple, it carries security risks:
- **API Key exposure risk**: API Keys are directly exposed in frontend code or URLs, making them easily accessible through browser developer tools, network packet capture, or log records.
- **Potential consequences**: Once exposed, attackers could use the API Key to access your services long-term, potentially causing data leaks, resource abuse, or other security issues.

#### Disclaimer
Please note that when using this method, you bear full responsibility for any consequences resulting from API Key exposure. We strongly recommend:
1. Avoiding permanent API Key exposure: Use short-lived dynamic tokens (e.g., JWT) instead of permanent API Keys, generated and distributed through backend services.
2. Enabling HTTPS: Ensure all communications use encrypted HTTPS connections to prevent API Key interception during transmission.
3. Limiting API Key permissions: Set minimal permissions for API Keys to ensure limited damage if exposed.

For higher security requirements, deploying a forwarding service is recommended.