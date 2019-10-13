import configparser
import os

#global_value

global_save_time=100#存檔頻率
global_save_counter=0#執行計數器
global_config = configparser.ConfigParser()#全域物件
global_config.optionxform = str


global_new_id_read_cfg=True
global_id_now=0
global_id_remove=0



#新增section
#結構cfg_file_src>section>option>data
def cfg_add_section(cfg_file_src,section):
    config = configparser.ConfigParser()
    config.optionxform = str
    

    if os.path.isfile(cfg_file_src):
        config.read(cfg_file_src,encoding="utf-8")
    else:
        with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
            config.write(configfile)

    if config.has_section(section)==False:
        config.add_section(section)
        with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
            config.write(configfile)


#移除section
#結構cfg_file_src>section>option>data
def cfg_remove_section(cfg_file_src,section):
    config = configparser.ConfigParser()
    config.optionxform = str
    
    if os.path.isfile(cfg_file_src):
        config.read(cfg_file_src,encoding="utf-8")
        if config.has_section(section)==True:
            config.remove_section(section)
            with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
                config.write(configfile)

#新增資料
#結構cfg_file_src>section>option>data
def cfg_add_data(cfg_file_src,section,option,data):
    global global_save_counter
    global global_config
    #cfg_add_section(cfg_file_src,section)
    global_config.set(section,option,data)
    global_save_counter+=1
    if global_save_counter>=global_save_time:
        cfg_save_file(cfg_file_src,global_config)
        global_save_counter=0

#新增資料到config但不儲存版本
#結構cfg_file_src>section>option>data
def cfg_add_data_unsave(cfg_file_src,section,option,data):
    global global_config
    cfg_add_section(cfg_file_src,section)
    global_config.read(cfg_file_src,encoding="utf-8")
    global_config.set(section,option,data)

#移除option
#結構cfg_file_src>section>option>data
def cfg_remove_option(cfg_file_src,section,option):
    config = configparser.ConfigParser()
    config.optionxform = str
    cfg_add_section(cfg_file_src,section)
    config.read(cfg_file_src,encoding="utf-8")
    if (config.has_option(section,option)==True):
        config.remove_option(section, option)
        with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
            config.write(configfile)

#取得cfg資料    
def cfg_get_data(cfg_file_src,section,option):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(cfg_file_src,encoding="utf-8")
    return config.get(section,option, fallback='not find data')

#暫存寫入檔案
def cfg_save_file(cfg_file_src,config_object):
    with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
        config_object.write(configfile)
        
#全域暫存寫入檔案
def cfg_global_save_file(cfg_file_src):
    global global_config
    with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
        global_config.write(configfile)
        
#全域暫存載入檔案
def cfg_global_reload_file(cfg_file_src):
    global global_config
    global_config.read(cfg_file_src,encoding="utf-8")
# 初始化cfg_control
def init_cfg_control(cfg_file_src):
    global global_config
    if cfg_get_data(cfg_file_src, 'cfg_control', 'id_now') == 'not find data':
        
        #創建初始section
        cfg_add_section(cfg_file_src,'cfg_control')
        cfg_add_section(cfg_file_src,'filelist')
        cfg_add_section(cfg_file_src,'id_remove_list')
        #第一次創建section需自行reload，reload後cfg_add_data才可正常運作
        cfg_global_reload_file(cfg_file_src)
        # 現在使用過的最新id
        cfg_add_data(cfg_file_src, 'cfg_control', 'id_now', '0')
        # 被移除過的id數量
        cfg_add_data(cfg_file_src, 'cfg_control', 'id_remove', '0')
        # 此add會立即被使用，因此須立即寫入檔案
        cfg_save_file(cfg_file_src,global_config)
        
# 取得一個新id(int)    
def cfg_control_get_newid(cfg_file_src):
    global global_new_id_read_cfg
    global global_id_now
    global global_id_remove
    global global_config
    if global_new_id_read_cfg:
        global_id_now=int(cfg_get_data(cfg_file_src, 'cfg_control', 'id_now'))
        global_id_remove=int(cfg_get_data(cfg_file_src, 'cfg_control', 'id_remove'))
        global_new_id_read_cfg=False
        

    if global_id_remove >0:
        
        #取得末端一筆位置
        remove_last=int(cfg_get_data(cfg_file_src, 'id_remove_list',str(global_id_remove)))
        
        #刪除id_remove_list末端一筆
        cfg_remove_option(cfg_file_src,'id_remove_list',str(global_id_remove))
        
        #修改id_remove數量
        global_id_remove-=1
        cfg_global_reload_file(cfg_file_src)
        cfg_add_data(cfg_file_src,'cfg_control','id_remove',str(global_id_remove))
        cfg_save_file(cfg_file_src,global_config)
        #優先使用被移除的id
        return remove_last
    else:
        global_id_now+=1
        cfg_add_data_unsave(cfg_file_src,'cfg_control','id_now',str(global_id_now))
        #cfg_global_reload_file(cfg_file_src)
        #cfg_add_data(cfg_file_src,'cfg_control','id_now',str(global_id_now))
        
    return global_id_now

#移除指定id資料
def cfg_remove_id(cfg_file_src,cfg_id):
    
    if(cfg_get_data(cfg_file_src,'filelist',str(cfg_id))!='not find data'):
        #有找到才移除
        cfg_remove_option(cfg_file_src,'filelist',str(cfg_id))
        id_remove_int=int(cfg_get_data(cfg_file_src, 'cfg_control', 'id_remove'))
        id_remove_int+=1
        #id_remove_list(被移除清單)
        #id_remove_int(被移除清單序號)
        #cfg_id(被移除id)
        cfg_add_data(cfg_file_src,'id_remove_list',str(id_remove_int),str(cfg_id))
        cfg_add_data(cfg_file_src,'cfg_control','id_remove',str(id_remove_int))
        cfg_save_file(cfg_file_src,global_config)
def cfg_read_dir(cfg_file_src,dir_src):
    list_allfile=os.listdir(dir_src)
    for index in range (len(list_allfile)):
        #先分類檔案目錄
        new_teaget_src=dir_src+'/'+list_allfile[index]
        init_cfg_control(cfg_file_src)
        if os.path.isdir(new_teaget_src):
            pass
        else:
            cfg_add_data(cfg_file_src,'filelist',str(cfg_control_get_newid(cfg_file_src)),list_allfile[index])
            
            
def cfg_read_alldir(cfg_file_src,dir_src):

    list_allfile=os.listdir(dir_src)
    for index in range (len(list_allfile)):
        #先分類檔案目錄
        new_teaget_src=dir_src+'/'+list_allfile[index]
        init_cfg_control(cfg_file_src)
        if os.path.isdir(new_teaget_src):
            cfg_read_alldir(cfg_file_src,new_teaget_src)
        else:
            cfg_add_data(cfg_file_src,'filelist',str(cfg_control_get_newid(cfg_file_src)),list_allfile[index])
            #print(str(global_id_now))
   