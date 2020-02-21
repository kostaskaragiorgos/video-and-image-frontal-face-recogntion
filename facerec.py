"""
frontal face recognition project
"""
from tkinter import Menu, Tk
from tkinter import messagebox as msg
from tkinter import filedialog
import cv2
class FRONTAL_FACE_RECOGNTION():
    """
    frontal face recognition class
    """

    def __init__(self, master):
        self.master = master
        self.master.title("FRONTAL FACE RECOGNTION")
        self.master.geometry("250x120")
        self.master.resizable(False, False)

        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="IMAGE FACE RECOGNITION", command = self.imgrec)
        self.file_menu.add_command(label="VIDEO FACE RECOGNITION", command = self.vidrec)
        self.file_menu.add_command(label="Exit", accelerator= 'Alt+F4', command = self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator= 'Ctrl+I', command=self.aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator = 'Ctrl+F1', command=self.helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.master.config(menu=self.menu)
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F1>', lambda event: self.helpmenu())
        self.master.bind('<Control-i>', lambda event:self.aboutmenu())
        
    def imgrec(self):
        """ image face recognition """
        imgfile = filedialog.askopenfilename(initialdir ="/",title ="Select an image file",
                                             filetypes =(("image files","*.jpg"),("all files","*.*")))
        if ".jpg" in imgfile:
            image = cv2.imread(imgfile)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faceRects = self.faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 6, minSize=(30, 30))
            for (x, y, w, h) in faceRects:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow("Faces", image)
            cv2.waitKey(0)
            msg.showinfo("FACES FOUND", "FACES FOUND:"+str(len(faceRects)))
        else:
            msg.showerror("Abort", "Abort")
    def vidrec(self):
        """ video face recognition """
        videofile = filedialog.askopenfilename(initialdir = "/", title = "Select a video file",
                                               filetypes = (("video files", "*.mp4"), ("all files", "*.*")))
        if ".mp4" in videofile:
            camera =cv2.VideoCapture(videofile)
        
            while True:
                (check, frame) = camera.read()
                frame = cv2.resize(frame, (400, 400), 400,0)
                gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faceRects = self.faceCascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 6, minSize=(30, 30))
                for (x, y, w, h) in faceRects:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
                cv2.imshow("Face", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            camera.release()
            cv2.destroyAllWindows()
        else:
            msg.showerror("Abort", "Abort")
            
    def exitmenu(self):
        """ exit menu"""
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
    
    def helpmenu(self):
        """ help menu """
        msg.showinfo("HELP", "HELP \n 1. Choose from the menu \n 2. Import a file")
    
    def aboutmenu(self):
        """ about """
        msg.showinfo("About", "About \nVersion 1.0")
def main():
    root=Tk()
    FRONTAL_FACE_RECOGNTION(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()