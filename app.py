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
from PERTmodels import Activity, Milestone


###############
# SET UP UI
###############

# tk  root frame
tkapp = Tk()

# title
tkapp.className = 'Perfect PERT'

# window dimensions
tkapp.geometry('450x500')

# bkg colour
tkapp.configure(bg='SkyBlue1')



# List of activities
activities_input = []

# List of milstones
milestones = []

# Variables that store USER  input in GUI
name = StringVar(tkapp, value='A')
dur = IntVar(tkapp)
lab = IntVar(tkapp)




#######
#
# Checkbar for prereqs
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


#return value of current activity name GUI input


########
#
# create activity for '+ add activity' command
#
# takes data from input field 
# then creates an Activity Obj
#
#########
def add_activity():
    #set up activity creation
    activity_start = Milestone()
    activity_end = Milestone()
    # Create Activity object
    activity_prep = Activity(name.get(), dur.get(), lab.get(), activity_start, activity_end)
    #Add the newly created activity to list of dependants/prerequisites
    activity_start.dependants.append(activity_prep)
    activity_end.prerequisites.append(activity_prep)
    # Add created activity to list 
    activities_input.append(activity_prep)

    print('button pressed\n')
    print('NEW activity: '+name.get()+' '+str(dur.get())+' '+str(lab.get())+'\n')

##########
#
#
#
###########
def update_prereqs():
    prereqs_inputs.insert(name.get())
 
 # function to open a new window 
# on a button click
def openPERT_windown():
   pass
##########
#
#
#
###########
def openNewWindow():
      
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
durTf = Entry(tkapp, textvariable=str(dur.get)).place(x=175, y=100)

# labour label
lab_label = Label(tkapp, text='Labour:', bg='grey').place(x=0, y=150)
# labour input
labTf = Entry(tkapp, textvariable=lab).place(x=175, y=150)


# prereqs label
prereqs_label = Label(tkapp, text='Prerequisites:', bg='grey').place(x=1, y=200)
# listbox of activities currently in activities_input

########


#prereqs_inputs = Listbox(tkapp, listvariable=activities_input).
prereq_box = Checkbar(tkapp, ['A', 'B']).place(x=175, y=200)



########
# labour label
activity_counter = Label(tkapp, text='# of Activities inputed : '+str(len(activities_input)) , bg='grey').place(x=0, rely=0.9)




#list box
#var2 = StringVar()
#var2.set((1,2,3,4))
#lb =
#############
#
# input task VIA entry textbox:
#prereqs_var = StringVar(tkapp, value='A')
#prereqTf = Entry(tkapp, textvariable=prereqs_var).place(x=175, y=200)
#
############

 


#list_items = [11,22,33,44]
# for each items in a activities_input
#for item in activities_input:
#    lb.insert('end', item)

#Listbox insert
#lb.insert(1, 'first')
#lb.insert(2, 'second')
#lb.pack()




################
#
#      Main
#
################

# Add activity BUTTON
add_activity_button = Button(tkapp, text=' + add activity ', width=10, height=1, bg='grey23', fg='wheat1', command=add_activity,
                             highlightbackground='green').place(relx=0.1,rely=0.7)

# Schedule PERT BUTTON
evaluate_button = Button(tkapp, height='2', text='Evaluate PERT', bg='gold',
                         fg='white', highlightbackground='black').place(relx=0.6, rely=0.8)

# Select Preset network BUTTON
evaluate_button = Button(tkapp, height='2',width='15', command=openNewWindow(), text='Preset #1: Daycare', bg='gold',
                         fg='white', highlightbackground='black').place(x=300,y=10)


#############################



tkapp.mainloop()

# end
