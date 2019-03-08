from .pyGP2 import pyGP2_configs_array, pyGP2_current_config

def parse_graph(graph_string):
    pyGP2_configs_array[pyGP2_current_config].graph_parser.node_map = {}
    return pyGP2_configs_array[pyGP2_current_config].graph_parser.parse(graph_string)

class GP2_Program():
    def __init__(self, name, program_code = None, program_path = None):
        self.name = name
        if(program_code == program_path == None):
            raise ValueError("Invalid GP2 program. Requires one of positional arguments 'program_code' or 'program_path'")
        if program_code != None:
            self.program_path = None
            self.program_code = program_code
            self.mode = "FROM_CODE"
        else:
            self.program_path = program_path
            self.program_code = None
            self.mode = "FROM_PATH"
        self.compiled = False
    
    def set_program_code(self, code):
        self.program_code = code
        self.program_path = None
        self.mode = "FROM_CODE"
    
    def set_program_path(self, path):
        self.program_path = path
        self.program_code = None
        self.mode = "FROM_PATH"
    
    def get_program_code(self):
        return self.program_code
    
    def get_program_path(self, path):
        return self.program_path
    
    def get_mode(self):
        return self.mode
    
    def is_from_code(self):
        return self.mode == "FROM_CODE"
    
    def is_from_path(self):
        return self.mode == "FROM_PATH"
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def is_compiled(self):
        return self.compiled
        
    def compile_program(self):
        pyGP2_configs_array[pyGP2_current_config].compile_program(self)
        self.compiled = True
        
    def run_on_file(self, file_path):
        if not self.compiled:
            raise RuntimeError("Attempting to run non-compiled code.")
        pyGP2_configs_array[pyGP2_current_config].execute(self, file_path)
        return pyGP2_configs_array[pyGP2_current_config].get_result(self)
    
    def run_on_local_file(self, file_path):
        import os 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return self.run_on_file(dir_path + '\\' + file_path)
        
        
    def run_on_string_graph(self, graph_string):
        f_path = pyGP2_configs_array[pyGP2_current_config].write_host_graph(self, graph_string)
        return self.run_on_file(f_path)
        
    def run_on_graph(self, graph):
        return self.run_on_string_graph(graph.to_string())
    