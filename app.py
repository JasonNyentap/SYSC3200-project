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


################
#
#      Main
#
################
# List of activities
activities = []

# List of milstones
milestones = []

###############
# SET UP UI
###############

# tk  root frame
tkapp = Tk()

# title
tkapp.title = 'Perfect PERT'

# window dimensions
tkapp.geometry('450x300')

# bkg colour
tkapp.configure(bg='SkyBlue1')

##############################

###################
#
#     INPUTs
#
###################

# label
task_label = Label(tkapp, text='Activity', bg='grey')
task_label.place(relx=0, y=10)
# input task
name = StringVar(tkapp, value='A')
nameTf = Entry(tkapp, textvariable=name).place(x=175, y=10)

# duration label
dur_label = Label(tkapp, text='Duration', bg='grey')
dur_label.place(x=1, y=70)
# duration input
dur = IntVar(tkapp, value=1)
durTf = Entry(tkapp, textvariable=str(dur.get)).place(x=175, y=70)

# labour label
lab_label = Label(tkapp, text='Enter labour:', bg='grey')
lab_label.place(x=0, y=150)
# labour input
lab = StringVar(tkapp, value='1')
labTf = Entry(tkapp, textvariable=lab).place(x=175, y=150)


# prereqs label
prereqs_label = Label(tkapp, text='Prerequisites', bg='grey').place(x=1, y=200)
# input checkboxes of activities currently in project
prereqs_inputs = Label(tkapp, text='A [] B[] C[]', bg='grey').place(x=175, y=200)



# create an activity obj,
#newAct = Activity(name, dur, lab, [])
# add  obj to list


# Add activity BUTTON
add_activity_button = Button(tkapp, text=' + add activity ', width=3, height=1, bg='grey23', fg='wheat1',
                             highlightbackground='green').place(x=250,y=330)



######################
#
# Schedule PERT & CRM
# BUTTON
#
######################
evaluate_button = Button(tkapp, height='2', text='PERT & CRM', bg='gold',
                         fg='white', highlightbackground='black').place(x=250, y=300)


# Add activity to list


x0 = 200
y0 = 200


def addActivity(taskname, duration, labour, predecessors):
    pass


test_activity = createActivity('A', 11, 1, [])


tkapp.mainloop()

# end
