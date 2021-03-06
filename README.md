# GymAutoOrder
Order gym automatically in SEU.

Forked from [kimixuchen/GymAutoOrder](https://github.com/kimixuchen/GymAutoOrder) and mod by ParadiseDS for easier use

-----------------------
## 简介 ##
* 由于学校羽毛球馆晚上的时段比较抢手，需要早起卡时间点“抢票”，所以制作了这款软件。
* 当天运行程序后，程序会在第二天早8点自动预约1天后的羽毛球场，时间段自定义。大家可以晚上把程序挂在实验室电脑上，然后就回去睡觉吧。
* **但是不宜过多人同时使用**。

----------------------
## 需求环境 ##
1. [python2.7](https://www.python.org/downloads/)
2. ~~[PIL](http://www.pythonware.com/products/pil/)~~[Pillow with jpeg decoder lib support](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pil)

---
## 使用方法 ##
1. 转到文件目录下，运行 `python WebLogin_V1.0.py`
2. 按照提示依次输入学校网站的用户名，密码，手机号，伙伴ID，希望预约的时间段，支持将个人信息录入文件并在下次运行时优先载入，避免重复输入（登录用户名密码使用明文保存，注意安全）
3. 程序~~在午夜12点前启动~~自适应判断，在下一次早晨8点进行预约，离开时不要关闭程序进程和电脑
