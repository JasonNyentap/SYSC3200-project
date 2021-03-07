

#models

#############################################
#
# Represents an activity in a PERT diagram
# 
#
#############################################
class Activity:
    
    # Default constructor
    def __init__(self, name, duration, labour, predecessor, successor):
        
        # Activity attributes:

        # Name of this activity, or nothing if it is a dummy
        self.name = name 

        # Time to complete this activity
        self.duration = duration 

        # Milestone this activity starts at
        self.predecessor = predecessor 

        # Milestone this activity ends at
        self.successor = successor 
        
        # Total slack time for this activity
        self.slack = 0 
        
        # Free slack time for this activity
        self.free_slack = 0 
        
        # Amount of labour needed to complete this activity
        self.labour = labour 
        
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




#############################################
# 
# Class Milestone Represents a milestone activity in a PERT diagram  
# 
#############################################

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