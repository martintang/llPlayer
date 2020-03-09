import os
import sys
import re
import json
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from window import Ui_MainWindow
from maskwidget import MaskWidget
from playerthread import PlayerThread
from chunkthread import ChunkThread


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        self.mask = MaskWidget(self.label)
        self.mask.hide()
        self.player_t = PlayerThread(self)
        self.chunk_t = ChunkThread(self)
        self.slider_allow_update = True
        self.progress = 0
        self.position = 0
        self.config_name = ""
        self.config = {}
        self.show()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.config:
            with open(self.config_name, 'w') as fp:
                self.config['progress'] = self.progress
                json.dump(self.config, fp)
        self.player_t.close()
        self.chunk_t.quit()
        super().closeEvent(a0)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if self.mask.isVisible():
            self.mask.setGeometry(self.label.geometry())
        super().resizeEvent(a0)

    def prev_sentence(self):
        self.player_t.next_prev(False)

    def next_sentence(self):
        self.player_t.next_prev(True)

    def start_pause(self):
        self.player_t.toggle_pause()

    def is_show_mask(self, show_mask):
        if show_mask == 2:
            self.mask.show()
        else:
            self.mask.hide()

    def is_image_stretch(self, stretch):
        if stretch == 2:
            self.player_t.image_stretch(True)
        else:
            self.player_t.image_stretch(False)

    def open_file(self):
        video_name, _ = QFileDialog.getOpenFileName(self,
                                                   "打开视频",
                                                   "",
                                                   " *.mp4;;*.avi;;All Files (*)")
        if video_name is "":
            return
        self.player_t.set_video_name(video_name)
        base_name = re.compile(r'(.+)\..*').findall(video_name)[0]
        self.setWindowTitle(base_name)
        self.config_name = base_name + '.json'
        if os.path.exists(self.config_name) is not True:
            self.chunk_t.set_video_name(video_name)
        else:
            with open(self.config_name, 'r') as fp:
                self.config = json.load(fp)
            self.player_t.set_config(self.config)
            try:
                self.player_t.seek(self.config['progress'])
            except Exception as e:
                pass
            self.prev_btn.setEnabled(True)
            self.next_btn.setEnabled(True)

    def slider_press(self):
        self.slider_allow_update = False

    def move_to(self, position):
        self.position = position

    def start_here(self):
        self.player_t.seek(self.position / 100)
        self.slider_allow_update = True

    def set_status(self, is_pause):
        if is_pause is True:
            self.start_pause_btn.setText("开始")
        else:
            self.start_pause_btn.setText("暂停")

    def set_progress(self, progress):
        if self.slider_allow_update:
            self.progress = progress
            self.progress_slider.setValue(int(100 * progress))

    def set_image(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def set_config(self, config):
        self.player_t.pause()
        if config:
            self.config = config
            with open(self.config_name, 'w') as fp:
                json.dump(self.config, fp)
            self.player_t.set_config(config)
            reply = QMessageBox.question(self, 'Message', '音频解析完成，可以操作上一句，下一句',
                                         QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.prev_btn.setEnabled(True)
                self.next_btn.setEnabled(True)
                self.player_t.toggle_pause()
        else:
            reply = QMessageBox.question(self, 'Message', '音频解析出错，该片不能上一句，下一句',
                                         QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.player_t.toggle_pause()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    sys.exit(app.exec_())
