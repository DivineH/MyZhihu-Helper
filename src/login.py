# -*- coding: utf-8 -*-

import http.cookiejar as cookielib
import os
import re
import sys
import platform
import webbrowser
import json
import urllib.request as urllib2
import time
from src.guide import *
from src.tools.http import Http
from src.tools.match import Match
from src.tools.path import Path
from src.tools.extra_tools import ExtraTools

class Login():
    def __init__(self):
        self.cookieJar = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJar))
        urllib2.install_opener(self.opener)

    def login(self, account, password, captcha=''):
        content = Http.get_content('https://www.zhihu.com/')
        xsrf = Match.xsrf(content)
        if not xsrf:
            print(u'登录失败')
            print(u'敲击回车重新发送登陆请求')
            return False
        xsrf = xsrf.split('=')[1]
        # add xsrf as cookie into cookieJar,
        cookie = Http.make_cookie(name='_xsrf', value=xsrf, domain='www.zhihu.com')
        self.cookieJar.set_cookie(cookie)
        if captcha:
            post_data = {'_xsrf': xsrf, 'email': account, 'password': password, 'remember_me': True,
                         'captcha': captcha}
        else:
            post_data = {'_xsrf': xsrf, 'email': account, 'password': password, 'remember_me': True}

        header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate',  # 主要属性，只要有此项知乎即认为来源非脚本
            'Accept-Language': 'zh,zh-CN;q=0.8,en-GB;q=0.6,en;q=0.4',
            'Host': 'www.zhihu.com',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36(KHTML, like Gecko)Chrome/34.0.1847.116 Safari/537.36',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://www.zhihu.com',
            'Referer': 'https://www.zhihu.com/',
        }
        result = Http.get_content(url=r'https://www.zhihu.com/login/email', data=post_data, extra_header=header)
        if not result:
            print(u'登陆失败，请敲击回车重新登陆')
            return False
        response = json.loads(result.decode('utf-8'))

        if response['r'] == 0:
            print(u'登陆成功！')
            print(u'登陆账号:', account)
            
            cookie = self.get_cookie()
            return True
        else:
            print('')
            print(u'登陆失败')
            print(response['msg'])
            return False

    @staticmethod
    def get_captcha():
        # 知乎此处的r参数为一个13位的unix时间戳
        unix_time_stp = str(int(1000 * time.time()))[0:13]
        content = Http.get_content('https://www.zhihu.com/captcha.gif?r={}&type=login'.format(unix_time_stp))  # 开始拉取验证码
        captcha_path = Path.base_path + u'/验证码.gif'

        image = open(captcha_path, 'wb')
        image.write(content)
        image.close()
        
        print('')
        print(u'请输入您所看到的验证码')
        print(u'验证码位置:')
        print(captcha_path)
        if platform.system() == "Darwin":
            os.system(u'open "{}" &'.format(captcha_path).encode(sys.stdout.encoding))
        else:
            webbrowser.get().open_new_tab(u'file:///' + captcha_path)

        print(u'如果不需要输入验证码可点按回车跳过此步')
        captcha = input()
        return captcha

    def start(self):
        hello_world()
        account, password = set_account()
        captcha = ''
        while not self.login(account, password, captcha):
            print(u'登录失败，可能需要输入验证码')
            print(u'输入『y』按回车更换其他账号')
            print(u'直接敲击回车获取验证码')
            confirm = input()
            if confirm == 'y':
                account, password = set_account()
            captcha = self.get_captcha()
        return

    def get_cookie(self):
        filename = ExtraTools.md5(ExtraTools.get_time())
        with open(filename, 'w') as f:
            pass
        self.cookieJar.save(filename)
        with open(filename) as f:
            content = f.read()
        os.remove(filename)
        return content