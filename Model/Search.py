from os import listdir

class Search():
    @staticmethod
    def findFiles(path='',endswitch=""):
        try:
            files = listdir(path)
        except:
            return []
        list_files = []
        for file in files:
            if file.endswith(endswitch):
                list_files.append(path + "/" + file)
        return list_files
