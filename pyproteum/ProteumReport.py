class ProteumReport:
    """ Proteum Report Handler
        Responsible for parsing relevant information from ProteumIM's output reports
        
        Author: Geraldo B. Landre (geraldo@facom.ufms.br) 
    """

    line_sep = "[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]"
    
    def __init__(self, lst):
        self.lst = lst

    def load(self):
        with open(self.lst, 'r') as lst_file:
            self.load_general(lst_file)

    def load_general(self, f):
        trash = f.readline()
        trash = f.readline()
        trash = f.readline()

        self.program = f.readline().strip().split()[-1]

        trash = f.readline()

        self.source_file = f.readline().strip().split()[-1]

        trash = f.readline()

        self.total_mutants = int(f.readline().strip().split()[-1])

        trash = f.readline()

        self.anomalous_mutants = int(f.readline().strip().split()[-1])

        trash = f.readline()

        self.active_mutants = int(f.readline().strip().split()[-1])

        trash = f.readline()

        self.alive_mutants = int(f.readline().strip().split()[-1])

        trash = f.readline()

        self.equivalent_mutants = int(f.readline().strip().split()[-1])

        trash = f.readline()

        self.mutation_score = float(f.readline().strip().split()[-1])

        trash = f.readline()
        trash = f.readline()

        #self.operators = []
        self.operators = {}
        self.ordered_op_keys = []

        line = f.readline() #2,4,6
        split = line.split()
        #print ("line:", line)
        #print ("split:", split)
        while line and (len(split) == 3 or len(split) == 5 or len(split) == 7):
            #print ("while[%d]: %s" % (len(split), line))
            #print("[%s] = %d" % (split[1], int(split[2])))
            #self.operators.append({split[1] : int(split[2])})
            self.operators[split[1]] = int(split[2])
            self.ordered_op_keys.append(split[1])
            if len(split) >= 5:
                #print("[%s] = %d" % (split[3], int(split[4])))
                #self.operators.append({split[3] : int(split[4])})
                self.operators[split[3]] = int(split[4])
                self.ordered_op_keys.append(split[3])
                if len(split) == 7:
                    #print("[%s] = %d" % (split[5], int(split[6])))
                    #self.operators.append({split[5] : int(split[6])})
                    self.operators[split[5]] = int(split[6])
                    self.ordered_op_keys.append(split[5])
            line = f.readline()
            split = line.split()

        #print(self.operators)

    def load_test_cases(self, f):
        self.test_cases = []

        for line in f:
            tcase = TestCaseInfo()
            tcase.number = 0
            tcase.not_executed_mutants = 0
            tcase.alive_mutants = 0
            tcase.dead_by_stdout = 0
            tcase.dead_by_retcode = 0
            tcase.dead_by_timeout = 0
            tcase.dead_by_trap = 0
            tcase.avoided_mutants = 0
            tcase.dead_mutants = 0
            tcase.enabled = True
            tcase.cpu_exec_time = 0.0
            tcase.total_exec_time = 0.0
            tcase.retcode = 0
            tcase.parameters = ""
            tcase.input = ""
            tcase.output = ""
            tcase.stderr = ""

            self.test_cases.append(tcase)

    def str_ops(self, endl="\n"):
        string = ""
        j = 0
        for key in self.ordered_op_keys:
            string += " %-15s %5d    " % (key, self.operators[key])
            j = (j+1) % 3
            if j == 0:
                string += endl
        return string

    def __str__(self):
        return """
[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
[]
[]                  PROGRAM TESTE: """ + self.program + """
[]----------------------------------------------------------
[]   SOURCE FILE: """ + self.source_file + """
[]
[]   TOTAL MUTANTS: """ + str(self.total_mutants) + """
[]
[]   ANOMALOUS MUTANTS: """ + str(self.anomalous_mutants) + """
[]
[]   ACTIVE MUTANTS: """ + str(self.active_mutants) + """
[]
[]   ALIVE MUTANTS: """ + str(self.alive_mutants) + """
[]
[]   EQUIVALENT MUTANTS: """ + str(self.equivalent_mutants) + """
[]
[]   MUTATION SCORE: """ + str(self.mutation_score) + """
[]
[]   OPERATORS:
[]  """ + self.str_ops("\n[]\t") + """
[]
[][][][][][][][][][][][][][][][][][][][][][][][][][][][][][]
"""

# Main to test:
if __name__ == "__main__":
    report = ProteumReport("example.lst")
    #report = ProteumReport("simple-example.lst")
    report.load()
    print(report)
