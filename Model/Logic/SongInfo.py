from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC

class SongInfo:
    @staticmethod
    def trying(tag, s_song_location):
        try:
            info = MP3(s_song_location).tags[str(tag)].text
            return info[0]
        except:
            return "None"

    @staticmethod
    def tr(song):
        try:
            tags = ID3(song)
        except ID3NoHeaderError:
            print("Adding ID3 header;")
            tags = ID3()
        return tags

    @staticmethod
    def get_song_title(s_song_location):
        st = SongInfo.trying("TIT2", s_song_location)
        return st

    @staticmethod
    def get_song_artist(s_song_location):
        return SongInfo.trying("TPE1", s_song_location)

    @staticmethod
    def get_song_album(s_song_location):
        return SongInfo.trying('TALB', s_song_location)

    @staticmethod
    def set_song_artist(s_song_location, value=''):
        tags = SongInfo.tr(s_song_location)
        tags["TPE1"] = TPE1(encoding=3, text=value)
        tags.save(s_song_location)

    @staticmethod
    def set_song_title(s_song_location, value=''):
        tags = SongInfo.tr(s_song_location)
        tags["TIT2"] = TIT2(encoding=3, text=value)
        tags.save(s_song_location)

    @staticmethod
    def set_song_album(s_song_location, value=''):
        tags = SongInfo.tr(s_song_location)
        tags["TALB"] = TALB(encoding=3, text=value)
        tags.save(s_song_location)