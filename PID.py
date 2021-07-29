import time

class PID:

    def __init__(self, P, I, D):
        self.P = P
        self.I = I
        self.D = D

        self.time_now = time.time()
        self.last_time = self.time_now
        self.prev_error = 0

        self.Pval = 0.0
        self.Ival = 0.0
        self.Dval = 0.0
        self.result = 0.0

    def revise(self, feedback, goal):
        self.time_now = time.time()
        error = goal - feedback
        time_change = self.time_now - self.last_time
        error_change = error - self.prev_error

        self.Pval = self.P * error
        self.Ival = self.Ival + error * time_change
        self.Dval = error_change / time_change

        self.prev_error = error
        self.prev_time = time

        self.result = self.Pval + (self.I * self.Ival) + (self.D * self.Dval)




