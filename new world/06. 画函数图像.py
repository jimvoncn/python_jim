if True:
    # pip install matplotlib  #1.需要安装python的matplotlib依赖包，2.建议：不要像这样文件名(包含中文、包含空格、包含标点符号、以数字开头)
    import matplotlib.pyplot as plt
    import math  # 导入依赖包

    # x轴即时间轴取00年代到60年代
    lt_time = [i * 0.01 for i in range(0, 6 * 100 + 1)]

    # 红色 正弦函数，原地踏步
    red = [math.sin(x) for x in lt_time]
    # 蓝色 抛物线，横着放像圆锥曲线那样 sqrt()取平方根
    blue = [math.sqrt(x) for x in lt_time]
    # 紫色 对数函数，=0时None即没有值
    purple = [None] + [math.log(x) for x in lt_time[1:]]
    # 青色 反正切函数，你还当真以为自己是在进步吗
    cyan = [math.atan(x) for x in lt_time]

    yellow = []
    for x in lt_time:
        try:
            # 黄绿橙 双曲线，后来居上 在后期遥遥领先
            yellow.append(math.sqrt(x * x - 1))
        except:
            yellow.append(None)

    # 输出
    plt.cla()  # 清空画布
    plt.plot(lt_time, red, color="red")
    plt.plot(lt_time, blue, color="blue")
    plt.plot(lt_time, purple, color="purple")
    plt.plot(lt_time, cyan, color="cyan")
    plt.plot(lt_time, yellow, color="yellow")
    plt.show()
