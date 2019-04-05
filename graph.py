from enum import Enum

class Type(Enum):
     NUM = 0
     CHAR = 1
     STRING = 2

class GP2_Atom():
    def __init__(self, num=None,ch=None,string=None):
        if(num == ch == string == None):
            raise ValueError("Invalid GP2_Atom. Requires one of positional arguments 'num', 'ch' and 'string'")
        self.num = num
        self.ch = ch
        self.string = string
        if not self.verify():
            raise ValueError("Invalid GP2_Atom.")
    
    def get_type(self):
        if(self.num != None):
            return Type.NUM
        if(self.ch != None):
            return Type.CHAR
        if(self.string != None):
            return Type.STRING
    
    def verify(self):
        if(self.num != None and type(self.num) != int):
            print("Invalid GP2_Atom. Not a valid number (num): " + str(self))
        if(self.ch != None and (type(self.ch) != str or len(self.ch) > 1)):
            print("Invalid GP2_Atom. Not a valid char (ch): " + str(self))
        if(self.string != None and type(self.string) != str):
            print("Invalid GP2_Atom. Not a valid string: " + str(self))
        if self.num == self.ch == self.string == None:
            print("Invalid GP2_Atom. All data types (num, char and string) are None: " + str(self))
            return False
        if [self.num, self.ch, self.string].count(None) < 2:
            print("Invalid GP2_Atom. Multiple data types detected: " + str(self))
            return False
        return True
    
    def __str__(self):
        string = ""
        if(self.num != None):
            string += str(self.num)
        if(self.ch != None):
            string += "'" + str(self.ch) + "'" 
        if(self.string != None):
            string += "\"" + str(self.string) + "\"" 
        return string
            
    def set_num(self, num):
        self.num = num
        self.ch = None
        self.string = None
        
    def set_ch(self, ch):
        self.ch = ch
        self.num = None
        self.string = None
    
    def set_string(self, string):
        self.string = string
        self.num = None
        self.ch = None
       
def validate_mark(mark):
    values = set(item.value for item in Mark) 
    return mark in values

class Mark(Enum):
     NONE = 0
     RED = 1
     GREEN = 2
     BLUE = 3
     GREY = 4
     DASHED = 5
     
def validate_label(label):
    for atom in label:
        if atom == None:
            print("Atom " + str(atom) + " is None.")
            return False
        if not isinstance(atom, GP2_Atom):
            print("Atom " + str(atom) + " is not GP2 Atom.")
            return False
        if not atom.verify():
            print("Atom " + str(atom) + " is valid.")
            return False
    return True

def label_string(label):
    if len(label) == 0:
        return "empty"
    try:
        string = ""
        for i in range(len(label)):
            if i != 0:
                string += ":"
            string += str(label[i])
        string += ""
        return string
    except:
        return str(label)
    
def mark_string(mark):
    if mark == Mark.NONE:
        return ""
    elif mark == Mark.RED:
        return "#red"
    elif mark == Mark.GREEN:
        return "#green"
    elif mark == Mark.BLUE:
        return "#blue"
    elif mark == Mark.GREY:
        return "#grey"
    elif mark == Mark.DASHED:
        return "#dashed"
    else:
        raise ValueError(str(mark) + " is not a valid mark.")
        
def list_to_label(ls):
    label = []
    for l in ls:
        if(type(l) == int):
            label.append(GP2_Atom(num = l))
        elif(type(l) == str):
            label.append(GP2_Atom(string=l))
        else:
            raise ValueError("Object " + str(l) + " is not a valid label.")
    return label
 
class GP2_Edge():
    def __init__(self, source, target, label=[], mark=Mark.NONE):
        if not validate_label(label):
            raise ValueError("Invalid label: " + label_string(label))
        self.label = label
        self.mark = mark
        self.source = source
        self.target = target
        if mark == Mark.GREY:
            raise ValueError("Edges cannot be marked GREY")
            
    def get_source(self):
        return self.source
    
    def get_target(self):
        return self.target
    
    def get_label(self):
        return self.label
    
    def set_label(self, new_label):
        if not validate_label(new_label):
            raise ValueError("Invalid label: " + label_string(new_label))
        self.label = new_label
    
    def get_mark(self):
        return self.mark
    
    def set_mark(self, mark):
        if not validate_mark(mark):
            raise ValueError(str(mark) + " is not a valid mark.")
        self.mark = mark
        
    def to_string(self, graph):
        return "    (" + str(graph.get_edge_index(self)) + ", " + str(graph.get_node_index(self.source)) + ", " + str(graph.get_node_index(self.target)) + ", " + label_string(self.label) + mark_string(self.mark) + ")"   

class GP2_Node():
    def __init__(self, label=[], mark=Mark.NONE, root = False):
        if not validate_label(label):
            raise ValueError("Invalid label: " + label_string(label))
        self.label = label
        self.mark = mark
        self.in_edges = []
        self.out_edges = []
        self.root = root
        if mark == Mark.DASHED:
            raise ValueError("Nodes cannot be marked DASHED.")
        
    def copy(self):
        label_copy = [item.copy() for item in self.label]
        return GP2_Node(label = label_copy, mark = self.mark, root = self.root)
    
    def add_in_edge(self, source, label=[], mark=Mark.NONE):
        e = GP2_Edge(source, self, label=label, mark=mark)
        self.in_edges.append(e)
        source.out_edges.append(e)
    
    def add_out_edge(self, target, label=[], mark=Mark.NONE):
        e = GP2_Edge(self, target, label=label, mark=mark)
        self.in_edges.append(e)
        target.in_edges.append(e)
        
    def delete_in_edge(self, edge):
        if edge not in self.in_edges:
            raise IndexError("Edge " + str(edge) + " not found.")
        self.in_edges.remove(edge)
        edge.source.out_edges.remove(edge)
        
    def delete_out_edge(self, edge):
        if edge not in self.out_edges:
            raise IndexError("Edge " + str(edge) + " not found.")
        self.out_edges.remove(edge)
        edge.target.in_edges.remove(edge)
        
    def get_label(self):
        return self.label
    
    def set_label(self, new_label):
        if not validate_label(new_label):
            raise ValueError("Invalid label: " + label_string(new_label))
        self.label = new_label
    
    def get_mark(self):
        return self.mark
    
    def set_mark(self, mark):
        if not validate_mark(mark):
            raise ValueError(str(mark) + " is not a valid mark.")
        self.mark = mark
        
    def is_root(self):
        return self.root

    def set_root(self, root):
        self.root = root
        
    def to_string(self, graph):
        root_str = ""
        if(self.is_root()):
            root_str = "(R)"
        return "    (" + str(graph.get_node_index(self)) + root_str + ", " + label_string(self.label) + mark_string(self.mark) + ")"

class GP2_Graph():
    def __init__(self):
        self.nodes= []
        
    def count_nodes(self):
        return len(self.nodes)
    
    def get_edges(self):
        edge_arr = []
        for node in self.nodes:
            edge_arr += [e for e in node.out_edges]
        return edge_arr
    
    def count_edges(self):
        return len(self.get_edges())
    
    def get_node_index(self, node):
        return self.nodes.index(node)
    
    def get_edge_index(self, edge):
        return self.get_edges().index(edge)
    
    def get_node(self, index):
        return self.nodes[index]
    
    def get_edge(self, index):
        return self.get_edges()[index]
    
    def add_node(self, node):
        if not isinstance(node, GP2_Node):
            raise ValueError(str(node) + " is not a GP2 Node.")
        self.nodes.append(node)
        
    def delete_node(self, node):
        if not node in self.nodes:
            raise IndexError("Node " + str(node) + " not found in graph node list.")
        if len(node.in_edges) > 0 or len(node.out_edges) > 0:
            raise RuntimeError("Node " + str(node) + " has incoming or outgoing edges.")
        self.nodes.remove(node)
        
    def delete_node_and_context(self, node):
        if not node in self.nodes:
            raise IndexError("Node " + str(node) + " not found in graph node list.")
        for edge in node.in_edges:
            self.delete_edge(edge)
        for edge in node.out_edges:
            self.delete_edge(edge)
        self.delete_node(node)        
    
    def add_edge(self, source, target, label=[], mark=Mark.NONE):
        if source not in self.nodes:
            raise IndexError("Source " + str(source) + " not found in graph node list.")
        if target not in self.nodes:
            raise IndexError("Target " + str(target) + " not found in graph node list.")
        target.add_in_edge(source, label, mark)
        
    def delete_edge(self, edge):
        if edge not in self.get_edges():
            raise IndexError("Edge " + str(edge) + " not found in graph edge list.")
        edge.target.delete_in_edge(edge)
        
    def to_string(self):
        string = "[\n"
        for node in self.nodes:
            string += node.to_string(self) + "\n"
        string += "    |\n"
        for edge in self.get_edges():
            string += edge.to_string(self) + "\n"
        string += "]\n"
        return string
    
    def copy(self):
        from .program import parse_graph
        return parse_graph(self.to_string())