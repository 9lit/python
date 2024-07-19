import os
import subprocess
from webdav4.client import Client
from datetime import datetime
import json
"""
遍历 webdav 服务器, 展示并选择视频列表, 并使用 mpv 进行播放视频
"""

year = str(datetime.today().year)

def cache(mode:str, *args):

    _file = ".playerdav.json"

    def read():
        try: 
            with open(_file, 'r', encoding='utf-8') as f: 
                cache_dict = json.load(f)
                if isinstance(cache_dict, dict): return cache_dict
                else: False
        except FileNotFoundError: return False

    def wirte(content):
        with open(_file, 'w', encoding='utf-8') as f: json.dump(content, f, ensure_ascii=False)

    
    def read_cache():
        cache_dict = read()
        try:
            return cache_dict[args[0]]
        except:
            return False
    
    def del_datetime(value):
        try: 
            for index in range(len(value)): del value[index]['modified']; del value[index]['created']
        except: pass

        return value
    
    def wirte_cache():
        content = read()
        key, value = args; del_datetime(value)
        
        if content : content[key] = value
        else: content = {key:value}
        
        wirte(content)

    
    def del_cache():
        if args: cache_dict = read(); del cache_dict[args[0]]; wirte(cache_dict)
        else: os.remove(_file)
            
        print("缓存已删除")

    match mode:
        case 'r': return read_cache()
        case 'w': wirte_cache()
        case 'd': del_cache()

def ls_dir(path:str):
    def exclude_file(dir):
        # 排除非视频文件和非目录文件
        def main(file):
            if file['type'] != 'directory':
                if 'video' not in file['content_type']: return False
            return True
        
        return [d for d in dir if main(d)]

    def get_dir(cache_dir):
        def auto_enter(dir):
            # 如果列表长度只有 1, 且类型为目录, 则直接进行下一层级
            if len(dir) == 1 and dir[0]['type'] == "directory": dir = client.ls(dir[0]['name'])
            return exclude_file(dir)
        
        if cache_dir: return cache_dir

        dir = exclude_file(client.ls(path)); dir = auto_enter(dir)
        cache('w', path, dir)
        return dir
    
    
    def printf() -> tuple:
        def crumbs():
            # 面包屑
            if path == root: print("Home")
            else: print(path.split('/')[2:4])
        
        def mark(index, file:str) -> None:
            # 标记年份为今年的番剧, 第一季为今年的
            try:
                file_name, file_year = file.split('.')
                context = printf_color(file) if mark_this_year(file_year) or mark_whitelist(file_name) else file
            except:
                context = file
            print(index, context)

        def mark_this_year(file_year:str) -> bool:
            return True if file_year == year else False

        def mark_whitelist(file_name:str) -> bool:
            whitelist = ['物语系列']
            return True if file_name in whitelist else False
        
        def printf_color(file:str) -> str:
            return  f"\033[0;31;40m{file}\033[0m"

        
        for index, d in enumerate(dir): mark(index, d['display_name'])

        crumbs()
     
    dir =  get_dir(cache('r', path)); printf()
    return dir, path

def open_file(dir:str, old_path:str, value:str):

    def open_video(path, href):

        def get_url(href):
            return url.replace("/dav", "/d/video") + href.replace("/dav", "")
        
        def get_sub(path, href):
            def replace_ext(path): return os.path.splitext(path)[0] + e
            ext = ['.ass', '.chs.ass', '.cht.ass']
            for e in ext: 
                sub_path = replace_ext(path); sub_href = get_url(replace_ext(href))
                if client.exists(sub_path): return sub_href
            return False
        
        def main():

            sub_href = get_sub(path, href); video_href = get_url(href)

            if sub_href: command = f"{video_href} --sub-file={sub_href}"
            else: command = video_href
            
            print(f"mpv.exe {command}")
            subprocess.Popen(f"mpv.exe {command}", shell=True)

        main()

    def open_dir():
        def number_to_path(number:int):
            file = dir[number]; new_path = file['name']; type = file['type']; href = file['href']
            if type == 'file': open_video(new_path, href); return old_path
            else: return new_path

        if value.isdigit():
            number = int(value); path = number_to_path(number)
            return ls_dir(path)

    
    return open_dir()

def main():
        

    def __return(path):
        try: path = "/".join(path.split("/")[:-1])
        except UnboundLocalError: path = root
        
        return ls_dir(path)
    
    def home(): return ls_dir(root)
    
    def clean_cache(is_all=False): cache('d') if is_all else cache('d', path)

    def ls(path): return ls_dir(path)
    
    dir, path = ls_dir(root)
    
    while True:
        value = input("请输入命令: ")

        __new_value = open_file(dir, path, value)
        if __new_value: dir, path = __new_value; continue
        match value:
            case 'q': return
            case '/': dir, path = home()
            case 'r': dir, path = __return(path)
            case 'd': clean_cache()
            case 'ls': dir, path = ls(path)
            case 'delete all': clean_cache(is_all=True)

if __name__ == "__main__":

    # webdav 服务地址
    url = "https://your_url/dav"; root = '/'
    username = "user"; password = "passwd"
    client = Client(url, auth=(username, password))
    
    try: main()
    except KeyboardInterrupt: print("退出程序.")
