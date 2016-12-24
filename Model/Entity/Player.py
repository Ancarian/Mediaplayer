from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist


class Player():
    def __init__(self):
        self.__player = QMediaPlayer()
        self.__player.setVolume(50)

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, value):
        if isinstance(value, QMediaPlayer):
            self.__player = value

    def set_playlist(self, playlist):
        if isinstance(playlist, QMediaPlaylist):
            self.__player.setPlaylist(playlist)

    def set_volume(self, value):
        if isinstance(value, int):
            self.__player.setVolume(value)
        else:
            self.__player.setVolume(50)

    def pause(self):
        if self.__player.state() == QMediaPlayer.PausedState:
            self.__player.play()
        else:
            self.__player.pause()

    def play(self):
        if self.__player.state() == QMediaPlayer.PlayingState:
            self.__player.setPosition(0)
        else:
            self.__player.play()

    def media_status(self):
        return self.__player.mediaStatus()

    def set_position(self,value):
        if isinstance(value, int) and self.__player.duration() > value > 0:
            self.__player.setPosition(value)

    def get_duration(self, factor=1):
        if isinstance(factor, int):
            return self.__player.duration()/factor
        else:
            return 0

    def get_position(self, factor=1):
        if isinstance(factor, int):
            return self.__player.position()/factor


if __name__ == '__main__':
    player = Player()
    playlist = QMediaPlaylist()
    player.set_playlist(playlist)
    player.play()
    player.pause()
    print(player.get_duration())
