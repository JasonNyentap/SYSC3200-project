# Represents an activity in a PERT diagram
class Activity:
    def __init__(self, name, duration, labour, predecessor, successor):
        self.name = name # Name of this activity, or nothing if it is a dummy
        self.duration = duration # Time to complete this activity
        self.predecessor = predecessor # Milestone this activity starts at
        self.successor = successor # Milestone this activity ends at
        self.slack = 0 # Total slack time for this activity
        self.free_slack = 0 # Free slack time for this activity
        self.labour = labour # Amount of labour needed to complete this activity
        self.delay = 0 # How long to wait before starting the activity (within free_slack)
        
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
                if(len(tokens) < 3):
                    print('Error on line ' + str(lineno) + ': Invalid activity definition \"' + line.strip() + '\"')
                    return False
                    
                # Check that the duration is a valid number
                if(not tokens[1].isnumeric()):
                    print('Error on line ' + str(lineno) + ': Invalid activity duration \"' + tokens[1] + '\"')
                    return False
                elif(int(tokens[1]) < 0):
                    print('Error on line ' + str(lineno) + ': Activity duration less than 0')
                    return False
                
                # Check that the required labour is a valid number
                if(not tokens[2].isnumeric()):
                    print('Error on line ' + str(lineno) + ': Invalid labour requirement \"' + tokens[2] + '\"')
                    return False
                elif(int(tokens[2]) < 0):
                    print('Error on line ' + str(lineno) + ': Labour requirement less than 0')
                    return False
                
                # Check that activity does not exist already
                for activity in activities:
                    if(activity.name == tokens[0]):
                        print('Error on line ' + str(lineno) + ': Activity redefined \"' + line.strip() + '\"')
                        return False
                
                # Make a list of prerequisites for this activity, and make sure they have been defined previously
                prerequisites = []
                for i in range(3, len(tokens)):
                    prerequisites.append(tokens[i])
                    found = False
                    for activity in activities:
                        if(activity.name == tokens[i]):
                            found = True
                            break
                            
                    if(not found):
                        print('Error on line ' + str(lineno) + ': Prerequisite undefined \"' + tokens[i] + '\"')
                        return False
                
                # Create the activity and add new milestones to the start and finish of it
                activity_start = Milestone()
                activity_end = Milestone()
                activity = Activity(tokens[0], int(tokens[1]), int(tokens[2]), activity_start, activity_end)
                activity_start.dependants.append(activity)
                activity_end.prerequisites.append(activity)
                activities.append(activity)
                
                # Find the prerequite milestones for this activity, and link them with dummy activities to activity_start
                for prerequisite in prerequisites:
                    found = False
                    for milestone in milestones:
                        if(len(milestone.prerequisites) == 1 and milestone.prerequisites[0].name == prerequisite):
                            dummy = Activity('', 0, 0, milestone, activity_start)
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
                # Check if milestone and equivalent can be merged
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
                # Check if milestone and equivalent are both end points, if they are merge them
                elif(milestone != equivalent and len(milestone.dependants) == 0 and len(equivalent.dependants) == 0):
                    # Redirect the prerequisite activities of equivalent to milestone and add them to milestone
                    for prerequisite in equivalent.prerequisites:
                        milestone.prerequisites.append(prerequisite)
                        prerequisite.successor = milestone
                    
                    # Get rid of equivalent                  
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
    
    calc_times(milestones)
    return milestones

# Calculates the TL, TE, and slack for milestones, as well as slack and free slack for activities
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
            activity.free_slack = activity.successor.earliest - activity.predecessor.earliest - activity.duration

# Returns a list of activities on the critical path
# The milestones given as input must have had their parameters calculated beforehand by calc_times()
def critical_path(milestones):
    critical = []
    for milestone in milestones:
        for dependant in milestone.dependants:
            if(dependant.slack == 0 and dependant.predecessor.slack == 0 and dependant.successor.slack == 0):
                if(dependant.name != ''):
                    critical.append(dependant)
                
    return critical

# Calculate the maximum required labour for a list of activities
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

# Finds all schedules for activities that will result in the lowest peak resource usage 
def resource_level(milestones):
    # Get the the list of activities in the diagram, and set their delay to 0 (earliest schedule)
    activities = []
    slack_activities = []
    for milestone in milestones:
        for dependant in milestone.dependants:
            if(dependant.name != ''):
                dependant.delay = 0
                activities.append(dependant)
                if(dependant.slack != 0):
                    slack_activities.append(dependant)
        
    # Exhaustively search for the lowest resource schedule by incrementing the delay time for each activity between 0 and free_slack inclusive
    lowest_resource = float('inf')
    schedules = []
    while(True):
        to_increment = 0
        while(to_increment < len(slack_activities) and slack_activities[to_increment].delay == slack_activities[to_increment].slack):
            slack_activities[to_increment].delay = 0
            to_increment += 1
    
        if(to_increment < len(slack_activities)):
            slack_activities[to_increment].delay = (slack_activities[to_increment].delay + 1) % (slack_activities[to_increment].slack + 1)
            to_increment = 0
            
            # Check that this schedule is valid
            valid = True
            for milestone in milestones:
                prerequisite_finish = 0
                dependant_start = float('inf')
                for prerequisite in milestone.prerequisites:
                    if(prerequisite.name != ''):
                        prerequisite_finish = max(prerequisite_finish, prerequisite.predecessor.earliest + prerequisite.delay + prerequisite.duration)
                for dependant in milestone.dependants:
                    if(dependant.name != ''):
                        dependant_start = min(dependant_start, milestone.earliest + dependant.delay)
                    
                if(dependant_start < prerequisite_finish):
                    valid = False
                    break
            
            if(valid):
                resources = calc_labour(activities)
            else:
                resources = float('inf')
            
            if(resources < lowest_resource):
                lowest_resource = resources
                schedules = []
            
            if(resources == lowest_resource):
                activity_schedule = []
                for activity in activities:
                    activity_schedule.append((activity.name, activity.predecessor.earliest + activity.delay))
                    
                schedules.append(activity_schedule)
        else:
            return (lowest_resource, schedules)

# The code below here is for testing
data = load_problem('Problems/Assignment3.txt')
if(data == False):
    print('An error occured while loading the problem')
else:
    print('[ Problem milestones and activities ]')
    for milestone in data:
        print(str(milestone))

    print('[ Critical path activities ]')    
    for activity in critical_path(data):
        print(str(activity))
        
    print('\n[ Labour requirements ]')        
    lowest, schedules = resource_level(data)
    print('Lowest possible peak requirement: ' + str(lowest))
    print('Schedules achieving lowest requirement (Activity, Start time):')
    for schedule in schedules:
        print(schedule)
    