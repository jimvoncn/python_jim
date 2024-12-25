# 第一个python代码，注意有效性和可控性、注意我的代码十分精简


# 1. a是变量名，第1关：编程简单得跟玩一样
a = 0
b = a + 1


# 2. 第2关
x = -3.3 / 10
if not (x == -0.33):
    print(f"负3.3除以10实际上={x}，小数是不精确的")


# 3. 质变：函数
def sub_test03():
    def f(x):  # 建议：不要像这样嵌套定义函数
        y = x * 9
        return y

    x = 0
    y = f(x)

    y = f(12345679) * 8

    iv_x = -9000.00000000000000000000000000000000000000000000000000000000000000009
    y = f(iv_x)
    # sub_test03()函数在最后面__name__ == "__main__"的时候被调用
    # 打断点debug看效果，可以百度搜索：怎么在vscode运行和debug python文件


# 4. 量变：数学的小数函数
def sub_test04():
    import math  # math命名空间、math依赖包、math库、math Library
    import random  # random命名空间

    # 小数函数
    lv_x = math.sin(math.pi)
    lv_x = math.log(math.e)
    lv_x = math.sqrt(3)
    lv_x = math.pow(3, 1 / 2)  # 3的二分之一次方，与math.sqrt根号3相同
    lv_x = random.random() * 60
    try:
        lv_x = 10 / 0  # 报错：除0异常
        lv_x = math.log10(-1)  # 报错：对数函数不能为负数
        lv_x = math.pow(2, 10000)  # 报错：无限大，才2的1万次方而已
    except Exception as lo_ex:
        lv_str = str(lo_ex)

    # 整数函数
    lv_int = int(-15.5)
    lv_int = math.floor(-15.001)
    lv_int = round(-15.5)  # 四舍五入与整除、余数
    lv_div = -23.4 // 6
    lv_mod = 23.4 % 6


# 5. 未来展望
def sub_test05():
    if False:
        # 如果是已经会Java、C++的程序员
        lv_x = 1 << 10  # 正常的移位操作
        lv_x = 2**10  # 乘方
        lv_x = 1 + 2j  # 复数、虚数
        if lv_x == 1:  # 确实没有case-when
            pass  # 不能不写，必须写pass语句
        elif lv_x == 2:  # 不是 else if 吗
            pass
        else:
            pass

    # 科学计算：import numpy
    # 科学计算-高级：import scipy
    # 可视化-折线图：import matplotlib.pyplot as plt
    # 数据挖掘：import pandas
    # 机器学习：import torch
    # 推论：
    #     数学运算-->线性代数-->机器学习-->人工智能
    #     字符串处理-->纯文字-->代码和文档-->可控性


if __name__ == "__main__":
    sub_test03()
    sub_test04()
    sub_test05()

    # 加一句input让命令行窗口停住
    lv_ret = input("ENTER to exit...")
