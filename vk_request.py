
import vk_requests
import vk_requests.exceptions
import vk_requests.settings
import shelve
from PyQt5.QtCore import pyqtSignal
import time
class vk_request():
    @staticmethod
    def get_music(user):
        fd = shelve.open("file2.txt")
        fd['color']=[]
        fd.close()
        list_ids=user.messages.getDialogs(count=1).get('items')
        ids=[]
        for id in list_ids:
            id=id.get('message')
            ids.append(id.get('user_id'))

        for id in ids:
            l=0
            strr=''

            Items=user.messages.getHistory(user_id=str(id),count=200)
            while(Items.get('count')>l):
                print(str(Items.get('count'))+"/"+str(l)+"\n")
                for k in Items.get('items'):
                    strr+=(str(k.get('from_id')) + ": " + k.get('body'))+"\n"
                l+=200
                Items = user.messages.getHistory(user_id=str(id), count=200,offset=l)

                time.sleep(0.3)

            print(str(Items.get('count'))+"\n--\n")
            fd = shelve.open("file2.txt")
            fd['color'].append(strr)
            fd.close()
        fd.close()
        print("complete")
