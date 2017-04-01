# -*- coding: utf-8 -*-
import os
import shutil
import locale

class Path(object):
    # 初始地址,不含分隔符
    # 此时sys.stdout.encoding已被修改为utf-8，故改为使用locale.getpreferredencoding()获取默认编码
    base_path = os.path.abspath('.')

    @staticmethod
    def reset_path():
        Path.chdir(Path.base_path)
        return

    @staticmethod
    def pwd():
        print(os.path.realpath('.'))
        return

    @staticmethod
    def get_pwd():
        path = unicode(os.path.abspath('.').decode(locale.getpreferredencoding()))
        return path

    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except OSError:
            pass
        return

    @staticmethod
    def chdir(path):
        try:
            os.chdir(path)
        except OSError:
            Path.mkdir(path)
            os.chdir(path)
        return

    @staticmethod
    def rmdir(path):
        if path:
            shutil.rmtree(path, ignore_errors=True)
        return

    @staticmethod
    def copy(src, dst):
        if not os.path.exists(src):
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src=src, dst=dst)
        return

    @staticmethod
    def get_filename(src):
        return os.path.basename(src)

    @staticmethod
    def init_base_path():
        Path.base_path = Path.get_pwd()
        return

    @staticmethod
    def init_work_directory():
        Path.reset_path()
        return

    @staticmethod
    def is_file(path):
        return os.path.isfile(path)
