from autoStop import Stopper
import cv2
import serial
import numpy as np
import threading
import serial.tools.list_ports
from DecoratorSets import *
from collections import namedtuple



'''
1偏移量
2开始停车的标志位
3什么时候停（暂定）
4发右边线的角度
5
'''

def init_serial_data_dict():
    Data_dict = namedtuple('data', ['id', 'header'])
    id_sets = ['offset_flag', 'backing_start_flag', 'stop_flag', 'right_pos_angle']
    data_dict_sets = [Data_dict(n, [0, 0])._asdict() for n in id_sets]
    data_dict_sets = {item['id']: item['header'] for item in data_dict_sets}
    data_dict_sets['offset_flag'] = [0xFF, 0xFE]
    data_dict_sets['backing_start_flag'] = [0xEF, 0xEE]
    data_dict_sets['stop_flag'] = [0xDF, 0xDE]
    data_dict_sets['right_pos_angle'] = [0xCF, 0xCE]
    return data_dict_sets

def init_serial():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        print('找不到串口')
    else:
        for i in range(0, len(port_list)):
            print(port_list[i][0])
        try:
            ser = serial.Serial(port_list[0][0], 115200, timeout=0.000001)
            # ser1 = serial.Serial(port_list[1][0],115200,timeout=0.001)
            return ser
        except:
            print('please check the serial')

def reset():
    global cross_num, cross_flag, cross_is_finish, stop_flag, back_start,is_backing,is_backing_finish,offset_flag
    global cross_none_num
    cross_flag = False
    cross_is_finish = True
    stop_flag = False
    back_start = False
    #is_backing = False
    #is_backing_finish = True
    offset_flag = 0
    cross_none_num = 0

#@Timer
def display(img,flag_crossing,line_num,point,pos_angel,error_y,error_x,lines,cross_num,cross_none_num):
    global cross_ROI,xunxian_mode
    cv2.circle(img, (int(point[0]), int(point[1])), 5, (255, 255, 255), 3)
    cv2.putText(img, str(line_num), (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    if xunxian_mode == 0:
        cv2.line(img, (0, int(error_y)), (640, int(error_y)), (128, 0, 0), 1)
    elif xunxian_mode == 1:
        cv2.line(img, (int(error_x), 0), (int(error_x), int(np.array(Detector.width, np.int32))), (0, 0, 255), 1)
        cv2.line(img, (0, int(error_y)), (int(np.array(Detector.height, np.int32)), int(error_y)), (0, 0, 255), 1)

    cv2.putText(img, str(flag_crossing), (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, str(pos_angel), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(img, str(cross_num), (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (98,120, 255), 2, cv2.LINE_AA)
    cv2.putText(img, str(cross_none_num), (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (98, 120, 76), 2, cv2.LINE_AA)
    cv2.rectangle(img,(cross_ROI[0],cross_ROI[1]),(cross_ROI[0]+cross_ROI[2],cross_ROI[1]+cross_ROI[3]),(156,189,109),1)

    if lines[0][0] != None and lines[0][1] != None: #竖线
        img = Detector.show_hough_line(img, lines[0][0], lines[0][1])

    if lines[1][0] != None and lines[1][1] != None: #横线
        img = Detector.show_hough_line(img, lines[1][0], lines[1][1])

    return img


def ROI_judge(point):
    global cross_ROI
    if cross_ROI[0]<point[0]<cross_ROI[0]+cross_ROI[2] and cross_ROI[1]<point[1]<cross_ROI[1]+cross_ROI[3]:
        return True
    else:return False



@LoggerPrinter
def data_packing(data,dict_id):
    global data_dict_sets
    sum_judge = (data_dict_sets[dict_id][0]+data_dict_sets[dict_id][1]+data) / 256
    pack_data = [data_dict_sets[dict_id][0],data_dict_sets[dict_id][1],int(data),int(sum_judge)]
    try:
        ser.write(pack_data)
        return pack_data
    except Exception as e:
        return e

@Eventer
def main_thread():
    global cross_num,cross_flag,cross_is_finish,stop_flag,back_start,g_frame
    global mode,is_backing,is_backing_finish,offset_flag,cross_none_num,cross_ROI,xunxian_mode
    cross_classfic_temp = False
    line_num = 0
    mode = 0
    while True:
        if mode == 1:
            thread_lock.acquire()
            frame = g_frame
            thread_lock.release()
        elif mode == 0:
            ret,frame = capture.read()
        img_display = frame.copy()
        img,cross_flag,lines,point,pos_angel = Detector.crossing_det(frame,img_inner_set=True,img_red_or_gra=True)
        error_y,error_x,contours = Detector.get_error_y(lines[1][0],lines[1][1],xunxian_mode)
        offset_flag = Detector.width/2 - error_y
        _ = data_packing(offset_flag, 'offset_flag')



        if lines[0][0] != None and lines[0][1] != None:
            line_num += 1
            # img_display = Detector.show_hough_line(img_display, lines[0][0], lines[0][1])

        if lines[1][0] != None and lines[1][1] != None:
            # img_display= Detector.show_hough_line(img_display, lines[1][0], lines[1][1])
            line_num += 1

        if cross_flag == 1 and cross_classfic_temp == False and ROI_judge(point) and not is_backing:
            cross_classfic_temp = True
            cross_num += 1

        if cross_classfic_temp and not ROI_judge(point):
            cross_none_num += 1
            if cross_none_num >= 10:
                cross_classfic_temp = False
                cross_none_num = 0

        # if cross_num == 3 or cross_num == 7:
        #     is_backing = True

        img_display= display(img_display, cross_flag, line_num,point,pos_angel,error_y,error_x,lines,cross_num,cross_none_num)
        cv2.imshow('result',img_display)





@Eventer
@Timer
def read_frame_thread():
    global g_frame
    while True:
        ret, g_frame = capture.read()
        if not ret:
            print('camera error')
            capture.release()


if __name__ == '__main__':
    cross_num = 0
    cross_flag = False
    cross_is_finish = True
    stop_flag = False
    back_start = False
    is_backing = False
    is_backing_finish = True
    offset_flag = 0
    cross_none_num = 10
    xunxian_mode = 1
    capture = cv2.VideoCapture(0+cv2.CAP_DSHOW)
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    capture.set(cv2.CAP_PROP_FOURCC, fourcc)
    cross_ROI = [440,0,200,480]
    data_dict_sets = init_serial_data_dict()




    '''
    打开硬件串口
    '''

    ser = init_serial()

    '''
    类实例化
    '''

    Detector = Stopper()

    '''
    线程控制
    '''

    g_frame = np.zeros((352, 288, 3), dtype=np.uint8)
    thread_lock = threading.Lock()

    t_frame = threading.Thread(target=read_frame_thread, args=())
    t_main = threading.Thread(target=main_thread, args=())
    t_main.daemon = True

    '''
    启动线程
    '''
    # t_frame.start()
    # t_main.start()

main_thread()
