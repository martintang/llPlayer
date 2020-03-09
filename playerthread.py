import time
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage
from ffpyplayer.player import MediaPlayer


class PlayerThread(QThread):
    image_sig = pyqtSignal(QtGui.QImage)
    status_sig = pyqtSignal(bool)
    progress_sig = pyqtSignal(float)

    def __init__(self, parent):
        super().__init__(parent)
        self.label = parent.label
        self.image_sig.connect(parent.set_image)
        self.status_sig.connect(parent.set_status)
        self.progress_sig.connect(parent.set_progress)
        self.player = None
        self.duration = None
        self.progress = 0
        self.ratio_mode = Qt.KeepAspectRatio
        self.config = {}

    def set_video_name(self, video_name):
        if self.player is not None:
            self.player.close_player()
        self.player = MediaPlayer(video_name)
        self.status_sig.emit(self.player.get_pause())
        self.start()

    def set_config(self, config):
        self.config = config

    def close(self):
        if self.player is not None:
            self.player.close_player()
        self.quit()

    def pause(self):
        if self.player is not None:
            self.player.set_pause(True)
            self.status_sig.emit(True)

    def toggle_pause(self):
        if self.player is not None:
            self.player.toggle_pause()
            self.status_sig.emit(self.player.get_pause())

    def next_prev(self, is_forward):
        if self.player is not None:
            chunk_position = self.find_chunk(self.progress)
            if is_forward:
                if chunk_position < self.config['total'] - 1:
                    chunk_position += 1
                    self.player.seek(self.config['chunks'][chunk_position][0] / 1000, relative=False, accurate=False)
            else:
                if chunk_position > 0:
                    chunk_position -= 1
                self.player.seek(self.config['chunks'][chunk_position][0] / 1000, relative=False, accurate=False)

    def find_chunk(self, pts):
        if self.config:
            pts_ms = int(1000 * pts)
            front = 0
            rear = self.config['total'] - 1
            chunks = self.config['chunks']
            while front != rear:
                middle = (front + rear) // 2
                if pts_ms > chunks[middle][0]:
                    if pts_ms < chunks[middle + 1][0]:
                        break
                    else:
                        front = middle + 1
                else:
                    rear = middle
            return (front + rear) // 2
        else:
            return 0

    def seek(self, ratio):
        if self.duration is not None:
            pts = ratio * self.duration
            self.player.seek(pts, relative=False, accurate=False)

    def image_stretch(self, is_stretch):
        if is_stretch:
            self.ratio_mode = Qt.IgnoreAspectRatio
        else:
            self.ratio_mode = Qt.KeepAspectRatio

    def run(self):
        val = ''
        while val != 'eof':
            frame, val = self.player.get_frame()
            if self.duration is None:
                self.duration = self.player.get_metadata()['duration']
            if val != 'eof' and frame is not None:
                img, t = frame
                if img is not None:
                    byte = img.to_bytearray()[0]
                    width, height = img.get_size()
                    convert_to_qt_format = QtGui.QImage(byte, width, height, QImage.Format_RGB888)
                    p = convert_to_qt_format.scaled(self.label.width(), self.label.height(), self.ratio_mode)
                    self.image_sig.emit(p)
                    self.progress = t
                    if self.duration is not None:
                        self.progress_sig.emit(t / self.duration)
                    time.sleep(val)
