#! /usr/bin/env python
#  -*- coding: utf-8 -*-

# variables
var_receiveProgressStop = 'receiveProgressStop'
var_dataLogScrollStop = 'dataLogScrollStop'
var_dataLogScrollStopTime = 'dataLogScrollStopTime'
var_dataLogScrollStopDelayTime = 10.0
var_dataLogDelayTime = 1.0
# ui
CHECK_TYPE_NONE = "None"
CHECK_TYPE_CRC = "CRC"
CHECK_TYPE_2CRC = "2CRC"
CHECK_TYPE_SUM = "Sum"
CHECK_TYPE_2SUM = "2Sum"
CHECK_TYPE_XOR = "Xor"
CHECK_TYPE_2XOR = "2Xor"

# IdFormat = 'id_format_str'
IDF_ID_FORMAT_STR = 'id_format_str'
# IdF_id_start_index = 'id_start_index'
# IdF_id_start_limit = 'id_start_limit'
IdF_id_start = 'id_start'
IdF_id_nn_index = 'id_nn_index'
IdF_id_nn = 'id_nn'
IDF_ID_ID_H_OR_A = 'id_id_h_or_a'
IdF_id_id_index = 'id_id_index'
IdF_id_id = 'id_id'
IdF_id_state1_index = 'id_state1_index'
IdF_id_state1 = 'id_state1'
IdF_id_state2_index = 'id_state2_index'
IdF_id_state2 = 'id_state2'
IdF_id_rssi_index = 'id_rssi_index'
IdF_id_rssi = 'id_rssi'
IDF_ID_CHK_TYPE = 'id_chk_type'
IDF_ID_CHK_INDEX = 'id_chk_index'
IdF_id_chk = 'id_chk'
IDF_ID_CHK_START_INDEX = 'id_chk_start_index'
IDF_ID_CHK_STR = 'id_chk_str'
IDF_ID_R_PATTERN = 'id_r_pattern'
IdF_id_seg_str = 'id_seg_str'
IdF_id_seg_stp = 'id_seg_stp'
IdF_id_seg_ind = 'id_seg_ind'


# IdDict
IdDict_id_id  ='id_id'
IDDICT_SN = 'sn'
IDDICT_RSSI = 'rssi'
IDDICT_COUNT = 'count'
IdDict_1st_rec_data = '1st_rec_data'
IDDICT_1ST_REC_TIME = '1st_rec_time'
IdDict_rec_data = 'rec_data'
IdDict_rec_time = 'rec_time'

# defaults =
def_serial_port = 'serial_port'
def_baudrate = 'baudrate'
def_parity = 'parity'
def_bytesize = 'bytesize'
def_stopbits = 'stopbits'
def_rec_hex_ascii = 'rec_hex_ascii'
def_linefeed = 'linefeed'
def_linefeedtime = 'linefeedtime'
def_id_type = 'id_type'
def_rec_count = 'rec_count'
def_frame = '帧格式'
DEF_FRAME_LEN = '帧长'
DEF_CHECK = '效验'
DEF_CHECK_TYPE = '效验格式'
DEF_ID = 'id'
DEF_TOTAL_ID_NUM = '未检测标签数'
DEF_INVALID_ID_NUM = '实际无效标签数'
DEF_AVAILABLE_ID_NUM = '实际可用标签数'

# method
IDSEGMENT_HEAD = 'head'
IDSEGMENT_RR = 'rr'
IDSEGMENT_ID = 'id'
IDSEGMENT_NN = 'nn'
IDSEGMENT_CK = 'ck'

ID_ROWS_NAME = 'name'
ID_ROWS_STR = 'str'
ID_ROWS_START = 'start'
ID_ROWS_END = 'end'

# log data
LOG_DATA_TAG_WORNG_TAG = '错误'
LOG_DATA_TAG_AV_NEW_TAG = '新加入 可用'
LOG_DATA_TAG_AV_TAG = '可用'
LOG_DATA_TAG_IN_NEW_TAG = '新加入 无效'
LOG_DATA_TAG_IN_TAG = '无效'