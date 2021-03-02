# Represents an activity in a PERT diagram
class Activity:
    def __init__(self, name, duration, predecessor, successor):
        self.name = name # Name of this activity, or nothing if it is a dummy
        self.duration = duration # Time to complete this activity
        self.predecessor = predecessor # Milestone this activity starts at
        self.successor = successor # Milestone this activity ends at
        self.slack = 0 # Slack time for this activity
        
    def __str__(self):
        if(self.name == ''):
            return 'Dummy [S: ' + str(self.slack) + ']'
        else:
            return self.name + ' [D: ' + str(self.duration) + ', S: ' + str(self.slack) + ']'

# Represents a milestone in a PERT diagram
class Milestone:
    def __init__(self):
        self.prerequisites = [] # List of activities that must be completed before this milestone
        self.dependants = [] # List of activities that must start after this milestone
        self.earliest = 0 # Earliest start time for this milestone
        self.latest = 0 # Latest start time for this milestone
        self.slack = 0 # Slack time for this milestone
        
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

# Checks if two milestones have the same prerequisites and can therefore be merged        
def can_merge_milestones(m1, m2):
    # Make sure the two milestones are not the same one
    if(m1 == m2):
        return False
    
    # Make sure both milestones have same number of prerequisites
    if(len(m1.prerequisites) != len(m2.prerequisites)):
        return False

    # Make sure all prerequisites of m1 are dummy activities
    for prereq in m1.prerequisites:
        if(prereq.name != ''):
            return False
    
    # Make sure all prerequisites of m2 are dummy activities    
    for prereq in m2.prerequisites:
        if(prereq.name != ''):
            return False
    
    # Make sure the prerequisites are equivalent
    for m1p in m1.prerequisites:
        match = False
        for m2p in m2.prerequisites:
            if(m1p.predecessor == m2p.predecessor):
                match = True
                
        if(not match):
            return False
    
    return True

# Load the problem from the file
def load_problem(filename):
    lineno = 0
    activities = []
    milestones = []
    with open(filename) as problem:
        for line in problem.readlines():
            lineno = lineno + 1
            if(len(line) > 0 and line.strip() != '' and line[0] != '!'):
                tokens = [x.strip() for x in line.strip().split(',')]
                
                # Check that the activity definition is valid
                if(len(tokens) < 2):
                    print('Error on line ' + str(lineno) + ': Invalid activity definition \"' + line.strip() + '\"')
                    return False
                    
                # Check that the duration is a valid number
                try:
                    activity_duration = int(tokens[1])
                    if(activity_duration < 0):
                        print('Error on line ' + str(lineno) + ': Activity duration less than 0')
                        return False
                except ValueError:
                    print('Error on line ' + str(lineno) + ': Invalid activity duration \"' + tokens[1] + '\"')
                    return False
                    
                else:
                    # Check that activity does not exist already
                    for activity in activities:
                        if(activity.name == tokens[0]):
                            print('Error on line ' + str(lineno) + ': Activity redefined \"' + line.strip() + '\"')
                            return False
                    
                    # Make a list of prerequisites for this activity, and make sure they have been defined previously
                    prerequisites = []
                    for i in range(2, len(tokens)):
                        prerequisites.append(tokens[i])
                        found = False
                        for activity in activities:
                            if(activity.name == tokens[i]):
                                found = True
                                break
                                
                        if(not found):
                            print('Error on line ' + str(lineno) + ': Prerequisite undefined \"' + tokens[i] + '\"')
                            return False
                    
                    # Create the activity and a new milestones to the start and finish of it
                    activity_start = Milestone()
                    activity_end = Milestone()
                    activity = Activity(tokens[0], int(tokens[1]), activity_start, activity_end)
                    activity_start.dependants.append(activity)
                    activity_end.prerequisites.append(activity)
                    activities.append(activity)
                    
                    # Find the prerequite milestones for this activity, and link them with dummy activites to activity_start
                    for prerequisite in prerequisites:
                        found = False
                        for milestone in milestones:
                            if(len(milestone.prerequisites) == 1 and milestone.prerequisites[0].name == prerequisite):
                                dummy = Activity('', 0, milestone, activity_start)
                                milestone.dependants.append(dummy)
                                activity_start.prerequisites.append(dummy)
                                found = True
                    
                    milestones.append(activity_start)
                    milestones.append(activity_end)
     
    # Merge all milestones with the exact same prerequisites together
    merged = True
    while(merged):
        remove = None
        merged = False
        for milestone in milestones:
            for equivalent in milestones:
                if(can_merge_milestones(milestone, equivalent)):
                    # Merge the dependant activities of the two milestones
                    for dependant in equivalent.dependants:
                        if(dependant not in milestone.dependants):
                            dependant.predecessor = milestone
                            milestone.dependants.append(dependant)
                  
                    # Remove dummy activities leading to the milestone that will be removed
                    for prerequisite in equivalent.prerequisites:
                        remaining_dependants = []
                        for activity in prerequisite.predecessor.dependants:
                            if(activity != prerequisite):
                                remaining_dependants.append(activity)
                        prerequisite.predecessor.dependants = remaining_dependants
                    remove = equivalent
                    break      
            
            if(remove != None):
                break      
        if(remove != None):
            merged = True
            milestones.remove(remove)
    
    # Collapse all milestones with a single prerequisite and single dependant where one is a dummy activity
    collapsed = True
    while(collapsed):
        remove = None
        collapsed = False
        for milestone in milestones:
            if(len(milestone.prerequisites) == 1 and len(milestone.dependants) == 1):
                if(milestone.prerequisites[0].name == ''):
                    dummy = milestone.prerequisites[0]
                    activity = milestone.dependants[0]
                    dummy.predecessor.dependants.remove(dummy)
                    dummy.predecessor.dependants.append(activity)
                    activity.predecessor = dummy.predecessor
                    remove = milestone
                    break
                
                if(milestone.dependants[0].name == ''):
                    dummy = milestone.dependants[0]
                    activity = milestone.prerequisites[0]
                    dummy.successor.prerequisites.remove(dummy)
                    dummy.successor.prerequisites.append(activity)
                    activity.successor = dummy.successor
                    remove = milestone
                    break
        
        if(remove != None):
            collapsed = True
            milestones.remove(remove)
    
    return milestones

# Calculates the TL, TE, and slack for milestones, as well as slack for activities
def calc_times(milestones):
    # Calculate the TE for each milestone
    solved = []
    while(len(solved) != len(milestones)):
        for milestone in milestones:
            if(milestone not in solved):
                unsolved_prerequisites = False
                te = 0
                for prerequisite in milestone.prerequisites:
                    if(prerequisite.predecessor in solved):
                        te = max(te, prerequisite.predecessor.earliest + prerequisite.duration)
                    else:
                        unsolved_prerequisites = True
                        break
                    
                if(not unsolved_prerequisites):
                    milestone.earliest = te
                    solved.append(milestone)
                    
    # Calculate the TL for each milestone
    solved = []
    while(len(solved) != len(milestones)):
        for milestone in milestones:
            if(milestone not in solved):
                unsolved_dependants = False
                tl = float('inf')
                
                if(len(milestone.dependants) == 0):
                    tl = milestone.earliest
                else:
                    for dependant in milestone.dependants:
                        if(dependant.successor in solved):
                            tl = min(tl, dependant.successor.latest - dependant.duration)
                        else:
                            unsolved_dependants = True
                            
                if(not unsolved_dependants):
                    milestone.latest = tl
                    solved.append(milestone)
                            
    # Calculate the slack for each milestone, and activity 
    for milestone in milestones:
        milestone.slack = milestone.latest - milestone.earliest
        for activity in milestone.dependants:
            activity.slack = activity.successor.latest - activity.predecessor.earliest - activity.duration

data = load_problem('Problems/Lab6_Excalibur.txt')
calc_times(data)
for item in data:
    print(str(item))