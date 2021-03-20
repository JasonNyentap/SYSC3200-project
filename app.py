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
prereqs_label = Label(tkapp, text='Prerequisites', bg='grey').place(relx=0.5, y=200)
# input checkboxes of activities currently in project


# create an activity obj,
#newAct = Activity(name, dur, lab, [])
# add  obj to list


# Add activity BUTTON
#add_activity_button = Button(tk, text=' + ', width=1, height=1, bg='grey23', fg='wheat1',
                             #highlightbackground='green', command=createActivity).place(relx=0.5, y=300)



######################
#
# Schedule PERT & CRM
# BUTTON
#
######################
evaluate_button = Button(tkapp, height='2', text='PERT & CRM', bg='black',
                         fg='white', highlightbackground='gold').place(x=40, y=300)


# Add activity to list


x0 = 200
y0 = 200


def createActivity(taskname, duration, labour, predecessors):

    # store list of prerequisites
    prereqs = predecessors

    label_str = taskname + ', dur: ' + str(duration)+' labour:', str(labour)

    task_label = Label(tkapp, text=label_str, bg='grey24',
                       highlightbackground='coral').place(x=x0, y=y0)

    #return newActivity = Activity(taskname, duration, labour, prereqs)


test_activity = createActivity('A', 11, 1, [])


tkapp.mainloop()

# end
