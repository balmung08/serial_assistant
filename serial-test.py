import serial
import tkinter as tk
import threading
import serial.tools.list_ports
from tkinter import ttk, scrolledtext,filedialog
import tkinter.messagebox
import time
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


#初始化默认设置
def update():

    global status,uart,baud,parity,bytesize,stopbits,send_status,ti,canvas,ly,lx,data,i
    status = "go"
    text = ""
    i=0
    ser=serial.Serial(uart,int(baud),timeout=0.02)
    ser.parity = parity
    ser.bytesize = int(bytesize)
    ser.stopbits = stopbits
    canvas.create_oval(715, 375, 735, 395, fill='red')
    canvas.update()
    while True:
        try:
            size = ser.inWaiting()
            if send_status == "go":
                result = ti.get("1.0", "end")+"\r\n"
                ser.write(result.encode())
                send_status = "stop"
            if size != 0:
                while True:
                    response = ser.read(size) # 读取内容并显示
                    t.insert("insert", response)
                    t.yview_moveto(1.0)
                    
                    if text.endswith("\r\n"):
                        try:
                            print("1")
                            findLink = re.compile(r'ng=(.*)')
                            data = float(re.findall(findLink, text)[0])
                            text = ""
                            ly.append(data)
                            lx.append(i)
                            i += 1
                            break
                        except IndexError as e:
                            print(1,e)
                            text=""
                            pass
                    else:
                        try:
                            text = text + response.decode()
                        except UnicodeDecodeError as e:
                            print(5,e)
                            pass
                            text=""
                    if status == "stop":
                        print("stop1")
                        canvas.create_oval(715, 375, 735, 395,fill='black')
                        canvas.update()
                        break
                if status == "stop":
                    print("stop2")
                    canvas.create_oval(715, 375, 735, 395,fill='black')
                    canvas.update()
                    break

        except UnicodeDecodeError as e:
            print(2,e)
            pass
            text=""

        except ValueError as e:
            print(3,e)
            text = ""
def ui():
    global t,status,canvas
    status = "go"
    #窗体初始化
    window = tk.Tk()
    window.title('串口助手')
    window.geometry('800x600')
    window.resizable(False, False)
    canvas = tk.Canvas(window, width=800, height=600, bg="#F5F5F5")
    canvas.create_rectangle(4, 4, 600, 400, outline='black')
    canvas.create_oval(715,375,735,395,fill='black')
    canvas.place(x=0,y=0)

    w1 = tk.Label(window, text="串口选择:",background="#F5F5F5",font=('', 11))
    w1.place(x=615,y=2)
    w2 = tk.Label(window, text="波特率:",background="#F5F5F5",font=('', 11))
    w2.place(x=615,y=60)
    w3 = tk.Label(window, text="停止位:",background="#F5F5F5",font=('', 11))
    w3.place(x=615,y=95)
    w4 = tk.Label(window, text="数据位:",background="#F5F5F5",font=('', 11))
    w4.place(x=615,y=130)
    w5 = tk.Label(window, text="校验位:",background="#F5F5F5",font=('', 11))
    w5.place(x=615,y=165)
    w6 = tk.Label(window, text="串口操作:",background="#F5F5F5",font=('', 11))
    w6.place(x=615,y=200)
    w6 = tk.Label(window, text="数据操作:",background="#F5F5F5",font=('', 11))
    w6.place(x=615,y=270)
    w7 = tk.Label(window, text="测试功能:",background="#F5F5F5",font=('', 11))
    w7.place(x=615,y=345)
    w8 = tk.Label(window, text="串口状态:", background="#F5F5F5", font=('', 11))
    w8.place(x=615, y=375)



    #文本显示框部署
    t = tk.scrolledtext.ScrolledText(width=82, height=30)
    t.place(x=5,y=5)

    #menu控件部署
    menubar = tk.Menu(window)
    helpmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='关于', menu=helpmenu)
    def ar():
        tk.messagebox.showinfo('关于作者', '本程序来自balmung')
    helpmenu.add_command(label='关于', command=lambda: ar())
    window.config(menu=menubar)

    #按钮控件部署
    botton1 = tk.Button(window, text="开启串口",command=t2_go).place(x=630,y=230)
    botton2 = tk.Button(window, text="关闭串口", command=t2_stop).place(x=720, y=230)
    botton3 = tk.Button(window, text="清除接收", command=delete_all).place(x=630, y=295)
    botton4 = tk.Button(window, text="保存接收", command=save_all).place(x=720, y=295)
    botton5 = tk.Button(window, text="实时绘图",command=t4_go).place(x=710, y=340)
    #组合框控件部署-串口选择组合框
    def uart_detect():
        while True:
            global combobox1, uart_list
            uart_list = []
            uart_class = serial.tools.list_ports.comports()
            for i in uart_class:
                uart_list.append(i[0])
            old_uart_list = []
            if old_uart_list != uart_list:
                combobox1["values"] = uart_list
    thread3 = myThread(3, "Thread-3", uart_detect)
    thread3.daemon = True
    thread3.start()
    time.sleep(0.01)
    global uart_list,combobox1
    values1 = uart_list
    combobox1 = ttk.Combobox(
            master=window,  # 父容器
            height=3,  # 高度,下拉显示的条目数量
            width=20,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 12),  # 字体
            values=values1,  # 设置下拉框的选项
            )

    def choose1(event):
        global uart
        uart = combobox1.get()

    combobox1.bind('<<ComboboxSelected>>', choose1)
    combobox1.place(x=615,y=25)
    #window.mainloop()

    #组合框控件部署-波特率选择组合框
    values2 = ['9600','14400','19200','38400','57600','115200','256000','460800']
    combobox2 = ttk.Combobox(
            master=window,  # 父容器
            height=4,  # 高度,下拉显示的条目数量
            width=11,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 12),  # 字体
            values=values2,  # 设置下拉框的选项
            )
    combobox2.current(5)
    def choose2(event):
        global baud
        baud = combobox2.get()

    combobox2.bind('<<ComboboxSelected>>', choose2)
    combobox2.place(x=685,y=60)

    #组合框控件部署-停止位选择组合框
    values3 = ['1','1.5','2']
    combobox3 = ttk.Combobox(
            master=window,  # 父容器
            height=3,  # 高度,下拉显示的条目数量
            width=11,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 12),  # 字体
            values=values3,  # 设置下拉框的选项
            )
    combobox3.current(0)
    def choose3(event):
        global stopbits
        stopbits = combobox3.get()
        if stopbits==1 or stopbits==2:
            stopbits = int(stopbits)
        else:
            stopbits = float(stopbits)
    combobox3.bind('<<ComboboxSelected>>', choose3)
    combobox3.place(x=685,y=95)

    #组合框控件部署-数据位选择组合框
    values4 = ['8','7']
    combobox4 = ttk.Combobox(
            master=window,  # 父容器
            height=2,  # 高度,下拉显示的条目数量
            width=11,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 12),  # 字体
            values=values4,  # 设置下拉框的选项
            )
    combobox4.current(0)
    def choose4(event):
        global bytesize
        bytesize = combobox4.get()
    combobox4.bind('<<ComboboxSelected>>', choose4)
    combobox4.place(x=685,y=130)

    #组合框控件部署-数据位选择组合框
    values5 = ["奇校验","偶校验","无校验"]
    combobox5 = ttk.Combobox(
            master=window,  # 父容器
            height=3,  # 高度,下拉显示的条目数量
            width=11,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 12),  # 字体
            values=values5,  # 设置下拉框的选项
            )
    combobox5.current(2)
    def choose5(event):
        global parity
        parity = combobox5.get()
        if parity=="奇校验":
            parity = 'O'
        elif parity=="偶校验":
            parity = 'E'
        elif parity=="无校验":
            parity = 'N'
    combobox5.bind('<<ComboboxSelected>>', choose5)
    combobox5.place(x=685,y=165)

    notebook = tkinter.ttk.Notebook(window,width=795,height=162)
    frameOne = tkinter.Frame()
    global frameTwo
    frameTwo = tkinter.Frame()
    frameThree = tkinter.Frame()
    notebook.add(frameOne, text='串口发送')
    notebook.place(x=5,y=405)
    canvas1 = tk.Canvas(frameOne, width=800, height=600, bg="#F5F5F5")
    canvas1.create_rectangle(2, 2, 655, 151, outline='black')
    canvas1.place(x=0,y=0)
    global ti
    ti = tk.scrolledtext.ScrolledText(frameOne,width=90, height=11)
    ti.place(x=3,y=3)
    w9 = tk.Label(frameOne, text="发送操作:",background="#F5F5F5",font=('', 11))
    w9.place(x=660,y=2,)
    def send():
        global send_status
        send_status = "go"
    tk.Button(frameOne, text="发送",command=send).place(x=700, y=35,width = 59, height = 30)

    def delete_send():
        global ti
        ti.delete(1.0, tk.END)
    tk.Button(frameOne, text="清除发送",command=delete_send).place(x=700, y=75)

    def read_send():
        global ti, status
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"),))
        if filename != "":
            try:
                with open(filename, "r",newline='') as f:
                    text = f.read()
                    ti.insert("insert", text)
            except Exception as e:
                print(4,e)
    tk.Button(frameOne, text="读取文件",command=read_send).place(x=700, y=115)
    def delete_list():
        global lx,ly,i
        lx=[]
        ly=[]
        i = 0
    notebook.add(frameTwo, text='图片显示')
    tk.Button(frameTwo, text="清除", command=delete_list).place(x=740, y=75)
    valuesn = ['20','50','100','200','400','800','2000',]
    combobox7 = ttk.Combobox(
            master=frameTwo,  # 父容器
            height=4,  # 高度,下拉显示的条目数量
            width=6,  # 宽度
            state='readonly',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 12),  # 字体
            values=valuesn,  # 设置下拉框的选项
            )
    combobox7.current(2)
    def choose7(event):
        global length
        length = combobox7.get()

    combobox7.bind('<<ComboboxSelected>>', choose7)
    combobox7.place(x=720,y=25)
    w10 = tk.Label(frameTwo, text="横轴长度:", background="#F5F5F5", font=('', 11))
    w10.place(x=715, y=0)

    notebook.add(frameThree, text='注意事项')
    w11 = tk.Label(frameThree, text="画图请输入balmung=______,下划线处填写数据，注意没有引号", background="#F5F5F5", font=('华文行楷', 16))
    w11.place(x=100, y=15)
    w12 = tk.Label(frameThree, text="请不要在正在绘图时点击实时绘图按钮", background="#F5F5F5", font=('华文行楷', 16))
    w12.place(x=100, y=55)
    w13 = tk.Label(frameThree, text="想要暂停则直接关闭串口，清空图像则直接点击清空按钮", background="#F5F5F5", font=('华文行楷', 16))
    w13.place(x=100, y=95)
    w14 = tk.Label(frameThree, text="画图功能未完善，数据仅在一秒30帧及以下有较高的保真度", background="#F5F5F5", font=('华文行楷', 16))
    w14.place(x=100, y=135)
    window.mainloop()

def mat_draw():
    global lx,ly,length
    def draw():
        while True:
            try:
                plt.cla()  # 清除上一次的残留

                start = len(lx)-int(length)
                if start < 0:
                    start = 0
                plt.xlim(start, len(lx))  # 设置x轴坐标范围
                plt.ylim(1.2*min(ly), 1.2*max(ly))  # 设置y轴坐标范围
                plt.plot(lx,ly)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tkinter.BOTTOM,  # 上对齐
                                        # fill=tkinter.BOTH,  # 填充方式
                                            expand=tkinter.YES)  # 随窗口大小调整而调整
                frameTwo.update()

            except Exception as e:
                print(5,e)
                continue

    fig, ax = plt.subplots()
    canvas = FigureCanvasTkAgg(fig, frameTwo)
    draw()

#区分线程来使得ui和刷新异步
class myThread(threading.Thread):
    def __init__(self, threadID, name, function):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.function = function
        # self.lock = threading.RLock()

    def run(self):
        # self.lock.acquire()
        self.function()
        # self.lock.acquire()


def t1_go():
    thread1.start()
def t2_go():
    thread2 = myThread(2, "Thread-2", update)
    thread2.daemon = True
    thread2.start()
def t2_stop():
    global status
    status = "stop"
    print("STOP")
def t4_go():
    thread4 = myThread(4, "Thread-4", mat_draw)
    thread4.daemon = True
    thread4.start()

def delete_all():
    global t
    t.delete(1.0, tk.END)
def save_all():
    global t,status
    status = "stop"
    result = t.get("1.0", "end")
    filename = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"),))
    if filename != "":
        try:
            with open(filename+".txt", "w+") as f:
                f.write(result)
                f.close()
        except Exception as e:
            pass


if __name__ == '__main__':
    baud = 115200
    parity = 'N'
    bytesize = 8
    stopbits = 1
    send_status = "stop"
    ly = [0]
    lx = [0]
    data = 0
    i = 0
    length = 100
    thread1 = myThread(1, "Thread-1", ui)
    t1_go()







