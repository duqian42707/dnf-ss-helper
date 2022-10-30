# -*- coding: utf-8 -*-
# 打开史诗养成模拟器，并切换到物品栏标签

from tkinter.dnd import dnd_start
import pyautogui
import time


# 可信度
confidence = 0.8


# 相对坐标 转 绝对坐标
def transform(arr, origin):
    return (arr[0] + origin[0], arr[1]+origin[1])


# 左上角坐标 转 中心坐标
def transformCenter(arr, width):
    return (arr[0] + width/2, arr[1]+width/2)

# 装备正方形


class Square(object):
    # 面板左上角的绝对坐标
    origin = (0, 0)
    # 装备左上角相对于面板左上角的坐标
    rel_location = (0, 0)
    # 装备左上角的绝对坐标
    abs_location = (0, 0)
    # 装备中心点的绝对坐标
    abs_center_location = (0, 0)
    # 装备待匹配时，扩大后的图片左上角的绝对坐标
    abs_match_location = (0, 0)

    width = 30
    # 1 身上 2 背包
    type = 0
    # 编号，身上1~11，背包1~60
    id = 0
    img = None
    matchImg = None

    def __init__(self, origin, location, type, id):
        self.origin = origin
        self.rel_location = location
        self.abs_location = transform(self.rel_location, self.origin)
        self.abs_center_location = transformCenter(
            self.abs_location, self.width)
        self.abs_match_location = (
            self.abs_location[0]-3, self.abs_location[1]-3)
        self.type = type
        self.id = id

    # 获取本装备图片
    def getShootImg(self, save=True):
        if self.img == None:
            filename = "imgs/type_" + \
                str(self.type)+"_id_"+str(self.id) + ".png"
            if save:
                self.img = pyautogui.screenshot(filename, region=(
                    self.abs_location[0], self.abs_location[1], self.width, self.width))
            else:
                self.img = pyautogui.screenshot(
                    region=(self.abs_location[0], self.abs_location[1], self.width, self.width))
        return self.img

    # 获取本装备作为比对样本时的图片，范围会适当扩大
    def getMatchImg(self, save=True):
        if self.matchImg == None:
            filename = "imgs/match_type_" + \
                str(self.type)+"_id_"+str(self.id) + ".png"
            if save:
                self.matchImg = pyautogui.screenshot(filename, region=(
                    self.abs_match_location[0], self.abs_match_location[1], self.width+6, self.width+6))
            else:
                self.matchImg = pyautogui.screenshot(region=(
                    self.abs_match_location[0], self.abs_match_location[1], self.width+6, self.width+6))
        return self.matchImg

    # 判断这个区域是不是空白的
    def is_blank(self):
        img = self.getShootImg()
        return pyautogui.locate(img, 'blank.png', confidence=confidence) != None

    # 判断本装备是否和另一个装备一样
    def is_img_match(self, another):
        img1 = self.getShootImg()
        img2 = another.getMatchImg()
        return pyautogui.locate(img1, img2, confidence=confidence) != None

    # 将鼠标移动到本装备的中心点
    def moveToMe(self):
        pyautogui.moveTo(
            self.abs_center_location[0], self.abs_center_location[1], 0.3)


class DnfSSFind(object):
    origin = ()
    matchImgs = []

    # 获取面板左上角坐标
    def initOrigin(self):
        print('1.根据物品栏图标获取面板坐标...')
        wupinlan = pyautogui.locateOnScreen(
            'wupinlan.png', confidence=confidence)
        if wupinlan == None:
            print('-->未找到物品栏，请打开史诗养成模拟机并切换到物品栏!')
            return
        self.origin = (wupinlan[0] - 204, wupinlan[1] - 509)
        print('-->成功')

    # 身上11件装备
    def initOnBody(self):
        print('2.初始化身上11件装备...')
        self.onBody = [
            # 左边五件
            Square(self.origin, (80, 122), 1, 1),
            Square(self.origin, (119, 122), 1, 2),
            Square(self.origin, (80, 158), 1, 3),
            Square(self.origin, (119, 158), 1, 4),
            Square(self.origin, (80, 196), 1, 5),
            # 右边六件
            Square(self.origin, (370, 122), 1, 6),
            Square(self.origin, (410, 122), 1, 7),
            Square(self.origin, (370, 158), 1, 8),
            Square(self.origin, (410, 158), 1, 9),
            Square(self.origin, (370, 195), 1, 10),
            Square(self.origin, (410, 195), 1, 11)
        ]
        print('-->成功')

    # 背包5排,排除空白格子
    def initInPackage(self):
        print("3.初始化背包5排装备，排除空白栏位")
        left = 57
        top = 316
        self.inPackage = []
        for i in range(0, 5):
            for j in range(0, 12):
                x = left + j * 34
                y = top + i * 34
                id = i*12+j+1
                if j > 3:
                    x = x+1
                if j > 6:
                    x = x+1
                if j > 9:
                    x = x+1
                item = Square(self.origin, (x, y), 2, id)
                if item.is_blank():
                    continue
                self.inPackage.append(item)
        print('-->成功')

    # 遍历背包所有装备，进行匹配，看是否有相同的
    def match(self):
        print('4.开始匹配，背包里共有 '+str(len(self.inPackage))+" 件装备")
        print('4.1.先和身上的匹配...')
        for index1, item1 in enumerate(self.inPackage):
            # print('比对背包装备：'+str(index1))
            for item2 in self.onBody:
                # print("正在匹配"+str(item1)+str(item2))
                if item1.is_img_match(item2):
                    self.matchImgs.append([item1, item2])

        print('-->匹配结果：'+str(len(self.matchImgs)))
        print('4.2.再和背包里的匹配...')
        for index1, item1 in enumerate(self.inPackage):
            # print('比对背包装备：'+str(index1))
            for index2, item2 in enumerate(self.inPackage):
                # 如果item1在item2后面，则已经匹配过了，跳过
                if index1 >= index2:
                    continue
                # print("正在匹配"+str(item1)+str(item2))
                if item1.is_img_match(item2):
                    self.matchImgs.append([item1, item2])
        print('-->匹配结果：'+str(len(self.matchImgs)))

    # 展示匹配的装备
    def showLocation(self):
        print("5.展示匹配成功的装备...")
        for index, match in enumerate(self.matchImgs):
            if index > 0:
                key = input('? 按任意键继续，按 1 退出\n')
                if key == '1':
                    break
            match[0].moveToMe()
            time.sleep(0.5)
            match[1].moveToMe()

        key = input('? 按任意键再展示一次，按 1 退出\n')
        if key != '1':
            self.showLocation()

    # 主程序开始

    def start(self):
        self.initOrigin()
        self.initOnBody()
        self.initInPackage()
        self.match()
        if len(self.matchImgs) == 0:
            return
        self.showLocation()


if __name__ == '__main__':
    dnfSSFind = DnfSSFind()
    dnfSSFind.start()
