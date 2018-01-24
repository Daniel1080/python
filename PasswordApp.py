import tkinter as tk
import tkinter.ttk as ttk
import enchant
import re
from simplecrypt import encrypt, decrypt





class PasswordApp(tk.Tk):

	def __init__(self):

		tk.Tk.__init__(self)

		self.var = tk.StringVar()
		
		

		banimg = tk.PhotoImage(file="passbanner.gif")
		self.banner = tk.Label(self, image=banimg)
		self.banner.image = banimg
		

		self.entry = tk.Entry(self, width=200, show='*', justify='center', font="Arial 8")
		self.button = tk.Button(self, text="Check", command=self.CheckDictWord)
		self.label1 = tk.Label(self, text="none", bg="#ecf0f1", font="Arial 6")
		self.label2 = tk.Label(self, text="none", bg="#ecf0f1", font="Arial 6")
		self.label3 = tk.Label(self, text="none", bg="#ecf0f1", font="Arial 6")
		self.label4 = tk.Label(self, text="none", bg="#ecf0f1", font="Arial 6")
		self.banner.pack(padx=0, pady=2)
		self.pb = ttk.Progressbar(orient='horizontal', length=200, value=0.0, maximum=10, mode='determinate')
		self.proglbl = tk.Label(self, text="", bg="#ecf0f1", font="Arial 6")
		self.lbltotal= tk.Label(self, text="", bg="#ecf0f1", font="Arial 6")

		self.entry.pack()
		self.button.pack()
		self.label1.pack()
		self.label2.pack()
		self.label3.pack()
		self.label4.pack()
		self.pb.pack()
		self.proglbl.pack()
		self.lbltotal.pack()

	def Encrypt(self, cipher, pw):

		encrypw = encrypt(cipher, pw)
		return encrypw

	def Decrypt(self, cipher, encrypw):
		quoted = re.compile("(?<=')[^']+(?=')")

		plaintext = decrypt(cipher, encrypw)

		plaintext = str(plaintext)

		for value in quoted.findall(plaintext):
			plpw = value
		print(plpw)

		return plpw

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
			self.label4.config(text = "\n Password contains symbols! \n")
		else:
			self.label4.config(text = "\n Password contains no Symbols! \n Please add a special character to your password some examples are \n !£@*%+")

	def CheckLength(self, cipher, epw):
		ciph2 = "hello"
		pw = self.Decrypt(cipher, epw)

		y = len(pw)
		print("Y is equal to " + str(y))
		if(y < 8):
			self.label2.config(text = "\n Password too short! Less than 8 characters! \n Please ensure that your supplied password \n is at least 8 characters or more in length.")
		elif( y >= 8 ):
			self.label2.config(text = "\n Password length ok! Password more than 8 characters! \n")

		epw = self.Encrypt(ciph2, pw)
		self.CheckForNumbers(ciph2, epw)

	def CheckForNumbers(self, cipher, epw):
		ciph3="PQR6"

		pw = self.Decrypt(cipher, epw)



		num = 0
		for char in pw:
			if(char.isdigit()):
				num = num + 1

		if(num > 0):
			self.label3.config(text = "\n Password contains " + str(num) + " numbers! \n")
			
			self.pb.step()
		elif(num == 0):
			self.label3.config(text = "\n Password does not contain any numbers! \n")

		epw = self.Encrypt(ciph3, pw)
		self.CheckSymbols(ciph3,epw)



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
			self.pb.step()
			self.proglbl.config(text="1/10")
	
		self.CheckLength(cipher, epw)

#End of Class

def WinCreate(w):
	w.geometry('502x520')



w = PasswordApp()
WinCreate(w)
w.configure(background = '#ecf0f1')
w.title("Password App")
w.mainloop()
