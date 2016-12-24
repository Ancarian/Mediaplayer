from os import listdir

class Search:
    @staticmethod
    def find_files(path='', end_switch=""):
        try:
            files = listdir(path)
        except:
            return []
        list_files = []
        for file in files:
            if file.endswith(end_switch):
                list_files.append(path + "/" + file)
        return list_files
