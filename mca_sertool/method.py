#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import binascii
import re
from datetime import datetime
import time
import copy
from keymaps import *


def print_to_debug_log(tag, ids, count, one_time):
    s = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + '] ' + \
        "%s ID:%s count=%d 1st_time=%s" % (tag, ids, count, one_time) + \
        '\n'

    return s


def print_class(c):
    print('parent:', c)
    print('__doc__', c.__doc__)
    print('__dict__', c.__dict__)


def asciib_to_hexstring(strb):
    str_hex = binascii.b2a_hex(strb).upper()
    return re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", str_hex.decode()) + " "


def id_add_id_dict(parent, id_line, dict_des, dict_tmp):
    if dict_des.setdefault(id_line, None) is None:
        dict_des[id_line] = copy.deepcopy(dict_tmp['id_id'])
        dict_des[id_line][IdDict_1st_rec_data] = datetime.now().strftime('%Y-%m-%d')
        dict_des[id_line][IdDict_1st_rec_time] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        dict_des[id_line][IdDict_rec_data] = datetime.now().strftime('%Y-%m-%d')
        dict_des[id_line][IdDict_rec_time] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print('new id add:', parent.IdDictBuf)
    else:
        dict_des[id_line]['count'] += 1
        dict_des[id_line][IdDict_rec_data] = datetime.now().strftime('%Y-%m-%d')
        dict_des[id_line][IdDict_rec_time] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        print('has id :', parent.IdDictBuf)


def id_dict_updata_ui(parent, id_dict_buf, id_dict_total, id_dict_av, id_dict_inv):
    id_keys = id_dict_buf.keys()
    print('id_keys=', id_keys)
    b_id_inds = []
    for id_id in id_keys:
        if parent.IdFormat[IdF_id_id_h_or_a] == 'hex':
            b_id_id = int(id_id, 16)
            b_id_seg_str = int(parent.IdFormat[IdF_id_seg_str], 16)
            b_id_seg_stp = int(parent.IdFormat[IdF_id_seg_stp], 16)
            for id_ind in parent.IdFormat[IdF_id_seg_ind]:
                b_id_inds = b_id_inds.append(int(id_ind, 16))
        else:
            b_id_id = int(id_id)
            b_id_seg_str = int(parent.IdFormat[IdF_id_seg_str])
            b_id_seg_stp = int(parent.IdFormat[IdF_id_seg_stp])
            for id_ind in parent.IdFormat[IdF_id_seg_ind]:
                b_id_inds = b_id_inds.append(int(id_ind))

        print('b_id_id=%d,b_id_seg_str=%d,b_id_seg_stp=%d' %
              (b_id_id, b_id_seg_str, b_id_seg_stp))

        print('b_id_inds=', b_id_inds)

        if b_id_seg_str <= b_id_id <= b_id_seg_stp or \
                any(True for i in b_id_inds if b_id_id == i):
            # find in dict total
            keys = list(id_dict_total.keys())
            print('id_dict_total.keys()')
            if keys.count(id_id):
                i = keys.index(id_id)
                print('id in total id index=', str(i))
                id_dict_total.pop(id_id)
                start = '%d.0' % (i + 1)
                end = '%d.0' % (i + 2)
                parent.tag_info_total_listbox.delete(start, end)
                count = int(parent.TKvariables['未检测标签数'].get()) - 1
                parent.TKvariables['未检测标签数'].set(str(count))
                # add to available dict
                parent.id_add_id_dict(id_id, id_dict_av, parent.IdDict)
                print('IdAvailableDict add')
                parent.tag_info_available_listbox.insert(tk.END, 'ID:' + id_id + '\n')
                count = int(parent.TKvariables['实际可用标签数'].get()) + 1
                parent.TKvariables['实际可用标签数'].set(str(count))
                # add to debug_log
                vkey = id_dict_av[id_id]
                print('vkey=', vkey)
                log = print_to_debug_log('新加入 实际可用标签', id_id, vkey[IdDict_count],
                                         vkey[IdDict_1st_rec_time])
                parent.log_notebook_frame2_data.insert(tk.END, log)
                if parent.variables[var_dataLogScrollStop]:
                    if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                            parent.variables[var_dataLogScrollStopDelayTime]:
                        parent.variables[var_dataLogScrollStop] = False
                if not parent.variables[var_dataLogScrollStop]:
                    parent.log_notebook_frame2_data.see(tk.END)

            else:
                # add to available dict
                parent.id_add_id_dict(id_id, id_dict_av, parent.IdDict)
                print('IdAvailableDict add')
                # add to debug_log
                vkey = id_dict_av[id_id]
                print('vkey=', vkey)
                log = print_to_debug_log('实际可用标签', id_id, vkey[IdDict_count],
                                         vkey[IdDict_1st_rec_time])
                parent.log_notebook_frame2_data.insert(tk.END, log)
                if parent.variables[var_dataLogScrollStop]:
                    if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                            parent.variables[var_dataLogScrollStopDelayTime]:
                        parent.variables[var_dataLogScrollStop] = False
                if not parent.variables[var_dataLogScrollStop]:
                    parent.log_notebook_frame2_data.see(tk.END)

        else:
            keys = list(id_dict_inv.keys())
            if keys.count(id_id):
                # add to invalid dict
                parent.id_add_id_dict(id_id, id_dict_inv, parent.IdDict)
                print('invalid Dict add')
                # add to debug_log
                vkey = id_dict_inv[id_id]
                print('vkey=', vkey)
                log = print_to_debug_log('实际无效标签', id_id, vkey[IdDict_count],
                                         vkey[IdDict_1st_rec_time])
                parent.log_notebook_frame2_data.insert(tk.END, log)
                if parent.variables[var_dataLogScrollStop]:
                    if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                            parent.variables[var_dataLogScrollStopDelayTime]:
                        parent.variables[var_dataLogScrollStop] = False
                if not parent.variables[var_dataLogScrollStop]:
                    parent.log_notebook_frame2_data.see(tk.END)
            else:
                count = int(parent.TKvariables['实际无效标签数'].get()) + 1
                parent.TKvariables['实际无效标签数'].set(str(count))

                # add to invalid dict
                parent.id_add_id_dict(id_id, id_dict_inv, parent.IdDict)
                print('invalid Dict add')
                parent.tag_info_invalid_listbox.insert(tk.END, 'ID:' + id_id + '\n')
                # add to debug_log
                vkey = id_dict_inv[id_id]
                print('vkey=', vkey)
                log = print_to_debug_log('新加入 实际无效标签', id_id, vkey[IdDict_count],
                                         vkey[IdDict_1st_rec_time])
                parent.log_notebook_frame2_data.insert(tk.END, log)
                if parent.variables[var_dataLogScrollStop]:
                    if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                            parent.variables[var_dataLogScrollStopDelayTime]:
                        parent.variables[var_dataLogScrollStop] = False
                if not parent.variables[var_dataLogScrollStop]:
                    parent.log_notebook_frame2_data.see(tk.END)

def id_format_check_process(parent, rec_bytes):
    # parent.IdCheckStr += rec_bytes
    ics = parent.IdCheckStr
    ics = ics + rec_bytes
    print('rec_bytes = %s ics=%s' % (rec_bytes, ics))
    # str_ind = -1

    id_par = re.compile(parent.IdFormat['id_r_pattern'], re.I)
    id_len = len(parent.IdFormat[IdF_IdF_id_format_str])

    if len(ics) >= id_len:
        m = id_par.finditer(ics)
        ics_stp = 0
        for it in m:
            id_id = it.group(2)
            parent.id_add_id_dict(id_id, parent.IdDictBuf, parent.IdDict)
            ics_stp = it.end()

        if len(ics[ics_stp:len(ics)]) > id_len:
            ics = ics[-(id_len - 1):]
            parent.IdCheckStr = ics
            print(' 0 IdCheckStr Remaining = ', parent.IdCheckStr)
        else:
            ics = ics[ics_stp:len(ics)]
            parent.IdCheckStr = ics
            print(' 1 IdCheckStr Remaining = ', parent.IdCheckStr)

        if len(parent.IdDictBuf) != 0:
            parent.id_dict_updata_ui(
                parent.IdDictBuf,
                parent.IdTotalDict,
                parent.IdAvailableDict,
                parent.IdInvalidDict,
            )

            parent.IdDictBuf.clear()
    else:
        parent.IdCheckStr = ics

    print('parent.IdCheckStr=', parent.IdCheckStr)


def long_repeat(line, b):
    """
        length the longest substring that consists of the same char
    """
    return 0 if line == '' else max(
        [i for i in range(1, len(line) + 1)
         if any([True for char in line if line.find(b * i) != -1])])


def iss_hex(line):
    if (('0' > line or '9' < line)
            and ('A' > line or 'F' < line)
            and ('a' > line or 'f' < line)):
        return False
    return True


def id_format_gen(parent):
    # try:

        #
        id_format = parent.id_format_frame_id_frame_entry.get()
        id_format = id_format.replace(' ', '')
        id_format = id_format.upper()
        parent.IdFormat[IdF_IdF_id_format_str] = id_format

        '''
            检测 CHK
            '''
        chk = parent.TKvariables[def_check].get()
        id_chk_str = parent.TKvariables[def_check_type].get()

        if chk != "None" :
            if id_chk_str :
                id_chk_start_index = id_format.find(id_chk_str)
                if id_chk_start_index != -1:
                    if chk.find('2') != -1:
                        chk_len = 2
                    else:
                        chk_len = 1
                    id_chk_index = id_format.find('KK')
                    if  id_chk_index != -1:
                        kk_len = long_repeat(id_format, 'KK')

                        if kk_len == chk_len:
                            parent.IdFormat[IdF_id_chk_type] = chk
                            parent.IdFormat[IdF_id_chk_index] = id_chk_index
                            parent.IdFormat[IdF_id_chk] = 'KK' * chk_len
                            parent.IdFormat[IdF_id_chk_str] = id_chk_str
                            parent.IdFormat[IdF_id_chk_start_index] = id_chk_start_index
                        else:
                            print('4 ID效验格式错误！')
                            messagebox.showerror(message='ID效验格式错误！')
                            return

                    else:
                        print('5 ID效验格式错误！')
                        messagebox.showerror(message='ID效验格式错误！')
                        return
                else:
                    print('0 ID效验格式错误！')
                    messagebox.showerror(message='ID效验格式错误！')
                    return
            else:
                print('1 ID效验格式错误！')
                messagebox.showerror(message='ID效验格式错误！')
                return
        else:
            chk_len = 0

        '''
        检测 ID 长度
        '''
        # x = 0
        if id_format.find('X') != -1:
            id_id_len = long_repeat(id_format, 'X')
        else:
            print('5 ID号格式错误！')
            messagebox.showerror(message='ID号格式错误！')
            return
        # id_id_len = parent.long_repeat(id_format, 'X')
        print('id_id_len=', str(id_id_len))

        id_id_index = id_format.find('X' * id_id_len)

        id_format_tmp = id_format.replace('X' * id_id_len, '')

        if id_format_tmp.find('X') is not -1:
            print('6 ID号格式错误！')
            messagebox.showerror(message='ID号格式错误！')
            return

        parent.IdFormat['id_id_index'] = id_id_index
        parent.IdFormat['id_id'] = 'X' * id_id_len

        '''
        检测 id 帧头
        '''
        p = r'^(?P<head>\S{3,20})\|+'
        p = re.compile(p,re.I)
        m = p.match(id_format)

        if m:
            md = m.groupdict()
            print('md=', md)
            if md.__contains__('head'):
                id_start = m.group('head')
            else:
                print('ID帧头格式错误!')
                messagebox.showerror(message='ID帧头格式错误！')
                return

        else:
            print('ID帧头格式错误!')
            messagebox.showerror(message='ID帧头格式错误！')
            return

        parent.IdFormat['id_start'] = id_start

        '''
        正则表达
        '''
        parent.IdFormat['id_r_pattern'] = \
            r'(?P<head>%s)+[nr]*(?P<id>[x]{%d})+[nr]*(?P<head2>[kk]{%d})?'\
            % (id_start,id_id_len,chk_len)

        print('id格式获取成功', parent.IdFormat)

        '''
        检测 ID 号段
        '''
        id_seg = parent.TKvariables['id'].get()

        if id_seg is None:
            print('1 ID段号格式错误！')
            messagebox.showerror(message='ID段号格式错误！')
            return
        s = ''
        id_seg_str = ''
        id_seg_stp = ''
        id_seg_ind = []
        try:
            for i in range(0, len(id_seg)):
                s += id_seg[i]
                print('i=%d s=%s' % (i, s))
                if not iss_hex(id_seg[i]):
                    # if s.isdigit() is False:
                    if id_seg[i] is '-':
                        if id_seg_str is '':
                            id_seg_str = s[0:len(s) - 1]
                            s = ''
                        else:
                            print('1.1 ID段号格式错误！')
                            messagebox.showerror(message='ID段号格式错误！')
                            return
                    elif id_seg[i] is '|':
                        print('id_seg[i]=%s,len(id_seg)=%d' % (id_seg[i], len(id_seg)))
                        if id_seg_stp is '' and id_seg_str is not '':
                            id_seg_stp = s[0:len(s) - 1]
                            s = ''
                        elif id_seg_stp is not '':
                            id_seg_ind.append(s[0:len(s) - 1])
                            s = ''
                        else:
                            print('1.1 ID段号格式错误！')
                            messagebox.showerror(message='ID段号格式错误！')
                            return
                    else:
                        print('2 ID段号格式错误！')
                        messagebox.showerror(message='ID段号格式错误！')
                        return
                else:
                    if i == len(id_seg) - 1:
                        if id_seg_stp is '' and id_seg_str is not '':
                            id_seg_stp = s[0:len(s)]
                            s = ''
                        elif id_seg_stp is not '':
                            id_seg_ind.append(s[0:len(s)])
                            s = ''
                        else:
                            print('2.1 ID段号格式错误！')
                            messagebox.showerror(message='ID段号格式错误！')
                            return

            parent.IdFormat['id_seg_str'] = id_seg_str
            parent.IdFormat['id_seg_stp'] = id_seg_stp

            for estr in id_seg_ind:
                parent.IdFormat['id_seg_ind'].append(estr)
            print('id_seg_str=%s,id_seg_stp=%s，id_seg_ind=%s' %
                  (parent.IdFormat['id_seg_str'], parent.IdFormat['id_seg_str'],
                   parent.IdFormat['id_seg_ind']))

        except Exception as e:
            messagebox.showerror(message=('ID段号获取失败 ', e))

        '''
        生成 ID 
        '''
        seg_ind = []
        is_hex = parent.IdFormat['id_id_h_or_a']
        if is_hex == 'hex':
            id_id_len = len(parent.IdFormat['id_id'])
            max_id = int('f' * id_id_len, 16)
            print('id_id_len=%d,max_id=%d' % (id_id_len, max_id))

            seg_str = int(id_seg_str, 16)
            seg_stp = int(id_seg_stp, 16)

            for estr in id_seg_ind:
                seg_ind.append(int(estr, 16))
        else:
            id_id_len = len(parent.IdFormat['id_id'])
            max_id = int('9' * id_id_len)
            seg_str = int(id_seg_str)
            seg_stp = int(id_seg_stp)

            for estr in id_seg_ind:
                seg_ind.append(int(estr))

        print('seg_str=%d,seg_stp=%d，seg_ind=%s' %
              (seg_str, seg_stp, seg_ind))

        if seg_str >= seg_stp:
            print('3 ID段号格式错误！')
            messagebox.showerror(message='ID段号格式错误！')
            return
        else:

            if seg_stp > max_id:
                print('3.1 ID段号格式错误！')
                messagebox.showerror(message='ID段号格式错误！')
                return
            else:
                for estr in seg_ind:
                    if estr > max_id:
                        print('3.2 ID段号格式错误！')
                        messagebox.showerror(message='ID段号格式错误！')
                        return
                    if seg_str <= estr <= seg_stp:
                        seg_ind.remove(estr)

        parent.tag_info_total_listbox.delete(1.0, tk.END)

        id_id_list = [id_id for id_id in range(seg_str, seg_stp + 1)]

        id_id_list.extend(seg_ind)
        print(id_id_list)

        # id_format_str_tmp = parent.IdFormat[IdF_IdF_id_format_str]
        # id_id_tmp = parent.IdFormat['id_id']
        # count = 0
        for index, id_id in enumerate(id_id_list):
            if is_hex == 'hex':
                id_str = format(id_id, 'x')
                id_str = id_str.zfill(id_id_len)
            else:
                id_str = str(id_id)
                id_str = id_str.zfill(id_id_len)
            # id_id_str = id_format_str_tmp
            # id_id_str = id_id_str.replace(id_id_tmp, id_str)

            # print('id_id_len=%d,id_str=%s, id_id_str=%s' %
            #       (id_id_len, id_str, id_id_str))
            id_add_id_dict(parent, id_str, parent.IdTotalDict, parent.IdDict)
            print('IdTotalDict add')
            parent.tag_info_total_listbox.insert(tk.END, 'ID:' + id_str + '\n')
            count = int(parent.TKvariables['未检测标签数'].get()) + 1
            parent.TKvariables['未检测标签数'].set(str(count))
            # add debug log
            vkey = parent.IdTotalDict[id_str]
            print('vkey=', vkey)
            log = print_to_debug_log('未检测标签', id_str, vkey[IdDict_count],
                                     vkey[IdDict_1st_rec_time])

            parent.log_notebook_frame2_data.insert(tk.END, log)

    # except Exception as e:
    #     parent.com.close()
    #     # parent.receiveProgressStop = True
    #     # parent.errorSignal.emit(parameters.strOpenFailed + "\n" + str(e))
    #     # parent.serialOpenCloseButton.setDisabled(False)
    #     messagebox.showerror(message=('ID格式获取失败 ', e))
    #
    # return
