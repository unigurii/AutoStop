import numpy as np
import cv2 as cv
import cv2
from DecoratorSets import Timer
from DecoratorSets import Fer
from DecoratorSets import Logger
from DecoratorSets import Eventer

class Stopper:
    def __init__(self,mode = 0,cross_num_flag = 0,img_w = 640,img_h = 480,canny_th1=45,canny_th2=135,kernel_ero=10, hough_line_point=80):
        self.mode = mode
        self.cross_num_flag = cross_num_flag
        self.width = img_w
        self.height = img_h
        self.kernel = cv.getStructuringElement(cv.MORPH_RECT, (kernel_ero, kernel_ero))
        self.hough_line_point = hough_line_point
        self.canny1 = canny_th1
        self.canny2 = canny_th2
        self.flag_crossing = False
        self.Vertical_max_thr = np.pi/4.
        self.Vertical_min_thr =3.* np.pi/4.0



    def __red_read(self,img):

        red0_low = np.array([224, 0, 255])
        red0_up = np.array([227, 62, 255])

        input = img
        hsv = cv2.cvtColor(input, cv2.COLOR_BGR2HSV)
        h, v, s = cv2.split(hsv)
        red_mask1 = cv2.inRange(np.array(h), np.array(red0_low[0]), np.array(red0_up[0]))
        red_mask2 = cv2.inRange(np.array(s), np.array(red0_low[1]), np.array(red0_up[1]))
        red_mask3 = cv2.inRange(np.array(v), np.array(red0_low[2]), np.array(red0_up[2]))
        mask_red = cv2.bitwise_or(cv2.bitwise_or(red_mask1, red_mask2), red_mask3)
        cv2.imshow('red_mask3', mask_red)
        mask_red = cv2.dilate(mask_red, self.kernel, iterations=1)
        output = cv2.erode(mask_red, self.kernel, iterations=2)
        self.binary = output
        return output

    def __line_mean(self, lines):
        add_r = 0
        add_th = 0
        add_r_ = 0
        add_th_ = 0
        num = 0
        num_ = 0
        mean_r = 0
        mean_th = 0
        mean_r_ = 0
        mean_th_ = 0
        if not lines:
            return None
        else:
            for line in lines:
                if line[0] > 0:
                    add_r += line[0]
                    add_th += line[1]
                    num = num + 1
                else:
                    add_r_ += line[0]
                    add_th_ += line[1]
                    num_ += 1
            if num != 0:
                mean_r = add_r / num
                mean_th = add_th / num

            elif num_ != 0:
                mean_r_ = add_r_ / num_
                mean_th_ = add_th_ / num_
            else:
                return None
            if mean_r > (-mean_r_):
                return [mean_r, mean_th]
            else:
                return [mean_r_, mean_th_]


    def __img_lines(self, input):
        dst = cv2.Canny(input, self.canny1, self.canny2, apertureSize=3)
        cv2.imshow('dst', dst)
        cv2.waitKey(10)
        lines = cv2.HoughLines(dst, 1, np.pi / 360, self.hough_line_point)
        if lines is None:
            #print('lines is None')
            return None
        else:
            add_lines = []
            lines_H = []
            lines_E = []
            for line in lines:
                [rho, theta] = line[0]
                if (theta < (np.pi / 4.)) or (theta > (3. * np.pi / 4.0)):
                    lines_H.append([rho, theta]) #lines_H为检测到的垂直方向线
                else:
                    lines_E.append([rho, theta])
            if self.__line_mean(lines_H) is not None:
                add_lines.append(self.__line_mean(lines_H))
            if self.__line_mean(lines_E) is not None:
                add_lines.append(self.__line_mean(lines_E))
            return add_lines
    def get_red(self, img):
        """
        获取红色掩膜
         """
        return self.__red_read(img)

    def cross_pos(self,r1,th1,r2,th2):
        a,b,r,a1,b1,r1 = (np.cos(th1),np.sin(th1),r1,np.cos(th2),np.sin(th2),r2)
        if a == 0:
            a = 0.001
        if b == 0:
            b = 0.001
        if a1 == 0:
            a1 = 0.001
        if b1 == 0:
            b1 = 0.001
        k,k1 = (-a / b, -a1 / b1)
        m,m1 = (r/b,r1/b1)
        pos  = np.arctan(abs((k -k1)/(1+k*k1)))*180/np.pi
        x,y= (abs((m1 - m)/(k1 - k))),abs((m1*k-m*k1)/(k-k1))
        print('the pos of line is {}'.format(pos))
        return pos,[x,y]

    def show_hough_line(self, img, rho, thata):
        a = np.cos(thata)
        b = np.sin(thata)
        x0, y0 = a * rho, b * rho
        x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * (a))
        x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * (a))
        error_y = (y1+y2)/2
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        return img


    def crossing_det(self, img, img_inner_set=False, img_red_or_gra=True):
        """
         十字标志识别
        """
        if img_inner_set:
            if img_red_or_gra:
                input = self.__red_read(img)
                #cv2.imshow('test1',input)
                #cv2.waitKey(0)
            else:
                input = self.__img_set(img)
        else:
            input = img
        input = cv2.bilateralFilter(img,9,75,75)
        add_lines = self.__img_lines(input)
        if add_lines is None:
            #print("lines add error")
            return img,False, [[None, None], [None, None]],[0,0],0
        else:
            y = 0
            r = None
            the = None
            r1, th1 = None, None
            line_0 = add_lines[0]
            if line_0 is not None:
                point = [0,0]
                if line_0[1] < np.pi / 4.0 or line_0[1] > 3.0 * np.pi / 4.0:
                    r = line_0[0]
                    the = line_0[1]
                elif np.pi / 3.0 < line_0[1] < 3.0 * np.pi / 5.0:
                    r1, th1 = line_0[0], line_0[1]
                if len(add_lines) >= 2:
                    r1, th1 = add_lines[1][0], add_lines[1][1]
                    # if (add_lines[0][1] - add_lines[1][1]) > 1.45 or (add_lines[0][1] - add_lines[1][1]) < -1.45:
                    if True:
                        y, point = self.cross_pos(add_lines[0][0], add_lines[0][1], add_lines[1][0], add_lines[1][1])
                        img = cv2.putText(img,str(y),(50,50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                        # print(y)
                        if 135 >y > 45:
                            self.flag_crossing = 1
                            print('there is 十')
                        else:
                            self.flag_crossing = 0
                    else:
                        self.flag_crossing = 0
                else:
                    self.flag_crossing = 0

            flag_crossing = self.flag_crossing
            #print(img,self.flag_crossing, [[r, the], [r1, th1]])
            return img,flag_crossing, [[r, the], [r1, th1]], point,y


    def get_error_y(self,rho,thata,mode):
        if mode == 0:
            if rho == None or thata == None:
                # print('no line which for error_x detect')
                return 0,0,0

            else:
                a = np.cos(thata)
                b = np.sin(thata)
                x0, y0 = a * rho, b * rho
                x1, y1 = int(x0 + 1000 * (-b)), int(y0 + 1000 * (a))
                x2, y2 = int(x0 - 1000 * (-b)), int(y0 - 1000 * (a))
                error_x = (x2 + x1) / 2
                error_y = (y2 + y1) / 2
                return error_y,error_x,0
        if mode == 1:
            contours_line, hierarchy0 = cv2.findContours(self.binary, 1, cv2.CHAIN_APPROX_NONE)
            if len(contours_line) > 0:
                # 最大轮廓
                c = max(contours_line, key=cv2.contourArea)
                M = cv2.moments(c)
                try:
                    x = int(M['m10'] / M['m00'])
                except:
                    a = 1
                    x = 0
                offset_flag = 320 - x
                try:
                    y = int(M['m01'] / M['m00'])  # 计算质心位置
                except:
                    a = 1
                    # print(x, y)

            return y , x,contours_line








