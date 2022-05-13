# -*- coding:utf-8 -*-
# @FileName  :ide1.py
# @Time      :2022/5/12 19:33
import os
import tkinter.messagebox as msgbox
from tkinter import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import filedialog, ttk

import pymongo
import gridfs

from bson import ObjectId
from Cryptodome.Cipher import AES
from Cryptodome import Random
from pymongo.server_api import ServerApi
import pandas as pd

class App:
    def __init__(self, root):
        uri = "mongodb+srv://user:password@cloud.youdomain.com/myFirstDatabase?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['files']
        self.fs_rar = gridfs.GridFS(self.db, 'rar')
        self.coll = self.db["rar.files"]

        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 200)  # pd.set_option('display.max_columns', None)
        pd.set_option('display.width', 1000)

        self.iv = Random.new().read(AES.block_size)
        self.key = Random.new().read(AES.block_size)
        title=''

        try:
            dblist = self.client.list_database_names()
            if dblist:
                # root.write_log_to_Text('数据库连接成功')
                title='数据库连接成功'
                # print(dblist)
        except:
            # root.write_log_to_Text('数据库连接失败')
            title = '数据库连接失败'





        #setting title
        # root.title("file2mongodb")
        root.title(title)
        #setting window size
        width=399
        height=329
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # 初始化Entry控件的textvariable属性值.
        self.select_path = tk.StringVar()
        GLineEdit_path=tk.Entry(root, textvariable = self.select_path)
        GLineEdit_path["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GLineEdit_path["font"] = ft
        GLineEdit_path["fg"] = "#333333"
        GLineEdit_path["justify"] = "left"
        GLineEdit_path["relief"] = "flat"
        GLineEdit_path.place(x=70,y=10,width=221,height=30)

        GButton_upload=tk.Button(root)
        GButton_upload["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_upload["font"] = ft
        GButton_upload["fg"] = "#000000"
        GButton_upload["justify"] = "center"
        GButton_upload["text"] = "上 传"
        GButton_upload["relief"] = "groove"
        GButton_upload.place(x=300,y=10,width=93,height=30)
        GButton_upload["command"] = self.GButton_upload_command

        #
        # GLineEdit_916=tk.Text(root) #主显示
        # GLineEdit_916["borderwidth"] = "1px"
        # ft = tkFont.Font(family='Times',size=10)
        # GLineEdit_916["font"] = ft
        # GLineEdit_916["fg"] = "#333333"
        # GLineEdit_916["relief"] = "flat"
        # GLineEdit_916.place(x=10,y=130,width=383,height=152)

        title = ('id', 'name',   'length')
        self.tv = ttk.Treeview(root, columns=title, show='headings', height=8)
        # self.tv.pack()
        for i in range(len(title)):
            self.tv.column(title[i], width=10, anchor='e')
            self.tv.heading(title[i], text=title[i])
        self.tv.column(0, width=100)
        self.tv.place(x=10, y=130, width=383, height=152)
        self.tv.bind("<ButtonRelease - 1>", self.selectItem)

        # def popup(event):
        #     "鼠标事件"
        #     item = self.tv.selection()[0]
        #     print( ", it's values = ", self.tv.item(item, "values"))
        #     print('___________________')
        #
        # # self.tv.bind("<Button-1>", popup)
        # self.tv.bind("<ButtonRelease - 1>", popup)

        GButton_download=tk.Button(root)
        GButton_download["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_download["font"] = ft
        GButton_download["fg"] = "#000000"
        GButton_download["justify"] = "center"
        GButton_download["text"] = "下 载"
        GButton_download["relief"] = "groove"
        GButton_download.place(x=300,y=50,width=94,height=30)
        GButton_download["command"] = self.GButton_download_command

        # 初始化Entry控件的textvariable属性值
        self.text_status = tk.StringVar()
        self.GLineEdit_778=tk.Entry(root, textvariable=self.text_status)  #状态
        self.GLineEdit_778["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_778["font"] = ft
        self.GLineEdit_778["fg"] = "#333333"
        self.GLineEdit_778["justify"] = "center"
        self.GLineEdit_778["relief"] = "groove"
        self.GLineEdit_778.place(x=10,y=290,width=379,height=30)

        self.text_search = tk.StringVar()
        self.GLineEdit_search=tk.Entry(root, textvariable=self.text_search)  #搜索
        self.GLineEdit_search["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        self.GLineEdit_search["font"] = ft
        self.GLineEdit_search["fg"] = "#333333"
        self.GLineEdit_search["justify"] = "left"

        self. GLineEdit_search["relief"] = "flat"
        self.GLineEdit_search.place(x=70,y=50,width=221,height=30)

        self.valrar = IntVar()
        GCheckBox_rar=tk.Checkbutton(root, variable=self.valrar)
        ft = tkFont.Font(family='Times',size=10)
        GCheckBox_rar["font"] = ft
        GCheckBox_rar["fg"] = "#333333"
        GCheckBox_rar["justify"] = "center"
        GCheckBox_rar["text"] = "RAR"
        GCheckBox_rar["relief"] = "flat"
        GCheckBox_rar.place(x=20,y=90,width=53,height=30)
        GCheckBox_rar["offvalue"] = "0"
        GCheckBox_rar["onvalue"] = "1"
        GCheckBox_rar["command"] = self.GCheckBox_rar_command

        GCheckBox_125=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GCheckBox_125["font"] = ft
        GCheckBox_125["fg"] = "#333333"
        GCheckBox_125["justify"] = "center"
        GCheckBox_125["text"] = "TXT"
        GCheckBox_125["relief"] = "flat"
        GCheckBox_125.place(x=100,y=90,width=51,height=30)
        GCheckBox_125["offvalue"] = "0"
        GCheckBox_125["onvalue"] = "1"
        GCheckBox_125["command"] = self.GCheckBox_125_command

        GCheckBox_45=tk.Checkbutton(root)
        ft = tkFont.Font(family='Times',size=10)
        GCheckBox_45["font"] = ft
        GCheckBox_45["fg"] = "#333333"
        GCheckBox_45["justify"] = "center"
        GCheckBox_45["text"] = "Excel"
        GCheckBox_45["relief"] = "flat"
        GCheckBox_45.place(x=170,y=90,width=64,height=30)
        GCheckBox_45["offvalue"] = "0"
        GCheckBox_45["onvalue"] = "1"
        GCheckBox_45["command"] = self.GCheckBox_45_command

        self.valother = IntVar()
        GCheckBox_other=tk.Checkbutton(root, variable=self.valother)
        ft = tkFont.Font(family='Times',size=10)
        GCheckBox_other["font"] = ft
        GCheckBox_other["fg"] = "#333333"
        GCheckBox_other["justify"] = "center"
        GCheckBox_other["text"] = "Other"
        GCheckBox_other["relief"] = "flat"
        GCheckBox_other.place(x=240,y=90,width=56,height=30)
        GCheckBox_other["offvalue"] = "0"
        GCheckBox_other["onvalue"] = "1"
        GCheckBox_other["command"] = self.GCheckBox_other_command

        GButton_delete=tk.Button(root)
        GButton_delete["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_delete["font"] = ft
        GButton_delete["fg"] = "#000000"
        GButton_delete["justify"] = "center"
        GButton_delete["text"] = "删 除"
        GButton_delete["relief"] = "groove"
        GButton_delete.place(x=300,y=90,width=91,height=30)
        GButton_delete["command"] = self.GButton_delete_command

        GButton_90=tk.Button(root)
        GButton_90["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_90["font"] = ft
        GButton_90["fg"] = "#000000"
        GButton_90["justify"] = "center"
        GButton_90["text"] = "选择文件"
        GButton_90["relief"] = "flat"
        GButton_90.place(x=0,y=10,width=66,height=30)
        GButton_90["command"] = self.GButton_90_command

        GButton_search=tk.Button(root)
        GButton_search["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        GButton_search["font"] = ft
        GButton_search["fg"] = "#000000"
        GButton_search["justify"] = "center"
        GButton_search["text"] = "搜索文件"
        GButton_search["relief"] = "flat"
        GButton_search.place(x=0,y=50,width=66,height=30)
        GButton_search["command"] = self.GButton_search_command



    def GButton_upload_command(self):
        self.text_status.set('上传')
        # self.select_path.set('D:/workspace/pythonProject/zszm/mongo/2.rar')
        if self.select_path.get():
            path = self.select_path.get()
            fileName = os.path.split(path)[1]
            print(fileName)
            self.text_status.set(fileName)
            id = self.findFileByName(fileName)
            rewrite = 1
            if id and rewrite == 0:
                self.text_status.set('%s文件存在，停止上传：%s' % (fileName,id))
                self.text_search.set(fileName)
            else:
                id = self.save_file_to_mongo(path, '', rewrite)
                if id:
                    self.text_search.set(fileName)
                    self.text_status.set('%s文件上传成功：%s' % (fileName,id))
                    self.GButton_search_command()

        else:
            self.text_status.set('未选择上传文件')



    def GButton_download_command(self):
        # print("command247")
        # self.text_status.set('文件保存成功：627d28720dc2723480ee1e7a')
        print(os.getcwd())
        downloadID  = self.text_status.get()
        # print(downloadID)
        if downloadID and len(downloadID.split('：'))>1:
            id = downloadID.split('：')[1]
            print(len(id))
            if len(id) == 24:
                fileName = self.findFileByID(id)
            # print(fileName)
                if fileName:
                    sp = fileName.split('.')
                    fileName = sp[0] + '_db.' + sp[1]
                    # print(fileName)
                    self.write_to_disk(fileName, self.get_file_from_mongo(id))

                    self.text_status.set('%s写入硬盘%s\\' % (fileName,os.getcwd()))
                else:
                    self.text_status.set('未发现id为%s的文件'%id )
            else:
                self.text_status.set('_id输入不正确')
        else:
            self.text_status.set('_id为空')

        # 文件保存成功：627d227c499b77d0150a0c15



    def GCheckBox_rar_command(self):
        print("command304")
        self.text_status.set('command304')


    def GCheckBox_125_command(self):
        print("command125")
        self.text_status.set('command125')


    def GCheckBox_45_command(self):
        print("command45")
        self.text_status.set('command45')


    def GCheckBox_other_command(self):
        print("command214")
        print(self.valother.get())
        self.text_status.set('command214')


    def GButton_delete_command(self):
        print("command730")
        # self.text_status.set('command730')
        id = self.text_status.get()
        if id and len(id.split('：'))>1:
            id = id.split('：')[1]
        if id and len(id) == 24:
            b=msgbox.askokcancel('确认操作', '真的要删除编号为%s的文件么？'%id)  # 返回值true/false
            # print(b)
            if b:
                # id = self.text_status.get()
                print(id)
                re = self.fs_rar.delete(ObjectId(id))
                print(re)


    def GButton_90_command(self):
        print("command90")
        # 单个文件选择
        selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
        self.select_path.set(selected_file_path)



    def GButton_search_command(self): #搜索
        print('command209')
        fileName =self.text_search.get()
        args = {}
        if fileName:
            args['filename'] = {'$regex':fileName}
        if self.valrar.get()==1:
            args['type'] = 'rar'
        print(args)
        result = self.coll.find(args).limit(10)
        print(result)
        # df = pd.DataFrame(list(result))
        # print(df)
        for row in  self.tv.get_children():
            self.tv.delete(row)
        for row in result:
            self.tv.insert('', 'end', values=(row['_id'],row['filename'],row['length']))

    def selectItem(self,event):
        curItem = self.tv.focus()
        # print (self.tv.item(curItem))
        list1 = self.tv.item(curItem)['values']
        # print(list1)
        if list1 and len(list1)>2:
            self.text_status.set('%s大小%s ID为：%s'%(list1[1],list1[2],list1[0]))

    def findFileByName(self,fileName):
        back =self.coll.find_one({"filename": fileName})
        if back:
            return back['_id']
        else:
            return back
        # 存储文件到mongo
    def findFileByID(self,id):
        back =self.coll.find_one({"_id": ObjectId(id)})
        # print(back)
        if back:
            return back['filename']
        else:
            return back
    def save_file_to_mongo(self, path, keyword, rewrite=0):

        fileName = os.path.split(path)[1]
        id = self.findFileByName(fileName)
        if id and rewrite == 0:
            print('文件存在，直接返回id')
            return id
        else:
            args = {}
            args['keyword'] = keyword
            args['type'] = fileName.split('.')[1]
            # args['key'] = self.key
            with open(path, 'rb') as f:
                data = f.read()
            data = self.encrypt(data)
            return self.fs_rar.put(data, filename=fileName, **args)

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciptext = self.iv + cipher.encrypt(data)+self.key
        return ciptext
    # 从mongo取出文件
    def get_file_from_mongo(self,id):
        gf = self.fs_rar.get(ObjectId(id))
        ciptext = gf.read()
        key = ciptext[-16:]
        mydecrypt = AES.new(key, AES.MODE_CFB, ciptext[:16])
        decrytext = mydecrypt.decrypt(ciptext[16:])
        return decrytext

    # 将文件写入硬盘
    def write_to_disk(self, fileName, content):
        with open(fileName, 'wb') as f:
            f.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    print('asdfas')
    root.mainloop()



