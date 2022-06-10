from core.status import Status

class Step:
    is_ok = False
    final_step = False
    def __init__(
        self, name, function, success, fail,
            function_params=None, interval=0, retry=0, final_step=False
        ):
        self.function = function
        self.name = name
        self.success = success
        self.fail = fail
        self.interval = interval
        self.retry = retry
        self.function_params = function_params
        self.final_step = final_step
    

class StateManager:
    NO_WAIT_INTERVAL = 0
    
    retry_counter = 0
    steps = {}

    def __init__(self, first_step):
        self.first_step = first_step
        
        self.organizer_step = Step(
            function=self.organizer,
            name="organizer", success="organizer", fail="organizer",
            function_params=None, interval=0, retry=0
        )

        self.success_step = Step(
            function=self.success,
            name="success", success="success", fail="success",
            function_params=None, interval=0, retry=0, final_step=True
        )

        self.failure_step = Step(
            function=self.failure,
            name="failure", success="failure", fail="failure",
            function_params=None, interval=0, retry=0, final_step=True
        )

        self.current = self.organizer_step

        # Add default steps to steps dictionary
        self.add_step(self.organizer_step)
        self.add_step(self.success_step)
        self.add_step(self.failure_step)

    def add_step(self, step):
        self.steps[step.name] = step

    def get_step(self, name):
        return self.steps[name]
    
    def clear_counter(self):
        self.retry_counter = 0

    def counter_tick(self):
        self.retry_counter += 1

    def organizer(self):
        if self.current.name == "organizer":
            self.current = self.first_step
        else:
            if self.current.is_ok:
                self.current.is_ok = False
                self.current = self.get_step(self.current.success)
            else:
                if self.retry_counter >= self.current.retry:
                    self.current = self.get_step(self.current.fail)
                    self.clear_counter()
                    self.current.interval = self.NO_WAIT_INTERVAL
                else:
                    self.current = self.get_step(self.current.name)
                    self.counter_tick()
        return {"status" : Status.SUCCESS}
    
    def success(self):
        return {"status": Status.SUCCESS}
    
    def failure(self):
        return {"status": Status.ERROR}

    def execute_organizer_step(self):
        self.organizer()

    def execute_current_step(self):
        params = self.current.function_params

        if params:
            result = self.current.function(**params)
        else:
            result = self.current.function()
        
        print(result)

        if result["status"] == Status.SUCCESS:
            self.current.is_ok = True
        else:
            self.current.is_ok = False
        
    def loop(self, begin=None, end=None):
        result={}
        if begin:
            self.current = self.get_step(begin)

        self.execute_organizer_step()
        self.execute_current_step()
        
        if end:
            if self.current.name == self.get_step(end).name:
                self.current.final_step = True
        
        if not self.current.final_step:
            result["status"] = Status.ONGOING
            result["interval"] = self.current.interval
            return result
        else:
            if self.current.name == "success":
                result["status"] = Status.SUCCESS
            elif self.current.name == "failure":
                result["status"] = Status.ERROR
            
            result["interval"] = self.NO_WAIT_INTERVAL
            return result
