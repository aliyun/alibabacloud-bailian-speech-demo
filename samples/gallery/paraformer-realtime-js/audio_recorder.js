class PCMAudioRecorder {
    constructor() {
        this.audioContext = null;
        this.stream = null;
        this.currentSource = null;
        this.audioCallback = null;
    }

    async connect(audioCallback) {
        this.audioCallback = audioCallback;
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
        }

        this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        this.currentSource = this.audioContext.createMediaStreamSource(this.stream);

        // 加载 AudioWorklet
        try {
            await this.audioContext.audioWorklet.addModule('./recorder_worklet.js');
        } catch (e) {
            console.error('Error loading AudioWorklet:', e);
            return;
        }

        // 创建 AudioWorkletNode
        this.processorNode = new AudioWorkletNode(this.audioContext, 'pcm-processor');

        // 监听从 AudioWorkletProcessor 发来的消息
        this.processorNode.port.onmessage = (event) => {
            if (event.data instanceof Int16Array) {
                if (this.audioCallback) {
                    this.audioCallback(event.data);
                }
            } else {
                console.log('Received message from AudioWorkletProcessor:', event.data);

                if (event.data == 'stopped') {
                    console.log('Recorder stopped.');
                    // this.processorNode.disconnect();
                    // this.processorNode.port.close();
                    // this.processorNode = null;
                }
            }
        };

        // 连接节点

        this.currentSource.connect(this.processorNode);
        this.processorNode.connect(this.audioContext.destination);
        console.log('Recorder connected.');
    }

    stop() {
        // 断开 AudioWorkletNode
        if (this.processorNode) {
            this.processorNode.port.postMessage('stop');
        }

        // 停止音频流
        if (this.stream) {
            const tracks = this.stream.getTracks();
            tracks.forEach(track => track.stop());
        }

        // 断开音频链接
        if (this.currentSource) {
            this.currentSource.disconnect();
            this.currentSource = null;
        }

        // 关闭音频上下文
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }

        // 重置音频回调
        this.audioCallback = null;
        if (this.processorNode) {
            this.processorNode.port.postMessage('stop');
            this.processorNode.disconnect();
            this.processorNode.port.close();
            this.processorNode = null;
        }
    }
}

export default PCMAudioRecorder;