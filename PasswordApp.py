#Import of required packages. 

#tk import required for gui
import tkinter as tk
#import of tkk. Required for progress bar
import tkinter.ttk as ttk
#Import of enchant package. Required for word lookup.
import enchant
#Import of re required for regular expressions. 
import re
#Import of encrypt and decrypt from simplecrypt. Required for data encryption.
from simplecrypt import encrypt, decrypt
import os

#Definition of main PasswordApp class. 
class PasswordApp(tk.Tk):

	def __init__(self):

		tk.Tk.__init__(self)

		self.var = tk.StringVar()
		
		self.progbarval = 0
		#Defining gui elements and setting required properties. 
		banimg = tk.PhotoImage(file="passbanner.gif")
		self.banner = tk.Label(self, image=banimg)
		self.banner.image = banimg
		

		self.entry = tk.Entry(self, show='*', justify='center', font="Arial 8")
		self.button = tk.Button(self, text="Check", command=self.CheckDictWord, font="Arial 6", bg = "#bdc3c7")
		self.sep1 = ttk.Separator(self, orient='horizontal')
		self.label1 = tk.Label(self, text="-", bg="#ecf0f1", font="Arial 6", height=4)
		self.label2 = tk.Label(self, text="-", bg="#ecf0f1", font="Arial 6", height=4)
		self.label3 = tk.Label(self, text="-", bg="#ecf0f1", font="Arial 6", height=4)
		self.label4 = tk.Label(self, text="-", bg="#ecf0f1", font="Arial 6", height=4)
		self.pb = ttk.Progressbar(orient='horizontal', length=300, value=0.0, maximum=4, mode='determinate')
		self.proglbl = tk.Label(self, text="", bg="#ecf0f1", font="Arial 6")
		self.lbltotal= tk.Label(self, text="", bg="#ecf0f1", font="Arial 6")

		#Positioning of gui elements. 
		self.banner.grid(row=0, columnspan=10, sticky='WE')
		self.entry.grid(row=5, pady=2, columnspan=10, sticky='WE')
		self.button.grid(row=10, columnspan=20, pady=3, padx=70, sticky='WE')
		self.sep1.grid(row=15, sticky='WE', columnspan=10,padx=9)
		self.label1.grid(row=20, sticky='WE', columnspan=10)
		self.label2.grid(row=30, sticky='WE', columnspan=10)
		self.label3.grid(row=40, sticky='WE', columnspan=10)
		self.label4.grid(row=50, sticky='WE', columnspan=10)
		self.pb.grid(row = 100,  sticky='WE', pady=4, padx=4, columnspan=10)
		self.proglbl.grid(row=110, sticky='WE', columnspan=10)
		self.lbltotal.grid(row = 120, sticky='WE', columnspan=10)

	def StepBar(self):
		self.progbarval = self.progbarval +1
		self.pb.step()
		self.proglbl.config(text=str(self.progbarval)+"/4")
		self.lbltotal.config(text="Selected password has met " + str(self.progbarval) + "\n out of 4 rules. ")
# Encyrption Method. Used to encrypt password string. 
	def Encrypt(self, cipher, pw):

		encrypw = encrypt(cipher, pw)
		return encrypw

# Decryption Method. Used decrypt encrypted password string. 
	def Decrypt(self, cipher, encrypw):
		quoted = re.compile("(?<=')[^']+(?=')")

		plaintext = decrypt(cipher, encrypw)

		plaintext = str(plaintext)

		for value in quoted.findall(plaintext):
			plpw = value
		print(plpw)

		return plpw
 
# Check Symbols method. Checks password for symbols. 
	def CheckSymbols(self, cipher, epw):

		pw = self.Decrypt(cipher, epw )

		s = 0
		listsymb = ['!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '-', '-', '{', '}', '[', ']', ',', '+']
		length = len(listsymb)



		for char in listsymb:
			if (char in pw):
				s = s + 1
				print(s)

		if(s > 0):
			self.label4.config(text = "Password contains symbols! \n")
			self.StepBar()
		else:
			self.label4.config(text = "Password contains no Symbols! \n Please add a special character to your password some examples are \n !£@*%+")

#Check length method. Checks password is at least 8 characters in length. 
	def CheckLength(self, cipher, epw):

		ciph2 = "hello"
		pw = self.Decrypt(cipher, epw)

		y = len(pw)
		print("Y is equal to " + str(y))
		if(y < 8):
			self.label2.config(text = "Password too short! Less than 8 characters! \n Please ensure that your supplied password \n is at least 8 characters or more in length.")
		elif( y >= 8 ):
			self.label2.config(text = "Password length ok! Password more than 8 characters! \n")
			self.StepBar()

		epw = self.Encrypt(ciph2, pw)
		self.CheckForNumbers(ciph2, epw)

#Check for numbers method. Checks password for numbers.
	def CheckForNumbers(self, cipher, epw):

		ciph3="PQR6"

		pw = self.Decrypt(cipher, epw)

		num = 0
		for char in pw:
			if(char.isdigit()):
				num = num + 1

		if(num > 0):
			self.label3.config(text = "Password contains " + str(num) + " numbers! \n")
			self.StepBar()
		elif(num == 0):
			self.label3.config(text = "Password does not contain any numbers! \n")

		epw = self.Encrypt(ciph3, pw)
		self.CheckSymbols(ciph3,epw)


#Check for Dictionary Word Method. Checks password for dictionary words. 
	def CheckDictWord(self):

		cipher = "chkd"

		print(self.entry.get())
		pw = self.entry.get()

		epw = self.Encrypt(cipher, pw)

		pw=""

		print(epw)


		print(pw)
		ChkPW = self.Decrypt(cipher, epw)

		ChkPW = re.sub(r'[^\w]','',ChkPW)
		print("ChkPW = " + ChkPW)

		ChkPW = re.sub(r'\d+', '', ChkPW)

		print(ChkPW)



		l = len(ChkPW)
		x = 0
		w = 0
		d = enchant.Dict()

		while(x < l):
			b = d.check(ChkPW[x:l])
			if(b):
				print(b)
				w = w + 1
				print(w)

			x = x + 1

		if(w > 0):

			self.label1.config(text= str(w) + " dictionary words found in password! \n Avoid using dictionary words within \n your password, try replacing letters with symbols.")
		elif(w == 0):
			self.label1.config(text= "0 dictionary words found in password!")
			self.StepBar()
			
	
		self.CheckLength(cipher, epw)

#End of Class

def WinCreate(w):

	w.geometry('502x570')
	w.resizable(width=False, height=False)
	
	




w = PasswordApp()
WinCreate(w)
w.configure(background = '#ecf0f1')
icon = tk.PhotoImage(file='py.png')
w.tk.call('wm', 'iconphoto', w._w, icon)
w.title("Password App")

w.mainloop()
