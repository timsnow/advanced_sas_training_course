#!/opt/anaconda3/bin/python
'''
Created on Jun 03, 2021

@author: Nathan Cowieson
@email: nathan.cowieson@diamond.ac.uk
'''

import code
import logging
import sys
from optparse import OptionParser
from optparse import OptionGroup
    
class Demo(object):
    """This is a template
    
    This is a blank dummy header for copying and making into a python script

    """
    
    '''
    Constructor
    '''
    __version__ = '1.01b'
    def __init__(self, input_variable='this'):
        ###start a log file
        self.logger = logging.getLogger('Demo')
        self.logger.setLevel(logging.INFO)
        if len(self.logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(module)s: %(message)s',"[%Y-%m-%d %H:%M:%S]")
            streamhandler = logging.StreamHandler()
            streamhandler.setFormatter(formatter)
            self.logger.addHandler(streamhandler)
        self.logger.info('Starting a new Demo job')

        self.a_variable = 0
        self.input_variable = input_variable

    def set_a_variable(self, var='this'):
        '''This functions set the global variable a_variable'''
        self.logger.debug('The set_a_variable function was called')
        self.a_variable = var
        self.logger.info(f'Set a_variable to "{var}"')

    def get_a_variable(self):
        '''Return the variable a_variable'''
        self.logger.debug('The get_a_variable function was called')
        return self.a_variable

    def set_log_level(self, level=logging.INFO):
        if level in logging._levelToName.keys():
            self.logger.setLevel(level)
            self.logger.info(f'Set log level to: {logging._levelToName[level]}')
        else:
            self.logger.error(f'Could not set log level to: {level}')
            
    def DemoFunction(self):
        self.logger.info('Running the DemoFunction function')
        return True
        
if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.argv.append('-h')

    parser = OptionParser()
    required = OptionGroup(parser, "Required Arguments")
    required.add_option("-s", "--my_string", action="store", type="string", dest="a_string", help="An essential command line variable stored as a string (no default, a required argument).") #A STRING

    optional = OptionGroup(parser, "Optional Arguments")
    optional.add_option("-f", "--my_float", action="store", type="float", dest="a_float", default=1.0, help="An optional command line variable stored as a float (default 1.0)") #A FLOAT
    optional.add_option("-i", "--my_integer", action="store", type="int", dest="a_number", default=1, help="A command line variable held as an integer, (default=1)") #AN INTEGER
    optional.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose mode, set log level to debug") #A BOOLEAN


    parser.add_option_group(required)
    parser.add_option_group(optional)
    (options, args) = parser.parse_args()
    if not options.a_string:
        sys.exit('Useage: Template.py -s mystring')

    job = Demo(options.a_string)
    
    code.interact(local=locals()) #FOR DEBUGGING, break into script at this point and enter interactive console

    if options.verbose:
        job.set_log_level(logging.DEBUG)

    job.set_a_variable(options.a_float)
        
    job.DemoFunction()

    job.logger.info('Finished normally')

