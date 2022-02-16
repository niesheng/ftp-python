#! /usr/bin/python # -*- coding: utf-8 -*
#import unittest # 单元测试用例   pyinstaller -F xxx.py（xxx.py，打包的文件）
import os
import re
import sys
import datetime,time
from ftplib import FTP # 定义了FTP类，实现ftp上传和下载
import traceback
import logging
import ftplib
import traceback
import getpass

def upload_dir(path_source, session, target_dir=None):
    files = os.listdir(path_source)

    # 先记住之前在哪个工作目录中
    last_dir = os.path.abspath('.')
    # 然后切换到目标工作目录
    os.chdir(path_source)

    if target_dir:
        current_dir = session.pwd()
        try:
            session.mkd(target_dir)
        except Exception:
            pass
        finally:
            session.cwd(os.path.join(current_dir, target_dir))

    for file_name in files:
        current_dir = session.pwd()
        if os.path.isfile(path_source + r'/{}'.format(file_name)):
            upload_file(path_source, file_name, session)
        elif os.path.isdir(path_source + r'/{}'.format(file_name)):

            current_dir = session.pwd()
            try:
                session.mkd(file_name)
            except:
                pass
            session.cwd("%s/%s" % (current_dir, file_name))
            upload_dir(path_source + r'/{}'.format(file_name), session)

        # 之前路径可能已经变更，需要再回复到之前的路径里
        session.cwd(current_dir)

    os.chdir(last_dir)


def upload_file(path, file_name, session, target_dir=None, callback=None):
    # 记录当前 ftp 路径
    cur_dir = session.pwd()

    if target_dir:
        try:
            session.mkd(target_dir)
        except:
            pass
        finally:
            session.cwd(os.path.join(cur_dir, target_dir))

    print("path:%s \r\n\t   file_name:%s" % (path, file_name))
    file = open(os.path.join(path, file_name), 'rb')  # file to send

    session.storbinary('STOR %s' % file_name, file, callback = callback)  # send the file
    file.close()  # close file
    session.cwd(cur_dir)
    
try:  
    session = ftplib.FTP(host='183.60.4.212',user='huangjianping',passwd='xsense5566')
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    last_month_str = last_month.strftime("%Y-%m")
    #print(last_month_str)
    local_path = 'C:/Users/'+getpass.getuser()+'/Desktop/AmazonReport/'+last_month_str
    #fname = 'ftp_info.txt'
    #with open(fname, 'w+') as f:
    #    f.write(local_path)
    remote_path = '/test2/amz/'+last_month_str
    upload_dir(local_path,session,remote_path)
except Exception as e:
    print(str(traceback.format_exc()))
    #fname = 'ftp_errors.txt'
    #with open(fname, 'w+') as f:
    #   f.write(str(traceback.format_exc()))
finally:
    input('Press any key to quit program.')
