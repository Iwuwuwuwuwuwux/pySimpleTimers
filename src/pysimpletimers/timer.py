import threading
from time import sleep

sleep_time = 1 #may be changed if you need a more precise timer (ex: a delay like 0.5 or 1.75), this is in seconds

class Timer(threading.Thread):

    def __init__(self, delay: int, callback, args: tuple, loop: bool):
        threading.Thread.__init__(self)
        self.daemon = True
        
        self.delay = delay
        self.callback = callback #must use only one arg (a tuple), (ex: def func(args: tuple): print(args[0])"
        self.args = args #a tuple containing all the args that will be used in the callback func
        self.loop = loop #will automatically repeat the timer whenever it ends
        
        self.is_running = False
        self.current_time = 0 #if the timer is started, will return the current uptime of this start
        self.close_thread = False
        
        threading.Thread.start(self)

    def start(self):        
        self.is_running = True
        
        self.current_time = 0

    def run(self): #shouldn't be called by the user, this is made to override the default "run" function of a Thread
        global sleep_time
            
        while True:
            if self.close_thread == True: break #the thread will be closed if the above while: True is broken
            elif self.is_running == False: continue #won't execute the timer part if the timer is not "started"
        
            self.current_time = 0
            while self.current_time < self.delay: #"current_time" can be greater than the set delay if the delay is a float,
                sleep(sleep_time) #to avoid this you should set "sleep_time" to a smaller or greater value (as you need it)
                
                if self.is_running == False: break #if the stop func is called then break to return to the waiting part
                
                self.current_time = self.current_time + self.sleep_time
            
            if self.close_thread == True: break
            elif self.is_running == False: continue
        
            self.callback(self.args) #calls the callback func with the args as an argument
            
            if self.loop == False:
                self.is_running = False
    
    def stop(self): #stop the timer but don't kill the thread, it can be restarted, the current time isn't cleared to you can still read it
        self.is_running = False
    
    def quit(self): #stops the timer AND kill the thread, after that the timer object 
        self.stop() #cannot be used anymore, except for storing data
        self.close_thread = True
    
    
"""
example of use:

def my_func(args: tuple):
    number1 = args[0]
    number2 = args[1]
    result = number1 + number2

    print("{} + {} = {} \n{}".format(number1, number2, result, args[2]))
    
my_timer = Timer(delay = 5, callback = my_func, args = (3, 9, "these are maths!"), loop = False)
my_timer.start()

sleep(10)

---------------------------------------
you can't set a var using the tuple, you are going to need this value to be global; not really understandable
so here is an example of what i mean:

what_animals_i_currently_prefer_str = "dogs"

def set_my_var(args: tuple):
    global what_animals_i_currently_prefer_str
    
    what_animals_i_currently_prefer_str = args[0]

my_timer = Timer(delay = 5, callback = set_my_var, args = ("cats"), loop = False)
my_timer.start()

sleep(10)
"""
