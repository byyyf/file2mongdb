# -*- coding:utf-8 -*-
# @FileName  :file2db.py
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
import configparser


class App:
    def __init__(self, root):
        self.iv = Random.new().read(AES.block_size)
        self.key = Random.new().read(AES.block_size)
        title = ''
        configpath = 'configfile.ini'
        state = 'disabled'
        self.rewrite = 0
        try:
            cf = configparser.RawConfigParser()
            cf.read(configpath, encoding='utf-8')
            uri = cf.get('mongodb', 'uri')
            self.rewrite = cf.get('rewrite', 'rewrite')
            self.client = pymongo.MongoClient(uri, server_api=ServerApi('1'))
            self.db = self.client['files']
            self.fs_rar = gridfs.GridFS(self.db, 'rar')
            self.coll = self.db['rar.files']
            dblist = self.client.list_database_names()
            if dblist:
                title = '数据库连接成功'
                state = 'active'
        except:
            title = '数据库连接失败'

        # setting title
        # root.title("file2mongodb")
        root.title(title)
        # setting window size
        width = 399
        height = 329
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        self.select_path = tk.StringVar()
        GLineEdit_path = tk.Entry(root, textvariable=self.select_path)
        GLineEdit_path["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        GLineEdit_path["font"] = ft
        GLineEdit_path["fg"] = "#333333"
        GLineEdit_path["justify"] = "left"
        GLineEdit_path["relief"] = "flat"
        GLineEdit_path.place(x=70, y=10, width=221, height=30)

        GButton_upload = tk.Button(root, state=state)
        GButton_upload["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_upload["font"] = ft
        GButton_upload["fg"] = "#000000"
        GButton_upload["justify"] = "center"
        GButton_upload["text"] = "上 传"
        GButton_upload["relief"] = "groove"
        GButton_upload.place(x=300, y=10, width=93, height=30)
        GButton_upload["command"] = self.GButton_upload_command

        #
        # GLineEdit_916=tk.Text(root) #主显示
        # GLineEdit_916["borderwidth"] = "1px"
        # ft = tkFont.Font(family='Times',size=10)
        # GLineEdit_916["font"] = ft
        # GLineEdit_916["fg"] = "#333333"
        # GLineEdit_916["relief"] = "flat"
        # GLineEdit_916.place(x=10,y=130,width=383,height=152)

        title = ('name', 'length', 'id')
        self.tv = ttk.Treeview(root, columns=title, show='headings', height=8)
        for i in range(len(title)):
            self.tv.column(title[i], width=10, anchor='e')
            self.tv.heading(title[i], text=title[i])
        self.tv.column(0, width=100)
        self.tv.place(x=10, y=130, width=383, height=152)
        self.tv.bind("<ButtonRelease - 1>", self.selectItem)

        GButton_download = tk.Button(root, state=state)
        GButton_download["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_download["font"] = ft
        GButton_download["fg"] = "#000000"
        GButton_download["justify"] = "center"
        GButton_download["text"] = "下 载"
        GButton_download["relief"] = "groove"
        GButton_download.place(x=300, y=50, width=94, height=30)
        GButton_download["command"] = self.GButton_download_command

        self.text_status = tk.StringVar()
        self.GLineEdit_778 = tk.Entry(root, textvariable=self.text_status)  # 状态
        self.GLineEdit_778["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GLineEdit_778["font"] = ft
        self.GLineEdit_778["fg"] = "#333333"
        self.GLineEdit_778["justify"] = "center"
        self.GLineEdit_778["relief"] = "groove"
        self.GLineEdit_778.place(x=10, y=290, width=379, height=30)

        self.text_search = tk.StringVar()
        self.GLineEdit_search = tk.Entry(root, textvariable=self.text_search)  # 搜索
        self.GLineEdit_search["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        self.GLineEdit_search["font"] = ft
        self.GLineEdit_search["fg"] = "#333333"
        self.GLineEdit_search["justify"] = "left"

        self.GLineEdit_search["relief"] = "flat"
        self.GLineEdit_search.place(x=70, y=50, width=221, height=30)

        self.valrar = IntVar()
        GCheckBox_rar = tk.Checkbutton(root, variable=self.valrar)
        ft = tkFont.Font(family='Times', size=10)
        GCheckBox_rar["font"] = ft
        GCheckBox_rar["fg"] = "#333333"
        GCheckBox_rar["justify"] = "center"
        GCheckBox_rar["text"] = "RAR"
        GCheckBox_rar["relief"] = "flat"
        GCheckBox_rar.place(x=20, y=90, width=53, height=30)
        GCheckBox_rar["offvalue"] = "0"
        GCheckBox_rar["onvalue"] = "1"


        self.valtxt = IntVar()
        GCheckBox_txt = tk.Checkbutton(root, variable=self.valtxt)
        ft = tkFont.Font(family='Times', size=10)
        GCheckBox_txt["font"] = ft
        GCheckBox_txt["fg"] = "#333333"
        GCheckBox_txt["justify"] = "center"
        GCheckBox_txt["text"] = "TXT"
        GCheckBox_txt["relief"] = "flat"
        GCheckBox_txt.place(x=100, y=90, width=51, height=30)
        GCheckBox_txt["offvalue"] = "0"
        GCheckBox_txt["onvalue"] = "1"


        self.valexe = IntVar()
        GCheckBox_exe = tk.Checkbutton(root, variable=self.valexe)
        ft = tkFont.Font(family='Times', size=10)
        GCheckBox_exe["font"] = ft
        GCheckBox_exe["fg"] = "#333333"
        GCheckBox_exe["justify"] = "center"
        GCheckBox_exe["text"] = "Exe"
        GCheckBox_exe["relief"] = "flat"
        GCheckBox_exe.place(x=170, y=90, width=64, height=30)
        GCheckBox_exe["offvalue"] = "0"
        GCheckBox_exe["onvalue"] = "1"


        self.valother = IntVar()
        GCheckBox_other = tk.Checkbutton(root, variable=self.valother)
        ft = tkFont.Font(family='Times', size=10)
        GCheckBox_other["font"] = ft
        GCheckBox_other["fg"] = "#333333"
        GCheckBox_other["justify"] = "center"
        GCheckBox_other["text"] = "Other"
        GCheckBox_other["relief"] = "flat"
        GCheckBox_other.place(x=240, y=90, width=56, height=30)
        GCheckBox_other["offvalue"] = "0"
        GCheckBox_other["onvalue"] = "1"


        GButton_delete = tk.Button(root, state=state)
        GButton_delete["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_delete["font"] = ft
        GButton_delete["fg"] = "#000000"
        GButton_delete["justify"] = "center"
        GButton_delete["text"] = "删 除"
        GButton_delete["relief"] = "groove"
        GButton_delete.place(x=300, y=90, width=91, height=30)
        GButton_delete["command"] = self.GButton_delete_command

        GButton_90 = tk.Button(root, state=state)
        GButton_90["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_90["font"] = ft
        GButton_90["fg"] = "#000000"
        GButton_90["justify"] = "center"
        GButton_90["text"] = "选择文件"
        GButton_90["relief"] = "flat"
        GButton_90.place(x=0, y=10, width=66, height=30)
        GButton_90["command"] = self.GButton_90_command

        GButton_search = tk.Button(root, state=state)
        GButton_search["bg"] = "#efefef"
        ft = tkFont.Font(family='Times', size=10)
        GButton_search["font"] = ft
        GButton_search["fg"] = "#000000"
        GButton_search["justify"] = "center"
        GButton_search["text"] = "搜索文件"
        GButton_search["relief"] = "flat"
        GButton_search.place(x=0, y=50, width=66, height=30)
        GButton_search["command"] = self.GButton_search_command

    def GButton_upload_command(self):
        self.text_status.set('上传')
        if self.select_path.get():
            path = self.select_path.get()
            fileName = os.path.split(path)[1]
            self.text_status.set(fileName)
            id = self.findFileByName(fileName)
            rewrite = self.rewrite  # 控制是否允许同名继续上传  1允许
            if id and rewrite == 0:
                self.text_status.set('%s文件存在，停止上传：%s' % (fileName, id))
                self.text_search.set(fileName)
            else:
                id = self.save_file_to_mongo(path, '', rewrite)
                if id:
                    self.text_search.set(fileName)
                    self.text_status.set('%s文件上传成功：%s' % (fileName, id))
                    self.GButton_search_command()

        else:
            self.text_status.set('未选择上传文件')

    def GButton_download_command(self):
        downloadID = self.text_status.get()
        if downloadID and len(downloadID.split('：')) > 1:
            id = downloadID.split('：')[1]
            if len(id) == 24:
                fileName = self.findFileByID(id)
                if fileName:
                    sp = fileName.split('.')
                    fileName = sp[0] + '_db.' + sp[1]
                    self.write_to_disk(fileName, self.get_file_from_mongo(id))
                    self.text_status.set('%s写入硬盘%s\\' % (fileName, os.getcwd()))
                else:
                    self.text_status.set('未发现id为%s的文件' % id)
            else:
                self.text_status.set('_id输入不正确')
        else:
            self.text_status.set('_id为空')

    def GButton_delete_command(self):
        id = self.text_status.get()
        if id and len(id.split('：')) > 1:
            id = id.split('：')[1]
        if id and len(id) == 24:
            b = msgbox.askokcancel('确认操作', '真的要删除编号为%s的文件么？' % id)  # 返回值true/false
            if b:
                re = self.fs_rar.delete(ObjectId(id))
                self.GButton_search_command()

    def GButton_90_command(self):
        # 单个文件选择
        selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
        self.select_path.set(selected_file_path)

    def getArgs(self):
        args = {}
        fileName = self.text_search.get()
        if fileName:
            if self.valother.get() == 1:
                args = {'$and': [{'filename': {'$regex': fileName}},
                                 {'$nor': [{'type': 'rar'}, {'type': 'exe'}, {'type': 'txt'}]}]}
            else:
                list = []
                type = ''
                if self.valrar.get() == 1:
                    list.append({'type': 'rar'})
                    type = 'rar'
                if self.valexe.get() == 1:
                    list.append({'type': 'exe'})
                    type = 'exe'
                if self.valtxt.get() == 1:
                    list.append({'type': 'txt'})
                    type = 'txt'
                if self.valrar.get() + self.valexe.get() + self.valtxt.get() > 1:
                    args = {'$and': [{'filename': {'$regex': fileName}}, {'$or': list}]}
                elif self.valrar.get() + self.valexe.get() + self.valtxt.get() == 1:
                    args = {'$and': [{'filename': {'$regex': fileName}}, {'type': type}]}
                else:
                    args['filename'] = {'$regex': fileName}
        return args

    def GButton_search_command(self):  # 搜索
        args = self.getArgs()
        result = self.coll.find(args).limit(10)
        for row in self.tv.get_children():
            self.tv.delete(row)
        for row in result:
            self.tv.insert('', 'end', values=(row['filename'], row['length'], row['_id']))

    def selectItem(self, event):
        curItem = self.tv.focus()
        list1 = self.tv.item(curItem)['values']
        if list1 and len(list1) > 2:
            self.text_status.set('%s大小%s ID为：%s' % (list1[0], list1[1], list1[2]))

    def findFileByName(self, fileName):
        back = self.coll.find_one({"filename": fileName})
        if back:
            return back['_id']
        else:
            return back

    def findFileByID(self, id):
        back = self.coll.find_one({"_id": ObjectId(id)})
        if back:
            return back['filename']
        else:
            return back

    # 存储文件到mongo
    def save_file_to_mongo(self, path, keyword, rewrite=0):
        fileName = os.path.split(path)[1]
        id = self.findFileByName(fileName)
        if id and rewrite == 0:
            # print('文件存在，直接返回id')
            return id
        else:
            args = {}
            args['keyword'] = keyword
            args['type'] = fileName.split('.')[1]
            with open(path, 'rb') as f:
                data = f.read()
            data = self.encrypt(data)
            return self.fs_rar.put(data, filename=fileName, **args)

    def encrypt(self, data):
        cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciptext = self.iv + cipher.encrypt(data) + self.key
        return ciptext

    # 从mongo取出文件
    def get_file_from_mongo(self, id):
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
    root.mainloop()
