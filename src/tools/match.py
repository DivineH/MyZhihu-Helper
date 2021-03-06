# -*- coding: utf-8 -*-
import re


class Match(object):
    @staticmethod
    def xsrf(content=''):
        xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', content.decode())
        if xsrf:
            return '_xsrf=' + xsrf.group(0)
        return ''

    @staticmethod
    def html_body(content=''):
        return re.search('(?<=<body>).*(?=</body>)', content, re.S).group(0)

    @staticmethod
    def fix_html(content=''):
        content = content.replace('</br>', '').replace('</img>', '')
        content = content.replace('<br>', '<br/>')
        content = content.replace('href="//link.zhihu.com', 'href="https://link.zhihu.com')  # 修复跳转链接
        for item in re.findall(r'\<noscript\>.*?\</noscript\>', content, re.S):
            content = content.replace(item, '')
        return content

    @staticmethod
    def fix_filename(filename):
        illegal = {
            '\\': '＼',
            '/': '',
            ':': '：',
            '*': '＊',
            '?': '？',
            '<': '《',
            '>': '》',
            '|': '｜',
            '"': '〃',
            '!': '！',
            '\n': '',
            '\r': '',
            '&': 'and',
        }
        for key, value in illegal.items():
            filename = filename.replace(key, value)
        return unicode(filename[:80])
