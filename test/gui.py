#import TKinter
import Tkinter as tk

#class declaration - inherits tk.Frame
class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

#instantiation
app = Application()
#set title
app.master.title('Sample application')
#execute app
app.mainloop()
