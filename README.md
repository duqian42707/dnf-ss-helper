# DNF史诗养成模拟机助手

## 功能简介

DNF（地下城与勇士）史诗养成模拟机小游戏，自动检测相同的装备，解放双眼，方便升级

[效果展示](./demo.mp4)

## 用法

1. 电脑需要安装 python 环境
2. 安装依赖：

```shell
   pip install pyautogui pillow opencv-python
```

3. 打开游戏中的史诗养成模拟机，切换到物品栏，运行命令

```shell
   python main.py
```

4. 注意命令窗口不要挡住游戏窗口

## 原理说明

- 利用`pyautogui.screenshot(region)`方法，返回单个物品的截图
- 利用`pyautogui.locate(needleImage, haystackImage, grayscale=False)`方法，判断两个物品图片是否相同
- 利用`pyautogui.moveTo(x, y, duration)`方法，将鼠标移动到对应的位置

## 参考资料

- [pyautogui](https://pyautogui.readthedocs.io/) 模拟人工鼠标键盘操作
- [pillow](https://python-pillow.org/) 图像处理库
- [opencv-python](https://github.com/opencv/opencv-python) 计算机视觉和机器学习软件库
