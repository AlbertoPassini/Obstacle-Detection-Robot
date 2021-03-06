import explorerhat
import random
import time

#A task instance
class TaskIns(object):
     #Constructor (should only be invoked with keyword parameters)
    def __init__(self, start, end, priority, name):
        self.start    = start
        self.end      = end
        self.usage    = 0
        self.priority = priority
        self.name     = name.replace("\n", "")
        self.id = int(random.random() * 10000)

    #Allow an instance to use the cpu (periodic)
    def use(self, usage):
        self.usage += usage
        if self.usage >= self.end - self.start:
            return True
        return False

    #Default representation
    def __repr__(self):
        return str(self.name) + "#" + str(self.id) + " - start: " + str(self.start) + " priority: " + str(self.priority) + budget_text

    #Get name as Name#id
    def get_unique_name(self):
        return str(self.name) + "#" + str(self.id)


#Task types (templates for periodic tasks)
class TaskType(object):
    #Constructor
    def __init__(self, period, release, execution, deadline, name):
        self.period    = period
        self.release   = release
        self.execution = execution
        self.deadline  = deadline
        self.name      = name


#Reads the sensor and puts the value at hasDetectedObj
class  SensorTask(TaskType):
    def task(self):
        global hasDetectedObj 
	hasDetectedObj = explorerhat.input.one.read()
	print hasDetectedObj

#Reads the input from frontend
class  InputTask(TaskType):
    def task(self):
        global inputDirection 
	inputDirection = "up"
	global speed
	speed = 100


class  MotorTask(TaskType):
    def turnLeft(self):
        explorerhat.motor.one.forwards(speed)
        explorerhat.motor.two.backwards(speed)
        self.stopMotors()

    def turnRight(self):
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.forwards(speed)
        self.stopMotors()

    def accelerate(self):
        explorerhat.motor.one.forwards(100)
        explorerhat.motor.two.forwards(100)
        self.stopMotors()

    def reverse(self):
        explorerhat.motor.one.backwards(speed)
        explorerhat.motor.two.backwards(speed)
        self.stopMotors()

    def stopMotors(self):
        time.sleep(0.2)
        explorerhat.motor.stop()


    def task(self):
	dict_ = {"left":self.turnLeft, "right":self.turnRight, "up":self.accelerate, "down":self.reverse, "stop":self.stopMotors}

        dict_[canMoveToDir]()


#Analyses both results from the sensor and the input
class AnalyserTask(TaskType):
    def task(self):
        if (hasDetectedObj == 1):
            global canMoveToDir 
	    canMoveToDir = inputDirection
	    print canMoveToDir
        else:
            canMoveToDir = "stop"
	    print canMoveToDir


#Send to frontend the result of analyser
class ReporterTask(TaskType):
    def task(self):
        if (hasDetectedObj == 0):
            print "Has detected object!"
        else:
            print "No object ahead!"
