#! /usr/bin/env python
#  -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import binascii
import re
from datetime import datetime
import time
import copy
from operator import itemgetter
from keymaps import *


def print_to_debug_log(tag, ids, key_dict):
    if tag == LOG_DATA_TAG_WORNG_TAG:
        s = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + '] ' + \
            "%s ID:%s " % (tag, ids)
    else:
        # s = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + '] ' + \
        #     "%s ID:%s count=%d 1st_time=%s " % (tag,
        #                                         ids,
        #                                         key_dict[IDDICT_COUNT],
        #                                         key_dict[IDDICT_1ST_REC_TIME])
        s = '[' + datetime.now().strftime('%H:%M:%S.%f')[:-3] + '] ' + \
            "%s ID:%s count=%d " % (tag,
                                    ids,
                                    key_dict[IDDICT_COUNT])
        if key_dict.__contains__(IDDICT_SN):
            s = s + 'sn = %s ' % key_dict[IDDICT_SN]
        if key_dict.__contains__(IDDICT_RSSI):
            s = s + 'rssi = %s ' % key_dict[IDDICT_RSSI]

    s = s + '\n'
    return s


def print_class(c):
    print('parent:', c)
    print('__doc__', c.__doc__)
    print('__dict__', c.__dict__)


def asciib_to_hexstring(strb):
    str_hex = binascii.b2a_hex(strb).upper()
    return re.sub(r"(?<=\w)(?=(?:\w\w)+$)", " ", str_hex.decode()) + " "


def id_check_crc(id_str, check_str_index, check_index, check_str_length):
    return False


def id_check_2crc(id_str, check_str_index, check_index, check_str_length):
    return False


def id_check_sum(id_str, check_str_index, check_index, check_str_length):
    return False


def id_check_2sum(id_str, check_str_index, check_index, check_str_length):
    return False


def id_check_xor(id_str, check_str_index, check_index, check_str_length):
    c = 0
    for d in range(check_str_index, check_str_length, 2):
        a = id_str[d:d + 2]
        c = c ^ int(a, 16)

    if c == int(id_str[check_index:check_index + 2], 16):
        print('check true c:0x%x' % c)
        return True
    else:
        print('check false c:0x%x' % c)
        return False


def id_check_2xor(id_str, check_str_index, check_index, check_str_length):
    return False


def id_check_method(parent, id_str):
    if parent.IdFormat[IDF_ID_CHK_TYPE] == CHECK_TYPE_CRC:
        return False
    elif parent.IdFormat[IDF_ID_CHK_TYPE] == CHECK_TYPE_2CRC:
        return False
    elif parent.IdFormat[IDF_ID_CHK_TYPE] == CHECK_TYPE_SUM:
        return False
    elif parent.IdFormat[IDF_ID_CHK_TYPE] == CHECK_TYPE_2SUM:
        return False
    elif parent.IdFormat[IDF_ID_CHK_TYPE] == CHECK_TYPE_XOR:

        return id_check_xor(id_str,
                            parent.IdFormat[IDF_ID_CHK_START_INDEX],
                            parent.IdFormat[IDF_ID_CHK_INDEX],
                            len(parent.IdFormat[IDF_ID_CHK_STR])
                            )

    elif parent.IdFormat[DEF_CHECK_TYPE] == CHECK_TYPE_2XOR:
        return False
    else:
        print('unknow id check type!')
        return False


def id_add_id_dict(id_line,id_dict, dict_des, dict_tmp):
    # id_line = id_dict[IDSEGMENT_ID]

    if dict_des.setdefault(id_line, None) is None:
        dict_des[id_line] = copy.deepcopy(dict_tmp['id_id'])
        dict_des[id_line][IdDict_1st_rec_data] = datetime.now().strftime('%Y-%m-%d')
        dict_des[id_line][IDDICT_1ST_REC_TIME] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        dict_des[id_line][IdDict_rec_data] = datetime.now().strftime('%Y-%m-%d')
        dict_des[id_line][IdDict_rec_time] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if id_dict is not None:
            if id_dict.__contains__(IDSEGMENT_NN):
                sn = id_dict[IDSEGMENT_NN]
                sn = int(sn, 16)
                dict_des[id_line][IDDICT_SN] = str(sn)
            if id_dict.__contains__(IDSEGMENT_RR):
                rssi = id_dict[IDSEGMENT_RR]
                rssi = int(rssi, 16)
                dict_des[id_line][IDDICT_RSSI] = r'-%ddbm' % rssi
            if id_dict.__contains__(IDDICT_SN):
                sn = id_dict[IDDICT_SN]
                dict_des[id_line][IDDICT_SN] = sn
            if id_dict.__contains__(IDDICT_RSSI):
                rssi = id_dict[IDDICT_RSSI]
                dict_des[id_line][IDDICT_RSSI] = rssi
        print('new id add:', dict_des)
    else:

        dict_des[id_line][IdDict_rec_data] = datetime.now().strftime('%Y-%m-%d')
        dict_des[id_line][IdDict_rec_time] = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if id_dict is not None:
            if id_dict.__contains__(IDSEGMENT_NN):
                sn = id_dict[IDSEGMENT_NN]
                sn = int(sn, 16)
                dict_des[id_line][IDDICT_SN] = str(sn)
            if id_dict.__contains__(IDSEGMENT_RR):
                rssi = id_dict[IDSEGMENT_RR]
                rssi = int(rssi, 16)
                dict_des[id_line][IDDICT_RSSI] = r'-%ddbm' % rssi
            if id_dict.__contains__(IDDICT_SN):
                sn = id_dict[IDDICT_SN]
                dict_des[id_line][IDDICT_SN] = sn
            if id_dict.__contains__(IDDICT_RSSI):
                rssi = id_dict[IDDICT_RSSI]
                dict_des[id_line][IDDICT_RSSI] = rssi
            if id_dict.__contains__(IDDICT_COUNT):
                dict_des[id_line][IDDICT_COUNT] += id_dict[IDDICT_COUNT]
            else:
                dict_des[id_line][IDDICT_COUNT] +=1

        print('has id :', dict_des)


def id_update_ui_log_data(parent, id_dict, id_id, tag):
    if tag == LOG_DATA_TAG_WORNG_TAG:
        log = print_to_debug_log(tag,
                                 id_dict[IDSEGMENT_ID],
                                 id_dict)
        pass
    else:
        vkey_dict = id_dict[id_id]
        # print('vkey=', vkey_dict)
        log = print_to_debug_log(tag, id_id, vkey_dict)

    parent.log_notebook_frame2_data.insert(tk.END, log)

    if parent.variables[var_dataLogScrollStop]:
        if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                var_dataLogScrollStopDelayTime:
            parent.variables[var_dataLogScrollStop] = False
    else:
        if time.time() - parent.timeLastReceive > var_dataLogDelayTime:
            parent.variables[var_dataLogScrollStop] = False
    if not parent.variables[var_dataLogScrollStop]:
        parent.log_notebook_frame2_data.see(tk.END)
        parent.variables[var_dataLogScrollStop] = True


def id_dict_updata_ui(parent, id_dict_buf, id_dict_total, id_dict_av, id_dict_inv):
    id_keys = id_dict_buf.keys()
    # print('id_keys=', id_keys)
    b_id_inds = []
    for id_id in id_keys:
        id_id_dict_buf = id_dict_buf[id_id]
        if parent.IdFormat[IDF_ID_ID_H_OR_A] == 'hex':
            b_id_id = int(id_id, 16)
            b_id_seg_str = int(parent.IdFormat[IdF_id_seg_str], 16)
            b_id_seg_stp = int(parent.IdFormat[IdF_id_seg_stp], 16)
            for id_ind in parent.IdFormat[IdF_id_seg_ind]:
                # b_id_inds = b_id_inds.append(int(id_ind, 16))
                b_id_inds.append(int(id_ind, 16))
        else:
            b_id_id = int(id_id)
            b_id_seg_str = int(parent.IdFormat[IdF_id_seg_str])
            b_id_seg_stp = int(parent.IdFormat[IdF_id_seg_stp])
            for id_ind in parent.IdFormat[IdF_id_seg_ind]:
                # b_id_inds = b_id_inds.append(int(id_ind))
                b_id_inds.append(int(id_ind))

        # print('b_id_id=%d,b_id_seg_str=%d,b_id_seg_stp=%d' %
        #       (b_id_id, b_id_seg_str, b_id_seg_stp))
        #
        # print('b_id_inds=', b_id_inds)

        if b_id_seg_str <= b_id_id <= b_id_seg_stp or \
                any(True for i in b_id_inds if b_id_id == i):
            # find in dict total
            keys = list(id_dict_total.keys())
            # print('id_dict_total.keys()')
            if keys.count(id_id):
                i = keys.index(id_id)
                # print('id in total id index=', str(i))
                id_dict_total.pop(id_id)
                start = '%d.0' % (i + 1)
                end = '%d.0' % (i + 2)
                parent.tag_info_total_listbox.delete(start, end)
                count = int(parent.TKvariables[DEF_TOTAL_ID_NUM].get()) - 1
                parent.TKvariables[DEF_TOTAL_ID_NUM].set(str(count))
                # add to available dict
                id_add_id_dict(id_id, id_id_dict_buf, id_dict_av, parent.IdDict)
                print('IdAvailableDict add')
                parent.tag_info_available_listbox.insert(tk.END, 'ID:' + id_id + '\n')
                count = int(parent.TKvariables[DEF_AVAILABLE_ID_NUM].get()) + 1
                parent.TKvariables[DEF_AVAILABLE_ID_NUM].set(str(count))
                # add to debug_log
                # vkey = id_dict_av[id_id]
                # print('vkey=', vkey)
                # log = print_to_debug_log('新加入 实际可用标签', id_id, vkey[IDDICT_COUNT],
                #                          vkey[IDDICT_1ST_REC_TIME])
                # parent.log_notebook_frame2_data.insert(tk.END, log)
                # if parent.variables[var_dataLogScrollStop]:
                #     if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                #             parent.variables[var_dataLogScrollStopDelayTime]:
                #         parent.variables[var_dataLogScrollStop] = False
                # if not parent.variables[var_dataLogScrollStop]:
                #     parent.log_notebook_frame2_data.see(tk.END)
                id_update_ui_log_data(parent, id_dict_av, id_id, LOG_DATA_TAG_AV_NEW_TAG)

            else:
                # add to available dict
                id_add_id_dict(id_id, id_id_dict_buf, id_dict_av, parent.IdDict)
                print('IdAvailableDict add')
                # add to debug_log
                # vkey = id_dict_av[id_id]
                # print('vkey=', vkey)
                # log = print_to_debug_log('实际可用标签', id_id, vkey[IDDICT_COUNT],
                #                          vkey[IDDICT_1ST_REC_TIME])
                # parent.log_notebook_frame2_data.insert(tk.END, log)
                # if parent.variables[var_dataLogScrollStop]:
                #     if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                #             parent.variables[var_dataLogScrollStopDelayTime]:
                #         parent.variables[var_dataLogScrollStop] = False
                # if not parent.variables[var_dataLogScrollStop]:
                #     parent.log_notebook_frame2_data.see(tk.END)
                id_update_ui_log_data(parent, id_dict_av, id_id, LOG_DATA_TAG_AV_TAG)

        else:
            keys = list(id_dict_inv.keys())
            if keys.count(id_id):
                # add to invalid dict
                id_add_id_dict(id_id, id_id_dict_buf, id_dict_inv, parent.IdDict)
                print('invalid Dict add')
                # add to debug_log
                # vkey = id_dict_inv[id_id]
                # print('vkey=', vkey)
                # log = print_to_debug_log('实际无效标签', id_id, vkey[IDDICT_COUNT],
                #                          vkey[IDDICT_1ST_REC_TIME])
                # parent.log_notebook_frame2_data.insert(tk.END, log)
                # if parent.variables[var_dataLogScrollStop]:
                #     if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                #             parent.variables[var_dataLogScrollStopDelayTime]:
                #         parent.variables[var_dataLogScrollStop] = False
                # if not parent.variables[var_dataLogScrollStop]:
                #     parent.log_notebook_frame2_data.see(tk.END)
                id_update_ui_log_data(parent, id_dict_inv, id_id, LOG_DATA_TAG_IN_TAG)
            else:
                count = int(parent.TKvariables[DEF_INVALID_ID_NUM].get()) + 1
                parent.TKvariables[DEF_INVALID_ID_NUM].set(str(count))

                # add to invalid dict
                id_add_id_dict(id_id, id_id_dict_buf, id_dict_inv, parent.IdDict)
                print('invalid Dict add')
                parent.tag_info_invalid_listbox.insert(tk.END, 'ID:' + id_id + '\n')
                # add to debug_log
                # vkey = id_dict_inv[id_id]
                # print('vkey=', vkey)
                # log = print_to_debug_log('新加入 实际无效标签', id_id, vkey[IDDICT_COUNT],
                #                          vkey[IDDICT_1ST_REC_TIME])
                # parent.log_notebook_frame2_data.insert(tk.END, log)
                # if parent.variables[var_dataLogScrollStop]:
                #     if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                #             parent.variables[var_dataLogScrollStopDelayTime]:
                #         parent.variables[var_dataLogScrollStop] = False
                # if not parent.variables[var_dataLogScrollStop]:
                #     parent.log_notebook_frame2_data.see(tk.END)
                id_update_ui_log_data(parent, id_dict_inv, id_id, LOG_DATA_TAG_IN_NEW_TAG)


def id_format_check_process(parent, rec_bytes):
    # parent.IdCheckStr += rec_bytes
    rec_bytes = rec_bytes.replace(' ','')
    parent.receive_count_without_space += len(rec_bytes)
    print('receive_count_without_space=%d' % parent.receive_count_without_space)
    ics = parent.IdCheckStr
    ics = ics + rec_bytes
    # ics = ics.replace(' ','')
    print('ics=%s' % (ics))
    # str_ind = -1

    id_par = re.compile(parent.IdFormat[IDF_ID_R_PATTERN], re.I)
    id_len = len(parent.IdFormat[IDF_ID_FORMAT_STR])

    if len(ics) >= id_len:
        m = id_par.finditer(ics)
        # print('m', m)
        ics_stp = 0
        for it in m:
            id_dict_buf = it.groupdict()
            ics_str = it.start()
            ics_stp = it.end()
            parent.id_data_count += (ics_stp - ics_str)
            print('id_data_count:%d' % parent.id_data_count)
            print('it.groupdict():%s it.start():%s it.end():%s' %
                  (it.groupdict(), it.start(), it.end()))
            '''
            检测 id 效验
            '''
            if id_dict_buf.__contains__(IDSEGMENT_CK):
                if id_check_method(parent, ics[ics_str:ics_stp]) is True:
                    # id_id = it.group(2)
                    id_id = id_dict_buf[IDSEGMENT_ID]
                    id_add_id_dict(id_id, id_dict_buf, parent.IdDictBuf, parent.IdDict)
                    parent.id_correct_data_count += (ics_stp - ics_str)
                    print('id_correct_data_count:%d' % parent.id_correct_data_count)
                else:
                    id_update_ui_log_data(parent,
                                          id_dict_buf,
                                          id_dict_buf[IDSEGMENT_ID],
                                          LOG_DATA_TAG_WORNG_TAG
                                          )
            else:
                # id_id = it.group(2)
                id_id = id_dict_buf[IDSEGMENT_ID]
                id_add_id_dict(id_id, id_dict_buf, parent.IdDictBuf, parent.IdDict)

        '''
        剩余字节处理
        '''
        if len(ics[ics_stp:len(ics)]) > id_len:
            ics = ics[-(id_len - 1):]
            parent.IdCheckStr = ics
            print(' 0 IdCheckStr Remaining = ', parent.IdCheckStr)
        else:
            ics = ics[ics_stp:len(ics)]
            parent.IdCheckStr = ics
            print(' 1 IdCheckStr Remaining = ', parent.IdCheckStr)

        '''
        update ui
        '''
        if len(parent.IdDictBuf) != 0:
            id_dict_updata_ui(
                parent,
                parent.IdDictBuf,
                parent.IdTotalDict,
                parent.IdAvailableDict,
                parent.IdInvalidDict)

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


def check_regex_for_gen(line, par, rows, seg, g_num):
    try:
        regex_par_str = par
        regex_par = re.compile(regex_par_str, re.I)
        ma = regex_par.findall(line)
        print(ma)
        if len(ma) == 1:
            ma = regex_par.search(line)
            print('ma:', ma)
            print('ma.groups():', ma.groups())
            print('ma.group():', ma.group(g_num))
            d = {ID_ROWS_NAME: seg, ID_ROWS_STR: ma.group(g_num),
                 ID_ROWS_START: ma.start(), 'end': ma.end()}
            rows.append(d)
            # rows[seg] = ma.start()
            # rows['str'] = ma.group(g_num)
            # r_dict[seg][ID_ROWS_START] = ma.start()
            # r_dict[seg].append(ma.group(g_num))
            # r_dict[seg].append(ma.start())
            # r_dict[seg].append(ma.end())

            # r_dict[seg] = ma.start()
            # print(r_dict)
            return True
        else:
            print('false count:', len(ma))
            return False
    except Exception as e:
        print('check_regex_for_gen error:',e)
        messagebox.showerror(message=('check_regex_for_gen error:', e))

def id_format_interprete(parent, rows):
    try:
        id_format = parent.id_format_frame_id_frame_entry.get()
        id_format = id_format.replace(' ', '')
        id_format = id_format.upper()

        # g_rows = []

        '''
        检测 id 帧头
        '''
        if id_format.count('|') == 0 or id_format.count('|') > 1:
            print('0 ID帧头格式错误！')
            messagebox.showerror(message='ID帧头格式错误！')
            return False

        p = r'^([^\|]{3,30})\|'
        if not check_regex_for_gen(id_format, p, rows, IDSEGMENT_HEAD, 1):
            print('1 ID帧头格式错误！')
            messagebox.showerror(message='ID帧头格式错误！')
            return False

        id_start = rows[len(rows) - 1][ID_ROWS_STR]
        id_format = id_format.replace('|', '')

        parent.IdFormat[IDF_ID_FORMAT_STR] = id_format
        parent.IdFormat[IdF_id_start] = id_start

        '''
        检测 ID 长度
        '''
        p = r'[x]{3,30}'
        if not check_regex_for_gen(id_format, p, rows, IDSEGMENT_ID, 0):
            print('1 ID号格式错误！')
            messagebox.showerror(message='ID号格式错误！')
            return False

        id_id = rows[len(rows) - 1][ID_ROWS_STR]
        id_id_index = rows[len(rows) - 1][ID_ROWS_START]
        is_hex = parent.TKvariables[def_id_type].get()

        parent.IdFormat[IdF_id_id] = id_id
        parent.IdFormat[IdF_id_id_index] = id_id_index
        parent.IdFormat[IDF_ID_ID_H_OR_A] = is_hex
        '''
        检测 CHK
        '''
        chk = parent.TKvariables[DEF_CHECK].get()
        id_chk_str = parent.TKvariables[DEF_CHECK_TYPE].get()
        id_chk_str = id_chk_str.replace('|', '')
        id_chk_str = id_chk_str.replace(' ', '')
        id_chk_str = id_chk_str.upper()
        print('id_chk_str', id_chk_str)

        if chk != CHECK_TYPE_NONE:
            if id_chk_str is not None:
                id_chk_start_index = id_format.find(id_chk_str)
                if id_chk_start_index != -1:
                    if chk.find('2') != -1:
                        chk_len = 2
                    else:
                        chk_len = 1

                    p = r'[k]{%d}' % (chk_len * 2)
                    if not check_regex_for_gen(id_format, p, rows, IDSEGMENT_CK, 0):
                        print('1 ID效验格式错误！')
                        messagebox.showerror(message='ID效验格式错误！')
                        return False
                    id_chk = rows[len(rows) - 1][ID_ROWS_STR]
                    id_chk_index = rows[len(rows) - 1][ID_ROWS_START]
                    parent.IdFormat[IDF_ID_CHK_TYPE] = chk
                    parent.IdFormat[IDF_ID_CHK_INDEX] = id_chk_index
                    parent.IdFormat[IdF_id_chk] = id_chk
                    parent.IdFormat[IDF_ID_CHK_STR] = id_chk_str
                    parent.IdFormat[IDF_ID_CHK_START_INDEX] = id_chk_start_index
                else:
                    print('1 ID效验格式错误！')
                    messagebox.showerror(message='ID效验格式错误！')
                    return False
            else:
                print('2 ID效验格式错误！')
                messagebox.showerror(message='ID效验格式错误！')
                return False

        '''
        检测 RSSI
        '''
        p = r'[r]{2}'
        if not check_regex_for_gen(id_format, p, rows, IDSEGMENT_RR, 0):
            print('no Rssi')
            pass
        else:
            id_rssi = rows[len(rows) - 1][ID_ROWS_STR]
            id_rssi_index = rows[len(rows) - 1][ID_ROWS_START]
            parent.IdFormat[IdF_id_rssi] = id_rssi
            parent.IdFormat[IdF_id_rssi_index] = id_rssi_index
        '''
        检测 SN
        '''
        p = r'[n]{2}'
        if not check_regex_for_gen(id_format, p, rows, IDSEGMENT_NN, 0):
            print('no sn')
            pass
        else:
            id_nn = rows[len(rows) - 1][ID_ROWS_STR]
            id_nn_index = rows[len(rows) - 1][ID_ROWS_START]
            parent.IdFormat[IdF_id_rssi] = id_nn
            parent.IdFormat[IdF_id_nn_index] = id_nn_index

        # print(rows)
        # rows = sorted(rows, key=itemgetter(ID_ROWS_START))

        # print(rows)
        print('parent.IdFormat',parent.IdFormat)
        return True
    except Exception as e:
        print('id_format_interprete error:',e)
        messagebox.showerror(message=('id_format_interprete error:', e))

def id_format_pattern_gen(parent, rows):
    """
    生成正则表达式
    """
    par = ''
    s = ''
    last_end = 0
    try:
        # print('row in gen:', rows)
        for d in rows:
            print('d[ID_ROWS_NAME]', d[ID_ROWS_NAME])
            if d[ID_ROWS_NAME] == IDSEGMENT_HEAD:
                s = r'(?P<%s>%s)' % (d[ID_ROWS_NAME], parent.IdFormat[IdF_id_start])
                last_end = d[ID_ROWS_END] - 1
            else:
                if d[ID_ROWS_START] > last_end:
                    s = r'[0-9a-z]{%d}' % (d[ID_ROWS_START] - last_end)
                s = s + r'(?P<%s>[0-9a-z]{%d})' % (d[ID_ROWS_NAME],
                                                   (d[ID_ROWS_END] - d[ID_ROWS_START]))
                last_end = d[ID_ROWS_END]
            par = par + s
            s = ''

        print('pattern:', par)
        return par
    except Exception as e:
        print('id_format_pattern_gen error:', e)
        messagebox.showerror(message=('id_format_pattern_gen error:', e))


def id_available_dict_clear(parent):
    # clear
    parent.TKvariables[DEF_AVAILABLE_ID_NUM].set(str(0))
    parent.IdAvailableDict.clear()
    parent.tag_info_available_listbox.delete(1.0, tk.END)


def id_clear_invalid_dict(parent):
    # clear
    parent.TKvariables[DEF_INVALID_ID_NUM].set(str(0))
    parent.IdInvalidDict.clear()
    parent.tag_info_invalid_listbox.delete(1.0, tk.END)


def id_total_dict_clear(parent):
    # clear
    parent.TKvariables[DEF_TOTAL_ID_NUM].set(str(0))
    parent.IdTotalDict.clear()
    parent.tag_info_total_listbox.delete(1.0, tk.END)


def id_format_gen_reg(parent):
    """
    解析ID格式
    """

    id_seg_rows = []

    if not id_format_interprete(parent, id_seg_rows):
        print('id_format_interprete 错误！')
        # messagebox.showerror(message='ID效验格式错误！')
        return False
    else:
        rows_by_start = sorted(id_seg_rows, key=itemgetter(ID_ROWS_START))
        print(rows_by_start)
        par = id_format_pattern_gen(parent, rows_by_start)
        parent.IdFormat[IDF_ID_R_PATTERN] = par

    '''
    检测 ID 号段
    '''
    id_seg = parent.TKvariables[DEF_ID].get()

    id_seg = id_seg.replace(' ', '')

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
        print('ID段号获取失败 ', e)
        messagebox.showerror(message=('ID段号获取失败 ', e))
    '''
    生成 ID
    '''
    try:
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
            id_add_id_dict(id_str, None, parent.IdTotalDict, parent.IdDict)
            print('IdTotalDict add')
            parent.tag_info_total_listbox.insert(tk.END, 'ID:' + id_str + '\n')
            count = int(parent.TKvariables[DEF_TOTAL_ID_NUM].get()) + 1
            parent.TKvariables[DEF_TOTAL_ID_NUM].set(str(count))
            # add debug log
            # vkey = parent.IdTotalDict[id_str]
            # print('vkey=', vkey)
            # log = print_to_debug_log('未检测标签', id_str, vkey[IDDICT_COUNT],
            #                          vkey[IDDICT_1ST_REC_TIME])
            #
            # parent.log_notebook_frame2_data.insert(tk.END, log)
    except Exception as e:
        print('生成 ID ', e)
        messagebox.showerror(message=('生成 ID ', e))


# def id_format_gen_reg_reset(parent):


def com_close(parent):
    parent.variables[var_receiveProgressStop] = True
    parent.receiveCount = 0
    parent.receive_count_without_space = 0
    parent.id_data_count = 0
    parent.id_correct_data_count = 0
    parent.com.close()
    parent.frm_status_label.config(text='Closed', foreground='#C0392B')


def rec_update_log_ui(parent, log):
    parent.log_notebook_frame1_data.insert(tk.END, log)
    # end = time.time()
    # print('rec leedting = %5fs' % (end - start))

    if parent.variables[var_dataLogScrollStop]:
        if time.time() - parent.variables[var_dataLogScrollStopTime] > \
                var_dataLogScrollStopDelayTime:
            parent.variables[var_dataLogScrollStop] = False
    else:
        if time.time() - parent.timeLastReceive > var_dataLogDelayTime:
            parent.variables[var_dataLogScrollStop] = False
    if not parent.variables[var_dataLogScrollStop]:
        parent.log_notebook_frame1_data.see(tk.END)
        parent.variables[var_dataLogScrollStop] = True