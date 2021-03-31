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

import tkinter as tk
from tkinter import ttk
from tkinter import *

from PERT import *

# Import scheduler functions
# from PERTscheduler import *

# Import node classes
from PERTmodels import Activity, Milestone, Activity_Input #, Application

from PERTwidgets import Checkbar #, Warningwindow

# For event listener 
#from PERTlistener import EventListener

# Scheduler Functions
#from PERTscheduler import load_problem#,executePERT_daycare,executePERT_excalibur


##############################
#
#      Function Definitions
#
##############################

###
#
# Preset warning pop up window
#
###
def preset_warning(event):
    pass

def get_input_string():
    data=''
    for act in activities_input:
        data = str(act.name+', '+ str(act.duration)+', '+str(act.labour))+str(act.preds)
                
        # must call state of Checkframe state toString 
        for item in act.preds:
            data += ', '+str(item)

        data += '\n' 
        #end  Activity with newline

        print('get_input_string will return:')
        print(data)

        #store input string into variable
    
    return data



######
# Create a txt file based on inputs
#
#   to be called in add_activity()
#
######
def write_txt_data(input_string):
    print('Opening PERT_input.txt')
    text_file = open("Problems/PERT_input.txt", "w")
    
    print('Application is now writing to TXT')
    
    #stores result of write to variable
    result = text_file.write(input_string)

    #not defined
    prereq_checkbar = Checkbar(root, getActivityNames()).place(x=175, y=200)
    
    
    text_file.close()

    #Update available prereqs
    def update_prereq_list():
        prereq_checkbar = Checkbar(root, getActivityNames()).place(x=175, y=200)
        print('Checkbar update:')
        print('SIZE OF BAR '+len(prereq_checkbar.barbuttons))

    
        



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

    print('Opening PERT results window')
    # Toplevel object which will 
    # be treated as a new window
    results_window = Toplevel()

    # sets the title of the
    # Toplevel widget
    results_window.title("PERT EXECUTED")
    results_window.configure(bg='lightgreen')

    input_file = open('Problems/PERT_input.txt', 'r')
    milestones = parse_problem(input_file)
    #answer stored
    result = critical_path(milestones) 

    # sets the geometry of toplevel
    results_window.geometry("300x300")

    # A Label widget to show in toplevel
    Label(results_window, 
        text ="~ Accoring to our calculation of PERT ~").place(relx=0,y=10)

    Label(results_window ,
        text ='Lowest possible peak requirement: ').place(relx=0,y=100)
    # Lowest possible peak requirement
    Label(results_window ,
        text =result[0]).place(relx=0,y=150)

    # List of activities in order
    Label(results_window ,
        text ='Schedules achieving lowest requirement (Activity, Start time):').place(relx=0,y=200)
    Label(results_window ,
        text =result[1]).place(relx=0,y=250)



    top = Toplevel() 
    top.geometry('300x300')
    top.configure(bg='lightgreen')

    # Header
    Label(top, 
        text ="~ Accoring to our calculation of PERT ~").place(relx=0,y=10)
    
    # Lowest possible peak requirement
    Label(top ,
        text ='Lowest possible peak requirement: ').place(relx=0,y=100)
    

    Label(top ,
        text ='?').place(relx=0,y=150)

    # List of activities in order
    Label(top ,
        text ='Schedules achieving lowest requirement \n(Activity, Start time):').place(relx=0,y=200)
    Label(top ,
        text ='?' ).place(relx=0,y=250)



############
#
# Reset activity list and txt file
#
############
def reset_PERT():
    activities_input = []
    write_txt_data('')

    

##########
#
#
#
###########
def getActivityNames():
    name_list = []
    for activity in activities_input:
        name_list.append(activity.name)
    return name_list


##########
#
#   Returns state of checkbar
#
###########



##########
#
# Load Daycare
#
###########
def load_daycare():
    print('Pressed DAYCARE preset')

    print('Loading inputs into activities_input[]')
    #WARNING: Activities inputed will be replaced by preset POPUP WINDOW
    activities_input = []
    activities_input.append(Activity_Input('A',7,2,[]))
    activities_input.append(Activity_Input('B',3,1,['A']))
    activities_input.append(Activity_Input('C',1,1,['B']))
    activities_input.append(Activity_Input('D',8,1,['A']))
    activities_input.append(Activity_Input('E',2,1,['D','C']))
    activities_input.append(Activity_Input('F',1,2,['D','C']))
    activities_input.append(Activity_Input('G',1,1,['D','C']))
    activities_input.append(Activity_Input('H',3,1,['F']))
    activities_input.append(Activity_Input('J',2,2,['H']))
    activities_input.append(Activity_Input('K',1,1,['E','G','J']))

    #store input string into variable
    data=''
    for act in activities_input:
        data += act.name+', '+str(act.duration)+', '+str(act.labour)
        
        #add predecessors to activity line
        for pred in act.preds:
            data += ', '+pred
        data+='\n'
    
    print('This will be added to TXT file')
    print(data)

    # Write to TXT file
    write_txt_data(data)
    print('Inputs have been loaded to PERT_input.txt')
    parse_problem(data)

    



###########
#
# Load Excalibur
#
###########
def load_excalibur():

    #WARNING: Activities inputed will be replaced by preset POPUP WINDOW

    activities_input = []
    activities_input.append(Activity_Input('A',4,2,[]))
    activities_input.append(Activity_Input('B',7,1,['A']))
    activities_input.append(Activity_Input('C',4,1,['B']))
    activities_input.append(Activity_Input('D',3,1,['B']))
    activities_input.append(Activity_Input('E',6,1,['C']))
    activities_input.append(Activity_Input('F',2,2,['D']))
    activities_input.append(Activity_Input('G',1,3,['D','E']))
    activities_input.append(Activity_Input('H',4,2,['F']))
    activities_input.append(Activity_Input('I',4,2,['G','H']))
    activities_input.append(Activity_Input('J',2,2,['G']))
    activities_input.append(Activity_Input('K',4,1,['H']))
    activities_input.append(Activity_Input('L',4,1,['J','I','K']))

    #store input string into variable
    data=''
    for item in activities_input:
        data += item.name+', '+str(item.duration)+', '+str(item.labour)
        
        #add predecessors to activity line
        for pred in item.preds:
            data += ', '+pred
        data+='\n'
    
    print('This will be added to TXT file')
    print(data)

    # Write to TXT file
    write_txt_data(data)
    print('Inputs have been loaded to PERT_input.txt')



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
    activity_prep = Activity_Input(name.get(), dur.get(), lab.get(),[])


    #Add the newly created activity to list of dependants/prerequisites
    for item in activities_input:
        
        #Checks if name is already in activities_input
        if(item.name==name.get()):
            
            #Warning label
            #
            # stop adding activity
            pass

        # Add created activity to LIST
        else:
            activities_input.append(activity_prep)

            # UPDATE # of activities inputed COUNTER
            activity_counter.config(text(str(len(activities_input))))

            print('ADD ACTIVITY button pressed\n')
            #print ('PREREQS: '+reveal_current_prereqs())
            print('NEW activity: '+activity_prep.name+' '+str(activity_prep.duration)+' '+str(activity_prep.labour)+'\n')
            

            # !!! Writes activities currently in activity_inputs[]
            #     to 'PERT_input.txt'
            write_txt_data(get_input_string())
            

    

################
#
#      Main
#
################

if __name__ == "__main__":
    
    #Create Application window object
    

    ###################
    #
    #    GUI 
    #
    ###################

    #INPUTS WINDOW
    # tk  root window
    root = tk.Tk()
     # title
    root.title('Perfect PERT')
    # window dimensions
    root.geometry('450x500') 
    # bkg colour
    root.configure(bg='SkyBlue1')


    ##################

    #milestones = parse_problem(get_input_string())

    # RESULTS WINDOW
    top = Toplevel() 
    top.geometry('300x300')
    top.configure(bg='lightgreen')

    # Header
    Label(top, 
        text ="~ Accoring to our calculation of PERT ~").place(relx=0,y=10)
    
    # Lowest possible peak requirement
    Label(top ,
        text ='Lowest possible peak requirement: ').place(relx=0,y=100)
    

    Label(top ,
        text ='?').place(relx=0,y=150)

    # List of activities in order
    Label(top ,
        text ='Schedules achieving lowest requirement \n(Activity, Start time):').place(relx=0,y=200)
    Label(top ,
        text ='?' ).place(relx=0,y=250)


    ###########
  
    
    
   

    ############
    # Inputs
    ############

    # List of Activity() objects to write into PERT_input.txt
    activities_input = []

    input_string = ''

    # Variables that store USER  input in GUI
    name =StringVar(root, value='A')
    dur = IntVar()
    lab = IntVar()


    # label
    task_label = Label(root, text='Activity:', bg='grey').place(relx=0, y=50)
    # input task
    name_entry = Entry(root, textvariable=name).place(x=175, y=50)

    # duration label
    dur_label = Label(root, text='Duration:', bg='grey').place(x=1, y=100)
    # duration input
    duration_entry = Entry(root, textvariable=dur).place(x=175, y=100)

    # labour label
    lab_label = Label(root, text='Labour:', bg='grey').place(x=0, y=150)
    # labour input
    labour_entry = Entry(root, textvariable=lab).place(x=175, y=150)


    # prereqs label
    prereqs_label = Label(root, text='Prerequisites:', bg='grey').place(x=1, y=200)
    #Check bar of activities that may be preceded
    prereq_checkbar = Checkbar(root, getActivityNames()).place(x=175, y=200)
    print(Checkbar(root, getActivityNames()).getvar())





    # Add activity BUTTON
    add_activity_button = Button(root, text=' + add activity ', width=10, height=1, bg='grey23', fg='wheat1', command=add_activity,
                                highlightbackground='green').place(relx=0.1,rely=0.7)

    # NUMBER OF ACTIVITIES INPUTED BY USER (update on button press)
    activity_counter = Label(root, text='# of Activities inputed : '+str(len(activities_input)) , bg='grey').place(x=0, rely=0.9)

    # Schedule PERT BUTTON
    evaluate_button = Button(root, height='2',command=execute_PERT, text='Evaluate PERT', bg='gold',
                            fg='white', highlightbackground='black').place(relx=0.6, rely=0.8)

    # Reset GUI list BUTTON
    reset_button = Button(root, height='2',command=reset_PERT, text='RESET', bg='red',
                            fg='white', highlightbackground='black').place(relx=0.2, rely=0.8)


    # Select Preset network BUTTON
    daycare_button = Button(root, height='2',width='15', command=load_daycare, text='Preset #1: Daycare', bg='grey',
                            fg='white', highlightbackground='black').place(x=300,y=230)
    #daycare_button.bind('<Enter>', preset_warning)

    # Select Preset network BUTTON
    excalibur_button = Button(root, height='2',width='15', command=load_excalibur, text='Preset #2: Excalibur', bg='gold',
                            fg='white', highlightbackground='black').place(x=300,y=260)



    root.mainloop()





# end
