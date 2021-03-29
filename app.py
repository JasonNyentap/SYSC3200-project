######################################################
#
# 
#                   PERT GUI
# 
#   (OPTION 1) Creates Activity and Milestone nodes
# 
#   (OPTION 2) Loads Problem inputs from TXT file
#   
#   @author Reginald Pradel
#
#######################################################

from tkinter import *

# Import scheduler functions
# from PERTscheduler import *

# Import node classes
from PERTmodels import Activity, Milestone, Activity_Input

# Scheduler Functions
#from PERTscheduler import load_problem#,executePERT_daycare,executePERT_excalibur


####################
########################################
####################
#
# GLOBAL VARIABLES
#
####################
#########################################
####################

# List of Activity() objects to hold state info 
activities_input = []
# List of type Milstone()
milestones = []

###############
#
# Initialize GUI 
#
###############

# tk  root frame
tkapp = Tk()

# title
tkapp.className = 'Perfect PERT'

# window dimensions
tkapp.geometry('450x500')

# bkg colour
tkapp.configure(bg='SkyBlue1')

# Variables that store USER  input in GUI
name = StringVar(tkapp, value='A')
dur = IntVar(tkapp)
lab = IntVar(tkapp)

# NUMBER OF ACTIVITIES INPUTED BY USER (update on button press)
activity_counter = Label(tkapp, text='# of Activities inputed : '+str(len(activities_input)) , bg='grey').place(x=0, rely=0.9)

####################
########################################
####################
#
# Tkinter custom WIDGETS
#
####################
#########################################
####################

#######
#
# Checkbar Widget for prereqs
#
# https://www.python-course.eu/tkinter_checkboxes.php
#
#######
class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      
      Frame.__init__(self, parent)
      
      self.vars = []
      
      for pick in picks:
         var = IntVar()
         chk = Checkbutton(self, text=pick, variable=var, bg='black')
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)



##############################
#
#      Helper Methods
#
##############################

######
# Create a txt file based on inputs
#
#   to be called in add_activity()
#
######
def write_txt_data():
    text_file = open("Problems/PERT_input.txt", "w")
    
    for act in activities_input:
        n = text_file.write(act.name+', '+ str(act.duration)+', '+str(act.labour) +'\n')
        
        # must call state of Checkframe state toString 
        #for pred in act.predecessor:
         #   n += ', '+pred.name
        #n += '\n' #end line with newline


    text_file.close()

########
#
# create activity for '+ add activity' command
#
# takes data from input field 
# then creates an Activity Obj
#
#########
def add_activity():
    # Create Activity object from GUI contents
    activity_prep = Activity_Input(name.get(), dur.get(), lab.get(), Milestone())
    #Add the newly created activity to list of dependants/prerequisites
   
    # Add created activity to LIST
    activities_input.append(activity_prep)

    # UPDATE # of activities inputed COUNTER
    #activity_counter.config(text(str(len(activities_input))))
    

    print('ADD ACTIVITY button pressed\n')
    print('NEW activity: '+activity_prep.name+' '+str(activity_prep.duration)+' '+str(activity_prep.labour)+'\n')
    

    # !!! Writes activities currently in activity_inputs[]
    #     to 'PERT_input.txt'
    write_txt_data()



########
#
# input --> string --> data.txt
# dump input data into .txt file
# call PERTscheduler.load_problem(filename) 
#
# Results in new window opening
#
#########
def execute_PERT():
    print('Evaluate PERT button pressed\n')


##########
#
#
#
###########
def getActivityNames():
    name_list = []
    for activity in activities_input:
        name_list.append(activity.__str__new(showname))
    return name_list

##########
#
#   reload checkback widget upon this call
#
###########
def update_prereq_list():
    pass

##########
#
# Load Daycare
#
###########
def load_daycare():
    print('Opening PERT results window')
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(tkapp)
  
    # sets the title of the
    # Toplevel widget
    newWindow.title("PERT EXECUTED")
  
    # sets the geometry of toplevel
    newWindow.geometry("200x200")
  
    # A Label widget to show in toplevel
    Label(newWindow, 
          text ="~ Accoring to our calculation of PERT ~").pack()

    Label(newWindow ,
        text ='Lowest possible peak requirement: '
            + 'VARIABLE lowest from PERTscheduler').pack() 
    
    Label(newWindow ,
        text ='Schedules achieving lowest requirement (Activity, Start time):'
            + 'VARIABLE lowest from PERTscheduler').pack()
###########
#
# Load Excalibur
#
###########
def load_excalibur():
    pass

##########
#
#
#
###########

def open_results_window():
    print('Opening PERT results window')
    # Toplevel object which will 
    # be treated as a new window
    newWindow = Toplevel(tkapp)
  
    # sets the title of the
    # Toplevel widget
    newWindow.title("PERT EXECUTED")
  
    # sets the geometry of toplevel
    newWindow.geometry("200x200")
  
    # A Label widget to show in toplevel
    Label(newWindow, 
          text ="~ Accoring to our calculation of PERT ~").pack()

    Label(newWindow ,
        text ='Lowest possible peak requirement: '
            + 'VARIABLE lowest from PERTscheduler').pack() 
    
    Label(newWindow ,
        text ='Schedules achieving lowest requirement (Activity, Start time):'
            + 'VARIABLE lowest from PERTscheduler').pack()
   
      
    



###################
#
#    GUI INPUTs
#
###################

# label
task_label = Label(tkapp, text='Activity:', bg='grey').place(relx=0, y=50)
# input task
nameTf = Entry(tkapp, textvariable=name).place(x=175, y=50)

# duration label
dur_label = Label(tkapp, text='Duration:', bg='grey').place(x=1, y=100)
# duration input
durTf = Entry(tkapp, textvariable=dur).place(x=175, y=100)

# labour label
lab_label = Label(tkapp, text='Labour:', bg='grey').place(x=0, y=150)
# labour input
labTf = Entry(tkapp, textvariable=lab).place(x=175, y=150)


# prereqs label
prereqs_label = Label(tkapp, text='Prerequisites:', bg='grey').place(x=1, y=200)
#Check bar of activities that may be preceded
prereq_boxes = Checkbar(tkapp, getActivityNames()).place(x=175, y=200)




################
#
#      Main
#
################

# Add activity BUTTON
add_activity_button = Button(tkapp, text=' + add activity ', width=10, height=1, bg='grey23', fg='wheat1', command=add_activity,
                             highlightbackground='green').place(relx=0.1,rely=0.7)

# Schedule PERT BUTTON
evaluate_button = Button(tkapp, height='2',command=execute_PERT, text='Evaluate PERT', bg='gold',
                         fg='white', highlightbackground='black').place(relx=0.6, rely=0.8)

# Select Preset network BUTTON
daycare_button = Button(tkapp, height='2',width='15', command=load_daycare(), text='Preset #1: Daycare', bg='pink',
                         fg='white', highlightbackground='black').place(x=300,y=10)

# Select Preset network BUTTON
excalibur_button = Button(tkapp, height='2',width='15', command=load_excalibur(), text='Preset #2: Excalibur', bg='gold',
                         fg='white', highlightbackground='black').place(x=300,y=50)


#############################











tkapp.mainloop()

# end
