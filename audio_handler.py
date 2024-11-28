import asyncio
import numpy as np
import wave
from pathlib import Path
from livekit import rtc

class AudioHandler:
    def __init__(self, sample_rate=48000, channels=1):
        self.audio_source = rtc.AudioSource(sample_rate, channels)
        self.audio_track = rtc.LocalAudioTrack.create_audio_track("background_audio", self.audio_source)
        self.audio_task = None
        self.audio_running = asyncio.Event()
        
    async def start_audio(self, wav_path: Path | str, volume: float = 0.3):
        self.audio_running.set()
        self.audio_task = asyncio.create_task(self._play_audio(wav_path, volume))
        
    async def stop_audio(self):
        self.audio_running.clear()
        if self.audio_task:
            await self.audio_task
            self.audio_task = None
            
    async def _play_audio(self, wav_path: Path | str, volume: float):
        samples_per_channel = 9600
        wav_path = Path(wav_path)
        
        while self.audio_running.is_set():
            with wave.open(str(wav_path), 'rb') as wav_file:
                sample_rate = wav_file.getframerate()
                num_channels = wav_file.getnchannels()
                
                audio_data = wav_file.readframes(wav_file.getnframes())
                audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
                
                if num_channels == 2:
                    audio_array = audio_array.reshape(-1, 2).mean(axis=1)
                
                for i in range(0, len(audio_array), samples_per_channel):
                    if not self.audio_running.is_set():
                        break
                    
                    chunk = audio_array[i:i + samples_per_channel]
                    
                    if len(chunk) < samples_per_channel:
                        chunk = np.pad(chunk, (0, samples_per_channel - len(chunk)))
                    
                    chunk = np.tanh(chunk / 32768.0) * 32768.0
                    chunk = np.round(chunk * volume).astype(np.int16)
                    
                    await self.audio_source.capture_frame(rtc.AudioFrame(
                        data=chunk.tobytes(),
                        sample_rate=48000,
                        samples_per_channel=samples_per_channel,
                        num_channels=1
                    ))
                    
                    await asyncio.sleep((samples_per_channel / 48000) * 0.98)
    
    async def publish_track(self, room):
        await room.local_participant.publish_track(
            self.audio_track,
            rtc.TrackPublishOptions(
                source=rtc.TrackSource.SOURCE_MICROPHONE,
                stream="background_audio"
            )
        ) 