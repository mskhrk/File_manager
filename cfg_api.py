import configparser
import os


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
    config = configparser.ConfigParser()
    config.optionxform = str
    cfg_add_section(cfg_file_src,section)
    config.read(cfg_file_src,encoding="utf-8")
    config.set(section,option,data)
    with open(cfg_file_src, 'w+',encoding="utf-8") as configfile:
        config.write(configfile)

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
    #print(config.get(section,option, fallback='not find data'))
    return config.get(section,option, fallback='not find data')

# 初始化cfg_control
def init_cfg_control(cfg_file_src):
    if cfg_get_data(cfg_file_src, 'cfg_control', 'id_now') == 'not find data':
        # 現在使用過的最新id
        cfg_add_data(cfg_file_src, 'cfg_control', 'id_now', '0')
        # 被移除過的id數量
        cfg_add_data(cfg_file_src, 'cfg_control', 'id_remove', '0')
        # 建立移除表單
        cfg_add_section(cfg_file_src,'id_remove_list')
        
# 取得一個新id(int)    
def cfg_control_get_newid(cfg_file_src):
    init_cfg_control(cfg_file_src)
    id_now_int=int(cfg_get_data(cfg_file_src, 'cfg_control', 'id_now'))
    id_remove_int=int(cfg_get_data(cfg_file_src, 'cfg_control', 'id_remove'))

    if id_remove_int >0:
        
        #取得末端一筆位置
        remove_last=int(cfg_get_data(cfg_file_src, 'id_remove_list',str(id_remove_int)))
        
        #刪除id_remove_list末端一筆
        cfg_remove_option(cfg_file_src,'id_remove_list',str(id_remove_int))
        
        #修改id_remove數量
        id_remove_int-=1
        cfg_add_data(cfg_file_src,'cfg_control','id_remove',str(id_remove_int))
        
        #優先使用被移除的id
        return remove_last
    else:
        id_now_int+=1
        cfg_add_data(cfg_file_src,'cfg_control','id_now',str(id_now_int))
    return id_now_int

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

def cfg_read_dir(cfg_file_src,dir_src):
    list_allfile=os.listdir(dir_src)
    for index in range (len(list_allfile)):
        #先分類檔案目錄
        new_teaget_src=dir_src+'/'+list_allfile[index]
        if os.path.isdir(new_teaget_src):
            pass
        else:
            cfg_add_data(cfg_file_src,'filelist',str(cfg_control_get_newid(cfg_file_src)),list_allfile[index])
        
def cfg_read_alldir(cfg_file_src,dir_src):
    list_allfile=os.listdir(dir_src)
    for index in range (len(list_allfile)):
        #先分類檔案目錄
        new_teaget_src=dir_src+'/'+list_allfile[index]
        if os.path.isdir(new_teaget_src):
            cfg_read_alldir(cfg_file_src,new_teaget_src)
        else:
            cfg_add_data(cfg_file_src,'filelist',str(cfg_control_get_newid(cfg_file_src)),list_allfile[index])
        