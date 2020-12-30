#! /usr/bin/env python
import rospy
import cv2
from hashlib import sha1
from cv_bridge import CvBridge, CvBridgeError
import sensor_msgs.msg
from std_msgs.msg import String
from Tkinter import*
import ttk
import tkMessageBox

from PIL import ImageTk, Image
import threading

bridge = CvBridge()
global panel
panel = None


class Login:
    def __init__(self, root):
        self.root=root
        self.root.title("Login System")
        self.root.geometry("1200x600+100+50")
        self.root.resizable(False, False)
        # backgound Image
        self.bg = ImageTk.PhotoImage(file="background.jpg")
        self.bg_image = Label(self.root, image = self.bg).place(x=0,y=0,relwidth=1,relheight=1)

        #login frane
        self.Frame_login = Frame(self.root, bg="black")
        self.Frame_login.place(x=70,y=150,height=340,width=500)

        title = Label(self.Frame_login, text="WELCOME !", font=("Impact",25,"bold"),fg="#8ddbf0", bg="black").place(x=150,y=30)

        user_label = Label(self.Frame_login, text = "Username", font=("Goudy old style", 15), fg="#8ddbf0", bg="black").place(x=90,y=100)
        self.user = Entry(self.Frame_login, font=("times new roman",15), bg="lightgray")
        self.user.place(x=90,y=140,width=320,height=35)

        password_label = Label(self.Frame_login, text = "Password", font=("Goudy old style", 15), fg="#8ddbf0", bg="black").place(x=90,y=190)
        self.password = Entry(self.Frame_login, font=("times new roman",15), bg="lightgray")
        self.password.place(x=90,y=230,width=320,height=35)

        self.Login_btn = Button(self.Frame_login, command=self.login_function, text= "Log In", bg="#8ddbf0", fg="black", font=("times new roman",20)).place(x=175, y=285, width=150, height=35)

    def createOval(self, r, c):
        circleCanvas = Canvas(self.tab1, width=20, height=20)
        circleCanvas.grid(row=r, column=c)
        oval = circleCanvas.create_oval(0, 0, 20, 20, width=0, fill='green')
        return [oval,circleCanvas]

    def login_function(self):
        global panel
        if self.user.get()=="" or self.password.get()=="":
            # tkMessageBox.showerror("Error","All fields are required", parent=self.root)
        # elif self.user.get() != "k" or self.password.get() != "1":
            # tkMessageBox.showerror("Error","Invalid password/username", parent=self.root)
        # else:
            # for widget in self.root_children():
            #    widget.destroy()
            #
            # # this will clear frame and frame will be empty
            # # if you want to hide the empty panel then
            # self.root.pack_forget()
            self.Frame_login.destroy()

            self.tab_parent = ttk.Notebook(root)
            self.tab1 = ttk.Frame(self.tab_parent)
            tab2 = ttk.Frame(self.tab_parent)
            tab3 = ttk.Frame(self.tab_parent)

            self.tab_parent.add(self.tab1, text="Feedback")
            self.tab_parent.add(tab2, text="Command")
            self.tab_parent.add(tab3, text="Training")
            self.tab_parent.pack(expand=1, fill='both')

            # Progress bar widget
            self.prox1 = ttk.Progressbar(self.tab1, orient = HORIZONTAL,length = 100, mode = 'determinate')
            self.prox1.grid(column=4, row=3)
            self.prox2 = ttk.Progressbar(self.tab1, orient = HORIZONTAL,length = 100, mode = 'determinate')
            self.prox2.grid(column=4, row=4)
            self.prox3 = ttk.Progressbar(self.tab1, orient = HORIZONTAL,length = 100, mode = 'determinate')
            self.prox3.grid(column=4, row=5)

            # canvas = Canvas(root, width = 300, height = 300)
            # canvas.pack()
            # img = ImageTk.PhotoImage(cv2_img)
            # canvas.create_image(20, 20, anchor=NW, image=img)
            #
            ttk.Label(self.tab1, text="Feedback Information").grid(column=0, row=0, padx=1, pady=1)
            ttk.Label(self.tab1, text="Proximity sensor 1(forward): ").grid(column=3, row=3, padx=40, pady=1)
            ttk.Label(self.tab1, text="Proximity sensor 2(left): ").grid(column=3, row=4, padx=1, pady=1)
            ttk.Label(self.tab1, text="Proximity sensor 2(right): ").grid(column=3, row=5, padx=1, pady=1)


            ttk.Label(self.tab1, text="IR receiver 1").grid(column=3, row=8, padx=40, pady=1)
            ttk.Label(self.tab1, text="IR receiver 2").grid(column=3, row=9, padx=1, pady=1)
            ttk.Label(self.tab1, text="IR receiver 3").grid(column=3, row=10, padx=1, pady=1)

            ttk.Label(self.tab1, text="IMU 1").grid(column=3, row=13, padx=1, pady=1)
            ttk.Label(self.tab1, text="IMU 2").grid(column=3, row=14, padx=1, pady=1)
            ttk.Label(self.tab1, text="IMU 3").grid(column=3, row=15, padx=1, pady=1)
            ttk.Label(self.tab1, text="IMU 4").grid(column=3, row=16, padx=1, pady=1)
            ttk.Label(self.tab1, text="IMU 5").grid(column=3, row=17, padx=1, pady=1)
            ttk.Label(self.tab1, text="IMU 6").grid(column=3, row=18, padx=1, pady=1)

            self.OvalPos = []

            self.OvalPos.append(self.createOval(8,4))
            self.OvalPos.append(self.createOval(9,4))
            self.OvalPos.append(self.createOval(10,4))
            print(self.OvalPos)

            # circleCanvas1.itemconfig(self.ir1,fill='red')

            ttk.Label(tab2, text="This is Tab 2").grid(column=0, row=0, padx=1, pady=1)
            ttk.Label(tab3, text="This is Tab 3").grid(column=0, row=0, padx=1, pady=1)

            # self.Login_btn.place_forget()
            rospy.init_node('ui', anonymous=True)

            publisher = rospy.Publisher('/Command', String, queue_size=1)
            rospy.Subscriber('/Sensor', String, self.callback1)

            rospy.Subscriber('/Image', sensor_msgs.msg.Image, self.callback_image)



    def callback1(self,data):
        msg = data.data
        if msg.startswith("003"): #Proximity 003U(50,30,25)+28f8649b62d435dc29a95d8f34399195e8f93922
            msg = msg.split("+")
            if msg[1] == str(sha1(msg[0]).hexdigest()):
                ultrasonics = (msg[0][5:-1]).split(",")
                self.prox1['value'] = float(ultrasonics[0])
                self.prox2.step(float(ultrasonics[1]))
                self.prox3.step(float(ultrasonics[2]))

        elif msg.startswith("005"): #IR 005IR(0,0,1)+checksum
            msg = msg.split("+")
            if True: #msg[1] == str(sha1(msg[0]).hexdigest()):
                ir_receivers = (msg[0][6:-1]).split(",")

                ir_receivers = [int(i)*True for i in ir_receivers]
                for i in range(3):
                    if ir_receivers[i] == True:
                        self.OvalPos[i][1].itemconfig(self.OvalPos[i][0],fill='red')
                    else:
                        self.OvalPos[i][1].itemconfig(self.OvalPos[i][0],fill='green')

    def callback_image(self,data):
        global panel
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(data, "bgr8")
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        cv2_img = Image.fromarray(cv2_img)
        cv2_img = ImageTk.PhotoImage(cv2_img)

        if panel is None:
            panel = Label(self.tab1, image=cv2_img)
            # panel.pack(side="bottom", fill="both", expand="yes")

        else:
            panel.configure(image=cv2_img)
            panel.image = cv2_img
            panel.grid(column=0, row=1, rowspan=25, padx=1, pady=1)
            # Save your OpenCV2 image as a jpeg
            # cv2.imshow('camera_image', cv2_img)

            # image = cv2.imread(data.data)
            # cv2.imshow('keshiponk', image)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()


if __name__ == '__main__':

    root = Tk()
    obj=Login(root)
    root.mainloop()

    # rate = rospy.Rate(10)
    # while not rospy.is_shutdown():
    #     info="ui"
    #     # rospy.loginfo(info)
    #     publisher.publish(info)
    #     rate.sleep()
