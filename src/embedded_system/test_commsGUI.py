import tkinter.messagebox
import comms_module as TestTools2
import threading
import tkinter
import random
import time

MyESP_Port = TestTools2.find_esp_port()
MyESP = TestTools2.initialize_connection(MyESP_Port)

if(MyESP == -1): 
    tkinter.messagebox.showerror("Error", "ESP32 Device Not Found")

MainWindows = tkinter.Tk()
MainWindows.geometry("600x400")
MainWindows.title("TestGUI")


def sendcommand(serial_conn, finger_count):
    start = time.perf_counter()  # chính xác hơn time.time() cho đo ping nhỏ
    result = TestTools2.send_command(serial_conn, finger_count)
    send_lable.config(text = f"Send: {finger_count:.2f}")
    if result:
        ping = (time.perf_counter() - start) * 1000  # ms
        print(f"Ping: {ping:.2f} ms")
        ping_label.config(text=f"Ping: {ping:.2f} ms")
        receivce_lable.config(text = "Receive: OK")
        return ping
    else:
        print("Failed!")
        receivce_lable.config(text = "Receive: Failed")
        ping_label.config(text="Ping: Failed")
        return None


for i in range(6): # button 0 -> 5
    button = tkinter.Button(MainWindows, text=i, font=("Arial", 20,"bold"),command= lambda i = i: sendcommand(MyESP,i))
    button.place(width=100,height=75,x=i*100,y=325)

ping_label = tkinter.Label(MainWindows, text="Ping: -- ms", font=("Arial", 20, "bold"))
ping_label.place(x=200, y=50)  # đặt ở vị trí phù hợp
send_lable =  tkinter.Label(MainWindows, text="Send: -- ", font=("Arial", 20, "bold"))
send_lable.place(x=200,y = 80)
receivce_lable = tkinter.Label(MainWindows, text="Receive: HELLO ", font=("Arial", 20, "bold"))
receivce_lable.place(x=200, y=110)  # đặt ở vị trí phù hợp 


StressProcess = 0
def stress_test():
    global StressProcess
    StressProcess += 1
    global StressTest
    StressTest = True
    if (StressProcess == 1):
        while(StressTest):
            sendcommand(MyESP, random.randint(0,5))
    StressProcess -= 1

def stop_stress():
    global StressTest
    StressTest = False


StressTestButton = tkinter.Button(MainWindows, text="Stress", font=("Arial", 20,"bold"),command = lambda: threading.Thread(target = stress_test).start())
StressTestButton.place(width=100,height=75,x=500,y=0)
Stop = tkinter.Button(MainWindows, text="Stop", font=("Arial", 20,"bold"),command = stop_stress)
Stop.place(width=100,height=75,x=500,y=75)
        


def on_close():
    TestTools2.close_connection(MyESP)
    global StressTest
    StressTest = False  # dừng vòng lặp
    MainWindows.destroy()  # thoát GUI

MainWindows.protocol("WM_DELETE_WINDOW", on_close)

MainWindows.mainloop()

