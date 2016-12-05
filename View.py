import sys

from PyQt5.QtCore import Qt,QFileInfo,QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QDialog,QInputDialog,QSlider,QFileDialog,QGraphicsDropShadowEffect
from PyQt5.uic import loadUiType

from Model import SongInfo
from Model.Pixel import *
from Model.Player import *
from Model.Playlist import *
from Model.Search import Search
from Model.VkMusic import *

app = QApplication(sys.argv)
app.setApplicationName('PyAmp')
form_class, base_class = loadUiType("Interface.ui")

class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.mpos=QPoint(-1, -1)
        self.setupUi(self)
        self.playlist = Playlist()
        self.player = Player()
        self.player.setPlaylist(self.playlist.playlist)
        self.player.player.positionChanged.connect(self.qmp_positionChanged)
        self.player.player.mediaStatusChanged.connect(self.MediaStatus)
        shadowEffect = QGraphicsDropShadowEffect()
        shadowEffect.setBlurRadius(25)
        shadowEffect.setOffset(5)
        self.setGraphicsEffect(shadowEffect)

    def MediaStatus(self):
        if self.player.mediaStatus() == QMediaPlayer.LoadedMedia:
            qfile_info=QFileInfo(self.playlist.get_urls(self.playlist.current_track()))
            path_to_jpg=Search.findFiles(qfile_info.path(),".jpg")
            if len(path_to_jpg)!=0:
                self.label_5.setPixmap(QPixmap(path_to_jpg[0]))
                rgb=Pixels.pix(path_to_jpg[0])
                string = "rgb(" + str(rgb[0]) + ", " + str(rgb[1]) + ", " + str(rgb[2]) + ")"
                self.widget.setStyleSheet("QWidget#widget { background-color:"+string+";}")
                self.listWidget.setStyleSheet(""" QListWidget::item:selected {
                                        background:"""+string+""" ;}""")
            self.horizontalSlider_2.setRange(0, self.player.getDuration())
            self.listWidget.setCurrentRow(self.playlist.current_track())
            self.label_4.setText('%d:%02d' % (int(self.player.getDuration(60000)), int((self.player.getDuration(1000)) % 60)))

    def show_Dialog(self):
        files = QFileDialog.getOpenFileNames(self, None, '',
                                             'Media file(*.mp4 *.wmv *.avi *.3gp *.oog *.mpeg *.mp2 *.wma *.mp3)'
                                             ';;All files(*.*)')
        if len(files) != 0:
            self.populate_list(files[0])
            self.populate_playlist(files[0])

    def showDialog(self):
        login = QInputDialog.getText(self, 'Input Dialog', 'Enter your login:')
        password = QInputDialog.getText(self, 'Input Dialog', 'Enter your password:')
        vk = vkMusic()
        try:
            vk.loginn(login[0],password[0])
            if len(vk.get_music_list()) != 0:
                self.populate_playlist_from_vk(vk.get_music_list())
        except:
            self.label.setText("Неверный Логин или пароль")

    def check(self):
        if self.listWidget.isVisible() == True:
            self.listWidget.setVisible(False)
            #int x, int y, int width, int height
            self.widget.setGeometry(0, 0, 491, 180)
            self.setGeometry(self.x(), self.y(), 491, 180)
        else:
            self.listWidget.setVisible(True)
            self.widget.setGeometry(0, 0, 491, 641)
            self.setGeometry(self.x(), self.y(), 491, 641)

    def populate_list(self,files):
        for file in files:
            self.listWidget.addItem(SongInfo.SongInfo.get_song_artist(QFileInfo(file).absoluteFilePath()) + SongInfo.SongInfo.get_song_title(QFileInfo(file).absoluteFilePath()))

    def populate_playlist(self, files):
        for file in files:
            self.playlist.set_audio(QUrl(file))

    def populate_playlist_from_vk(self,files):
        for file in files:
            self.listWidget.addItem("*from VK* "+ file.get('artist')+" - "+file.get('title'))
            self.playlist.set_audio(QUrl(file.get('url')))

    def button_click_next(self):
        self.playlist.track_next()
        self.player.play()

    def button_click_prev(self):
        self.playlist.track_previous()
        self.player.play()

    def button_click_play(self):
        self.player.play()

    def button_click_pause(self):
        self.player.pause()

    def list_changed_track(self):
        self.playlist.set_track(self.listWidget.currentRow())
        self.player.play()

    def volume(self,value):
        self.player.setVolume(value)

    def seekPosition(self, position):
        sender = self.sender()
        if isinstance(sender, QSlider):
            self.player.setPosition(position)

    def mouseReleaseEvent(self,event):
        self.mpos = QPoint(-1, -1)

    def mousePressEvent(self, event):
        self.mpos = event.pos()

    def mouseMoveEvent(self, event):
        if (self.mpos.x() >= 0 and event.buttons() and Qt.LeftButton):
            diff =QPoint( event.pos() - self.mpos)
            newpos = QPoint (self.pos() + diff)
            self.move(newpos)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.listWidget.takeItem(self.listWidget.currentRow())
            self.playlist.remove_track(self.listWidget.currentRow())

        if e.key() == Qt.Key_Right:
            self.playlist.track_next()
            print(self.playlist.get_urls())
        if e.key() == Qt.Key_Left:
            self.playlist.track_previous()

    def qmp_positionChanged(self):
        self.label_3.setText('%d:%02d' % (int(self.player.getPosition()/60000), int((self.player.getPosition()/1000) % 60)))
        self.horizontalSlider_2.setValue(self.player.getPosition())

if __name__ == '__main__':
    form = MainWindow()
    form.setWindowTitle('Aimp5.2')
    form.show()
    sys.exit(app.exec_())
