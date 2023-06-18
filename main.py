#Import Libraries
import tkinter as tk
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import Canvas, PhotoImage
from tkinter import Label
import tkinter.font as tkFont
import cv2
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from tkinter import messagebox
import pyttsx3
import ast

TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
LABEL_MAP_URL = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_asia_V1_label_map.csv'
IMAGE_SHAPE = (321, 321)

df = pd.read_csv(LABEL_MAP_URL)

classifer = tf.keras.Sequential([
    hub.KerasLayer(
        TF_MODEL_URL,
        input_shape = IMAGE_SHAPE + (3,),
        output_key = "predictions:logits"
    )
])

label_map = dict(zip(df.id, df.name))

def classifyimg(RGBimg):
    RGBimg = np.array(RGBimg) / 255
    RGBimg = np.reshape(RGBimg, (1, 321, 321, 3))
    prediction = classifer.predict(RGBimg)
    return label_map[np.argmax(prediction)]


class LoginScreen:
    def __init__(self,master):
        self.master = master
        self.master.geometry("480x800")
        self.master.title("TensorGaze")
        self.master.configure(bg = "#38b6ff")
        self.master.config(highlightthickness = 3, highlightbackground = "#0000cd")
        self.master.resizable(False,False)
        
        self.heading = tk.Label(self.master, text = "Sign In", fg = "white", bg = "#38b6ff", font = ("Bauhaus 93", 55))
        self.heading.place(relx = 0.5, rely = 0.15, anchor = 'center')

        def on_enter(e):
            self.user.delete(0, "end")

        def on_leave(e):
            self.name = self.user.get()
            if self.name == "" :
                self.user.insert(0, "Username")

        self.user = tk.Entry(self.master, width = 25, fg = "black", border = 0, bg = "white",  font = ("Rockwell", 11))
        self.user.place(relx = 0.25, rely = 0.4, anchor = 'center')
        self.user.insert(0, "Username")
        self.user.bind("<FocusIn>", on_enter)
        self.user.bind("<FocusOut>", on_leave)

        def on_enter(e):
            self.code.delete(0, "end")
            self.code.config(show = '*')
            
        def on_leave(e):
            self.name = self.code.get()
            
            if self.name == "":
                self.code.delete(0, "end")
                self.code.config(show = '')
                self.code.insert(0, "Password")
                
        self.code = tk.Entry(self.master, width = 25, fg = "black", border = 0, bg = "white", font = ("Rockwell", 11), show = '')
        self.code.place(relx = 0.75, rely = 0.4, anchor = 'center')
        self.code.insert(0, "Password")
        self.code.bind("<FocusIn>", on_enter)
        self.code.bind("<FocusOut>", on_leave)

        self.signin_button = tk.Button(self.master, width = 20, pady = 5, text = "Log In", bg = "#2f318b", fg = "white",
                                       font = ("Berlin Sans FB Demi", 13), border = 2, relief = "ridge", borderwidth = 5, bd = 1,
                                       highlightthickness = 0, cursor = "hand2", command = self.SignIn)
        self.signin_button.place(relx = 0.5, rely = 0.55, anchor = 'center')

        self.donthaveacc_button = tk.Button(self.master, text = "Dont Have An Account ?", bg = "#2f318b", fg = "white", font = ("Berlin Sans FB Demi",13), border = 2,
        relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, cursor = "hand2",command = self.donthaveacc)
        self.donthaveacc_button.place(x = 10,y = 750)

    def SignIn(self):
        username = self.user.get()
        password = self.code.get()

        try:
            with open('datasheet.txt', 'r') as file:
                data = file.read()
                stored_credentials = ast.literal_eval(data)

            if username in stored_credentials and password == stored_credentials[username]:
                messagebox.showinfo('Sign In', 'Successfully Signed In')

                self.master.destroy()
                MainScreen()

            else:
                messagebox.showerror('Invalid', 'Invalid Username or Password')

        except FileNotFoundError:
            messagebox.showerror('Error', 'Data file not found')


    def donthaveacc(self):
        self.master.destroy()
        SignUpScreen()
        

class SignUpScreen:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("480x800")
        self.master.title("TensorGaze")
        self.master.configure(bg="#38b6ff")
        self.master.config(highlightthickness=3, highlightbackground="#0000cd")
        self.master.resizable(False, False)
        
        self.heading_signup = tk.Label(self.master, text="Sign Up", fg="white", bg="#38b6ff", font=("Bauhaus 93", 55))
        self.heading_signup.place(relx=0.5, rely=0.15, anchor='center')

        def on_enter_user(e):
            self.user1.delete(0, "end")

        def on_leave_user(e):
            self.name = self.user1.get()
            if self.name == "":
                self.user1.insert(0, "Username")

        self.user1 = tk.Entry(self.master, width=25, fg="black", border=0, bg="white", font=("Rockwell", 11))
        self.user1.place(relx=0.25, rely=0.4, anchor='center')
        self.user1.insert(0, "Username")
        self.user1.bind("<FocusIn>", on_enter_user)
        self.user1.bind("<FocusOut>", on_leave_user)

        def on_enter_code(e):
            self.code1.delete(0, "end")
            self.code1.config(show='*')

        def on_leave_code(e):
            self.name = self.code1.get()
            
            if self.name == "":
                self.code1.delete(0, "end")
                self.code1.config(show='')
                self.code1.insert(0, "Password")
                
        self.code1 = tk.Entry(self.master, width=25, fg="black", border=0, bg="white", font=("Rockwell", 11), show='')
        self.code1.place(relx=0.75, rely=0.4, anchor='center')
        self.code1.insert(0, "Password")
        self.code1.bind("<FocusIn>", on_enter_code)
        self.code1.bind("<FocusOut>", on_leave_code)

        def on_enter_confirm(e):
            self.confirm.delete(0, "end")
            self.confirm.config(show='*')
            
        def on_leave_confirm(e):
            self.name = self.confirm.get()
            
            if self.name == "":
                self.confirm.delete(0, "end")
                self.confirm.config(show='')
                self.confirm.insert(0, "Confirm Password")
                
        self.confirm = tk.Entry(self.master, width=25, fg="black", border=0, bg="white", font=("Rockwell", 11), show='')
        self.confirm.place(relx=0.5, rely=0.5, anchor='center')
        self.confirm.insert(0, "Confirm Password")
        self.confirm.bind("<FocusIn>", on_enter_confirm)
        self.confirm.bind("<FocusOut>", on_leave_confirm)

        self.signup_button = tk.Button(self.master, width=20, pady=5, text="Sign Up", bg="#2f318b", fg="white",
                                       font=("Berlin Sans FB Demi", 13), border=2, relief="ridge", borderwidth=5, bd=1,
                                       highlightthickness=0, cursor="hand2", command=self.sign_up)
        self.signup_button.place(relx=0.5, rely=0.6, anchor='center')

        self.ihaveacc_button = tk.Button(self.master, text="I Have An Account?", bg="#2f318b", fg="white",
                                         font=("Berlin Sans FB Demi", 13), border=2, relief="ridge", borderwidth=5, bd=1,
                                         highlightthickness=0, cursor="hand2", command=self.ihaveacc)
        self.ihaveacc_button.place(x=10, y=750)


    def sign_up(self):
        username1 = self.user1.get()
        password1 = self.code1.get()
        confirm_password = self.confirm.get()

        if password1 == confirm_password:
            try:
                with open('datasheet.txt', 'r+') as file:
                    data = file.read()
                    stored_credentials = ast.literal_eval(data)

                    stored_credentials[username1] = password1
                    file.seek(0)
                    file.write(str(stored_credentials))
                    file.truncate()

                messagebox.showinfo('SignUp', 'Successfully Signed Up')

                self.master.destroy()
                LoginScreen(tk.Tk())

            except FileNotFoundError:
                with open('datasheet.txt', 'w') as file:
                    credentials = {username1: password1}
                    file.write(str(credentials))

                messagebox.showinfo('SignUp', 'Successfully Signed Up')

                self.master.destroy()
                LoginScreen(tk.Tk())

        else:
            messagebox.showerror('Invalid', 'Both Password and Confirm Password should match')

    def ihaveacc(self):
        self.master.destroy()
        LoginScreen(tk.Tk())


class MainScreen:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("480x800")
        self.master.title("TensorGaze")
        self.master.configure(bg = "#38b6ff")
        self.master.config(highlightthickness = 3, highlightbackground = "#0000cd")
        self.master.resizable(False,False)

        self.welcome_label = tk.Label(self.master, text = 'Welcome', bg = "#38b6ff" ,fg = "white", font = ("Bauhaus 93", 55))
        self.welcome_label.place(relx = 0.5, rely = 0.3, anchor = 'center')
        
        self.ab_button = tk.Button(self.master, text = "About",cursor = "hand2", bg = "#2f318b", fg = "white", relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, font = ("Berlin Sans FB Demi", 14), command = self.switch_screen1)
        self.ab_button.place(x = 10, y = 10)
        
        self.get_started_button = tk.Button(self.master, text = "Get Started",cursor = "hand2", bg = "#2f318b", fg = "white", relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, font = ("Berlin Sans FB Demi", 18), command = self.switch_screen)
        self.get_started_button.place(relx = 0.5, rely = 0.5, anchor = 'center')
        
    def switch_screen(self):
        self.master.destroy()
        SecondScreen()

    def switch_screen1(self):
        self.master.destroy()
        ThirdScreen()


class SecondScreen:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("480x800")
        self.master.title("TensorGaze")
        self.master.configure(bg = "#38b6ff")
        self.master.config(highlightthickness = 3, highlightbackground = "#0000cd")
        self.master.resizable(False,False)

        self.Live_detect_button = tk.Button(self.master, text = "      Live Detecting      ",cursor = "hand2", bg = "#2f318b", fg = "white", relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, font = ("Berlin Sans FB Demi", 14), command = self.live_detecting)
        self.Live_detect_button.place(relx = 0.50, rely = 0.4, anchor = 'center')

        self.detect_button = tk.Button(
            self.master,text = "          Detect Images          ", bg = "#2f318b",cursor = "hand2", fg = "white", relief = "ridge", borderwidth = 5, bd = 1,
            highlightthickness = 0, font = ("Berlin Sans FB Demi", 14), command = self.detect_image)
        self.detect_button.place(relx = 0.50, rely = 0.5, anchor = 'center')


        self.back_button = tk.Button(self.master, text = "Go back",cursor = "hand2", bg = "#2f318b", fg = "white", relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, font = ("Berlin Sans FB Demi", 14), command = self.switch_screen)
        self.back_button.place(x = 10, y = 10)

        self.tensorgaze_logo = tk.PhotoImage(file = "TensorGaze 2.png")
        self.tensorgaze_logo = self.tensorgaze_logo.subsample(2, 2)
        
        self.logo_label = tk.Label(self.master, image = self.tensorgaze_logo,bg = "#38b6ff")
        self.logo_label.place(relx = 0.5, rely = 0.78, anchor = 'center')

        self.explore_label = tk.Label(self.master, text = "Explore!", bg = "#38b6ff", fg = "white", font = ("Bauhaus 93", 45))
        self.explore_label.place(relx = 0.5, rely = 0.18, anchor = 'center')
        
    def switch_screen(self):
        self.master.destroy()
        MainScreen()

    def detect_image(self):
        file_path = filedialog.askopenfilename()
        print("Selected file path :", file_path)

        if file_path:
            img = cv2.imread(file_path)
            BGRimg = cv2.resize(img, (640, 480))
            RGBimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            RGBimg = cv2.resize(RGBimg, (321, 321))
            result = classifyimg(RGBimg)
            print(result)
            cv2.rectangle(BGRimg, (0, 480), (640, 425), (50, 50, 255), -2)
            cv2.putText(BGRimg, 'Predicted : {}'.format(str(result)), (20, 460), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.imshow("Predicted Image", BGRimg)
            cv2.waitKey(0)

    def live_detecting(self):
        thres = 0.5
        
        cap = cv2.VideoCapture(1)
        cap.set(3,640)
        cap.set(4,480)
        
        classnames = []
        classfile = "coco.pbtxt"
        
        with open(classfile, 'rt') as f:
            classnames = f.read().rstrip("\n").split("\n")
            
        configpath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightspath = 'frozen_inference_graph.pb'
        
        net = cv2.dnn_DetectionModel(weightspath,configpath)
        net.setInputSize(320,320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5,127.5,127.5))
        net.setInputSwapRB(True)
        
        while True:
            success,img = cap.read()
            classIds , confs , bbox = net.detect(img,confThreshold = thres)
            print(classIds,bbox)
            
            if len(classIds) != 0:
                for classId , confidence , box in zip(classIds.flatten(),confs.flatten(),bbox):
                    cv2.rectangle(img,box,color = (0,255,2),thickness = 3)
                    cv2.putText(img,classnames[classId - 1].upper(),(box[0] + 10,box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence * 100,2)),(box[0] + 200,box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,5),2)
                    
            cv2.imshow("Live-Detecting",img)
            # Exit loop when 'q' key is pressed
            if cv2.waitKey(1) == ord('q'):
                break
            
        cv2.destroyAllWindows()       


class ThirdScreen:
    def __init__(self):
        self.master = tk.Tk()
        self.master.geometry("480x800")
        self.master.title("TensorGaze")
        self.master.configure(bg = "#38b6ff")
        self.master.config(highlightthickness = 3, highlightbackground = "#0000cd")
        self.master.resizable(False,False)

        self.goback_button = tk.Button(self.master, text = "Go back",cursor = "hand2", bg = "#2f318b", fg = "white", relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, font = ("Berlin Sans FB Demi", 14), command = self.switch_screen)
        self.goback_button.place(x = 10, y = 10)

        self.about_label = tk.Label(self.master, text = "About", bg = "#38b6ff" ,fg = "white", font = ("Bauhaus 93", 30))
        self.about_label.pack(pady = 20)

        self.info_label = tk.Label(self.master, text = "TensorGaze is an innovative photo recognition application that allows you to do Live Detecting or upload an image and Detect. Our advanced image recognition technology uses artificial intelligence and machine learning algorithms to accurately identify objects, and even person in photos or Live Detecting. With TensorGaze, you can explore and discover the world around you in a new way. Whether you're traveling, sightseeing, or just curious about the world, TensorGaze is the perfect tool to help you learn more about the things you see. Try TensorGaze today and start exploring the world like never before! Follow the Developer on Instagram for more apps and inspiration: @gazif_satarkar", 
                                   font = ("Rockwell", 16), wraplength = 400, justify = "center", bg = "#38b6ff" ,fg = "white")
        self.info_label.pack(padx = 20, pady = 10)

        self.developer_label = tk.Label(self.master, text = "Developed by Gazif Satarkar", font = ("Bauhaus 93", 16), bg = "#38b6ff" ,fg = "white")
        self.developer_label.pack(padx = 20, pady = 10)

        self.logo_image = tk.PhotoImage(file = "G.png")
        self.logo_image = self.logo_image.subsample(5, 5)
        
        self.label = tk.Label(self.master, image = self.logo_image,bg = "#38b6ff")
        self.label.place(x = 190,y = 630)

        self.read_button = tk.Button(self.master, text = "Read Aloud",cursor = "hand2", bg = "#2f318b", fg = "white", relief = "ridge", borderwidth = 5, bd = 1, highlightthickness = 0, font = ("Berlin Sans FB Demi", 14), command = self.Read_Aloud)
        self.read_button.place(x = 350, y = 745)

    def Read_Aloud(self):
        text = self.info_label.cget("text") 
        engine = pyttsx3.init()
        voices = engine.getProperty("voices") 
        engine.setProperty("voice", voices[1].id) 
        engine.setProperty("rate", 150)
        engine.say(text)
        engine.runAndWait()

    def switch_screen(self):
        self.master.destroy()
        MainScreen()
        

LoginScreen(tk.Tk())
tk.mainloop()
