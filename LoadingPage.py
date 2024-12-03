from tkinter import *
import os , sys
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import sys
import HomePage

application_path = os.path.dirname(sys.executable)
print (os.path.dirname(sys.executable) + "\\ Scripts")

root=Tk()
root.resizable(0, 0)

height=430
width=530

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (width // 2)
y = (screen_height //2) - (height // 2)

root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.wm_attributes('-topmost', True)

root.overrideredirect(1)
root.config(background = 'lightpink')

exit_btn = Button(root, text='X', command=lambda: exit_window(), font=("yu gothic ui", 13, 'bold'), fg='red', bg='lightpink', bd=0, activebackground='lightpink')
exit_btn.place(x=500, y=0)

welcome_label = Label(root, text='WELCOME TO OUR RECIPE MANAGEMENT APP', font=("yu gothic ui", 17, 'bold'), bg='lightpink')
welcome_label.place(x=25, y=30)

image_path = 'Images/ChefSticker.jpg'
image = Image.open(image_path)

image_width, image_height = image.size

bg_label_x = (width-image_width) //2
bg_label_y = 85

photo = ImageTk.PhotoImage(image)
bg_label = Label(root, image=photo, bg='lightpink')
bg_label.place(x=bg_label_x, y=bg_label_y)

progress_label = Label(root, text='Please Wait...',font=("yu gothic ui", 10, 'bold'), bg='lightpink')
progress_label.place(x=200, y= 350)

progress = Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
progress.place(x=15, y=385)



def exit_window():
    root.destroy()
    sys.exit()
    

def top():
    win = Toplevel()
    HomePage.RecipeManagerApp(window=win, master=root)  # Provide both 'window' and 'master'
    root.withdraw()
    win.deiconify()
i=0

def load():
    global i
    if i <=10:
        txt = 'Please Wait...' + (str(10*i)+'%')
        progress_label.config(text=txt)
        progress_label.after(800, load)
        progress['value'] = 10*i
        i +=1
        
    else:
        top()
        
load()
    
    
    
root.mainloop()