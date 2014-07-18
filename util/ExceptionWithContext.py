import traceback
from opcode import *

import sys
import threading
import traceback
import io

last_error = threading.local()

_exc_info = sys.exc_info
def exc_info():
    result = _exc_info()
    if result[0] is not None:
        last_error.result = result
        # maybe change to weak references
        # references are a problem that can only be solved by the compiler
        # or in the byte code
    return result


def last_exc_info():
    exc_info()
    if not hasattr(last_error, 'result'):
        return None, None, None
    return last_error.result

MESSAGE_IN_BETWEEN_THE_ERRORS = 'This exception occured during the handling of the exception below:'

class ExceptionWithContext(Exception):
    __context__ = None
    __traceback__ = None
    def __init__(self, *args, **kw):
        Exception.__init__(self, *args, **kw)
        ty, err, tb = exception_context()
        self.__context__ = err
        self.__traceback__ = tb

    def __str__(self):
        try:
            base_string = Exception.__str__(self)
            if self.__context__ is None: return base_string
            file = io.StringIO()
            traceback.print_exception(type(self.__context__), self.__context__, \
                                      self.__traceback__, file = file)
            return base_string + '\n\n' + \
                   MESSAGE_IN_BETWEEN_THE_ERRORS + '\n\n' + \
                   file.getvalue()
        except:
            traceback.print_exc()

def calling_frame():
    # TODO: change this to allow more modules to take part
    import sys, _thread
    id = _thread.get_ident()
    frame = sys._current_frames()[id]
    while frame.f_globals is globals():
        if not frame.f_back:
            # so the error occured here in this module...
            return frame 
        frame = frame.f_back
    return frame

def get_opcodes(co):
    code = co.co_code
    n = len(code)
    i = 0
    result = []
    while i < n:
        c = code[i]
        op = ord(c)
        result.append( (i, opname[op]))
        i = i+1
        if op >= HAVE_ARGUMENT:
            i = i+2
    return result

def to_opcode_index(opcodes, frame_index):
    for index, opcode in enumerate(opcodes):
        if opcode[0] > frame_index:
            return index - 1
    raise Exception('This should never happen. {} {}'.format(opcodes, frame_index))


def f():
    try:pass
    except:pass
    finally:pass

opcodes = [opcode for index, opcode in get_opcodes(f.__code__)]
_opcodes = list(zip([None] + opcodes, opcodes + [None]))
assert ('SETUP_FINALLY', 'SETUP_EXCEPT') in _opcodes, """this is important for an assumption in is_in_error_handling. When try:except:finally: occur there must be two opening blocks right after each other. {}""".format(opcodes)

del f, _opcodes, opcodes
        
def exception_context():
    """=> called in the except or finally block of the last exception"""
    ty, err, tb = last_exc_info()
##    traceback.print_exception(ty, err, tb)    
    if None in (ty, err, tb):
        return None, None, None
    frame = calling_frame()
    if not tb.tb_frame is frame:
        # a reraise of an exception with another traceback occurred
        # or we got the error from somewhere
##        print ' not tb.tb_frame is frame'
        return None, None, None
    last_tb = tb
    while tb.tb_frame.f_code is frame.f_code:
##        print 'finally'
        tb = tb.tb_next # there were finallys in between
        if not tb: break
    tb = last_tb # this is still in our frame
    opcodes = get_opcodes(frame.f_code)
    tb_index = to_opcode_index(opcodes, tb.tb_lasti)
    lasti = to_opcode_index(opcodes, frame.f_lasti)
    # never use frame. or tb. from here on
    assert lasti > tb_index, (lasti, tb_index, frame.f_lasti, tb.tb_lineno)
    i = tb_index
    counted_except_ends = 0
    # assumption: dis.dis(function)
##  2           0 SETUP_FINALLY           18 (to 21)
##              3 SETUP_EXCEPT             4 (to 10)
    # find number of 'SETUP_EXCEPT', 'SETUP_FINALLY'
    op_name = lambda index: opcodes[i][1]
    while i >= 0:
        if op_name(i) in ('SETUP_EXCEPT', 'SETUP_FINALLY'):
            found_my_exception_start = counted_except_ends == 0
            if found_my_exception_start:
                break
            counted_except_ends += 1
        if op_name(i) == 'END_FINALLY':
            counted_except_ends -= 1
        i -= 1
    counted_except_ends = 0
    while i < len(opcodes):
        print(op_name(i).ljust(20), i, end=' ')
        if op_name(i) in ('SETUP_EXCEPT', 'SETUP_FINALLY'): print('+1', end=' ')
        if op_name(i) in ('END_FINALLY',): print('-1', end=' ')
        if i == tb_index: print('tb', end=' ')
        if i == lasti: print('frame', end=' ')
        if i == lasti:
            print("last!", counted_except_ends)
            if counted_except_ends > 0 :
                return ty, err, tb
            return None, None, None
        print()
        if 'END_FINALLY' == op_name(i):
            counted_except_ends -= 1
        if op_name(i) in ('SETUP_EXCEPT', 'SETUP_FINALLY'):
            counted_except_ends += 1
        if i == lasti and counted_except_ends <= 0:
            return None, None, None
##            i += 1
        i = i+1
    return None, None, None


## last but not least
sys.exc_info = exc_info


__all__ = ['exception_context', 'calling_frame', 'ExceptionWithContext', \
           'last_exc_info']


if __name__ == '__main__':
    from test_ExceptionWithContext import module_main
    module_main()