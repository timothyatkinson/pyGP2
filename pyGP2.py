import json
import os
import platform
import shutil
import subprocess
from enum import Enum
import random
from .graph_parser import make_graph_parser
import time

def is_windows():
    return (platform.win32_ver())

def verify_folder(folder_name):
    return os.path.exists(folder_name) and os.path.isdir(folder_name)

def verify_file(file_name):
    return os.path.exists(file_name) and not os.path.isdir(file_name)

class Result(Enum):
    Error = 0
    Fail = 1
    Success = 2

class config():
    def __init__(self, gp2_directory, working_directory, seeding=False):
        self.gp2_dir = gp2_directory
        self.exe_dir = gp2_directory + "/bin/gp2"
        self.run_cmd = "gp2run"
        if is_windows():
            self.exe_dir += ".exe"
            self.run_cmd += ".exe"
        self.working_dir = working_directory
        if not os.path.exists(self.working_dir):
            os.mkdir(self.working_dir)
        if not self.verify_paths():
            raise ValueError("Invalid configuration: \n" + str(self))
        self.seeding = seeding
        self.graph_parser = make_graph_parser()
        
    def __str__(self):
        return "GP2 Configuration with directory " + str(self.gp2_dir) + ", working directory " + str(self.working_dir) + "."
    
    def verify_paths(self):
        if not verify_folder(self.gp2_dir):
            print("Cannot find GP2 directory " + self.gp2_dir)
            return False
        if not verify_folder(self.working_dir):
            print("Cannot find working directory " + self.working_dir)
            return False
        if not verify_folder(self.gp2_dir + "/bin"):
            print("Cannot find bin directory " + self.gp2_dir + "/bin")
            return False
        if not verify_folder(self.gp2_dir + "/lib"):
            print("Cannot find lib directory " + self.gp2_dir + "/lib")
            return False
        if not verify_folder(self.gp2_dir + "/include"):
            print("Cannot find include directory " + self.gp2_dir + "/include")
            return False
        if not verify_file(self.exe_dir):
            print("Cannot find exe file " + self.exe_dir)
            return False
        return True
    
    def get_program_folder(self, program):
        return self.working_dir + "/tmp_pyGP2" + program.name
    
    def compile_program(self, program):
        program_folder = self.get_program_folder(program)
        if os.path.exists(program_folder):
            shutil.rmtree(program_folder)
        os.mkdir(program_folder)
        program_file = program.program_path
        if program.mode == "FROM_CODE":
            program_file = program_folder + "/program.gp2"
            f = open(program_file, "w")
            f.write(program.program_code)
            f.close()
        if not verify_file(program_file):
            raise ValueError("Program file " + program_file + " does not exist.")
        success = subprocess.call([self.exe_dir, "-l", self.gp2_dir, "-o", program_folder, program_file])
        success = subprocess.call(["make", "-C", program_folder])
        return success
    
    def write_host_graph(self, program, graph_string):
        d = self.get_program_folder(program)
        f_path = d + "/input.host"
        f = open(f_path, "w")
        f.write(graph_string)
        f.close()        
        return f_path
    
    def delete_program(self, program):
        program_folder = self.get_program_folder(program)
        if os.path.exists(program_folder):
            shutil.rmtree(program_folder)
            
    def execute(self, program, host_path):
        if not os.path.exists(host_path):
            raise RuntimeError("Host graph " + str(host_path) + " does not exist.")
        program_folder = self.get_program_folder(program)
        cmd = program_folder + "/" + self.run_cmd
        if not verify_file(cmd):
            raise RuntimeError("Executable " + str(cmd) + " does not exist.")
        if os.path.exists(program_folder + "/gp2.output"):
            os.remove(program_folder + "/gp2.output")
        if self.seeding:
            seed = random.randint(-2147483648, +2147483647)
            proc = subprocess.Popen([cmd, host_path, str(seed)], cwd=program_folder)
        else:
            proc = subprocess.Popen([cmd, host_path], cwd=program_folder)
        success = proc.wait()
        time.sleep(0.002)
        return success
    
    def get_result(self, program):
        result_path = self.get_program_folder(program) + "/gp2.output"
        if not verify_file(result_path):
            return (Result.Error, None)
        else:
            f = open(result_path, 'r')
            graph_str = f.read()
            f.close()
            self.graph_parser.node_map = {}
            return self.graph_parser.parse(input=graph_str.replace(" ", ""))
        
    
def load_configs():
    configs = []
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = dir_path + "/config.json"
    with open(config_path, "r") as read_file:
        data = json.load(read_file)
        config_arr = data["configs"]
        for conf in config_arr:
            gp2_dir = conf["gp2_directory"]
            work_dir = conf["working_directory"]
            seeding = bool(conf["seeding"])
            configs.append(config(gp2_dir, work_dir, seeding))
    return configs

pyGP2_configs_array = load_configs()
pyGP2_current_config = 0

def set_config(new_config):
    if new_config >= 0 and new_config < len(pyGP2_configs_array):
        pyGP2_current_config = new_config
    else:
        raise ValueError("Invalid new GP2 configuration " + str(new_config) + ". There are " + str(len(pyGP2_configs_array)) + " configurations available.")
    return pyGP2_current_config 

set_config(0)

def get_current_config():
    return pyGP2_current_config

def get_config(index):
    return pyGP2_configs_array[index]

def get_num_configs(index):
    return len(pyGP2_configs_array)