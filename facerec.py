"""
frontal face recognition project
"""
from datetime import datetime
from tkinter import Menu, Tk
from tkinter import messagebox as msg
from tkinter import filedialog
import random
import cv2
def helpmenu():
    """ help menu """
    msg.showinfo("HELP", "HELP \n 1. Choose from the menu \n 2. Import a file")
def aboutmenu():
    """ about """
    msg.showinfo("About", "About \nVersion 1.0")
class FrontalFaceRecognition():
    """
    frontal face recognition class
    """
    def __init__(self, master):
        self.master = master
        self.master.title("FRONTAL FACE RECOGNTION")
        self.master.geometry("250x120")
        self.master.resizable(False, False)

        self.faceRects = ""

        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.menu = Menu(self.master)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="IMAGE FACE RECOGNITION",
                                   accelerator='Ctrl+O', command=self.imgrec)
        self.file_menu.add_command(label="VIDEO FACE RECOGNITION",
                                   accelerator='Alt+O', command=self.vidrec)
        self.file_menu.add_command(label="CAMERA FACE RECOGNITION",
                                   accelerator='Alt+R', command=self.webcamrecognition)
        self.file_menu.add_command(label="Exit", accelerator='Alt+F4', command=self.exitmenu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.show_menu = Menu(self.menu, tearoff=0)
        self.show_menu.add_command(label="Show Number of faces", accelerator='Ctrl+F5', command=self.shownumberoffaces)
        self.menu.add_cascade(label="Show", menu=self.show_menu)
        self.about_menu = Menu(self.menu, tearoff=0)
        self.about_menu.add_command(label="About", accelerator='Ctrl+I', command=aboutmenu)
        self.menu.add_cascade(label="About", menu=self.about_menu)
        self.help_menu = Menu(self.menu, tearoff=0)
        self.help_menu.add_command(label="Help", accelerator='Ctrl+F1', command=helpmenu)
        self.menu.add_cascade(label="Help", menu=self.help_menu)

        self.master.config(menu=self.menu)
        self.master.bind('<Control-o>', lambda event: self.imgrec())
        self.master.bind('<Alt-o>', lambda event: self.vidrec())
        self.master.bind('<Alt-r>', lambda event: self.webcamrecognition())
        self.master.bind('<Alt-F4>', lambda event: self.exitmenu())
        self.master.bind('<Control-F5>', lambda event: self.shownumberoffaces())
        self.master.bind('<Control-F1>', lambda event: helpmenu())
        self.master.bind('<Control-i>', lambda event: aboutmenu())

    def shownumberoffaces(self):
        """shows the number of faces found"""
        if self.faceRects == "":
            msg.showinfo("NUMBER OF FACES", "THERE ARE NO FACES")
        else:
            msg.showinfo("NUMBER OF FACES", "THERE ARE " + str(len(self.faceRects))+ " FACES")

    
    def webcamrecognition(self):
        """ web cam face recognition"""
        f = open("Video"+str(random.randint(1, 100))+".txt", "a")
        self.videocapture(self, f=f, capturetype=0)


    def imgrec(self):
        """ image face recognition """
        imgfile = filedialog.askopenfilename(initialdir="/", title="Select an image file",
                                             filetypes=(("image files", "*.jpg"),
                                                        ("all files", "*.*")))
        if ".jpg" in imgfile:
            image = cv2.imread(imgfile)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.faceRects = self.faceCascade.detectMultiScale(gray,
                                                          scaleFactor=1.2,
                                                          minNeighbors=6,
                                                          minSize=(30, 30))
            f = open("image"+str(random.randint(1, 100))+".txt", "a")
            for (x, y, w, h) in self.faceRects:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                f.write("Image :"+str(x)+" "+str(y)+" "+str(w)+" "+" "+str(h)+"\n")
            cv2.imshow("Faces", image)
            cv2.waitKey(0)
            msg.showinfo("FACES FOUND", "FACES FOUND: "+str(len(self.faceRects)))
            f.write("Path: "+imgfile+"\n")
            f.write("Number of faces: "+str(len(self.faceRects)))
            f.close()
        else:
            msg.showerror("Abort", "Abort")

    def cameracapture(self, camera, f):
        while True:
            (check, frame) = camera.read()
            frame = cv2.resize(frame, (400, 400), 400, 0)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.faceRects = self.faceCascade.detectMultiScale(gray,
                                                          scaleFactor=1.2,
                                                          minNeighbors=6,
                                                          minSize=(30, 30))
            for (x, y, w, h) in self.faceRects:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                f.write("Video: "+str(x)+" "+str(y)+" "+str(w)+" "+" "+str(h)+"\n")
            cv2.imshow("Face ", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        camera.release()
        cv2.destroyAllWindows()

    def videocapture(self, videofile, f=None, capturetype=-1):
        """ video face recognition """
        if  capturetype == 0:
            camera = cv2.VideoCapture(0)
        else:
            camera = cv2.VideoCapture(videofile)
            self.cameracapture(camera, f)
        if capturetype == 0:
            current_time = datetime.now().strftime("%H:%M:%S")
            f.write("Camera capture:"+ current_time+"\n")
        else:
            f.write("Path: "+videofile+"\n")
        f.close()

    def vidrec(self):
        """ video face recognition """
        videofile = filedialog.askopenfilename(initialdir="/", title="Select a video file",
                                               filetypes=(("video files", "*.mp4"),
                                                          ("all files", "*.*")))
        if ".mp4" in videofile:
            f = open("Video"+str(random.randint(1, 100))+".txt", "a")
            self.videocapture(videofile=videofile, f=f)
        else:
            msg.showerror("Abort", "Abort")
    def exitmenu(self):
        """ exit menu"""
        if msg.askokcancel("Quit?", "Really quit?"):
            self.master.destroy()
def main():
    """ main function """
    root = Tk()
    FrontalFaceRecognition(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()
