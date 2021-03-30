import tkinter
import os    
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import PERT

class ResultWindow(object):
    def __init__(self, msg, root):
        self.top = Toplevel(root)
        self.top.title(root.title() + ' - Solution')

        frame = Frame(self.top)
        frame.pack(fill='both', expand=True)
        
        canvas = Canvas(frame, width=root.winfo_width(), height=root.winfo_height())
        canvas.pack(fill='both', expand=True)
        
        label = Label(canvas, text=msg, justify='left')
        canvas.create_window(0, 0, window=label, anchor=NW)
        
        scrollbarX = Scrollbar(canvas, orient=HORIZONTAL, command=canvas.xview)
        scrollbarX.place(relx=0, rely=1, relwidth=1, anchor=SW)
        scrollbarY = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
        scrollbarY.place(relx=1, rely=0, relheight=1, anchor=NE)
        canvas.config(xscrollcommand=scrollbarX.set, yscrollcommand=scrollbarY.set, scrollregion=(0, 0, label.winfo_reqwidth(), label.winfo_reqheight()))
  
class PertWindow:
    width = 300
    height = 300
    root = Tk()
    textArea = Text(root)
    menuBar = Menu(root)
    fileMenu = Menu(menuBar, tearoff=0)
    solveMenu = Menu(menuBar, tearoff=0)
    scrollBar = Scrollbar(textArea)     
    file = None
  
    # Initialises the program and the main window
    def __init__(self,**kwargs):
        # Set window size
        try:
            self.width = kwargs['width']
        except KeyError:
            pass
  
        try:
            self.height = kwargs['height']
        except KeyError:
            pass
  
        # Set the window text
        self.root.title("PERT Solver - Untitled")
  
        # Center the window
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        left = (screenWidth / 2) - (self.width / 2) 
        top = (screenHeight / 2) - (self.height /2) 
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, left, top)) 
  
        # Make the textarea autosizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
  
        # Add controls
        self.textArea.grid(sticky = N + E + S + W)
          
        # Add file menu options
        self.fileMenu.add_command(label="New", command=self.__newFile)    
        self.fileMenu.add_command(label="Open", command=self.__openFile)
        self.fileMenu.add_command(label="Save", command=self.__saveFile)
        self.fileMenu.add_command(label="Save As", command=self.__saveFileAs)
        self.fileMenu.add_separator()                                         
        self.fileMenu.add_command(label="Exit", command=self.__exitApp)
                                        
        # Add solve menu options
        self.solveMenu.add_command(label="Solve", command=self.__solveProblem)  
        
        # Add menus to menu bar
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.menuBar.add_cascade(label="Solve", menu=self.solveMenu)  

        # Add menu bar and scroll bar to window
        self.root.config(menu=self.menuBar)
        self.scrollBar.pack(side=RIGHT,fill=Y)                    
          
        # Scrollbar will adjust automatically according to the content        
        self.scrollBar.config(command=self.textArea.yview)     
        self.textArea.config(yscrollcommand=self.scrollBar.set)
    
    # Clears the text editor
    def __newFile(self):
        self.root.title("PERT Solver - Untitled")
        self.file = None
        self.textArea.delete(1.0,END)
  
    # Opens a file and copies its contents to the text editor
    def __openFile(self):
        self.file = askopenfilename(defaultextension=".txt", filetypes=[("Text Documents","*.txt")])
  
        if self.file == "":
            self.file = None
        else:
            # Open the file and show it in the window title
            self.root.title("PERT Solver - " + os.path.basename(self.file))
            self.textArea.delete(1.0, END)
            file = open(self.file,"r")
            self.textArea.insert(1.0, file.read())
            file.close()
          
    # Saves the contents of the text editor to a file
    def __saveFile(self):
        # If file does not exist already, save it as a new file
        if self.file == None:
            self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("Text Documents","*.txt")])
  
            if self.file == "":
                self.file = None
            else:
                file = open(self.file,"w")
                file.write(self.textArea.get(1.0,END))
                file.close()
                  
                # Change the window title
                self.root.title("PERT Solver - " + os.path.basename(self.file))
                  
        # If the file aready exists, then just update it
        else:
            file = open(self.file,"w")
            file.write(self.textArea.get(1.0,END))
            file.close()
            
    # Saves the contents of the text editor to a new file
    def __saveFileAs(self):
        if self.file == None:
            self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("Text Documents","*.txt")])
        else:
            self.file = asksaveasfilename(initialfile=os.path.basename(self.file), defaultextension=".txt", filetypes=[("Text Documents","*.txt")])
  
        if self.file == "":
            self.file = None
        else:
            file = open(self.file,"w")
            file.write(self.textArea.get(1.0,END))
            file.close()
                  
            # Change the window title
            self.root.title("PERT Solver - " + os.path.basename(self.file))
    
    # Closes the app
    def __exitApp(self):
        self.root.destroy()
    
    # Solves the problem in the text editor
    def __solveProblem(self):
        pertData = PERT.parse_problem(self.textArea.get(1.0,END))
        
        # Check if something went wrong and an error was returned
        if(isinstance(pertData, str)):
            tkinter.messagebox.showerror(title="Error", message=pertData)
        else:
            msg = '[ Problem milestones and activities ]\n'
            for milestone in pertData:
                msg += str(milestone) + '\n'

            msg += '[ Critical path activities ]' + '\n'    
            for activity in PERT.critical_path(pertData):
                msg += str(activity) + '\n'
            
            msg += '\n[ Labour requirements ]\n'        
            lowest, schedules = PERT.resource_level(pertData)
            msg += 'Lowest possible peak requirement: ' + str(lowest) + '\n'
            msg += 'Schedules achieving lowest requirement (Activity, Start time):\n'
            for schedule in schedules:
                msg += str(schedule) + '\n'
            
            ResultWindow(msg, self.root)
            
            ans = askquestion(title='Problem Solved', message='Would you like to generate a diagram for the problem solution?')
            
            if ans == 'yes':
                imageName = 'Untitled'
                if(self.file != None):
                    imageName = os.path.basename(self.file).split('.')[0]
                    
                image = asksaveasfilename(initialfile=imageName, defaultextension=".png", filetypes=[("PNG","*.png")])
                if(image != None):
                    PERT.draw_graph(pertData, image)
                
    # Runs the program
    def run(self):
        self.root.mainloop()
  
# Run main application
pert = PertWindow(width=600,height=400)
pert.run()