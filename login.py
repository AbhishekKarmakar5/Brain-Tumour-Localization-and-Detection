from tkinter import*
from tkinter import messagebox
from PIL import Image,ImageTk
import pandas as pd

class Login_System:
	def __init__(self,root):
		self.root = root
		self.root.title("Login System")
		self.root.geometry("1350x700+0+0")
		#self.root.attributes('-fullscreen', True)

		self.bg_icon = ImageTk.PhotoImage(file = "bg1.jpg")		
		self.user_icon = ImageTk.PhotoImage(file = "man_user.png")
		self.pass_icon = ImageTk.PhotoImage(file = "password1.png")
		self.logo_icon = ImageTk.PhotoImage(file = "logo2.jpg")
		#-------------------------------------Variables-------------------
		self.uname=StringVar()
		self.pass_ = StringVar()

		bg_lbl = Label(self.root,image=self.bg_icon).pack()
		
		title = Label(self.root,text = "Patient Login Credentials",font=("times new roman", 25, "bold"),bg = "gold2",fg = "black",bd=10,relief=GROOVE)
		title.place(x=0,y=0,relwidth=1)
		
		Login_Frame = Frame(self.root,bg="black")
		Login_Frame.place(x=200,y=150)

		logolbl = Label(Login_Frame,image=self.logo_icon,bd=0).grid(row=0,columnspan=2,pady=20)

		lbluser = Label(Login_Frame,text="Username",image=self.user_icon,compound=LEFT,font=("times new roman", 20, "bold"),fg="white", bg = "black").grid(row=1,column=0,padx=20,pady=10)
		txtuser = Entry(Login_Frame,bd=5,textvariable=self.uname,relief=GROOVE,font=("",15)).grid(row=1,column=1,padx=20)

		lblpass = Label(Login_Frame,text="Password",image=self.pass_icon,compound=LEFT,font=("times new roman", 20, "bold"),fg="white", bg = "black").grid(row=2,column=0,padx=20,pady=10)
		txtpass = Entry(Login_Frame,bd=5,show="*",textvariable=self.pass_,relief=GROOVE,font=("",15)).grid(row=2,column=1,padx=20)

		btn_log = Button(Login_Frame,text="Login",width=10,font=("times new roman",20,"bold"), command=self.login,bg="gray11",fg="white").grid(row=3,column=1,pady=10)
		btn_reg = Button(Login_Frame,text="Register",width=10,font=("times new roman",20,"bold"), command=self.Registering,bg="gray11",fg="white").grid(row=3,column=0,pady=10)
		

	def Registering(self):
		self.root.destroy()
		import register


	def login(self):
		df = pd.read_csv("file1.csv")
		for ind in df.index:
			print(ind)
			print(type(df['email'][ind]),type(df['password'][ind]))			
			checknamestr = str(self.uname.get())
			checkpassstr = str(self.pass_.get())

			if self.uname.get()=="" or self.pass_.get()=="":
				messagebox.showerror("Error","All fields are required!")
				break
			elif (checknamestr==df['email'][ind]) and (checkpassstr==df['password'][ind]):
				messagebox.showinfo("Successful","Welcome User")
				self.root.destroy()
				import Impro
				
			elif (checknamestr==df['email'][ind]) and (checkpassstr!=df['password'][ind]):
				messagebox.showerror("Error","Wrong Password!")
				break


root = Tk()
root.configure(background="black")
obj = Login_System(root)
root.mainloop()