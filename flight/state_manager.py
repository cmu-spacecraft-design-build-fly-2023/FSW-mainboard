import apps.tasko as tasko


class StateManager:
    """Singleton Class"""

    def __init__(self):

        self.current_state = None
        self.previous_state = None
        self.scheduled_tasks = {}
        self.initialized = False

    def start(self, start_state: str):
        """Starts the state machine

        Args:
        :param start_state: The state to start the state machine in
        :type start_state: str
        """
        from sm_configuration import SM_CONFIGURATION, TASK_REGISTRY

        self.config = SM_CONFIGURATION
        self.task_registry = TASK_REGISTRY

        # TODO Validate the configuration and registry
        self.states = list(self.config.keys())

        # init task objects
        self.tasks = {key: task() for key, task in TASK_REGISTRY.items()}

        self.current_state = start_state

        # Will load all the tasks through the state switch
        self.switch_to(start_state)
        tasko.run()

    def switch_to(self, new_state):
        """Switches to a new state and actiavte all corresponding tasks as defined in the SM_CONFIGURATION

        Args:
        :param new_state: The name of the state to switch to
        :type new_state: str
        """

        if new_state not in self.states:
            raise ValueError(f"State {new_state} is not in the list of states")

        if self.initialized:
            # prevent illegal transitions
            if not (new_state in self.config[self.current_state]["MovesTo"]):
                raise ValueError(
                    f"No transition from {self.current_state} to {new_state}"
                )
        else:
            self.initialized = True

        self.previous_state = self.current_state

        # TODO transition functions

        ## Scheduling

        self.stop_all_tasks()
        self.scheduled_tasks = {}  # Reset
        self.current_state = new_state
        state_config = self.config[new_state]

        for task_name, props in state_config["Tasks"].items():
            if props["ScheduleLater"]:
                schedule = tasko.schedule_later
            else:
                schedule = tasko.schedule

            frequency = props["Frequency"]
            priority = props["Priority"]
            task_fn = self.tasks[task_name]._run

            self.scheduled_tasks[task_name] = schedule(
                frequency, task_fn, priority
            )

        print(f"Switched to state {new_state}")

    def stop_all_tasks(self):
        for name, task in self.scheduled_tasks.items():
            task.stop()

    def query_global_state(self):
        return self.current_state

    def query_state(self):
        state = {}
        for task in self.scheduled_tasks:
            state[task] = task.query_state()
        return state


state_manager = StateManager()
