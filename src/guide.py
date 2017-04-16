# -*- coding: utf-8 -*-
import re
import msvcrt
from src.tools.sql_manager import SqlManager

def hello_world():
    print(u'')
    print(u'现在开始登陆流程，请输入您的知乎账号和密码')
    print(u'')
    return

def set_account():
    print(u'请输入注册邮箱，或输入回车使用上次保存的账号登录')
    print(u'*****************************************')
    account = input()

    if not account:
        result = SqlManager.exeQuery('select * from config')
        if result:
            data = result.fetchone()
            if data:
                print('使用', data[0], '登录')
                return data[0], data[1]
            print('没有账号保存!')

    while not re.search(r'\w+@[\w\.]{3,}', account):
        print(u'抱歉，输入的账号不规范...\n请输入正确的知乎登录邮箱\n')
        print(u'范例：123456@qq.com\n7264abc@sina.cn')
        print(u'请重新输入账号，回车确认')
        account = input()
    print(u'请输入密码，回车确认')
    password = input()
    while len(password) < 6:
        print(u'密码长度不正确，密码至少6位')
        print(u'请重新输入密码，回车确认')
        password = input()
    return account, password

def input_password():
    password = []
    while True:
        newChar = msvcrt.getch()
        if newChar in b'\r\n':
            break
        elif newChar == b'\b':
            if password:
                del password[-1]
                print('\b \b', end = '', flush = True)
        else:
            password += newChar.decode()
            print('*', end = '', flush = True)
    return ''.join(password)