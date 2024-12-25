#! /usr/bin/env python3
# -*-coding:utf-8 -*-
# @Created on   : "Thursday June 20 2024 19:11:33 GMT+0800 (China Standard Time)"
# @Author       : github.com/zorrow2017
# @File         : ZServer81.py
# @Description  : 还差得远呢，代码完全没时间改，现在能用就行 以后有时间再大改大变样

r"""
ZServer81.py
python3版本地http服务器端
"""


if True:
    import base64
    import datetime
    import hashlib
    import json
    import math
    import os
    import random
    import re
    import shutil
    import sys
    import time
    import urllib
    import pathlib

    # pip install *
    # import requests
    import tornado.ioloop
    import tornado.web


# Configuration file
gs_config = {
    "port": 8081,
    "charset": "utf-8",
    "appname": "zserver81",
    "resource": {
        "base": "C:\\E\\code\\python_jim",
        "chat": "data/fileup/chat.txt",
        "index": "new util/zserver81/View/index.html",
        "fileup": "data/fileup",
    },
    "folderup": None,
}
go_threadScreenshot = None


class ZCL_MainHandler(tornado.web.RequestHandler):
    """
    zserver81
    """

    def get(self):
        self.post()

    def post(self):
        lv_charset = gs_config["charset"]
        lo_req = self.request
        lv_url = lo_req.full_url()
        lv_uri = lo_req.uri.strip()
        lv_reqpath = urllib.parse.unquote(lo_req.path)
        # print(lv_reqpath)
        self.log(lv_url)

        # 具体功能处理：主页、ajax、文件传输、文本传输、兼任GUI界面
        lv_isnull = False
        if self.sub_isHome(lv_reqpath):
            self.sub_home()
        elif lv_reqpath == "/ajax/getTime":
            lo_time = time.localtime()
        elif lv_reqpath == "/ajax/doACK":
            lv_request = lo_req.body
            self.write(lv_request)
        elif lv_reqpath == "/ajax/getSAP":
            lv_str = "尚未实现"  # java jco能连，py、js似乎不行
        elif lv_reqpath == "/ajax/getHash":
            self.doHash(lo_req)
        elif lv_reqpath == "/ajax/doEnc":
            self.doEnc(lo_req)
        elif lv_reqpath == "/ajax/doDec":
            self.doDec(lo_req)
        elif lv_reqpath == "/filedown":
            lv_filename = lo_req.query_arguments["file"][0].decode("utf-8")
            self.log(lv_filename)
            self.doFiledown(lv_filename)
        elif lv_reqpath == "/fileup":
            self.doFileup(lo_req)
        elif lv_reqpath == "/chat":
            self.doChat(lo_req)
        elif lv_reqpath.lower().startswith("/new util/zserver81"):
            self.doResource(lv_reqpath)
        # elif lv_reqpath.startswith("/gui"):
        elif lv_reqpath == "/gui/openScreenshot":
            self.doScreenshot(lo_req)
        elif lv_reqpath == "/gui/getKeyUse":
            self.doKeyUse()
        else:
            lv_isnull = True

        # 原样返回
        if lv_isnull == True:
            ev_response = 'url=<br><a href=".">%s</a><br>uri=%s' % (lv_url, lv_uri)
            self.write(ev_response.encode(lv_charset))

        # 不限制权限
        self.add_header("Access-Control-Allow-Origin", "*")  # //允许所有来源访问
        self.add_header("Access-Control-Allow-Method", "POST,GET,OPTIONS")  # //允许访问的方式
        self.add_header("Access-Control-Allow-Headers", "*")  #

    def options(self):
        """
        OPTIONS 是与GET、POST、PUT平起平坐的http常见方法之一
        options 的作用是允许其他网站的js ajax访问本网站的后台服务，这没什么，因为ajax、requests、postman、浏览器都是一个道理
        """
        self.add_header("Access-Control-Allow-Origin", "*")  # //允许所有来源访问
        self.add_header("Access-Control-Allow-Method", "POST,GET,OPTIONS")  # //允许访问的方式
        self.add_header("Access-Control-Allow-Headers", "*")  #
        self.set_status(200)

    def sub_isHome(self, iv_reqpath):
        lv_reqpath = iv_reqpath
        if (
            lv_reqpath == "/"
            or lv_reqpath == None
            or re.match("^\\s*$", lv_reqpath, re.IGNORECASE)
            or re.match(
                "^/index\\.?((html)|(htm)|(asp)|(aspx)|(jsp)|(php)|(io))?$",
                lv_reqpath,
                re.IGNORECASE,
            )
            or re.match(
                "^/main\\.?((html)|(htm)|(asp)|(aspx)|(jsp)|(php)|(do))?$",
                lv_reqpath,
                re.IGNORECASE,
            )
            or re.match(
                "^/home\\.?((html)|(htm)|(asp)|(aspx)|(jsp)|(php)|(do))?$",
                lv_reqpath,
                re.IGNORECASE,
            )
            or re.match(
                "^/launchpad\\.?((html)|(htm)|(asp)|(aspx)|(jsp)|(php)|(do))?$",
                lv_reqpath,
                re.IGNORECASE,
            )
        ):
            return True

    def sub_home(self):
        """
        是主页则返回主页
        home page, main page, index, index.html, launchpad
        """
        lv_url = self.request.full_url()
        lv_data = self.getPageIndex()
        self.write(lv_data)

    def log(self, iv_value, iv_key=""):
        lv_logfile = ""
        print(iv_value)

    def doFiledown(self, filename):
        """
        局域网文件下载
        """
        lv_folder = gs_config["folderup"]
        filepath = os.path.join(lv_folder, filename)
        #
        self.set_status(200)
        self.set_header(
            "Content-Disposition", "attachment; filename=" + urllib.parse.quote(filename)
        )
        self.set_header("content-type", "application/octet-stream")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.set_header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS")
        # TODO 中断继续功能
        lv_blockSize = 8 * 1000 * 1000  # 8MB
        with open(filepath, "rb") as fis:
            while True:
                lv_block = fis.read(lv_blockSize)
                if len(lv_block) <= 0:
                    break
                self.write(lv_block)

    def doFileup(self, io_req):
        """
        局域网文件上传
        """
        lv_str = ""
        lv_folder = gs_config["folderup"]
        #
        lo_file = io_req.files["fileup"][0]
        lv_filename = lo_file["filename"]
        lv_data = lo_file["body"]
        #
        lv_path = os.path.join(lv_folder, lv_filename)
        with open(lv_path, "wb") as fos:
            lv_int = fos.write(lv_data)
        #
        self.set_status(200)
        self.set_header("content-type", "text/html;charset=utf-8")
        lv_board = (
            "<div id=\"path\">/"
            + lv_filename
            + "</div><br/><br/><a href=\"/index.html\">backward</a><br/>"
        )
        self.write(lv_board)

    def doChat(self, io_req):
        """
        局域网文本发送刷新清空
        """
        es_data = {"allString": []}
        lt_reqString = []
        lv_operate = ""
        if io_req != None:
            lv_req = io_req.body.decode(gs_config["charset"])
            lo_json = json.loads(lv_req)
            lv_reqString = lo_json["reqString"]
            lv_operate = lo_json["operate"]
            if lv_reqString != None and len(lv_reqString) > 0:
                lt_reqString.append(lv_reqString)

        lv_chatFile = os.path.join(gs_config["resource"]["base"], gs_config["resource"]["chat"])
        if lv_operate == "clear" or os.path.exists(lv_chatFile) == False:
            with open(lv_chatFile, "wb") as fos:
                lv_return = fos.write(b"")
        if lv_operate == "chat":
            with open(lv_chatFile, "ab") as fos:
                for lv_reqString in lt_reqString:
                    lv_return = fos.write(lv_reqString.encode(gs_config["charset"]))
        if True or lv_operate == "refresh":
            with open(lv_chatFile, "rb") as fis:
                lv_str = fis.read().decode(gs_config["charset"])
                lt_board = lv_str.split("\n")

        es_data["allString"] = lt_board
        #
        self.set_status(200)
        self.set_header("content-type", "application/json")
        lv_board = json.dumps(es_data, ensure_ascii=False)
        self.write(lv_board)

    def doHash(self, io_req):
        """
        取文件的hash值
        """
        ev_data = ""
        ls_req = {}
        if io_req != None:
            lv_req = io_req.body.decode(gs_config["charset"])
            ls_req = json.loads(lv_req)

        lv_file = ls_req["iv_file"]
        lv_hash = ls_req["iv_hash"]
        if os.path.isfile(lv_file) == False:
            self.set_status(500)
            self.write(f"\"{lv_file}\" 这个文件路径在服务器电脑中不存在")
            return
        #
        lo_hash = hashlib.new(lv_hash)
        with open(lv_file, "rb") as fis:
            while True:
                lv_byte = fis.read(1024 * 1024 * 100)
                if len(lv_byte) == 0:
                    break
                lo_hash.update(lv_byte)
        lv_result = lo_hash.hexdigest()
        ev_data = lv_result.lower() + "\n" + lv_result.upper()

        #
        self.set_status(200)
        self.write(ev_data)

    def doEnc(self, io_req):
        """
        加密
        """
        try:
            import cryptography
            import cryptography.fernet
        except Exception as ex:
            self.set_status(500)
            self.write("失败，此功能必须安装依赖包：pip install cryptography")
            return

        ev_data = ""
        ls_req = {}
        if io_req != None:
            lv_req = io_req.body.decode(gs_config["charset"])
            ls_req = json.loads(lv_req)

        lv_key = ls_req["iv_key"]
        lv_data = ls_req["iv_data"]
        lv_keyPad = self.sub_pad(lv_key.encode("utf-8"), 32)
        lo_enc = cryptography.fernet.Fernet(lv_keyPad)

        ev_data = lo_enc.encrypt(lv_data.encode("utf-8"))

        #
        self.set_status(200)
        self.write(ev_data)

    def doDec(self, io_req):
        """
        解密
        """
        try:
            import cryptography
            import cryptography.fernet
        except Exception as ex:
            self.set_status(500)
            self.write("失败，此功能必须安装依赖包：pip install cryptography")
            return

        ev_data = ""
        ls_req = {}
        if io_req != None:
            lv_req = io_req.body.decode(gs_config["charset"])
            ls_req = json.loads(lv_req)

        lv_key = ls_req["iv_key"]
        lv_data = ls_req["iv_data"]
        lv_keyPad = self.sub_pad(lv_key.encode("utf-8"), 32)
        lo_enc = cryptography.fernet.Fernet(lv_keyPad)

        try:
            ev_data = lo_enc.decrypt(lv_data)
        except Exception as ex:
            self.set_status(500)
            self.write("解密报错：" + str(ex))
            return

        #
        self.set_status(200)
        self.write(ev_data)

    def doResource(self, iv_path):
        """
        服务器文件获取 (比如ico、js、css文件)
        """
        lv_path = iv_path.lstrip("/")
        lv_ico = os.path.join(gs_config["resource"]["base"], lv_path)
        with open(lv_ico, "rb") as fis:
            self.write(fis.read())

    def doGUI(self, iv_path):
        """
        本机python3代码的图形界面
        """
        a = 0

    def doScreenshot(self, io_req):
        """
        本机监听截图功能
        """
        import threading
        import zprintScreen

        lo_json = {}
        if io_req != None:
            lv_req = io_req.body.decode(gs_config["charset"])
            lo_json = json.loads(lv_req)

        try:
            global go_threadScreenshot
            if lo_json["iv_isRun"] == True:
                if go_threadScreenshot == None:
                    # 执行监听
                    go_threadScreenshot = zprintScreen.main()
                es_return = {"type": "S", "message": "已成功开启截屏截图快捷键监听服务zprintScreen"}
            else:
                if go_threadScreenshot != None:
                    go_threadScreenshot.stop()
                    go_threadScreenshot = None
                es_return = {"type": "S", "message": "已关闭zprintScreen"}
        except Exception as ex:
            lv_msg = str(ex)
            self.log(lv_msg)
            es_return = {"type": "E", "message": lv_msg}

        lv_str = json.dumps(es_return, ensure_ascii=False)
        self.write(lv_str)

    def doKeyUse(self):
        """
        基于本机监听截图功能，统计键盘频率
        """
        import zprintScreen

        lv_logKeyboard = os.path.join(zprintScreen.gv_baseScreenshotFolder, "log/a.txt")
        lv_str = zprintScreen.sub_clickSum(iv_isall=True, iv_file=lv_logKeyboard)
        self.write(lv_str)

    def getPageIndex(self):
        # 网页首页
        lv_html = ""
        with open(
            os.path.join(gs_config["resource"]["base"], gs_config["resource"]["index"]), "rb"
        ) as fis:
            lv_html = fis.read().decode(gs_config["charset"])

        # 替换文件列表
        ol = "<ol class=\"fileup_main_ol\"></ol>"
        res = "<ol class=\"fileup_main_ol\">\n"

        ls_len = 0
        ls = []
        # // fs.readdirSync()
        ls_name = []
        lt_file = []
        ls_file = {}
        # 获取gc_fdir文件夹下面第一层的文件和子文件夹；文件夹树形结构还没有；
        lv_folder = gs_config["folderup"]
        for filename in os.listdir(lv_folder):
            filepath = os.path.join(lv_folder, filename)
            lo_stat = os.stat(filepath)
            if os.path.isfile(filepath):
                lv_timestr = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(lo_stat.st_mtime))
                ls_file = {
                    "name": filename,
                    "full": filepath,
                    "size": self.convertSize(lo_stat.st_size),
                    "mtime": lv_timestr,
                    "isFile": True,
                    "stat": lo_stat,
                }
                lt_file.append(ls_file)
                ls_name.append(filename)
                ls.append(
                    " --%s  --%s" % (self.convertSize(lo_stat.st_size), lv_timestr)
                )  # //--${filename}
            else:
                ls_file = {
                    "name": filename,
                    "full": filepath,
                    "size": self.convertSize(lo_stat.st_size),
                    "mtime": lv_timestr,
                    "isFile": False,
                    "stat": lo_stat,
                }
                lt_file.append(ls_file)
                ls_name.append(filename)
                ls.append(filename + "  --is folder")

        lt_sortRule = [{"field": "isFile", "desc": True}, {"field": "mtime", "desc": True}]
        # lt_file = lt_file.sort(sub_sort(lt_sortRule));
        lt_file.sort(key=lambda x: x["stat"].st_mtime, reverse=True)
        for ls_file in lt_file:
            item = " --%s  --%s" % (ls_file["size"], ls_file["mtime"])
            if ls_file["isFile"] == False:
                item += "  --is folder"
            filename = ls_file["name"]
            res += '<li><a href="/filedown?file=%s">%s</a> %s</li>\n' % (
                urllib.parse.quote(filename),
                filename,
                item,
            )
        res += "</ol>"

        # 直接替换
        lv_html2 = lv_html.replace(ol, res)
        return lv_html2

    def sub_pad(self, iv_byte, iv_len):
        ev_result = iv_byte[0:iv_len]
        if len(ev_result) < iv_len:
            ev_result = ev_result + b"\0" * (iv_len - len(ev_result))
        ev_result = base64.b64encode(ev_result)
        return ev_result

    @staticmethod
    def convertSize(fileSize):
        if math.isnan(fileSize):
            return "0.0B"
        unit = ["B", "KB", "MB", "GB", "TB"]
        es = ""
        # //Number.MAX_SAFE_INTEGER=9 007 199 254 740 991;
        val = int(fileSize)
        if val <= 0:
            res = "0B"
        else:
            jie = 0
            while val >= 1000:
                jie += 1
                val = val / 1024
            if val <= 10:
                res = "%.2f" % val + unit[jie]
            else:
                res = "%.1f" % val + unit[jie]
        return res


def sub_getIP():
    """
    py 获取本机的IP地址
    """
    try:
        import scapy
        import scapy.all

        ev_ip = "127.0.0.1"
        for i in scapy.all.conf.ifaces.items():
            # ip of all Network Adapter
            lv_adapterName = str(i[1].name)
            lv_ip = scapy.all.get_if_addr(lv_adapterName)

            if lv_ip == "0.0.0.0":
                continue
            if scapy.all.conf.iface == i[1]:
                ev_ip = lv_ip
        return ev_ip
    except:
        # lv_ip = socket.gethostbyname(socket.gethostname())
        return "127.0.0.1"


def sub_isPortUsed(iv_port):
    """
    py 检查端口是否被占用
    """
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lo_socket:
        return lo_socket.connect_ex(("127.0.0.1", iv_port)) == 0


def main(args=None):
    """
    @description Main
    @param iv_file input file absolute path
    """
    print(__doc__)
    print("<begin> time: " + time.ctime())
    ############
    iv_file = ""
    print("如果命令行界面卡住了，请右击(刷新)")

    # 配置文件
    lv_port = gs_config["port"]
    if args != None and len(args) > 0:
        gs_config["resource"]["base"] = args
    gs_config["folderup"] = os.path.abspath(
        os.path.join(gs_config["resource"]["base"], gs_config["resource"]["fileup"])
    )

    # 顺便显示一下url
    if sub_isPortUsed(lv_port):
        # 请关闭占用端口的某程序、或改源代码改成8082、8083端口
        print(f"错误：{lv_port}端口已被占用；")
    lv_ip = sub_getIP()
    lv_lanurl = "http://%s:%s" % (lv_ip, str(lv_port))
    # print(lv_lanurl)
    print(gs_config["folderup"])

    # 真正启动服务器
    lo_webapp = tornado.web.Application([("/.*", ZCL_MainHandler)])
    lo_server = tornado.web.HTTPServer(
        lo_webapp, max_buffer_size=1024 * 1024 * 1000, max_body_size=1024 * 1024 * 1000
    )
    lo_server.listen(lv_port)

    print("一切正常，现在打开浏览器访问 %s" % lv_lanurl)
    os.system(f"start {lv_lanurl}")  # 用电脑默认浏览器访问本网站的主页

    tornado.ioloop.IOLoop.instance().start()  # wait PAI I/O loop

    ############
    print("<end> time: " + time.ctime())


# 主程序入口
if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        lv_msg = str(ex)
        print(lv_msg)

    input("ENTER to exit...")
