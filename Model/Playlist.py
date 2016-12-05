from PyQt5.QtMultimedia import QMediaPlaylist
from PyQt5.Qt import QMediaContent,QUrl

class Playlist():
    def __init__(self):
        self.__playlist = QMediaPlaylist()

    @property
    def playlist(self):
        return self.__playlist

    @playlist.setter
    def playlist(self,value):
        if isinstance(value,QMediaPlaylist):
            self.__playlist=value

    def set_audio(self,directory):
        try:
            self.__playlist.addMedia(QMediaContent(directory))
        except (TypeError):
            return

    def get_audio(self):
        return self.__playlist.currentMedia()

    def track_next(self):
        if self.__playlist.currentIndex()==self.__playlist.mediaCount():
            self.__playlist.setCurrentIndex(0)
        else:
            self.__playlist.next()

    def track_previous(self):
        if self.__playlist.currentIndex()==self.__playlist.mediaCount():
            self.__playlist.setCurrentIndex(0)
        else:
            self.__playlist.previous()

    def set_track(self,value):
        if self.count()>=value and value>=0:
            self.__playlist.setCurrentIndex(value)

    def current_track(self):
        return self.__playlist.currentIndex()

    def count(self):
        return self.__playlist.mediaCount()

    def get_urls(self,index=-1):
        if index!=-1:
            return self.__playlist.media(index).canonicalUrl().url()
        else:
            urls=[]
            for i in range(self.count()):
                urls.append(self.__playlist.media(i).canonicalUrl().url())
            return urls

    def remove_track(self, value):
        if self.count()!=1:
            self.set_track(value+1)
            self.__playlist.removeMedia(value)
        else:
            self.__playlist.removeMedia(0)

if __name__ == '__main__':
    playlist = Playlist()
    track=QUrl('d:/музыка/Kiss Discography/03.Compilations/1988 - Chikara [1988 Polystar P30R-20008 Japan]/03 - Love Gun.mp3')
    playlist.set_audio(track)
    track = QUrl('d:/музыка/Kiss Discography/03.Compilations/1988 - Chikara [1988 Polystar P30R-20008 Japan]/04 - I Was Made For Lovin You (Long Version).mp3')
    playlist.set_audio(track)
    print(playlist.get_urls())
    print(playlist.get_urls(1))
    playlist.track_next()
    playlist.track_next()
    playlist.track_previous()
    playlist.set_track(1)
    print("current index:"+str(playlist.current_track()))



