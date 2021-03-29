##################
#
# PERT functions
#
###################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Calculate the maximum required labour 
# given a list of Activities
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calc_labour(activities):
    time = 0
    done = False
    worst_labour = 0
    while(not done):
        done = True
        labour = 0
        for activity in activities:
            started = activity.predecessor.earliest + activity.delay
            ended = started + activity.duration
            if(time >= started and time < ended):
                done = False
                labour += activity.labour
        
        worst_labour = max(worst_labour, labour)
        time += 1
    
    return worst_labour





#######################
#
#   Models
#
#######################

class Activity:

    #################################
    # Default constructor
    #################################
    def __init__(self):
         # Activity attributes:
        # Name of this activity, or nothing if it is a dummy
        self.name = 'No-name' 
        # Time to complete this activity
        self.duration = 1 
        # Milestone this activity starts at
        self.predecessor = Milestone() 
        # Milestone this activity ends at
        self.successor = Milestone() 
        # Total slack time for this activity
        self.slack = 0 
        # Free slack time for this activity
        self.free_slack = 0 
        # Amount of labour needed to complete this activity
        self.labour = 1 
        # How long to wait before starting the activity (within free_slack)
        self.delay = 0

    ###############################################
    # Named Activity constructor (w/o predecessor)
    ###############################################
    def __init__(self, name, duration, labour):

         # Activity attributes:

        # Name of this activity, or nothing if it is a dummy
        self.name = name 
        # Time to complete this activity
        self.duration = duration 
        # Amount of labour needed to complete this activity
        self.labour = labour

        # Milestone this activity starts at
        self.predecessor = Milestone() 
        # Milestone this activity ends at
        self.successor = Milestone() 
        # Total slack time for this activity
        self.slack = 0 
        # Free slack time for this activity
        self.free_slack = 0 
        # How long to wait before starting the activity (within free_slack)
        self.delay = 0

    ###############################################
    # Named Activity constructor (w/ predecessor)
    ###############################################
    def __init__(self, name, duration, labour, predecessor):

         # Activity attributes:

        # Name of this activity, or nothing if it is a dummy
        self.name = name 
        # Time to complete this activity
        self.duration = duration  
        # Amount of labour needed to complete this activity
        self.labour = labour
        # Milestone this activity starts at
        self.predecessor = predecessor 

        # Milestone this activity ends at
        self.successor = Milestone() 
        # Total slack time for this activity
        self.slack = 0 
        # Free slack time for this activity
        self.free_slack = 0 
        # How long to wait before starting the activity (within free_slack)
        self.delay = 0

    #################################
    # Fully Paremtrized constructor (PERTscheduler)
    #################################
    #def __init__(self, name, duration, labour, predecessor, successor):
    def __init__(self, *args):
        
        # Every activity should be initialized w these 3 fields:
        self.name = args[0] 
        # Time to complete this activity
        self.duration = args[1] 
        # Amount of labour needed to complete this activity
        self.labour = args[2] 
     
            
        #contructor w predecessor and successor fields
        if len(args) == 5:
            # Activity attributes:

            # Name of this activity, or nothing if it is a dummy
            
            # Milestone this activity starts at
            self.predecessor = args[3] 
            # Milestone this activity ends at
            self.successor = args[4]


        # Total slack time for this activity
        self.slack = 0 
        # Free slack time for this activity
        self.free_slack = 0 
        # How long to wait before starting the activity (within free_slack)
        self.delay = 0

    
    
    def __str__(self):
        if(self.name == ''):
            return 'Dummy [S: ' + str(self.slack) + ']'
        else:
            res = self.name
            res += ' [D: ' + str(self.duration)
            res += ', L: ' + str(self.labour)
            res += ', S: ' + str(self.slack)
            res += ', FS: ' + str(self.free_slack)
            res += ']'
            return res
        
    def __str__new(self, command):
        if(self.name == ''):
            return 'No-name'
        return self.name

class Activity_Input:
    def __init__(self, name, duration, labour, predecessor):
        # Name of this activity, or nothing if it is a dummy
        self.name = name 
        # Time to complete this activity
        self.duration = duration  
        # Amount of labour needed to complete this activity
        self.labour = labour
        # Milestone this activity starts at
        self.predecessor = predecessor 
  

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
# Class Milestone Represents a milestone activity in a PERT diagram  
# 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Milestone(Activity):
    def __init__(self):
        # List of activities that must be completed before this milestone
        self.prerequisites = [] 
        
        # List of activities that must start after this milestone
        self.dependants = [] 
        
        # Earliest start time for this milestone
        self.earliest = 0 
        
        # Latest start time for this milestone
        self.latest = 0 
        
        # Slack time for this milestone
        self.slack = 0 

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #  
    # Python equivalent of toString()
    # 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __str__(self):

        
        res = 'Milestone [TE: ' + str(self.earliest) + ', TL:' + str(self.latest) + ', S:' + str(self.slack) + ']\n'
        
        res += '    Prerequisites:\n'
        if(len(self.prerequisites) > 0):
            for activity in self.prerequisites:
                res += '        ' + str(activity) + '\n'
        else:
            res += '        None\n'
        
        res += '    Dependants:\n'
        if(len(self.dependants) > 0):
            for activity in self.dependants:
                res += '        ' + str(activity) + '\n'
        else:
            res += '        None\n'
            
        return res


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # Checks if two milestones have the same prerequisites 
    # 
    # 
    # If true, they can be merged into one   
    # 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    # previously
    # def can_merge_milestones(m1, m2):

    def can_merge_milestones(self,m2):
        # Make sure the two milestones are not the same one
        if(self == m2):
            return False
        
        # Make sure both milestones have same number of prerequisites
        if(len(self.prerequisites) != len(m2.prerequisites)):
            return False

        # Make sure all prerequisites of self are dummy activities
        for prereq in self.prerequisites:
            if(prereq.name != ''):
                return False
        
        # Make sure all prerequisites of m2 are dummy activities    
        for prereq in m2.prerequisites:
            if(prereq.name != ''):
                return False
        
        # Make sure the prerequisites are equivalent
        for selfp in self.prerequisites:
            match = False
            for m2p in m2.prerequisites:
                if(selfp.predecessor == m2p.predecessor):
                    match = True
                    
            if(not match):
                return False
        
        return True


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Accessor Methods
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # def getName():
    #     return self.name


    # def getDuration():
    #     return self.duration
    
    # def getPredecessors():
    #     return self.predecessor

    # def getLabour():
    #         pass


        # Milestone this activity starts at
        # self.predecessor = predecessor

        # # Milestone this activity ends at
        # self.successor = successor 
        
        # # Total slack time for this activity
        # self.slack = 0 
        
        # # Free slack time for this activity
        # self.free_slack = 0 
        
        # # Amount of labour needed to complete this activity
        # self.labour = labour 
        
        # # How long to wait before starting the activity (within free_slack)
        # self.delay = 0

