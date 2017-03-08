import vk_requests.exceptions
import vk_requests.settings



class VkMusic():
    def __init__(self):
        self.__token=5665850

    def login(self,login,password):
        try:
            self.user=vk_requests.create_api(app_id=self.__token, login=str(login), password=str(password), scope=5000)
        except vk_requests.exceptions.VkAuthError:
            return vk_requests.exceptions.VkAuthError

    def get_music_list(self):
        try:
            music_list=self.user.audio.get(user_ids=160549169)
            return music_list.get('items')
        except :
            return AttributeError

if __name__ == '__main__':
    vk = VkMusic()
    login=str(input("login\n"))
    password=str(input("password\n"))
    vk.login(login,password)
    print(vk.get_music_list())