import ctypes
import time
import os
import platform


print(platform.system(), platform.machine())
SYSTEM = platform.system().lower()
MACHINE = platform.machine().lower()
LIBPATH = "../../../libsunvox/{}/{}/".format(SYSTEM, MACHINE)
SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

EXTENTION = ".so"
if SYSTEM == "windows":
    EXTENTION = ".dll"

LIBNAME = os.path.join(SCRIPTDIR+LIBPATH,"sunvox"+EXTENTION)
SVLIB = ctypes.CDLL(LIBNAME)
SVLIB.sv_init.restype=ctypes.c_int32
SVVER = SVLIB.sv_init(None, 44100, 2, 0)
SLOTS = -1

class Sunvoxer:
    def __init__(self, filename=None):
        global SLOTS
        SLOTS += 1
        self.slotnr = SLOTS
        success=SVLIB.sv_open_slot(self.slotnr)
        if filename:
            self.load_file(filename)
            self.set_volume()
            self.play()

    def load_file(self, filename):
        self.svfile = os.path.join(SCRIPTDIR+"/../../assets/sunvox", filename)
        self.bsvfile = self.svfile.encode('utf-8')
        success = SVLIB.sv_load(self.slotnr, ctypes.c_char_p(self.bsvfile))

    def set_volume(self, volume=256):
        SVLIB.sv_volume(self.slotnr,volume)

    def play(self):
        success = SVLIB.sv_play_from_beginning(self.slotnr)

    def stop(self):
        SVLIB.sv_stop(self.slotnr)

    def close(self):
        SVLIB.sv_close_slot(self.slotnr)

    def release(self):
        SVLIB.sv_deinit()

