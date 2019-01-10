#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import sys

#TODO HEX数据无法添加标签
#TODO 生成ID速度问题

if sys.version_info[0] < 3:
    # If we're executing with Python 2
    import Tkinter as tk
    import tkMessageBox as messagebox
    import ttk
    # import tkFileDialog as filedialog
    # import tkColorChooser as colorchooser
else:
    # Otherwise we're using Python 3
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk

import serial.tools.list_ports
# from defaults import defaults

import threading
# import time
import os
# from datetime import datetime
# import copy
import re
from defaults import *
from adaptive import *
# from keymaps import *
from method import *

g_default_theme = 'default'

if g_default_theme == 'dark':
    font = monaco_font
    font_right_send = monaco_font_9
    font_label_temp = monaco_font_9
else:
    font = None
    font_right_send = None
    font_label_temp = None


class SerialToolUI(object):
    def __init__(self, master=None):
        self.root = master

        self.com = serial.Serial()
        self.receiveCount = 0
        self.receive_count_without_space = 0
        self.id_data_count = 0
        self.id_correct_data_count = 0

        self.timeLastReceive = 0

        # self.thresholdValue = 1
        self.mbar = None
        self.fmenu = None
        self.etmenu = None

        self.frm = None
        self.frm_status = None

        self.panewin = None
        self.frm_left = None
        self.frm_right = None

        self.frm_left_notebook1 = None
        self.frm_left_notebook2 = None

        self.frm_left_notebook1_frame1 = None
        self.frm_left_notebook1_frame2 = None

        self.serial_set_label = None
        self.serial_set_frame = None
        self.serial_set_btn = None

        self.frm_left_combobox_serialport = None
        self.frm_left_combobox_baudrate = None
        self.frm_left_combobox_parity = None
        self.frm_left_combobox_databit = None
        self.frm_left_combobox_stopbit = None

        self.frm_left_notebook2_frame1 = None
        self.frm_left_notebook2_frame2 = None

        self.id_string_r0_label = None
        self.id_string_r1_frame = None
        self.id_string_r2_label = None
        self.id_string_r3_frame = None

        self.r1_rb_v = None
        self.r1_cb_v = None
        self.linefeed = None
        self.id_string_r1_linefeed_entry = None

        self.id_string_send_rb_v = None
        self.id_string_send_cb_v = None
        self.schedule_send = None
        self.id_string_schedule_send_entry = None
        self.id_string_send_CRLF_cb_v = None

        self.id_format_frame = None
        self.id_format_frame_id_frame_entry = None
        self.id_format_frame_len_entry = None
        self.id_format_id_type_entry = None
        self.id_string_combobox_frame_check = None
        self.id_format_id_label = None
        self.id_format_id_entry = None
        self.id_format_gen_btn = None
        self.id_format_id_check_entry = None
        self.id_string_combobox_frame_type = None
        self.id_format_restart_btn = None
        self.id_format_id_ex = None
        self.frame_len_v = None
        self.id_type_v = None
        self.id_v = None

        self.frm_right_panewin = None
        self.frm_right_tag_info = None
        self.frm_right_log = None

        self.frm_right_tag_info_available = None
        self.frm_right_tag_info_invalid = None
        self.frm_right_tag_info_total = None

        self.tag_info_available_label_num = None
        self.tag_info_available_label_num_entry = None
        self.tag_info_available_text_frame = None
        self.tag_info_available_label = None
        self.tag_info_available_scrollbar = None
        self.tag_info_available_listbox = None

        self.tag_info_invalid_label_num = None
        self.tag_info_invalid_label_num_entry = None
        self.tag_info_invalid_text_frame = None
        self.tag_info_invalid_label = None
        self.tag_info_invalid_scrollbar = None
        self.tag_info_invalid_listbox = None

        self.tag_info_total_label_num = None
        self.tag_info_total_label_num_entry = None
        self.tag_info_total_text_frame = None
        self.tag_info_total_label = None
        self.tag_info_total_scrollbar = None
        self.tag_info_total_listbox = None

        self.frm_right_log_notebook = None
        self.frm_right_log_notebook_frame1 = None
        self.frm_right_log_notebook_frame2 = None
        self.log_notebook_frame1_scrollbar = None
        self.log_notebook_frame1_data = None
        self.log_notebook_frame1_listbox = None

        self.log_notebook_frame2_scrollbar = None
        self.log_notebook_frame2_data = None

        self.frm_status_label = None
        self.frm_status_send_bytes = None
        self.frm_status_send_bytes_num = None
        self.frm_status_receive_bytes = None
        self.frm_status_receive_bytes_num = None

        self.menubar = None

        self.variables = {
            'receiveProgressStop': False,
            'dataLogScrollStop': True,
            'dataLogScrollStopTime': 10.0,
        }

        self.TKvariables = {}
        # Read in the defaults
        for key in defaults:
            self.TKvariables.update({key: tk.StringVar(value=defaults[key])})

        self.IdFormat = {
            'id_format_str': '',
            # 'id_start_index': 0,
            # 'id_start_limit': 3,
            'id_start': '',
            'id_nn_index': 0,
            'id_nn': '',
            'id_id_h_or_a': '',
            'id_id_index': 0,
            'id_id': '',
            'id_state1_index': 0,
            'id_state1': '',
            'id_state2_index': 0,
            'id_state2': '',
            'id_chk_type': 'None',
            IDF_ID_CHK_INDEX: 0,
            'id_chk': '',
            IDF_ID_CHK_START_INDEX: 0,
            'id_chk_str': '',
            'id_r_pattern': '',
            'id_seg_str': '',
            'id_seg_stp': '',
            'id_seg_ind': [],

        }

        self.IdDict = {
            'id_id': {
                'sn': '',
                'rssi': '',
                IDDICT_COUNT: 1,

                '1st_rec_data': "%Y-%m-%d %H:%M:%S.%f')[:-3]",
                '1st_rec_time': "%Y-%m-%d %H:%M:%S.%f')[:-3]",
                'rec_data': "%Y-%m-%d %H:%M:%S.%f')[:-3]",
                'rec_time': "%Y-%m-%d %H:%M:%S.%f')[:-3]",
            },

        }

        self.IdDictBuf = {}

        self.IdCheckStr = ''
        self.IdAvailableDict = {}
        self.IdInvalidDict = {}
        self.IdTotalDict = {}

        self.init_component()

    def init_component(self):
        """
        设置顶级窗体的行列权重，否则子组件的拉伸不会填充整个窗体
        """
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        """
        为顶级窗体添加菜单项
        """
        self.mbar = tk.Menu(self.root)  # 定义顶级菜单实例
        self.fmenu = tk.Menu(self.mbar, tearoff=False)  # 定义顶级菜单实例
        self.init_menu()
        self.init_tool()
        self.create_frame()

        self.menubar = tk.Menu(self.root, tearoff=False)

    def init_tool(self):
        self.com = serial.Serial()
        self.receiveCount = 0
        print('com.is_open = %d ' % self.com.is_open)

        # self.com = Serial()
        return

    def init_menu(self):
        """
        初始化菜单
        """
        self.mbar.add_cascade(label=' 文件 ', menu=self.fmenu,
                              font=font)  # 添加子菜单
        self.fmenu.add_command(label="打开", command=self.menu_click_event)
        self.fmenu.add_command(label="保存", command=self.menu_click_event)
        self.fmenu.add_separator()  # 添加分割线
        self.fmenu.add_command(label="退出", command=self.root.quit())

        self.etmenu = tk.Menu(self.mbar, tearoff=False)
        self.mbar.add_cascade(label=' 编辑 ', menu=self.etmenu)

        for each in ['复制', '剪切', '合并']:
            self.etmenu.add_command(label=each, command=self.menu_click_event)

        self.root.config(menu=self.mbar)  # 将顶级菜单注册到窗体

    def cut(self, editor):
        # editor.event_generate("<<Cut>>")
        """
        # 复制的回调函数
        :return:
        """
        # 获得文本框内容
        # content_from_text = editor.selection_clear()
        content_from_text = editor.selection_get()
        editor.delete(tk.SEL_FIRST, tk.SEL_LAST)
        print("content_from_text: ", content_from_text)
        # 添加至系统粘贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(content_from_text)
        print('self.root.clipboard_get() is', self.root.clipboard_get())

    def copy(self, editor):
        # editor.event_generate("<<Copy>>")
        # 获得文本框内容
        content_from_text = editor.selection_get()
        print("content_from_text: ", content_from_text)
        # print("selected text: '%s'" % editor.get(tk.SEL_FIRST, tk.SEL_LAST))

        # 添加至系统粘贴板
        self.root.clipboard_clear()
        self.root.clipboard_append(content_from_text)

        print('self.root.clipboard_get() is', self.root.clipboard_get())

    def paste(self, editor):
        # editor.event_generate('<<Paste>>')
        """
        # 粘贴的回调函数
        :return:
        """
        content_from_system = str()

        try:
            # 获得系统粘贴板内容
            content_from_system = self.root.clipboard_get()

        except tk.TclError:
            # 防止因为粘贴板没有内容报错
            pass

        # 在文本框中设置刚刚获得的内容
        editor.insert(tk.END, content_from_system)

    def right_key_event(self, event, editor):
        self.menubar.delete(0, tk.END)
        self.menubar.add_command(label='剪切', command=lambda: self.cut(editor))
        self.menubar.add_command(label='复制', command=lambda: self.copy(editor))
        self.menubar.add_command(label='粘贴', command=lambda: self.paste(editor))
        self.menubar.post(event.x_root, event.y_root)

    def create_frame(self):

        """
        新建窗口，分为上下2个部分，下半部分为状态栏
        """
        self.frm = ttk.LabelFrame(self.root)
        # self.frm_status = ttk.LabelFrame(self.root, height=25)
        self.frm_status = ttk.LabelFrame(self.root)
        self.frm.grid(row=0, column=0, sticky="wesn")
        self.frm_status.grid(row=1, column=0, sticky="we")
        # self.frm_status.grid_propagate(0)

        # 拉伸
        self.frm.rowconfigure(0, weight=1)
        self.frm.columnconfigure(0, weight=1)
        # self.frm_status.rowconfigure(0, weight=1)
        self.frm_status.columnconfigure(0, weight=1)
        # self.frm_status.columnconfigure(1, weight=1)
        self.frm_status.columnconfigure(2, weight=1)
        # self.frm_status.columnconfigure(6, weight=1)
        self.frm_status.columnconfigure(7, weight=1)

        self.create_frm()
        self.create_frm_status()

    def create_frm(self):
        """
        添加水平方向的推拉窗组件
        """
        self.panewin = ttk.Panedwindow(self.frm, orient=tk.HORIZONTAL)
        self.panewin.grid(row=0, column=0, sticky=tk.NSEW)  # 向四个方向拉伸填满MWindow帧

        """
        上半部分窗口分为左右2个部分
        """
        self.frm_left = ttk.LabelFrame(self.panewin)
        self.frm_right = ttk.LabelFrame(self.panewin)

        self.frm_left.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.frm_right.grid(row=0, column=1, padx=0, pady=0, sticky="wesn")

        self.frm_left.rowconfigure(0, weight=1)
        self.frm_left.rowconfigure(1, weight=1)
        self.frm_left.columnconfigure(0, weight=1)

        self.panewin.add(self.frm_left, weight=1)  # 将左侧Frame帧添加到推拉窗控件，左侧权重1

        self.frm_right.rowconfigure(0, weight=1)
        self.frm_right.rowconfigure(1, weight=1)
        self.frm_right.columnconfigure(0, weight=1)

        self.panewin.add(self.frm_right, weight=50)  # 将右侧Frame帧添加到推拉窗控件,右侧权重50

        self.create_frm_left()
        self.create_frm_right()

    def create_frm_left(self):
        """
        左边窗口,分上下两个Notebook
        """
        self.frm_left_notebook1 = ttk.Notebook(self.frm_left)
        self.frm_left_notebook2 = ttk.Notebook(self.frm_left)

        self.frm_left_notebook1.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.frm_left_notebook2.grid(row=1, column=0, padx=0, pady=0, sticky="wesn")

        #  拉升
        self.frm_left_notebook1.rowconfigure(0, weight=1)
        self.frm_left_notebook1.columnconfigure(0, weight=1)

        self.frm_left_notebook2.rowconfigure(0, weight=1)
        self.frm_left_notebook2.columnconfigure(0, weight=1)

        self.create_frm_left_notebook1()
        self.create_frm_left_notebook2()

    def create_frm_left_notebook1(self):
        """
        frame1 ：serial
        frame2 ：Mqtt
        """
        self.frm_left_notebook1_frame1 = ttk.Frame(self.frm_left_notebook1)
        self.frm_left_notebook1_frame2 = ttk.Frame(self.frm_left_notebook1)

        self.frm_left_notebook1_frame1.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.frm_left_notebook1_frame2.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")

        # self.frm_left_notebook1_frame1.rowconfigure(0, weight=1)
        self.frm_left_notebook1_frame1.columnconfigure(0, weight=1)
        # self.frm_left_notebook1_frame2.rowconfigure(0, weight=1)
        self.frm_left_notebook1_frame2.columnconfigure(0, weight=1)

        self.frm_left_notebook1.add(self.frm_left_notebook1_frame1, text='Serial')
        self.frm_left_notebook1.add(self.frm_left_notebook1_frame2, text='Mqtt')

        self.create_frm_left_notebook1_frame1_serial_set()
        self.create_frm_left_notebook1_frame2_mqtt_set()

    def create_frm_left_notebook1_frame1_serial_set(self):
        """
        frame1 ：serial
        Listbox显示可用的COM口
        Button按钮点击连接设备
        """
        # self.serial_set_label = ttk.Label(self.frm_left_notebook1_frame1,
        #                                      text="Serial Ports",
        #                                      font=font)

        # self.frm_left_listbox = pytk.PyListbox(self.frame1,
        #                                        height=size_dict[
        #                                            "list_box_height"],
        #                                        font=font)
        self.serial_set_frame = ttk.LabelFrame(self.frm_left_notebook1_frame1)
        self.serial_set_btn = ttk.Button(self.frm_left_notebook1_frame1,
                                         text="Open",
                                         font=font)

        # self.serial_set_label.grid(row=0, column=0, padx=0, pady=0, sticky="ws")
        # self.frm_left_listbox.grid(
        #     row=1, column=0, padx=0, pady=0, sticky="wesn")
        self.serial_set_frame.grid(
            row=1, column=0, padx=0, pady=0, sticky="wesn")
        self.serial_set_btn.grid(row=2, column=0, padx=0, pady=0, sticky="wesn")
        # 拉伸
        # self.serial_set_label.rowconfigure(0, weight=1)
        # self.serial_set_label.columnconfigure(0, weight=1)
        # self.serial_set_frame.rowconfigure(0, weight=1)
        # self.serial_set_frame.columnconfigure(0, weight=1)
        self.serial_set_frame.columnconfigure(1, weight=5)
        # self.serial_set_btn.rowconfigure(0, weight=1)
        # self.serial_set_btn.columnconfigure(0, weight=1)

        # self.frm_left_listbox.bind("<Double-Button-1>", self.Open)
        self.serial_set_btn.bind("<Button - 1>", self.serial_set_btn_event)

        self.create_serial_set_frame()

    def create_serial_set_frame(self):
        """
        串口配置，比如波特率，奇偶校验等
        """

        # Create a combobox containing the available COM ports
        comlst = self.get_comlst()

        setting_label_list = ["Serial Ports", "BaudRate :",
                              "Parity :", "DataBit :", "StopBit :"]
        baudrate_list = ["1200", "2400", "4800", "9600", "14400", "19200", "38400",
                         "43000", "57600", "76800", "115200"]
        # PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
        parity_list = ["N", "E", "O", "M", "S"]
        bytesize_list = ["5", "6", "7", "8"]
        stopbits_list = ["1", "1.5", "2"]
        for index, item in enumerate(setting_label_list):
            serial_set_label_temp = ttk.Label(self.serial_set_frame,
                                              text=item,
                                              font=font_label_temp)
            serial_set_label_temp.grid(
                row=index, column=0, padx=1, pady=0, sticky="e")

        self.frm_left_combobox_serialport = ttk.Combobox(self.serial_set_frame,
                                                         width=15,
                                                         values=comlst,
                                                         textvariable=self.TKvariables['serial_port'],
                                                         postcommand=self.update_com_box)

        self.frm_left_combobox_baudrate = ttk.Combobox(self.serial_set_frame,
                                                       width=15,
                                                       values=baudrate_list,
                                                       textvariable=self.TKvariables['baudrate'])
        self.frm_left_combobox_parity = ttk.Combobox(self.serial_set_frame,
                                                     width=15,
                                                     values=parity_list,
                                                     textvariable=self.TKvariables['parity'])
        self.frm_left_combobox_databit = ttk.Combobox(self.serial_set_frame,
                                                      width=15,
                                                      values=bytesize_list,
                                                      textvariable=self.TKvariables['bytesize'])
        self.frm_left_combobox_stopbit = ttk.Combobox(self.serial_set_frame,
                                                      width=15,
                                                      values=stopbits_list,
                                                      textvariable=self.TKvariables['stopbits'])

        self.frm_left_combobox_serialport.grid(
            row=0, column=1, padx=0, pady=0, sticky="we")
        self.frm_left_combobox_baudrate.grid(
            row=1, column=1, padx=0, pady=0, sticky="we")
        self.frm_left_combobox_parity.grid(
            row=2, column=1, padx=0, pady=0, sticky="we")
        self.frm_left_combobox_databit.grid(
            row=3, column=1, padx=0, pady=0, sticky="we")
        self.frm_left_combobox_stopbit.grid(
            row=4, column=1, padx=0, pady=0, sticky="we")

        # self.frm_left_combobox_serialport.current(0)
        self.frm_left_combobox_baudrate.current(10)
        self.frm_left_combobox_parity.current(0)
        self.frm_left_combobox_databit.current(3)
        self.frm_left_combobox_stopbit.current(0)

        self.frm_left_combobox_serialport.bind(
            '<<ComboboxSelected>>', self.serial_combobox_serialport_sel_event)
        self.frm_left_combobox_baudrate.bind(
            '<<ComboboxSelected>>', self.serial_combobox_baudrate_sel_event)
        self.frm_left_combobox_parity.bind(
            '<<ComboboxSelected>>', self.serial_combobox_parity_sel_event)
        self.frm_left_combobox_databit.bind(
            '<<ComboboxSelected>>', self.serial_combobox_bytesize_sel_event)
        self.frm_left_combobox_stopbit.bind(
            '<<ComboboxSelected>>', self.serial_combobox_stopbits_sel_event)

    def create_frm_left_notebook1_frame2_mqtt_set(self):
        pass

    def create_frm_left_notebook2(self):
        """
        notebook2 ：id string and id format
        """
        self.frm_left_notebook2_frame1 = ttk.Frame(self.frm_left_notebook2)
        self.frm_left_notebook2_frame2 = ttk.Frame(self.frm_left_notebook2)

        self.frm_left_notebook2.add(self.frm_left_notebook2_frame1, text='IDString')
        self.frm_left_notebook2.add(self.frm_left_notebook2_frame2, text='IDFormat')

        # frm_left_notebook2_frame1 列拉伸
        self.frm_left_notebook2_frame1.columnconfigure(0, weight=1)

        # frm_left_notebook2_frame2 列拉伸
        self.frm_left_notebook2_frame2.columnconfigure(0, weight=1)

        self.create_frm_left_notebook2_frame1_id_string()
        self.create_frm_left_notebook2_frame2_id_format()

    def create_frm_left_notebook2_frame1_id_string(self):
        """
        frame1 ：id string
        layout:frame
        frame r 0 c 0
        (label ) receive string
        frame r 1 c 0
        (label frame)
            1(radiobutton) ascii or hex
            2(Entry) linefeed ms

        frame r 2 c 0
        (label ) send string
        frame r 3 c 0
        (label frame)
            1(radiobutton)ascii or hex
            2(Entry) schedule send ms
            3(Checkbutton)CRLF
        """
        self.id_string_r0_label = ttk.Label(self.frm_left_notebook2_frame1,
                                            text="receive setting",
                                            font=font)
        self.id_string_r1_frame = ttk.LabelFrame(self.frm_left_notebook2_frame1)
        self.id_string_r2_label = ttk.Label(self.frm_left_notebook2_frame1,
                                            text="send setting",
                                            font=font)
        self.id_string_r3_frame = ttk.LabelFrame(self.frm_left_notebook2_frame1)

        self.id_string_r0_label.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.id_string_r1_frame.grid(row=1, column=0, padx=0, pady=0, sticky="wesn")
        self.id_string_r2_label.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.id_string_r3_frame.grid(row=3, column=0, padx=0, pady=0, sticky="wesn")

        # id_string_r1_frame c1拉伸
        self.id_string_r1_frame.columnconfigure(1, weight=5)
        # id_string_r3_frame c1拉伸
        self.id_string_r3_frame.columnconfigure(1, weight=5)

        self.create_id_string_r1_frame()
        self.create_id_string_send_frame()

    def create_id_string_r1_frame(self):
        """
        1(radiobutton) ascii or hex
        2(Entry) linefeed ms
        """

        __MODES = [
            (0, "ascii", 0),
            (1, "hex", 1),
        ]
        # self.r1_rb_v = tk.StringVar()
        # self.r1_rb_v.set("0")  # initialize
        # print('r1_rb_v.get()' + self.r1_rb_v.get())
        # index = 0
        for index, text, mode in __MODES:
            b = ttk.Radiobutton(self.id_string_r1_frame,
                                text=text,
                                variable=self.TKvariables['rec_hex_ascii'],
                                value=mode,
                                command=self.id_string_r1_radiobutton_cb)
            b.grid(row=index, column=0, padx=1, pady=0, sticky="w")

        c = ttk.Checkbutton(self.id_string_r1_frame, text="linefeed(ms)",
                            variable=self.TKvariables['linefeed'],
                            command=self.id_string_r1_checkbutton_cb)
        c.grid(row=2, column=0, padx=1, pady=0, sticky="w")

        self.id_string_r1_linefeed_entry = ttk.Entry(
            self.id_string_r1_frame,
            textvariable=self.TKvariables['linefeedtime'],
            font=font)
        self.id_string_r1_linefeed_entry.grid(row=2, column=1, padx=0, pady=0, sticky="we")

    def create_id_string_send_frame(self):
        """
        frame r 0 c 0        |  frame r 0 c 1
        (radiobutton)ascii   |  (radiobutton)hex
        frame r 1 c 0        |  frame r 1 c 1
        (Checkbutton)schedule
                send ms     |  (Entry)
        frame r 2 c 1
        (Checkbutton)CRLF
        """

        __MODES = [
            (0, "ascii", "0"),
            (1, "hex", "1"),
        ]
        # self.id_string_send_rb_v = tk.StringVar()
        # self.id_string_send_rb_v.set("0")  # initialize
        # print('r3_rb_v.get()' + self.id_string_send_rb_v.get())
        # index = 0
        for index, text, mode in __MODES:
            b = ttk.Radiobutton(self.id_string_r3_frame,
                                text=text,
                                variable=self.id_string_send_rb_v,
                                value=mode,
                                command=self.id_string_send_radiobutton_cb)
            b.grid(row=0, column=index, padx=1, pady=0, sticky="w")
            # index += 1

        self.id_string_send_cb_v = tk.IntVar()
        self.id_string_send_cb_v.set(0)  # initialize

        c = ttk.Checkbutton(self.id_string_r3_frame, text="schedule send(ms)",
                            variable=self.id_string_send_cb_v,
                            command=self.id_string_send_checkbutton_cb)
        c.grid(row=1, column=0, padx=1, pady=0, sticky="w")

        self.schedule_send = tk.StringVar()
        self.id_string_schedule_send_entry = ttk.Entry(self.id_string_r3_frame,
                                                       textvariable=self.schedule_send,
                                                       font=font)
        self.id_string_schedule_send_entry.grid(row=1, column=1, padx=0, pady=0, sticky="we")

        self.id_string_send_CRLF_cb_v = tk.IntVar()
        self.id_string_send_CRLF_cb_v.set(0)  # initialize
        d = ttk.Checkbutton(self.id_string_r3_frame, text="CRLF",
                            variable=self.id_string_send_CRLF_cb_v,
                            command=self.id_string_send_CRLF_checkbutton_cb)
        d.grid(row=2, column=0, padx=1, pady=0, sticky="w")

    def create_frm_left_notebook2_frame2_id_format(self):
        """
        frame1 ：id format
        layout:frame

        frame r 0 c 0          |  frame r 0 c 1
        (label ) ID标识符       |  (Entry)
        frame r 1 c 0          |  frame r 2 c 1
        (label ) 帧长         |  (Entry readonly)
        frame r 2 c 0          |   c 1
          (label ) 效验         |  Combobox  none 16crc  16sum  8sum
        frame r 3 c 0          |   c 1
          (label ) 效验格式     |  (Entry)
        frame r 4 c 0          |   c 1
        (label ) ID进制        |  (Combobox ) Ascii Hex
        frame r 5 c 0           |  c 1
        (label ) ID段号             | (Entry)
        frame r 6 c 1
        (btn) 生成
        frame r 7 c 1
        (btn) 重新补号
        frame r 8 c 0-1
        (text ) id   说明
        """

        self.id_format_frame = ttk.LabelFrame(self.frm_left_notebook2_frame2)
        self.id_format_frame.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")

        # 拉伸
        self.id_format_frame.columnconfigure(1, weight=5)

        # id 格式说明

        id_text = '''说明：
                    1.ID标识符字段:至少3个字符
                    2.ID号字段:用XX表示
                    3.ID校验字段:用KK表示
                    4.可变字符用NN表示
                    5.ID进制：dec十进制，hex十六进制
                    6.ID段号:101-200|232|253,-表示范围,|表示增加条件，进制和ID进制保持一致
                    7.空格会被忽视
                    '''

        setting_label_list = ["帧格式:",
                              # "ID号 :",
                              "帧长 :",
                              "效验 :",
                              "效验格式 :",
                              "ID进制 :",
                              "ID段号 :",
                              ]

        for index, item in enumerate(setting_label_list):
            a = ttk.Label(self.id_format_frame, text=item, font=font_label_temp)
            a.grid(row=index, column=0, padx=1, pady=0, sticky="e")

        self.id_format_frame_id_frame_entry = ttk.Entry(self.id_format_frame,
                                                        textvariable=self.TKvariables['帧格式'],
                                                        font=font_label_temp)

        self.id_format_frame_id_frame_entry.bind('<Button-1 >',
                                                 self.id_format_frame_id_frame_entry_event)
        self.id_format_frame_id_frame_entry.bind('<Key >',
                                                 self.id_format_frame_id_frame_entry_event)
        self.id_format_frame_id_frame_entry.bind(
            "<Button-3>",
            lambda x: self.right_key_event(
                x,
                self.id_format_frame_id_frame_entry))  # 绑定右键鼠标事件
        # self.id_format_frame_id_id_entry = ttk.Entry(self.id_format_frame,
        #                                                    textvariable=self.TKvariables['ID号'],
        #                                                    font=font_label_temp)

        self.id_format_frame_len_entry = ttk.Entry(self.id_format_frame,
                                                   textvariable=self.TKvariables[DEF_FRAME_LEN],
                                                   font=font_label_temp)
        self.id_format_frame_len_entry.bind('<Button-1 >',
                                            self.id_format_frame_len_entry_event)

        self.TKvariables[DEF_FRAME_LEN].set(len(self.id_format_frame_id_frame_entry.get()))
        self.id_format_frame_len_entry.config(state='disable')

        # __MODES = [
        #     (0, "Ascii", 0),
        #     (1, "Hex", 1),
        # ]

        # index = 0
        # for index, text, mode in __MODES:
        #     b = ttk.Radiobutton(self.id_format_frame,
        #                            text=text,
        #                            variable=self.TKvariables['rec_hex_ascii2'],
        #                            value=mode,
        #                            command=self.id_format_frame_type_radiobutton_cb)
        #
        #     b.grid(row=index+2, column=1, padx=1, pady=0, sticky="w")

        frame_check_type = [CHECK_TYPE_NONE, CHECK_TYPE_CRC, CHECK_TYPE_2CRC,
                            CHECK_TYPE_SUM, CHECK_TYPE_2SUM, CHECK_TYPE_XOR, CHECK_TYPE_2XOR]
        self.id_string_combobox_frame_check = ttk.Combobox(self.id_format_frame,
                                                           values=frame_check_type,
                                                           textvariable=self.TKvariables[DEF_CHECK])
        self.id_string_combobox_frame_check.current(0)

        ah = ["dec", "hex"]
        self.id_string_combobox_frame_type = ttk.Combobox(self.id_format_frame,
                                                          values=ah,
                                                          textvariable=self.TKvariables[def_id_type])
        self.id_string_combobox_frame_type.current(1)
        self.id_format_id_check_entry = ttk.Entry(self.id_format_frame,
                                                  textvariable=self.TKvariables[DEF_CHECK_TYPE],
                                                  font=font_label_temp)
        self.id_format_id_check_entry.bind(
            "<Button-3>",
            lambda x: self.right_key_event(
                x,
                self.id_format_id_check_entry))  # 绑定右键鼠标事件

        self.id_format_id_entry = ttk.Entry(self.id_format_frame,
                                            textvariable=self.TKvariables['id'],
                                            font=font_label_temp)
        self.id_format_id_entry.bind(
            "<Button-3>",
            lambda x: self.right_key_event(
                x,
                self.id_format_id_entry))  # 绑定右键鼠标事件

        self.id_format_gen_btn = ttk.Button(self.id_format_frame,
                                            text="生成",
                                            font=font)

        self.id_format_gen_btn.bind('<Button-1 >',
                                    self.id_format_gen_btn_event)

        self.id_format_restart_btn = ttk.Button(self.id_format_frame,
                                                text="重新计数",
                                                font=font)

        self.id_format_restart_btn.bind('<Button-1 >',
                                    self.id_format_restart_btn_event)

        self.id_format_id_ex = tk.Text(self.id_format_frame,
                                       fg='#ABB2B9',
                                       height=10,
                                       width=40,
                                       font=font_label_temp)
        # str = id_text.split('\n')

        s = re.split(r'\n\s\s*', id_text)

        for i in s:
            i += '\n'
            self.id_format_id_ex.insert(tk.END, i)

        self.id_format_id_ex.config(state='disable')

        self.id_format_frame_id_frame_entry.grid(row=0, column=1, padx=0, pady=0, sticky="we")
        # self.id_format_frame_id_id_entry.grid(row=1, column=1, padx=0, pady=0, sticky="we")
        self.id_format_frame_len_entry.grid(row=1, column=1, padx=0, pady=0, sticky="we")
        self.id_string_combobox_frame_check.grid(row=2, column=1, padx=0, pady=0, sticky="we")
        self.id_format_id_check_entry.grid(row=3, column=1, padx=0, pady=0, sticky="we")
        self.id_string_combobox_frame_type.grid(row=4, column=1, padx=0, pady=0, sticky="we")
        self.id_format_id_entry.grid(row=5, column=1, padx=1, pady=0, sticky="we")
        self.id_format_gen_btn.grid(row=6, column=0, columnspan=2, padx=1, pady=0, sticky="we")
        self.id_format_restart_btn.grid(row=7, column=0, columnspan=2, padx=0, pady=0, sticky="we")
        self.id_format_id_ex.grid(row=8, column=0, columnspan=2, padx=1, pady=0, sticky="we")

    def create_frm_right(self):
        """
        上半部分右边窗口：
        分为上下两个部分，放一个垂直拉伸窗：
        """

        """
        添加垂直方向的推拉窗组件
        """
        self.frm_right_panewin = ttk.Panedwindow(self.frm_right, orient=tk.VERTICAL)
        self.frm_right_panewin.grid(row=0, column=0, sticky=tk.NSEW)  # 向四个方向拉伸填满MWindow帧

        """
        上半部分窗口分为左右2个部分
        """
        self.frm_right_tag_info = ttk.LabelFrame(self.frm_right_panewin)
        self.frm_right_log = ttk.LabelFrame(self.frm_right_panewin)

        self.frm_right_tag_info.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.frm_right_log.grid(row=1, column=0, padx=0, pady=0, sticky="wesn")

        self.frm_right_tag_info.rowconfigure(0, weight=10)
        self.frm_right_tag_info.columnconfigure(0, weight=1)
        self.frm_right_tag_info.columnconfigure(1, weight=1)
        self.frm_right_tag_info.columnconfigure(2, weight=1)

        self.frm_right_log.rowconfigure(0, weight=1)
        self.frm_right_log.columnconfigure(0, weight=1)

        self.frm_right_panewin.add(self.frm_right_tag_info, weight=10)  # 将上侧Frame帧添加到推拉窗控件，权重50
        self.frm_right_panewin.add(self.frm_right_log, weight=1)  # 将下侧Frame帧添加到推拉窗控件, 权重1

        self.create_frm_right_tag_info()
        self.create_frm_right_log()

    def create_frm_right_tag_info(self):
        """
        3 列
        1 available
        2 invalid
        3 total
        """
        # self.frm_right_tag_info_available = ttk.LabelFrame(self.frm_right_tag_info, width=250, height=500)
        # self.frm_right_tag_info_invalid = ttk.LabelFrame(self.frm_right_tag_info, width=250, height=500)
        # self.frm_right_tag_info_total = ttk.LabelFrame(self.frm_right_tag_info, width=250, height=500)

        self.frm_right_tag_info_available = ttk.LabelFrame(self.frm_right_tag_info)
        self.frm_right_tag_info_invalid = ttk.LabelFrame(self.frm_right_tag_info)
        self.frm_right_tag_info_total = ttk.LabelFrame(self.frm_right_tag_info)

        self.frm_right_tag_info_available.grid(
            row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.frm_right_tag_info_invalid.grid(
            row=0, column=1, padx=0, pady=0, sticky="wesn")
        self.frm_right_tag_info_total.grid(
            row=0, column=2, padx=0, pady=0, sticky="wesn")

        # self.frm_right_tag_info_available.grid(
        #     row=0, column=0, padx=0, pady=0)
        # self.frm_right_tag_info_invalid.grid(
        #     row=0, column=1, padx=0, pady=0)
        # self.frm_right_tag_info_total.grid(
        #     row=0, column=2, padx=0, pady=0)

        # self.frm_right_tag_info_available.grid_propagate(0)
        # self.frm_right_tag_info_invalid.grid_propagate(0)
        # self.frm_right_tag_info_total.grid_propagate(0)
        # self.frm_right_tag_info_available.rowconfigure(0, weight=1)
        # self.frm_right_tag_info_available.rowconfigure(1, weight=1)
        self.frm_right_tag_info_available.rowconfigure(2, weight=10)
        # self.frm_right_tag_info_available.columnconfigure(0, weight=1)
        self.frm_right_tag_info_available.columnconfigure(1, weight=1)

        # self.frm_right_tag_info_invalid.rowconfigure(0, weight=1)
        # self.frm_right_tag_info_invalid.rowconfigure(1, weight=1)
        self.frm_right_tag_info_invalid.rowconfigure(2, weight=10)
        # self.frm_right_tag_info_invalid.columnconfigure(0, weight=1)
        self.frm_right_tag_info_invalid.columnconfigure(1, weight=1)

        # self.frm_right_tag_info_total.rowconfigure(0, weight=1)
        # self.frm_right_tag_info_total.rowconfigure(1, weight=1)
        self.frm_right_tag_info_total.rowconfigure(2, weight=10)
        # self.frm_right_tag_info_total.columnconfigure(0, weight=1)
        self.frm_right_tag_info_total.columnconfigure(1, weight=1)

        # self.frm_right_tag_info_available.grid_rowconfigure(0, weight=1)
        # self.frm_right_tag_info_available.grid_columnconfigure(0, weight=1)
        # self.frm_right_tag_info_invalid.grid_rowconfigure(0, weight=1)
        # self.frm_right_tag_info_invalid.grid_columnconfigure(0, weight=1)
        # self.frm_right_tag_info_total.grid_rowconfigure(0, weight=1)
        # self.frm_right_tag_info_total.grid_columnconfigure(0, weight=1)

        self.create_frm_right_tag_info_available()
        self.create_frm_right_tag_info_invalid()
        self.create_frm_right_tag_info_total()

    def create_frm_right_tag_info_available(self):
        """
        frame ：frm_right_tag_info_available
        layout:frame
        frame r 0 c 0            |  frame r 0 c 1
        (label ) 实际可用标签数   |  (text)
        frame r 1 c 0
        (label) 实际可用标签
        frame r 2 c 0    columnspan=2
        (text  Scrollbar)
        """
        self.tag_info_available_label_num = ttk.Label(
            self.frm_right_tag_info_available,
            text="实际可用标签数",
            font=font_label_temp)

        self.tag_info_available_label_num_entry = ttk.Entry(
            self.frm_right_tag_info_available,
            textvariable=self.TKvariables[DEF_AVAILABLE_ID_NUM],
            font=font_label_temp)

        self.tag_info_available_text_frame = ttk.LabelFrame(
            self.frm_right_tag_info_available)

        self.tag_info_available_label_num.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.tag_info_available_label_num_entry.grid(
            row=0, column=1, padx=0, pady=0, sticky="w")
        self.tag_info_available_text_frame.grid(
            row=2, column=0, columnspan=2, padx=0, pady=0, sticky="wesn")

        self.tag_info_available_text_frame.rowconfigure(1, weight=1)
        self.tag_info_available_text_frame.columnconfigure(0, weight=1)

        self.tag_info_available_label = ttk.Label(
            self.tag_info_available_text_frame,
            text="实际可用标签",
            font=font_label_temp)

        self.tag_info_available_scrollbar = ttk.Scrollbar(
            self.tag_info_available_text_frame)

        self.tag_info_available_listbox = tk.Text(
            self.tag_info_available_text_frame,
            width=50,
            height=100,
            yscrollcommand=self.tag_info_available_scrollbar.set)

        self.tag_info_available_label.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.tag_info_available_listbox.grid(
            row=1, column=0, padx=0, pady=0, sticky="wesn")
        self.tag_info_available_scrollbar.grid(
            row=1, column=1, padx=0, pady=0, sticky="esn")

        self.tag_info_available_scrollbar.config(command=self.tag_info_available_listbox.yview)

    def create_frm_right_tag_info_invalid(self):
        """
        frame ：frm_right_tag_info_available
        layout:frame
        frame r 0 c 0            |  frame r 0 c 1
        (label ) 实际可用标签数   |  (text)
        frame r 1 c 0
        (label) 实际可用标签
        frame r 2 c 0    columnspan=2
        (text  Scrollbar)
        """
        self.tag_info_invalid_label_num = ttk.Label(
            self.frm_right_tag_info_invalid,
            text="实际无效标签数",
            font=font_label_temp)

        self.tag_info_invalid_label_num_entry = ttk.Entry(
            self.frm_right_tag_info_invalid,
            textvariable=self.TKvariables[DEF_INVALID_ID_NUM],
            font=font_label_temp)

        self.tag_info_invalid_text_frame = ttk.LabelFrame(self.frm_right_tag_info_invalid)

        self.tag_info_invalid_label_num.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.tag_info_invalid_label_num_entry.grid(
            row=0, column=1, padx=0, pady=0, sticky="w")
        self.tag_info_invalid_text_frame.grid(
            row=2, column=0, columnspan=2, padx=0, pady=0, sticky="wesn")

        self.tag_info_invalid_text_frame.rowconfigure(1, weight=1)
        self.tag_info_invalid_text_frame.columnconfigure(0, weight=1)

        self.tag_info_invalid_label = ttk.Label(
            self.tag_info_invalid_text_frame,
            text="实际无效标签",
            font=font_label_temp)

        self.tag_info_invalid_scrollbar = ttk.Scrollbar(self.tag_info_invalid_text_frame)

        self.tag_info_invalid_listbox = tk.Text(
            self.tag_info_invalid_text_frame,
            width=50,
            height=100,
            yscrollcommand=self.tag_info_invalid_scrollbar.set)

        self.tag_info_invalid_label.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.tag_info_invalid_listbox.grid(
            row=1, column=0, padx=0, pady=0, sticky="wesn")
        self.tag_info_invalid_scrollbar.grid(
            row=1, column=1, padx=0, pady=0, sticky="esn")

        self.tag_info_invalid_scrollbar.config(command=self.tag_info_invalid_listbox.yview)

    def create_frm_right_tag_info_total(self):
        """
        frame ：frm_right_tag_info_available
        layout:frame
        frame r 0 c 0            |  frame r 0 c 1
        (label ) 实际可用标签数   |  (text)
        frame r 1 c 0
        (label) 实际可用标签
        frame r 2 c 0    columnspan=2
        (text  Scrollbar)
        """
        self.tag_info_total_label_num = ttk.Label(
            self.frm_right_tag_info_total,
            text="未检测到标签数",
            font=font_label_temp)

        self.tag_info_total_label_num_entry = ttk.Entry(
            self.frm_right_tag_info_total,
            textvariable=self.TKvariables[DEF_TOTAL_ID_NUM],
            font=font_label_temp)

        self.tag_info_total_text_frame = ttk.LabelFrame(self.frm_right_tag_info_total)

        self.tag_info_total_label_num.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.tag_info_total_label_num_entry.grid(
            row=0, column=1, padx=0, pady=0, sticky="w")
        self.tag_info_total_text_frame.grid(
            row=2, column=0, columnspan=2, padx=0, pady=0, sticky="wesn")

        self.tag_info_total_text_frame.rowconfigure(1, weight=1)
        self.tag_info_total_text_frame.columnconfigure(0, weight=1)

        self.tag_info_total_label = ttk.Label(
            self.tag_info_total_text_frame,
            text="未检测到标签",
            font=font_label_temp)

        self.tag_info_total_scrollbar = ttk.Scrollbar(self.tag_info_total_text_frame)

        self.tag_info_total_listbox = tk.Text(
            self.tag_info_total_text_frame,
            width=50,
            height=100,
            yscrollcommand=self.tag_info_total_scrollbar.set)

        self.tag_info_total_listbox.bind(
            "<Button-3>",
            lambda x: self.right_key_event(
                x,
                self.tag_info_total_listbox))  # 绑定右键鼠标事件

        self.tag_info_total_label.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.tag_info_total_listbox.grid(
            row=1, column=0, padx=0, pady=0, sticky="wesn")
        self.tag_info_total_scrollbar.grid(
            row=1, column=1, padx=0, pady=0, sticky="esn")

        self.tag_info_total_scrollbar.config(command=self.tag_info_total_listbox.yview)

        # t = time.time()
        # for i in range(1000):
        #     start = datetime.now()
        #     self.tag_info_total_listbox.insert(tk.END, i)
        #     self.tag_info_total_listbox.see(tk.END)
        #     # print('count %d leedting = %fms' %
        #     #       (i, time.time()-t))
        #     # time.sleep(0.009)
        #     # t = time.time()
        #     end = datetime.now()
        #     print('count %d leedting = %ss' % (i,(end - start)))

        str1 = 'ID:xxxxxxxx\r\n'
        for i in range(10):
            s = str(i)
            s = s.zfill(8)
            s = str1.replace('xxxxxxxx', s)
            # start = datetime.now()
            start = time.time()
            self.tag_info_total_listbox.insert(tk.END, s)
            self.tag_info_total_listbox.see(tk.END)
            # print('count %d leedting = %fms' %
            #       (i, time.time()-t))
            # time.sleep(0.009)
            # t = time.time()
            # end = datetime.now()
            end = time.time()
            print('count %d leedting = %5fs' % (i, (end - start)))
            # print('count %d leedting = %ss' % (i, (end - start)))

        print(self.tag_info_total_listbox.get("1.0", tk.END))

        # self.tag_info_total_listbox.delete(
        #     len(self.tag_info_total_listbox.get("1.0", tk.END))-2, tk.END)
        print(self.tag_info_total_listbox.index('2.3'))

        self.tag_info_total_listbox.delete('2.3', '3.0')
        # for i in range(10):
        #     s = str(i)
        #     s = s.zfill(8)
        #     s = str1.replace('xxxxxxxx', s)
        #     # start = datetime.now()
        #     start = time.time()
        #     print('count=',str(i),'index=',self.tag_info_total_listbox.index(i+1))
        #     # self.tag_info_total_listbox.see(tk.END)
        #     # print('count %d leedting = %fms' %
        #     #       (i, time.time()-t))
        #     # time.sleep(0.009)
        #     # t = time.time()
        #     # end = datetime.now()
        #     end = time.time()
        #     print('count %d leedting = %5fs' % (i, (end - start)))
        #     # print('count %d leedting = %ss' % (i, (end - start)))

    def create_frm_right_log(self):
        """
        两个Notebook
        """
        self.frm_right_log_notebook = ttk.Notebook(self.frm_right_log)

        self.frm_right_log_notebook.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")

        #  拉升
        self.frm_right_log_notebook.rowconfigure(0, weight=1)
        self.frm_right_log_notebook.columnconfigure(0, weight=1)

        self.create_frm_right_log_notebook()

    def create_frm_right_log_notebook(self):
        """
        frame1 ：data
        frame2 ：log
        """
        self.frm_right_log_notebook_frame1 = ttk.Frame(self.frm_right_log_notebook)
        self.frm_right_log_notebook_frame2 = ttk.Frame(self.frm_right_log_notebook)
        # self.frm_right_log_notebook_frame1 = ttk.Frame(self.frm_right_log_notebook,height=200)
        # self.frm_right_log_notebook_frame2 = ttk.Frame(self.frm_right_log_notebook,height=200)

        self.frm_right_log_notebook_frame1.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.frm_right_log_notebook_frame2.grid(row=0, column=0, padx=0, pady=0, sticky="wesn")
        # self.frm_right_log_notebook_frame1.grid_propagate(0)
        # self.frm_right_log_notebook_frame2.grid_propagate(0)

        self.frm_right_log_notebook_frame1.rowconfigure(0, weight=1)
        self.frm_right_log_notebook_frame1.columnconfigure(0, weight=1)
        self.frm_right_log_notebook_frame2.rowconfigure(0, weight=1)
        self.frm_right_log_notebook_frame2.columnconfigure(0, weight=50)

        self.frm_right_log_notebook.add(self.frm_right_log_notebook_frame1, text='数据')
        self.frm_right_log_notebook.add(self.frm_right_log_notebook_frame2, text='日志')

        self.create_frm_right_log_notebook_frame1()
        self.create_frm_right_log_notebook_frame2()

    def create_frm_right_log_notebook_frame1(self):

        self.log_notebook_frame1_scrollbar = ttk.Scrollbar(self.frm_right_log_notebook_frame1)

        self.log_notebook_frame1_data = tk.Text(
            self.frm_right_log_notebook_frame1,
            # height=15,
            yscrollcommand=self.log_notebook_frame1_scrollbar.set)

        self.log_notebook_frame1_data.grid(
            row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.log_notebook_frame1_scrollbar.grid(
            row=0, column=1, padx=0, pady=0, sticky="esn")

        self.log_notebook_frame1_scrollbar.config(command=self.log_notebook_frame1_data.yview)
        # self.log_notebook_frame1_scrollbar.bind('<Button-1 >', self.log_notebook_frame1_scrollbar_event)
        self.log_notebook_frame1_scrollbar.bind('<B1-Motion>', self.log_notebook_frame1_scrollbar_event)

    def create_frm_right_log_notebook_frame2(self):

        self.log_notebook_frame2_scrollbar = ttk.Scrollbar(self.frm_right_log_notebook_frame2)

        self.log_notebook_frame2_data = tk.Text(
            self.frm_right_log_notebook_frame2,
            # height=15,
            yscrollcommand=self.log_notebook_frame2_scrollbar.set)

        self.log_notebook_frame2_data.grid(
            row=0, column=0, padx=0, pady=0, sticky="wesn")
        self.log_notebook_frame2_scrollbar.grid(
            row=0, column=1, padx=0, pady=0, sticky="esn")

        self.log_notebook_frame2_scrollbar.config(command=self.log_notebook_frame2_data.yview)
        # self.log_notebook_frame2_scrollbar.bind('<Button-1 >', self.log_notebook_frame1_scrollbar_event)
        self.log_notebook_frame2_scrollbar.bind('<B1-Motion>', self.log_notebook_frame1_scrollbar_event)

    def create_frm_status(self):
        """
        底部状态栏窗口

        r 0 c 0       |   r 0 c 3      |    r 0 c 4  |   r 0 c 6         |   r 0 c 7
        (label) ready |   Send(bytes): |   0         |   Receive(bytes): |   0

        """
        self.frm_status_label = ttk.Label(self.frm_status,
                                          text="Closed",
                                          font=font_label_temp)
        self.frm_status_send_bytes = ttk.Label(self.frm_status,
                                               text="Send(bytes):",
                                               font=font_label_temp)
        self.frm_status_send_bytes_num = ttk.Label(self.frm_status,
                                                   text="0",
                                                   font=font_label_temp)

        self.frm_status_receive_bytes = ttk.Label(self.frm_status,
                                                  text="Receive(bytes):",
                                                  font=font_label_temp)
        self.frm_status_receive_bytes_num = ttk.Label(self.frm_status,
                                                      text="0",
                                                      # values=self.TKvariables['rec_count'],
                                                      font=font_label_temp)
        self.frm_status_label.grid(
            row=0, column=0, padx=0, pady=0, sticky="w")
        self.frm_status_send_bytes.grid(
            row=0, column=1, padx=0, pady=0, sticky="w")
        self.frm_status_send_bytes_num.grid(
            row=0, column=2, padx=0, pady=0, sticky="w")
        self.frm_status_receive_bytes.grid(
            row=0, column=6, padx=0, pady=0, sticky="w")
        self.frm_status_receive_bytes_num.grid(
            row=0, column=7, padx=0, pady=0, sticky="w")

    def menu_click_event(self):
        """
        菜单事件
        """
        pass

    def get_comlst(self):
        """Returns a list of available COM ports with description"""
        comports = serial.tools.list_ports.comports()
        comlst = []

        for item in comports:
            name = item[0]

            if len(item[1]) > 50:
                description = item[1][0:44] + "..."
            else:
                description = item[1]

            comlst.append(str(name + " - " + description))

        return sorted(comlst)

    def update_com_box(self):
        self.frm_left_combobox_serialport['values'] = self.get_comlst()
        print("updateCOMbox" + self.TKvariables['serial_port'].get())

    def serial_combobox_serialport_sel_event(self, dummy_event=None):
        print("serial_combobox_serialport_sel_event" + self.TKvariables['serial_port'].get())

    def serial_combobox_baudrate_sel_event(self, dummy_event=None):
        print("serial_combobox_baudrate_sel_event" + self.TKvariables['baudrate'].get())

    def serial_combobox_parity_sel_event(self, dummy_event=None):
        print("serial_combobox_parity_sel_event" + self.TKvariables['parity'].get())

    def serial_combobox_bytesize_sel_event(self, dummy_event=None):
        print("serial_combobox_bytesize_sel_event" + self.TKvariables['bytesize'].get())

    def serial_combobox_stopbits_sel_event(self, dummy_event=None):
        print("serial_combobox_stopbits_sel_event" + self.TKvariables['stopbits'].get())

    def serial_set_btn_event(self, event):
        self.open_close_serial()

    def id_string_r1_radiobutton_cb(self):
        print('r1_radiobutton=%d' % int(self.TKvariables['rec_hex_ascii'].get()))

    def id_string_r1_checkbutton_cb(self):
        print('linefeed is %s,time=%s' % (self.TKvariables['linefeed'].get(),
                                          self.TKvariables['linefeedtime'].get()))

    def linefeed_entry_event(self):
        pass

    def id_string_send_radiobutton_cb(self):
        print(self.id_string_send_cb_v.get())

    def id_string_send_checkbutton_cb(self):
        print(self.schedule_send.get())

    def id_string_send_CRLF_checkbutton_cb(self):
        print(self.id_string_send_CRLF_cb_v.get())

    def id_format_frame_id_frame_entry_event(self, event):
        print(datetime.now().strftime('%H:%M:%S.%f')[:-3],
              'id_format_frame_id_frame_entry_event,event.x=%d event.y=%d type=%s'
              % (event.x, event.y, event.type),
              'id_len=%d' % (len(self.id_format_frame_id_frame_entry.get())))
        if str(event.type) == 'ButtonPress' or str(event.type) == 'KeyPress':
            print("event.type == 'ButtonPress' and event.type == 'KeyPress'")

    def id_format_frame_len_entry_event(self, event):
        print(datetime.now().strftime('%H:%M:%S.%f')[:-3],
              'id_format_frame_len_entry_event,event.x=%d event.y=%d type=%s'
              % (event.x, event.y, event.type),
              'id_len=%d' % (len(self.id_format_frame_id_frame_entry.get())))
        if str(event.type) == 'ButtonPress':
            self.id_format_frame_len_entry.config(state='normal')
            s = self.id_format_frame_id_frame_entry.get()
            s = s.replace(' ', '')
            s = s.replace('|', '')
            self.TKvariables[DEF_FRAME_LEN].set(len(s))
            self.id_format_frame_len_entry.config(state='disable')

    def id_format_id_type_entry_event(self):
        pass

    def id_format_id_entry_event(self):
        pass

    def id_format_gen_btn_event(self, event):
        print(datetime.now().strftime('%H:%M:%S.%f')[:-3],
              'id_format_gen_btn_event,type=%s' % event.type)
        if str(event.type) == 'ButtonPress':
            gen_btn_process = threading.Thread(target=self.id_format_gen_thread())
            gen_btn_process.setDaemon(True)
            gen_btn_process.start()
            # self.id_format_gen()
            return

    def id_format_restart_btn_event(self, event):
        print(datetime.now().strftime('%H:%M:%S.%f')[:-3],
              'id_format_restart_btn_event,type=%s' % event.type)
        if str(event.type) == 'ButtonPress':
            restart_btn_process = threading.Thread(target=self.id_format_gen_reg_reset_thread())
            restart_btn_process.setDaemon(True)
            restart_btn_process.start()
            # self.id_format_gen()
            return

    def id_format_frame_type_radiobutton_cb(self):
        print('id_format_frame_type=%d' % int(self.TKvariables[def_id_type].get()))

    def log_notebook_frame1_scrollbar_event(self, event):
        print(datetime.now().strftime('%H:%M:%S.%f')[:-3],
              'id_format_frame_len_entry_event,event.x=%d event.y=%d type=%s type_type=%s'
              % (event.x, event.y, event.type, type(event.type)))

        if str(event.type) == 'Motion':
            self.variables[var_dataLogScrollStop] = True
            self.variables[var_dataLogScrollStopTime] = time.time()
            print('time type=%s time=%5f' % (type(self.variables[var_dataLogScrollStopTime])
                                             , self.variables[var_dataLogScrollStopTime]))

    def receive_data_thread(self):
        self.variables[var_receiveProgressStop] = False
        self.timeLastReceive = time.time()

        while not self.variables[var_receiveProgressStop]:
            try:
                # length = self.com.in_waiting
                # length = max(1, min(2048, self.com.in_waiting))
                length = min(2048, self.com.in_waiting)
                # print(time.time())

                if length:
                    rbytes = self.com.read(length)
                else:
                    rbytes = None

                if rbytes is not None:
                    # print(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                    print('[', datetime.now().strftime('%H:%M:%S.%f')[:-3], '] ', "len=%d rbytes=%s"
                          % (length, rbytes))
                    # start = time.time()
                    # print("len=%d" % (length))
                    # if self.isWaveOpen:
                    #     self.wave.displayData(bytes)
                    self.receiveCount += len(rbytes)
                    self.frm_status_receive_bytes_num.config(text=str(self.receiveCount))

                    # hex
                    if int(self.TKvariables['rec_hex_ascii'].get()):
                        str_received = asciib_to_hexstring(rbytes)
                        # self.receiveUpdateSignal.emit(str_received)
                        self.log_notebook_frame1_data.insert(tk.END, str_received)
                        # self.log_notebook_frame1_data.see(tk.END)
                    else:
                        # str_received = bytes.decode(rbytes)
                        str_received = rbytes.decode(errors='ignore')
                        log = \
                            '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + '] ' + \
                            str_received + '\n'

                        rec_update_log_ui(self, log)
                        # self.log_notebook_frame1_data.insert(tk.END, log)
                        # # end = time.time()
                        # # print('rec leedting = %5fs' % (end - start))
                        #
                        # if self.variables[var_dataLogScrollStop]:
                        #     if time.time() - self.variables[var_dataLogScrollStopTime] > \
                        #             self.variables[var_dataLogScrollStopDelayTime]:
                        #         self.variables[var_dataLogScrollStop] = False
                        # if not self.variables[var_dataLogScrollStop]:
                        #     self.log_notebook_frame1_data.see(tk.END)

                        # if (int(self.TKvariables['linefeed'].get())) == 1:
                        #     if time.time() - self.timeLastReceive > \
                        #             int(self.TKvariables['linefeedtime'].get()) / 1000:
                        #         # if self.sendSettingsCFLF.isChecked():
                        #         #     self.receiveUpdateSignal.emit("\r\n")
                        #         # else:
                        #         #     self.receiveUpdateSignal.emit("\n")
                        #         self.log_notebook_frame1_data.insert(tk.END, "\r\n")
                        #         # self.log_notebook_frame1_data.see(tk.END)
                        #
                        # if time.time() - self.timeLastReceive > 1:
                        #     self.log_notebook_frame1_data.see(tk.END)
                    # print('rec set format=%s,type str:%s' % (self.TKvariables['rec_hex_ascii'].get(),
                    #                                          type(str_received)))
                    if self.IdFormat['id_format_str'] is not '':
                        id_format_check_process(self,str_received)

                    self.timeLastReceive = time.time()

                # time.sleep(0.001)

            except Exception as e:
                com_close(self)
                # print("receiveData error")
                # if self.com.is_open and not self.serialPortCombobox.isEnabled():
                # self.open_close_serial()
                #     self.serialPortCombobox.clear()
                #     self.detectSerialPort()
                print('串口接收错误！', e)
                messagebox.showerror(message=('串口接收错误！', e))
            time.sleep(0.00050)
        return

    def open_close_serial_thread(self):

        if self.com.is_open:
            com_close(self)
        else:
            if self.TKvariables['serial_port'].get() == '':
                messagebox.showerror(message='Select a COM port!')
            else:
                try:
                    if os.name == 'nt':
                        c = re.match(r'^COM\d{1,2}', self.TKvariables['serial_port'].get(), re.I)
                        if c:
                            self.com.port = c.group()
                            # str = self.TKvariables['serial_port'].get()
                            # self.com.port = str[0:4]
                            print("os.name" + os.name + " serial port= " + c.group())
                    else:
                        messagebox.showerror(message='this os not support!')
                    self.com.baudrate = int(self.TKvariables['baudrate'].get())
                    self.com.parity = self.TKvariables['parity'].get()
                    self.com.bytesize = int(self.TKvariables['bytesize'].get())
                    self.com.stopbits = float(self.TKvariables['stopbits'].get())
                    # self.com.timeout = None
                    # if self.checkBoxRts.isChecked():
                    #     self.com.rts = False
                    # else:
                    #     self.com.rts = True
                    # if self.checkBoxDtr.isChecked():
                    #     self.com.dtr = False
                    # else:
                    #     self.com.dtr = True

                    # self.serialOpenCloseButton.setDisabled(True)
                    self.com.open()
                    print("open success")
                    print(self.com)
                    # self.serialOpenCloseButton.setText(parameters.strClose)
                    # self.statusBarStauts.setText("<font color=%s>%s</font>" % ("#008200", parameters.strReady))
                    self.frm_status_label.config(text='Ready', foreground='#27AE60')
                    self.frm_status_receive_bytes_num.config(text=str(self.receiveCount))
                    # self.serialPortCombobox.setDisabled(True)
                    # self.serailBaudrateCombobox.setDisabled(True)
                    # self.serailParityCombobox.setDisabled(True)
                    # self.serailStopbitsCombobox.setDisabled(True)
                    # self.serailBytesCombobox.setDisabled(True)
                    # self.serialOpenCloseButton.setDisabled(False)
                    receive_process = threading.Thread(target=self.receive_data_thread)
                    receive_process.setDaemon(True)
                    receive_process.start()

                    self.log_notebook_frame1_data.delete(1.0, tk.END)

                except Exception as e:
                    self.variables[var_receiveProgressStop] = True
                    self.com.close()
                    self.frm_status_label.config(text='Closed', foreground='#C0392B')
                    # self.receiveProgressStop = True
                    # self.errorSignal.emit(parameters.strOpenFailed + "\n" + str(e))
                    # self.serialOpenCloseButton.setDisabled(False)
                    messagebox.showerror(message=('COM port not available: ', e))

    def open_close_serial(self):
        t = threading.Thread(target=self.open_close_serial_thread)
        t.setDaemon(True)
        t.start()
        return

    def id_format_gen_thread(self):
        id_available_dict_clear(self)
        id_clear_invalid_dict(self)
        id_total_dict_clear(self)
        id_format_gen_reg(self)
        pass

    def id_format_gen_reg_reset_thread(self):
        # id_format_gen_reg_reset(self)
        id_available_dict_clear(self)
        id_clear_invalid_dict(self)
        id_total_dict_clear(self)
        id_format_gen_reg(self)
        pass

if __name__ == '__main__':
    """
    main loop
    """
    platform = sys.platform
    print('platform=',platform)
    root = tk.Tk()
    # root = tkthemes.ThemedTk()
    # root.set_theme("radiance")  # Sets an available theme
    # root.set_theme("keramik")  # Sets an available theme
    # root.set_theme("aquativo")  # Sets an available theme
    # root.set_theme("winxpblue")  # Sets an available theme

    # Equilux

    # if g_default_theme == "dark":
    #     root.configure(bg="#292929")
    #     combostyle = ttk.Style()
    #     combostyle.theme_use('alt')
    #     combostyle.configure("TCombobox", selectbackground="#292929", fieldbackground="#292929",
    #                          background="#292929", foreground="#FFFFFF")
    # else:
    #     combostyle = ttk.Style()
    #     combostyle.theme_use('alt')

    root.title("MCA4-Tool")
    root.iconbitmap('..\\logo.ico')
    root.geometry("900x700")
    # root.maxsize(1280, 1920)
    # root.minsize(1024, 768)

    serialtoolui = SerialToolUI(master=root)
    # root.bind("<B1-Motion>", frm_move_event)
    # serialtoolui.detectSerialPort()
    # root.resizable(False, False)

    root.mainloop()
