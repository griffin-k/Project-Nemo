import socket
import struct
import numpy as np
import sounddevice as sd

def stream_tts(text, server_ip="10.0.5.171", server_port=3839, sample_rate=22050):
    text = text.strip()
    if not text:
        return

    text_bytes = text.encode('utf-8')
    header = struct.pack('>I', len(text_bytes))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((server_ip, server_port))
        sock.sendall(header + text_bytes)

        print("[Client] Receiving and playing audio chunks...")

        while True:
            raw_len = sock.recv(8)
            if not raw_len or len(raw_len) < 8:
                break

            chunk_len = struct.unpack('>Q', raw_len)[0]
            if chunk_len == 0:
                print("[Client] Done.")
                break

            audio_buf = bytearray()
            while len(audio_buf) < chunk_len:
                part = sock.recv(min(4096, chunk_len - len(audio_buf)))
                if not part:
                    break
                audio_buf.extend(part)

            audio = np.frombuffer(audio_buf, dtype=np.float32)
            sd.play(audio, samplerate=sample_rate)
            sd.wait()




if __name__ == "__main__":

    stream_tts("Hello, world")
