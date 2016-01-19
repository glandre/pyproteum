class TestCaseInfo:
    """ Not implemented yet. """
    def __init__(self):
        self.not_executed_mutants = 0
        self.alive_mutants = 0
        self.dead_by_stdout = 0
        self.dead_by_retcode = 0
        self.dead_by_timeout = 0
        self.dead_by_trap = 0
        self.avoided_mutants = 0
        self.dead_mutants = 0
        self.enabled = True
        self.cpu_exec_time = 0.0
        self.total_exec_time = 0.0
        self.retcode = 0
        self.parameters = ""
        self.input = ""
        self.output = ""
        self.stderr = ""