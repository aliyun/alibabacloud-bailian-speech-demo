class PCMAudioPlayer {
    constructor(sampleRate) {
        this.sampleRate = sampleRate;
        this.audioContext = null;
        this.audioQueue = [];
        this.isPlaying = false;
        this.currentSource = null;
        const bufferThreshold = 2;
    }

    connect() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    pushPCM(arrayBuffer) {
        this.audioQueue.push(arrayBuffer);
        this._playNextAudio();
    }

    /**
     * 将arrayBuffer转为audioBuffer
     */
    _bufferPCMData(pcmData) {
        const sampleRate = this.sampleRate; // 设置为 PCM 数据的采样率
        const length = pcmData.byteLength / 2; // 假设 PCM 数据为 16 位，需除以 2
        const audioBuffer = this.audioContext.createBuffer(1, length, sampleRate);
        const channelData = audioBuffer.getChannelData(0);
        const int16Array = new Int16Array(pcmData); // 将 PCM 数据转换为 Int16Array

        for (let i = 0; i < length; i++) {
            // 将 16 位 PCM 转换为浮点数 (-1.0 到 1.0)
            channelData[i] = int16Array[i] / 32768; // 16 位数据转换范围
        }
        let audioLength = length/sampleRate*1000;
        console.log(`prepare audio: ${length} samples, ${audioLength} ms`)

        return audioBuffer;
    }

    async _playAudio(arrayBuffer) {
        if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }

        const audioBuffer = this._bufferPCMData(arrayBuffer);

        this.currentSource = this.audioContext.createBufferSource();
        this.currentSource.buffer = audioBuffer;
        this.currentSource.connect(this.audioContext.destination);

        this.currentSource.onended = () => {
            console.log('Audio playback ended.');
            this.isPlaying = false;
            this.currentSource = null;
            this._playNextAudio(); // Play the next audio in the queue
        };
        this.currentSource.start();
        this.isPlaying = true;
    }

    _playNextAudio() {
        if (this.audioQueue.length > 0 && !this.isPlaying) {
            // 计算总的字节长度
            const totalLength = this.audioQueue.reduce((acc, buffer) => acc + buffer.byteLength, 0);
            const combinedBuffer = new Uint8Array(totalLength);
            let offset = 0;

            // 将所有 audioQueue 中的 buffer 拼接到一个新的 Uint8Array 中
            for (const buffer of this.audioQueue) {
                combinedBuffer.set(new Uint8Array(buffer), offset);
                offset += buffer.byteLength;
            }

            // 清空 audioQueue，因为我们已经拼接完所有数据
            this.audioQueue = [];
            // 发送拼接的 audio 数据给 playAudio
            this._playAudio(combinedBuffer.buffer);
        }
    }
    stop() {
        if (this.currentSource) {
            this.currentSource.stop(); // 停止当前音频播放
            this.currentSource = null; // 清除音频源引用
            this.isPlaying = false; // 更新播放状态
        }
        this.audioQueue = []; // 清空音频队列
        console.log('Playback stopped and queue cleared.');
    }

}

export default PCMAudioPlayer;