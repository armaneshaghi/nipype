import subprocess
from ..base import (CommandLine, CommandLineInputSpec, traits,
                    isdefined)

from ... import logging
logger = logging.getLogger('interface')

nmr_arman_home='/home/arman'
cs_arman_home='/home/aeshaghi'
nmr_ip = 193
cs_ip = 128

def find_arman_home():
        p = subprocess.Popen(['curl', '-s', 'icanhazip.com'], stdout=subprocess.PIPE, 
                                                       stderr=subprocess.PIPE)
        out, err = p.communicate()
        #computer science ips start with 128 and NMR with 193
        if out:
                first_three_digits_of_ip = out.split('.')[0]
                if int(first_three_digits_of_ip) == nmr_ip:
                        environment = 'NMR'
                else:
                        environment = 'CS'
        if environment == 'CS':
                arman_home = cs_arman_home
        else:
                arman_home = nmr_arman_home

        return arman_home


class NMRCommandInputSpec(CommandLineInputSpec):
    """Base Input Specification for all customised NMR Commands
    """

    arman_home = traits.String(find_arman_home(), usedefault = True,
                    nohash = True,
                    desc = "arman's home depending on the environment where the nipype is running")
    pythonPath = "{arman_home}/anaconda/envs/development/bin/python".format(arman_home = arman_home)

class NMRCommand(CommandLine):
    """Base class for NMR interfaces
    """
    input_spec = NMRCommandInputSpec

    def __init__(self, **inputs):
        super(NMRCommand, self).__init__(**inputs)

        if not isdefined(self.inputs.arman_home):
                arman_home = find_arman_home()
