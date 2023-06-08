import time

class ExecutionTimer:

    def __init__(self):
        print("Initialize ExecutionTimer.")
        self.start_time = time.time()
        print( "> starting timer ", round(self.start_time / 365 / 24 / 60 / 60) , " years since January 1, 1970.")
    
    def print_time(self, text):
        elapsed_time = time.time() - self.start_time
        if (elapsed_time > (60*60)):
            print(text, ": elapsed: ",  round(elapsed_time/(60*60), 3), "hours" )
        if (elapsed_time > 60):
            print(text, ": elapsed: ",  round(elapsed_time/60, 3), "minutes" )
        elif (elapsed_time > 1):
            print(text, ": elapsed: ",  round(elapsed_time, 3), "s" )
        elif (elapsed_time > 0.001):
            print(text, ": elapsed: ",  round(elapsed_time * 1000, 3), "ms" )
        else:
            print(text, ": elapsed: ",  round(elapsed_time * 1000 * 1000, 3), "ns" )