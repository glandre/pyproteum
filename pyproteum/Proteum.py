from __future__ import print_function
import os, sys
from os.path import isfile
from ProteumReport import ProteumReport

class Proteum(object):
    """ Python Adapter for Proteum.
        This class adapts calls for proteum commands as if it was a Python object
        
        Author: Geraldo B. Landre (geraldo@facom.ufms.br)

        TODO:
        test-new subcommands:
            pteste -create -S year -E year  -D /path/to/directory -C "gcc year.c -o year" -test cmd_unit_all
            ptest -l cmd_unit_all
            li -D /path/to/directory -P __year year  __year
            li -l -D /path/to/directory __year __year convert
            tcase -create -D /path/to/directory manual
            muta -create -D /path/to/directory manual
            instrum -D /path/to/directory -EE manual __year
            instrum -build -D /path/to/directory __year manual

    """

    @staticmethod
    def operators(preffix=None):
        allops = ['u-OAAA', 'u-OAAN', 'u-OABA', 'u-OABN', 'u-OAEA', 
                'u-OALN', 'u-OARN', 'u-OASA', 'u-OASN', 'u-OBAA', 
                'u-OBAN', 'u-OBBA', 'u-OBBN', 'u-OBEA', 'u-OBLN', 
                'u-OBNG', 'u-OBRN', 'u-OBSA', 'u-OBSN', 'u-OCNG', 
                'u-OCOR', 'u-OEAA', 'u-OEBA', 'u-OESA', 'u-Oido', 
                'u-OIPM', 'u-OLAN', 'u-OLBN', 'u-OLLN', 'u-OLNG', 
                'u-OLRN', 'u-OLSN', 'u-ORAN', 'u-ORBN', 'u-ORLN', 
                'u-ORRN', 'u-ORSN', 'u-OSAA', 'u-OSAN', 'u-OSBA', 
                'u-OSBN', 'u-OSEA', 'u-OSLN', 'u-OSRN', 'u-OSSA', 
                'u-OSSN', 'u-SBRC', 'u-SBRn', 'u-SCRB', 'u-SCRn', 
                'u-SDWD', 'u-SGLR', 'u-SMTC', 'u-SMTT', 'u-SMVB', 
                'u-SRSR', 'u-SSDL', 'u-SSWM', 'u-STRI', 'u-STRP', 
                'u-SWDD', 'u-VDTR', 'u-VGAR', 'u-VGPR', 'u-VGSR', 
                'u-VGTR', 'u-VLAR', 'u-VLPR', 'u-VLSR', 'u-VLTR', 
                'u-VSCR', 'u-VTWD', 'u-Cccr', 'u-Ccsr', 'u-CRCR', 
                'I-CovAllEdg', '-I-CovAllNod', 'I-DirVarAriNeg', 
                'I-DirVarBitNeg', 'I-DirVarIncDec', 'I-DirVarLogNeg', 
                'I-DirVarRepCon', 'I-DirVarRepExt', 'I-DirVarRepGlo', 
                'I-DirVarRepLoc', 'I-DirVarRepPar', 'I-DirVarRepReq', 
                'I-IndVarAriNeg', 'I-IndVarBitNeg', 'I-IndVarIncDec', 
                'I-IndVarLogNeg', 'I-IndVarRepCon', 'I-IndVarRepExt', 
                'I-IndVarRepGlo', 'I-IndVarRepLoc', 'I-IndVarRepPar', 
                'I-IndVarRepReq', 'I-RetStaDel', 'I-RetStaRep', 
                'II-ArgAriNeg', 'II-ArgBitNeg', 'II-ArgDel', 
                'II-ArgIncDec', 'II-ArgLogNeg', 'II-ArgRepReq', 
                'II-ArgStcAli', 'II-ArgStcDif', 'II-FunCalDel']

        if preffix:
            return [op for op in allops if op.startswith(preffix)]

        return allops

    def __init__(self, of=None):
        """ Constructor: init the output file
            Argument:
            of: output file used as default to print the results on every execution.
        """
        self.of = of if of and isfile(of) else None

        self.bin_dir = ""
        self.if_dir = ""

    def set_bin_dir(self, new_bin_dir):
        """In case of Proteum not on PATH."""
        self.bin_dir=new_bin_dir

    def set_interface_dir(self, new_if_dir):
        """In case of Proteum not on PATH."""
        self.if_dir = ""

    def set_session(self, session):
        """In case when Proteum test session is already created."""
        self.session=session

    def echo(self, msg):
        if self.of:
            with open(self.of, "w+") as of:
                print(msg, file=of)
        else:
            print(msg)


    def test_new(self, session, research=False, S='', E='', D='', C=''):
        """ Create a new Proteum Test Session
            Arguments:
            session: Test Session being created.
            research:   if True, mutants will be executed in research mode,
                        which means that all mutants will be executed against
                        all test cases.
                        if False (default), mutants will be executed in test mode,
                        which means that if a test case kills a mutant, this mutant
                        will not be executed by the following test cases.
            S: Name of the source program (without the ".c" extension)
            E: Name of the executable program.
            D: Directory where executable program is located (Default is ".")
            C: Compilation command to use when creating the mutants

            The method works as the command. Examples:
            > test-new myprog 
            is equivalent to
            > test-new -C "gcc myprog.c -o myprog" myprog

            > test-new -S myprog.c -E myprog -C "gcc myprog.c -o myprog -lm" mytestsession
            defines that when the mutants are compiled, they have to be linked with 
            the math library. 
        """
        self.set_session(session)
        arguments = ''
        if research:
            arguments += ' -research'
        if len(S) > 0:
            arguments += ' -S ' + S
        if len(E) > 0:
            arguments += ' -E ' + E
        if len(D) > 0:
            arguments += ' -D "' + D + '"'
        if len(C) > 0:
            arguments += ' -C "' + C + '"'

        self.echo("%stest-new%s %s" % (self.bin_dir, arguments, session))
        os.system("%stest-new%s %s" % (self.bin_dir, arguments, session))

    def exec_command(self, command, session=None, of=None):
        """ Execute a command using os.system associated to a test session
            Arguments:
            command: command to execute
            session: Proteum test session
            of: output file
        """
        if session is None:
            session = self.session

        if of is None:
        	of = self.of
        if session:
            cmd = "%s %s" % (command, session)
            self.echo('[proteumIM executing]:' + cmd)
            os.system("%s%s" % (cmd,((" >> %s" % self.of) if self.of else "")))
        else:
            self.echo('Error: First create a test session with test-new!')

    def muta_gen(self, 
        operators=[], unit='', D='',
        seed=0, r=False, 
        caller_unit='', callee_unit='', 
        O='', DD='', 
        session=None):
        """ Usage: muta-gen -<operator name> <percentage> <maximum>
            operators: A list of operators to generate. Each operator should be a dictionary
                 with the following keys:
                  'filter':    a filter for operator's name, such as '-all', '-u-SSDL' or '-u-S'
                  'percent':   the percent of mutants to generate. 100 to generate 100% of mutants, 
                               50 to generate 50%, and so on
                  'max':       maximum number of mutants to generate
                               passing 0 means to generate all possible
            session: test session to work with.
        """
        if session is None:
            session = self.session

        arguments = ''
        if len(unit) > 0:
            arguments += ' -unit ' + unit
        if seed != 0:
            arguments += ' -seed ' + seed
        if caller_unit and callee_unit and len(caller_unit) > 0 and len(callee_unit) > 0:
            arguments += " -c %s %s" % (caller_unit, callee_unit)
        if r:
            arguments += ' -r'
        if D and len(D) > 0:
            arguments += ' -D ' + D
        if DD and len(DD) > 0:
            arguments += ' -DD ' + DD
        
        ops_str  = '-O ' + O if len(O) > 0 else ''
        ops_str += ' '.join("%s %s %s" % (op['filter'], op['percent'], op['max']) for op in operators)

        self.exec_command( ("muta-gen %s%s" % (ops_str, arguments)), session)

    def tcase(self, arg, f=0, t=0, x="", D="", session=None):
        """ Manage test cases from test session based on argument passed as arg
            Arguments:
            arg: action to perform on test set
            f: starts a range of test cases to manage (example: 2)
            t: ends the range of test cases to manage (example: 3)
            x: specifies the range of test cases to manage (examples: "3 7 8" / "3")
            D: directory where test cases to be managed are located (default is ".")
            session: test session to work with.
        """
        if session is None:
            session = self.session
        
        command = "tcase " + arg
        if f > 0:
            command += " -f " + str(f)
        if t > 0:
            command += " -t " + str(t)
        if len(x) > 0:
            command += " -x " + x
        if len(D) > 0:
            command += " -D " + D

        self.exec_command(command, session)

    def tcase_create(self, D, session=None):
        """ Creates (or recreates) an EMPTY test set
            Arguments:
            D: directory where test cases to be managed are located (default is ".")
            session: test session to work with.
            Notice: If the test session already contains a test set
                    calling this method will result on deleting all
                    tests in such set
        """
        if session is None:
            session = self.session
        
        self.tcase("-create", 0, 0, "", D, session)

    def tcase_list(self, f=0, t=0, x="", D="", session=None):
        """ List test cases from test session
            Arguments:
            f: starts a range of test cases (-f 2)
            t: ends the range of test cases (-t 3)
            x: specifies the range of test cases (-x "3 7 8")
            D: directory where test cases are located (default is ".")
            session: test session to work with.
        """
        if session is None:
            session = self.session
        
        self.tcase("-l", f, t, x, D, session)
        
    def tcase_show(self, f=0, t=0, x="", D="", session=None):
        """ Show test cases from test session
        Arguments:
        f: starts a range of test cases (-f 2)
        t: ends the range of test cases (-t 3)
        x: specifies the range of test cases (-x "3 7 8")
        D: directory where test cases are located (default is ".")
        session: test session to work with.
        """
        if session is None:
            session = self.session
        
        self.tcase("", f, t, x, D, session)

    def tcase_enable(self, f=0, t=0, x="", D="", session=None):
        """ Disable test cases from test session
        Arguments:
        f: starts a range of test cases (-f 2)
        t: ends the range of test cases (-t 3)
        x: specifies the range of test cases (-x "3 7 8")
        D: directory where test cases are located (default is ".")
        session: test session to work with.
        """
        if session is None:
            session = self.session
        
        self.tcase("-e", f, t, x, D, session)

    def tcase_disable(self, f=0, t=0, x="", D="", session=None):
        """ Enable test cases from test session
        Arguments:
        f: starts a range of test cases (-f 2)
        t: ends the range of test cases (-t 3)
        x: specifies the range of test cases (-x "3 7 8")
        D: directory where test cases are located (default is ".")
        session: test session to work with.
        """
        if session is None:
            session = self.session
        
        self.tcase("-i", f, t, x, D, session)

    def tcase_delete(self, f=0, t=0, x="", D="", session=None):
        """ Delete test cases from test session
        Arguments:
        f: starts a range of test cases (example: 2)
        t: ends the range of test cases (example: 3)
        x: specifies the range of test cases (example: "3 7 8")
        D: directory where test cases are located (default is ".")
        session: test session to work with.
        """
        if session is None:
            session = self.session
        
        self.tcase("-i", f, t, x, D, session)

    def tcase_add(self, p="", trace=False, label="", D="", E="", DD="", EE="", session=None):
        """Add a test case to test set
        Arguments:
        label: name the test case for future use
        p:  command line parameters (-P to prompt via stdin)
        D:  directory where test cases are located (default is ".")
        E:  which executable program should be used to insert test case.
        DD: directory where executable is located (default is ".")
        trace: if True, test case will also collect trace data for the test case
        EE: which executable program should be used to collect the execution trace
        session: test session to work with.
        """
        if session is None:
            session = self.session
        
        arguments = ""
        if trace:
            arguments += " -trace "

        if len(label) > 0:
            arguments += " -label " + label

        if len(p) > 0:
            if p == "-P":
                # command line parameters passed via stdin
                arguments += " -P"
            else:
                # command line parameters passed as string
                arguments += " -p " + p

        if len(D) > 0:
            arguments += " -D " + D

        if len(DD) > 0:
            arguments += " -DD " + DD

        if len(EE) > 0:
            arguments += " -EE " + EE

        if len(E) > 0:
            arguments += " -E " + E
            self.exec_command("tcase -add" + arguments, session)
        else:
            # if E is not passed, uses the session information
            self.exec_command("tcase-add" + arguments, session)

    def exemuta(self, command, trace=False, dual=False, D="", Q=0, f=0, t=0, T=0, v="", seed=0, session=None):
        """Execute an 'exemuta' command, according to what is passed.
        Arguments:
        command: command main argument, could be '-exec', '-compile', '-update', etc.
        trace: if True, will use the execution trace to avoid execute mutants that are not reached for each test case
        dual:  execute in dual mutation mode, a dual mutant M is killed by a test case t iff t reaches the mutation
               point of M and M produces the same result as the original program (Delamaro, 2004).
        D: directory where test cases and program files are located (default is ".")
        Q: which executable program should be used to insert test case.
        f: starts a range of mutants to be executed
        t: ends the range of mutants to be executed
        T: How many times the execution time of a mutant should exceed the execution time of the original program time
           to be considered dead.
        v: A character to use in verbose mode. When this parameter is passed, the verbose mode will be turned on and the
           character passed will be printed every time a mutant execution ends.
        seed: Ramdomly shuffles the order test cases must be executed using this parameter as the ramdom seed.
              If 0 is passed, test cases will executed ordered by their numbers.
        session: test session to work with.
        """
        if session is None:
            session = self.session
        
        arguments = ""
        if trace:
            arguments += " -trace"
        if dual:
            arguments += " -dual"
        if len(D) > 0:
            arguments += " -D " + D
        if Q > 0:
            arguments += " -Q " + str(Q)
        if f > 0:
            arguments += " -f " + str(f)
        if t > 0:
            arguments += " -t " + str(t)
        if T > 0:
            arguments += " -T " + str(T)
        if len(v) > 0:
            arguments += " -v " + v

        self.exec_command( ("exemuta %s%s" % (command, arguments)), session)

    def exemuta_exec(self, trace=True, dual=False, D="", Q=0, f=0, t=0, T=0, v="", seed=0, session=None):
        """ Execute mutants and modifies status of each mutant executed to reflect its condition of live or dead.
            Arguments:
            trace: if True, will use the execution trace to avoid execute mutants that are not reached for each test case
            dual:  execute in dual mutation mode, a dual mutant M is killed by a test case t iff t reaches the mutation
                   point of M and M produces the same result as the original program (Delamaro, 2004).
            D: directory where test cases and program files are located (default is ".")
            Q: which executable program should be used to insert test case.
            f: starts a range of mutants to be executed
            t: ends the range of mutants to be executed
            T: How many times the execution time of a mutant should exceed the execution time of the original program time
               to be considered dead.
            v: A character to use in verbose mode. When this parameter is passed, the verbose mode will be turned on and the
               character passed will be printed every time a mutant execution ends.
            seed: Ramdomly shuffles the order test cases must be executed using this parameter as the ramdom seed.
                  If 0 is passed, test cases will executed ordered by their numbers.
            session: test session to work with.
        """
        if session is None:
            session = self.session

        self.exemuta('-exec', trace, dual, D, Q, f, t, T, v, seed, session)

    def exemuta_compile(self, D="", Q=0, f=0, t=0, session=None):
        """ Create and compile mutants but not execute them.
            Arguments:
            D: directory where test cases and program files are located (default is ".")
            Q: which executable program should be used to insert test case.
            f: starts a range of mutants to be executed
            t: ends the range of mutants to be executed
            session: test session to work with.
        """
        if session is None:
            session = self.session

        self.exemuta('-compile', False, False, D, Q, f, t, 0, "", 0, session)

    def exemuta_update(self, dual=False, D="", Q=0, f=0, t=0, session=None):
        """ Update the counts of live/dead/equivalent mutants.
            Arguments:
            dual:  execute in dual mutation mode, a dual mutant M is killed by a test case t iff t reaches the mutation
                   point of M and M produces the same result as the original program (Delamaro, 2004).
            D: directory where test cases and program files are located (default is ".")
            Q: which executable program should be used to insert test case.
            f: starts a range of mutants to be executed
            t: ends the range of mutants to be executed
            session: test session to work with.
        """
        if session is None:
            session = self.session

        self.exemuta('-update', False, dual, D, Q, f, t, 0, "", 0, session)

    def exemuta_select(self, operators, is_global=False, k=False, D="", O="", DD="", f=0, t=0, x="", seed=0, session=None):
        """ Select a subset of mutants to work with.
            Selected mutants become actives and all others become inactive.
            Arguments:
            operators
            global: if True, determines that selection is not don for each mentioned operator, 
                    but among the complete set of mutants. Example:
                    > exemuta -select -global 0.1 myprog
                    selects 10% among all generated mutants.
            k: if True, the selection is applied only on active mutants. Example:
                > exemuta -select -all 0.5 myprog
                > exemuta -select -all 0.5 -k myprog
                will select 25% of mutants from all operators.

            D: directory where test cases and program files are located (default is ".")
            O: file in which the list of all operators and their respective percentage is stored.
            DD: when -O is used, this argument specifies in which directory operators file is stored (default is ".")
            f: starts a range of mutants (example: 2)
            t: ends the range of mutants (example: 3)
            x: specifies the range of mutants (example: "3 7 8")
            seed: with this parameter, different samplings of mutants are selected ramdomly.
            session: test session to work with.
        """
        if session is None:
            session = self.session

        args = ""
        if len(DD) > 0:
            args += ' -DD ' + DD
        if len(O) > 0:
            args += ' -O ' + O
        if is_global:
            args += " -global"
        if k:
            args += " -k"

        args += " ".join("%s %s" % (op['filter'], op['percent']) for op in operators)

        self.exemuta(command="-select %s" % args, D=D, f=f, t=t, x=x, seed=seed, session=session)

    def exemuta_invert(self, session=None):
        """ Invert the selection of mutants.
            Active mutants become inactives and inactives mutants become active.
            Argument:
            session: test session to work with.
        """
        if session is None:
            session = self.session

        self.exemuta("-invert", session)


    def report(self, trace=False, D="", S="", L="", session=None):
        if session is None:
            session = self.session

        if trace:
            arguments = '-trace'
        else:
            arguments = '-tcase'
        if len(D) > 0:
            arguments += ' -D ' + D
        if len(S) > 0:
            arguments += ' -S ' + S
        if len(L) > 0:
            arguments += ' -L ' + L

        self.exec_command("report %s" % arguments, session)
        return ProteumReport(os.path.join(D, session + '.lst'))