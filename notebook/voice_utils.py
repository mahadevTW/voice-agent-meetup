import sounddevice as sd
import soundfile as sf


def record_audio(filename="input.wav", duration=5, samplerate=16000):
    print(f"Recording for {duration}s...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
    sd.wait()
    sf.write(filename, audio, samplerate)
    print(f"Saved to {filename}")
    return filename


def play_audio(filename):
    audio, samplerate = sf.read(filename)
    sd.play(audio, samplerate)
    sd.wait()
