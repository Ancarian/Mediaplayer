from mutagen.mp3 import MP3
class SongInfo():
    @staticmethod
    def trying(tag,sSongLocation):
        try:
            info = MP3(sSongLocation).tags[str(tag)].text
            return info[0]
        except:
            return "None"

    @staticmethod
    def get_song_title(sSongLocation):
        return SongInfo.trying("TIT2",sSongLocation)

    @staticmethod
    def get_song_artist(sSongLocation):
        return SongInfo.trying("TPE1", sSongLocation)

