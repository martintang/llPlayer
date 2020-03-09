import os
import re
from PyQt5.QtCore import QThread, pyqtSignal
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


class ChunkThread(QThread):
    config_sig = pyqtSignal(dict)

    def __init__(self, parent):
        super().__init__(parent)
        self.video_name = ""
        self.wav_name = ""
        self.config_sig.connect(parent.set_config)

    def set_video_name(self, video_name):
        pattern = re.compile(r'(.+)\..*')
        self.video_name = video_name
        self.wav_name = pattern.findall(video_name)[0] + '.mp3'
        self.start()

    def run(self):
        try:
            if os.path.exists(self.wav_name) is not True:
                AudioSegment.from_file(self.video_name).export(self.wav_name, format='mp3', bitrate="64k")
            sound = AudioSegment.from_mp3(self.wav_name)
            chunks = detect_nonsilent(sound, min_silence_len=1000, silence_thresh=-45)

            # now recombine the chunks so that the parts are at least 60 sec long
            target_length = 60 * 1000
            output_chunks = [chunks[0]]
            for chunk in chunks[1:]:
                if output_chunks[-1][1] - output_chunks[-1][0] < target_length:
                    output_chunks[-1][1] = chunk[1]
                else:
                    # if the last output chunk is longer than the target length,
                    # we can start a new one
                    output_chunks.append(chunk)

            config = {'duration': sound.duration_seconds, 'total': len(output_chunks), 'chunks': output_chunks}
            self.config_sig.emit(config)
        except Exception as e:
            print(e)
            self.config_sig.emit({})

