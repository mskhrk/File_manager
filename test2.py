#-*- coding:utf-8 -*-
__author__ ="https://github.com/mskhrk"
import os
from cfg_api import * 
my_dir=os.path.dirname(__file__)
cfg_name='test.cfg'
cfg_path=my_dir+'\\'+cfg_name

work_dir='C:/Users/user/Desktop'
teaget_dir='C:/Users/user/Desktop'
teaget_dir2='C:/Users/user/Desktop/ttr'

#讀取指定目錄的檔案
#cfg_read_dir(cfg_path,teaget_dir)
cfg_read_alldir(cfg_path,teaget_dir)



'''
api_example
cfg_add_section(cfg_path,'Swection1')
cfg_remove_section(cfg_path,'Swection1')
cfg_add_data(cfg_path,'Swection2','dDdd','111')
cfg_remove_option(cfg_path,'Swection2','ddd')
cfg_get_data(cfg_path,'filelist2','0')
cfg_control_get_newid(cfg_path)
cfg_remove_id(cfg_path,'5')
cfg_read_dir(cfg_path,teaget_dir)
cfg_read_alldir(cfg_path,teaget_dir)
'''
