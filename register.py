from tkinter import*
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import pandas as pd

class Register:
	def __init__(self,root1):
		self.root1 = root1
		self.root1.title("Registration Window")
		self.root1.geometry("1350x700+0+0")
		self.root1.configure(background="black")
		#self.root1.attributes('-fullscreen', True)
		#------------------Image
		self.bg = ImageTk.PhotoImage(file = "b2.jpg")
		bg = Label(self.root1,image=self.bg,bg="LightCyan4").place(x=200,y=0,relwidth=1,relheight=1)


		#------------------Left Image
		self.left = ImageTk.PhotoImage(file = "side1.png")
		bg = Label(self.root1,image=self.left).place(x=125,y=150,width=300,height=450)

		#--------------------------Register Frame
		frame1  = Frame(self.root1,bg="LightCyan4")
		frame1.place(x=480,y=130,width=675,height=500)

		title=Label(frame1,text="REGISTER HERE",font=("times new roman",20,"bold"),bg="LightCyan4",fg="black").place(x=50,y=30)
		#----------------------Row1
		f_name=Label(frame1,text="First Name",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=50,y=100)
		self.txt_fname=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_fname.place(x=50,y=130,width=250)

		l_name=Label(frame1,text="Last Name",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=370,y=100)
		self.txt_lname=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_lname.place(x=370,y=130,width=250)

		#-----------------------Row2
		contact=Label(frame1,text="Contact Number",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=50,y=170)
		self.txt_contact=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_contact.place(x=50,y=200,width=250)

		email=Label(frame1,text="Email",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=370,y=170)
		self.txt_email=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_email.place(x=370,y=200,width=250)


		#-----------------------Row3
		question=Label(frame1,text="Category",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=50,y=240)
		
		self.cmb_quest=ttk.Combobox(frame1,font=("times new roman",13),state='readonly',justify=CENTER)
		self.cmb_quest['values']=("Select","Brain Tumour","Lung Cancer","Heart Disease")
		self.cmb_quest.place(x=50,y=270,width=250)		
		self.cmb_quest.current(0)

		answer=Label(frame1,text="Patient Age",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=370,y=240)
		self.txt_answer=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_answer.place(x=370,y=270,width=250)


		#-----------------------Row2
		password=Label(frame1,text="Password",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=50,y=310)
		self.txt_password=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_password.place(x=50,y=340,width=250)

		cpassword=Label(frame1,text="Confirm Password",font=("times new roman",15,"bold"),bg="LightCyan4",fg="white").place(x=370,y=310)
		self.txt_cpassword=Entry(frame1,font=("times new roman",15),bg="LightBlue3")
		self.txt_cpassword.place(x=370,y=340,width=250)

		#----------------Terms----------------
		self.var_chk = IntVar()
		chk = Checkbutton(frame1,text="I Agree the Terms & Conditions",variable = self.var_chk,onvalue=1,offvalue=0,bg="LightCyan4",font=("times new roman",12)).place(x=50,y=380)

		btn = Button(frame1,text="Register",font=("times new roman",20,"bold"),bd=0,cursor="hand2",command=self.register_data,bg="black",fg="yellow").place(x=70,y=420,width=180)

		btn_login = Button(self.root1,text="Sign In",font=("times new roman",20,"bold"),bd=0,cursor="hand2",command=self.exit_window,bg="black",fg="yellow").place(x=900,y=550,width=180)

	def register_data(self):
		print(type(self.txt_fname.get()),type(self.txt_lname.get()),type(self.txt_contact.get()),type(self.txt_email.get()),type(self.cmb_quest.get()),type(self.txt_answer.get()),type(self.txt_password.get()),type(self.txt_cpassword.get()))		
		if (self.txt_fname.get()=="" or self.txt_lname.get()=="" or self.txt_contact.get()=="" or self.txt_email.get()=="" or self.cmb_quest.get()=="" or self.txt_answer.get()=="" or self.txt_password.get()=="" or self.txt_cpassword.get()==""):
			messagebox.showerror("Error","All fields are required",parent=self.root1)
		elif (self.txt_password.get()!=self.txt_cpassword.get()):
			messagebox.showerror("Error","Password and Confirm Password should be same", parent=self.root1)
		elif (self.var_chk.get()==0):
			messagebox.showerror("Error","PLease agree to our terms and conditions", parent=self.root1)
		else:
			df = pd.read_csv("file1.csv")
			new_row = {'fname':self.txt_fname.get(), 'lname':self.txt_lname.get(), 'Cnumber':self.txt_contact.get(), 'email':self.txt_email.get(), 'cater':self.cmb_quest.get(), 'age':self.txt_answer.get(), 'password':self.txt_password.get()}
			df = df.append(	new_row,ignore_index = True)
			df.to_csv('file1.csv')

			messagebox.showinfo("Success","Registration Successful.\nPlease use email as your Username.", parent=self.root1)
			self.clear()
		
	def clear(self):
		self.txt_fname.delete(0,END)
		self.txt_lname.delete(0,END)
		self.txt_contact.delete(0,END)
		self.txt_email.delete(0,END)
		self.cmb_quest.delete(0,END)
		self.txt_answer.delete(0,END)
		self.txt_password.delete(0,END)
		self.txt_cpassword.delete(0,END)




	def exit_window(self):
		self.root1.destroy()
		import login

root1 = Tk()
obj = Register(root1)
root1.mainloop()
