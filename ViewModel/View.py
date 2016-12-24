import sys

from Model.Logic.Pixel import *
from Model.Entity.Player import *
from Model.Logic.Search import Search
from Model.Entity.SqlBase import SqlBase
from Model.Logic.StringRedactor import *
from Model.Entity.VkMusic import *
from Model.Logic.SongInfo import SongInfo
from PyQt5.QtCore import Qt, QFileInfo, QPoint
from PyQt5.QtWidgets import QApplication, QDialog, QInputDialog, QSlider, QFileDialog, QGraphicsDropShadowEffect, \
    QTableWidgetItem
from PyQt5.uic import loadUiType

from Model.Entity.Playlist import *

app = QApplication(sys.argv)
app.setApplicationName('PyAmp')
form_class, base_class = loadUiType('D:/CourseWork/PyAmp/View/Interface.ui')


class MainWindow(QDialog, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.base = SqlBase("muss.db")
        self.base.set_table("musiccc")
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.mpos = QPoint(-1, -1)
        self.setupUi(self)
        self.playlist = Playlist()
        self.player = Player()
        self.player.set_playlist(self.playlist.playlist)
        self.player.player.positionChanged.connect(self.qmp_position_changed)
        self.player.player.mediaStatusChanged.connect(self.media_status)
        shadowEffect = QGraphicsDropShadowEffect()
        shadowEffect.setBlurRadius(10)
        shadowEffect.setOffset(3)
        self.setGraphicsEffect(shadowEffect)
        self.flag = 1
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['artist', 'title', 'album', 'like'])

    def get_playlist_with_likes(self):

        arr = self.base.get_columns("musiccc", "like", "+1")
        urls = []
        for url in arr:
            urls.append(url[0])
        self.delete_all_tracks()
        self.populate_playlist(urls)
        self.populate_list(urls)

    def delete_all_tracks(self):
        for i in range(self.playlist.count()):
            self.listWidget.takeItem(self.listWidget.currentRow())
            self.playlist.remove_track(self.listWidget.currentRow())

    def media_status(self):
        if self.player.media_status() == QMediaPlayer.LoadedMedia:

            url = self.playlist.get_urls(self.playlist.current_track())

            artist = SongInfo.get_song_artist(
                self.playlist.get_urls(self.playlist.current_track()))
            title = SongInfo.get_song_title(
                self.playlist.get_urls(self.playlist.current_track()))

            album = SongInfo.get_song_album(
                self.playlist.get_urls(self.playlist.current_track()))
            self.label.setText(artist + " " + title)
            self.base.set_cell("musiccc", url, artist, title, album, "0")

            arr = self.base.get_columns('musiccc')
            self.tableWidget.setRowCount(len(arr))
            self.flag = 0
            arr.reverse()
            for i in range(len(arr)):
                self.tableWidget.setItem(i, 0, QTableWidgetItem(arr[i][1]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(arr[i][2]))
                self.tableWidget.setItem(i, 2, QTableWidgetItem(arr[i][3]))
                self.tableWidget.setItem(i, 3, QTableWidgetItem(arr[i][4]))
            self.listWidget.setCurrentRow(self.playlist.current_track())
            self.flag = 1
            qfile_info = QFileInfo(url)
            path_to_jpg = Search.find_files(qfile_info.path(), ".jpg")
            if len(path_to_jpg) != 0:
                pix = Pixels.resize(path_to_jpg[0], 140)
                self.label_5.setPixmap(pix)
                rgb = Pixels.pix(path_to_jpg[0])
                string = "rgb(" + str(rgb[0]) + ", " + str(rgb[1]) + ", " + str(rgb[2]) + ")"
                self.widget.setStyleSheet("QWidget#widget { background-color:" + string + ";}")
                self.listWidget.setStyleSheet("""
                     QListWidget::item:hover,QListWidget::item:selected:active,QListWidget::item:selected:!active,QListWidget::item:alternate, QListWidget::item:selected,QListWidget::item:selected,QScrollBar::sub-line:vertical,QScrollBar::add-line:vertical,QScrollBar::handle:vertical,QScrollBar:vertical,QScrollBar::sub-line:horizontal,QScrollBar::sub-line:horizontal,QScrollBar::add-line:horizontal ,QScrollBar:horizontal,QScrollBar::handle:horizontal,  QScrollBar::add-line:horizontal, QScrollBar::add-line:horizontal {
     background: %s;
 }""" % (string))

            self.horizontalSlider_2.setRange(0, self.player.get_duration())
            self.label_4.setText(
                '%d:%02d' % (int(self.player.get_duration(60000)), int((self.player.get_duration(1000)) % 60)))

    def show_table(self):
        if self.tableWidget.isVisible():
            self.flag = 0
            self.tableWidget.setVisible(False)
            # self.widget.setStyleSheet("QWidget#widget{border-color:rgb(26, 100, 127);}")
        else:
            self.tableWidget.setVisible(True)
            # self.widget.setStyleSheet("QWidget#widget{border-color:#ff4f52;}")
            self.flag = 1

    def show_dialog(self):
        files = QFileDialog.getOpenFileNames(self, None, '',
                                             'Media file(*.mp4 *.wmv *.avi *.3gp *.oog *.mpeg *.mp2 *.wma *.mp3)'
                                             ';;All files(*.*)')
        if len(files) != 0:
            self.populate_list(files[0])
            self.populate_playlist(files[0])

    def show_dialog_vk(self):
        vk_login = QInputDialog.getText(self, 'Input Dialog', 'Enter your login:')
        vk_password = QInputDialog.getText(self, 'Input Dialog', 'Enter your password:')
        vk = VkMusic()
        try:
            vk.login(vk_login[0], vk_password[0])
            if len(vk.get_music_list()) != 0:
                self.populate_playlist_from_vk(vk.get_music_list())
        except:
            self.label.setText("Неверный Логин или пароль")

    def check(self):
        if self.listWidget.isVisible():
            self.listWidget.setVisible(False)
            self.widget.setGeometry(0, 0, 491, 180)
            self.setGeometry(self.x(), self.y(), 491, 160)
        else:
            self.listWidget.setVisible(True)
            self.widget.setGeometry(0, 0, 491, 641)
            self.setGeometry(self.x(), self.y(), 491, 631)

    def populate_list(self, files):
        for file in files:
            artist = SongInfo.get_song_artist(QFileInfo(file).absoluteFilePath())
            album = SongInfo.get_song_album(QFileInfo(file).absoluteFilePath())
            title = SongInfo.get_song_title(QFileInfo(file).absoluteFilePath())
            self.listWidget.addItem(StringRedactor.to_concatenate(artist, "...", 20) + "\t" +
                                    StringRedactor.to_concatenate(album, "...", 20) + "\t" +
                                    StringRedactor.to_concatenate(title, "...", 20))

    def populate_playlist(self, files):
        for file in files:
            self.playlist.set_audio(QUrl(file))

    def populate_playlist_from_vk(self, files):
        for file in files:
            self.listWidget.addItem("*from VK* " + file.get('artist') + " - " + file.get('title'))
            self.playlist.set_audio(QUrl(file.get('url')))

    def button_click_next(self):
        self.playlist.track_next()

    def button_click_prev(self):
        self.playlist.track_previous()

    def button_click_play(self):
        self.player.play()

    def button_click_pause(self):
        self.player.pause()

    def list_changed_track(self):

        self.playlist.set_track(self.listWidget.currentRow())
        self.player.play()

    def volume(self, value):
        self.player.set_volume(value)

    def seek_position(self, position):
        sender = self.sender()
        if isinstance(sender, QSlider):
            self.player.set_position(position)

    def change_tag(self, x, y):
        if self.flag == 1:
            self.flag = 0
            pos_x = x
            pos_y = y
            value = self.tableWidget.item(x, y).text()
            arr = self.base.get_columns("musiccc", "ROWID", self.tableWidget.rowCount() - pos_x)

            if pos_y == 0:
                row = 'artist'
                SongInfo.set_song_artist(arr[0][0], value)
            elif pos_y == 1:
                row = 'title'
                SongInfo.set_song_title(arr[0][0], value)
            elif pos_y == 2:
                row = 'album'
                SongInfo.set_song_album(arr[0][0], value)
            elif pos_y == 3:
                row = 'like'

                try:
                    if int(value) > 0:
                        value = "+1"
                    elif int(value) < 0:
                        value = "-1"
                    else:
                        value = "0"

                    self.tableWidget.setItem(x, y, QTableWidgetItem(value))
                except:
                    self.tableWidget.setItem(x, y, QTableWidgetItem("0"))
                    value = 0

            self.base.update_cell( 'musiccc', row, value, 'id', arr[0][0])
            self.flag = 1

    def mouseReleaseEvent(self, event):
        self.mpos = QPoint(-1, -1)

    def mousePressEvent(self, event):
        self.mpos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mpos.x() >= 0 and event.buttons() and Qt.LeftButton:
            diff = QPoint(event.pos() - self.mpos)
            newpos = QPoint(self.pos() + diff)
            self.move(newpos)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Delete:
            self.listWidget.takeItem(self.listWidget.currentRow())
            self.playlist.remove_track(self.listWidget.currentRow())

        if e.key() == Qt.Key_Right:
            title = SongInfo.get_song_title(
                self.playlist.get_urls(self.playlist.current_track()))
            self.base.update_cell( 'musiccc', 'like', '+1', 'title', title)

        if e.key() == Qt.Key_Left:
            title = SongInfo.get_song_title(
                self.playlist.get_urls(self.playlist.current_track()))
            self.base.update_cell('musiccc', 'like', '-1', 'title', title)

    def qmp_position_changed(self):
        self.label_3.setText(
            '%d:%02d' % (int(self.player.get_position() / 60000), int((self.player.get_position() / 1000) % 60)))
        self.horizontalSlider_2.setValue(self.player.get_position())


if __name__ == '__main__':
    form = MainWindow()
    form.setWindowTitle('Aimp5.2')
    form.show()
    sys.exit(app.exec_())
