import cv2
import cv2 as cv
import numpy as np
#import detect


##滑动条初始化代码

def nothing():
    pass





def save_image_to_threshed():
    h_window = 'h_binary'
    s_window = 's_binary'
    l_window = 'l_binary'
    cv2.namedWindow(h_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(s_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(l_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow('binary', cv2.WINDOW_NORMAL)
    cv.createTrackbar('hmin', 'h_binary', 0, 255, nothing)
    cv.createTrackbar('hmax', 'h_binary', 0, 255, nothing)
    cv.createTrackbar('smin', 's_binary', 0, 255, nothing)
    cv.createTrackbar('smax', 's_binary', 0, 255, nothing)
    cv.createTrackbar('lmin', 'l_binary', 0, 255, nothing)
    cv.createTrackbar('lmax', 'l_binary', 0, 255, nothing)

    videoSourceIndex = 0
    cap = cv2.VideoCapture(cv2.CAP_DSHOW + videoSourceIndex)
    print('1')
    while (1):
        ret, frame = cap.read()

        cv.imshow('test', frame)
        cv.waitKey(10)
        c = cv.waitKey(1)

        if c == 27:
            cv2.imwrite('./1.jpg',frame)
            break
    image = cv2.imread('./1.jpg')
    a,b,c = detect.HSL('./1.jpg',0)
    print(a,b,c)


def HSV_adjuster(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h,v,s = cv2.split(image)


     # try:
    thd1_low,thd1_up,thd2_low,thd2_up,thd3_low,thd3_up = (cv2.getTrackbarPos('thd1_low', 'h_binary')
                                                          ,cv2.getTrackbarPos('thd1_up', 'h_binary')
                                                          ,cv2.getTrackbarPos('thd2_low', 's_binary')
                                                          ,cv2.getTrackbarPos('thd2_up', 's_binary')
                                                          ,cv2.getTrackbarPos('thd3_low', 'v_binary')
                                                          ,cv2.getTrackbarPos('thd3_up', 'v_binary'))

    #red_mask1 = cv2.inRange(image,np.array([thd1_low,thd2_low,thd3_low]),np.array([thd1_up,thd2_up,thd3_up]))
    red_mask1 = cv2.inRange(np.array(h),np.array(thd1_low),np.array(thd1_up))
    red_mask2 = cv2.inRange(np.array(s), np.array(thd2_low), np.array(thd2_up))
    red_mask3 = cv2.inRange(np.array(v), np.array(thd3_low), np.array(thd3_up))
    cv2.imshow('h_binary', red_mask1 )
    cv2.imshow('s_binary', red_mask2)
    cv2.imshow('v_binary', red_mask3)
    mask_red = cv2.bitwise_or(cv2.bitwise_or(red_mask1,red_mask2),red_mask3)
    cv2.imshow('binary', mask_red)
    cv2.waitKey(5)
    return [thd1_low,thd1_up],[thd2_low,thd2_up],[thd3_low,thd3_up]
     # except:
     #    return [thd1_low,thd1_up],[thd2_low,thd2_up],[thd3_low,thd3_up]
     #    print(1)



def save_image_to_threshed_HSL():
    h_window = 'h_binary'
    s_window = 's_binary'
    v_window = 'v_binary'
    cv2.namedWindow(h_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(s_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(v_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow('binary', cv2.WINDOW_NORMAL)
    cv.createTrackbar('thd1_low', 'h_binary', 0, 255, nothing)
    cv.createTrackbar('thd1_up', 'h_binary', 0, 255, nothing)
    cv.createTrackbar('thd2_low', 's_binary', 0, 255, nothing)
    cv.createTrackbar('thd2_up', 's_binary', 0, 255, nothing)
    cv.createTrackbar('thd3_low', 'v_binary', 0, 255, nothing)
    cv.createTrackbar('thd3_up', 'v_binary', 0, 255, nothing)


    videoSourceIndex = 0
    cap = cv2.VideoCapture(cv2.CAP_DSHOW + videoSourceIndex)
    print('1')
    while (1):
        ret, frame = cap.read()

        cv.imshow('test', frame)
        cv.waitKey(10)
        c = cv.waitKey(1)

        if c == 27:
            cv2.imwrite('./1.jpg',frame)
            break
    image = cv2.imread('./1.jpg')
    a,b,c = detect.HSL('./1.jpg',0)
    print(a,b,c)


def save_image_to_threshed_HSV():
    h_window = 'h_binary'
    s_window = 's_binary'
    v_window = 'v_binary'
    cv2.namedWindow(h_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(s_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow(v_window, cv2.WINDOW_NORMAL)
    cv2.namedWindow('binary', cv2.WINDOW_NORMAL)
    cv.createTrackbar('thd1_low', 'h_binary', 0, 255, nothing)
    cv.createTrackbar('thd1_up', 'h_binary', 0, 255, nothing)
    cv.createTrackbar('thd2_low', 's_binary', 0, 255, nothing)
    cv.createTrackbar('thd2_up', 's_binary', 0, 255, nothing)
    cv.createTrackbar('thd3_low', 'v_binary', 0, 255, nothing)
    cv.createTrackbar('thd3_up', 'v_binary', 0, 255, nothing)
    videoSourceIndex = 1
    cap = cv2.VideoCapture(cv2.CAP_DSHOW + videoSourceIndex)
    print('1')
    while (1):
        ret, frame = cap.read()
        cv.imshow('test', frame)
        cv.waitKey(10)
        c = cv.waitKey(1)

        if c == 27:
            cv2.imwrite('./1.jpg', frame)
            break
        image = frame
        a, b, c = HSV_adjuster(image)
        print(a, b, c)

save_image_to_threshed_HSV()
