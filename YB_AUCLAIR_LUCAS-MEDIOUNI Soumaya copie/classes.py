import re
from time import time
from copy import deepcopy
import networkx as nx
from collections import deque
import os


class RegistreManager:
    def __init__(self) -> None:
        # Initialize the input, main, and output registers as empty lists
        self.lr_input = []
        self.lr_main = []
        self.lr_output = []

    def __extend(self, lr:list, x:int):
        # Extend the list 'lr' to have (x+1) elements, filling any gaps with 0
        while len(lr) < x+1:
            lr.append(0)

    def __in_lr(self, lr:list, x:int) -> bool:
        # Check if the list 'lr' has an element at index 'x'
        try:
            lr[x]
            return True
        except:
            return False

    def __select_lr(self, r):
        # Select the appropriate list of registers based on the input 'r'
        match r:
            case 'I':
                return self.lr_input
            case 'R':
                return self.lr_main
            case 'O':
                return self.lr_output

    def __getset(self,rX):
        # Helper function to get or set the value of a register
        args = rX.split("@")
        match len(args):
            case 2:
                # If there is only one argument, assume it is a register index
                # Otherwise, assume it is a string in the format 'R@index'
                r, x = self.__select_lr(args[0]), self.get_registre(args[1])
            case 1:
                r, x = self.__select_lr(args[0][0]), int(args[0][1:])
        if self.__in_lr(r,x) is False:
            # If the index is out of bounds, extend the list with 0s
            self.__extend(r,x)
        return r,x

    def get_registre(self, rX:str)->int:
        # Get the value of a register
        r,x = self.__getset(rX)
        return r[x]

    def set_registre(self, rX:str, value:int):
        # Set the value of a register
        r,x = self.__getset(rX)
        r[x] = value

    def __repr__(self) -> str:
        # String representation of the registers
        output = "\nREGISTRES:\INPUT\n"
        for i, content in enumerate(self.lr_input):
            output += f"| I{i}={content} "
        output += "\nMAIN\n"
        for i, content in enumerate(self.lr_main):
            output += f"| R{i}={content} "
        output += "\nOUTPUT\n"
        for i, content in enumerate(self.lr_output):
            output += f"| O{i}={content} "
        return output+"\n"+50*"*"

class MachineUniverselle:
    def __init__(self) -> None:
        # Initialize the registers and tasks lists, and the position counter
        self.registres = RegistreManager()
        self.tasks = []
        self.pos = 0
    
    def load_input(self, data:list):
        # Load input data into the input registers
        data = [len(data)] + data
        print("Machine Universel : Start of Input Loading")
        t0 = time()
        for i, v in enumerate(data):
            self.registres.set_registre(f"I{i}", v)
        print(f"Machine Universel : Input Loaded in {round((time()-t0)*1000,1)}ms")
    
    def get_config(self)-> tuple:
        # Get the current configuration of the machine
        return (self.pos, deepcopy(self.registres))
    
    def set_config(self, new_pos, new_registres:RegistreManager):
        # Set the current configuration of the machine
        self.pos = new_pos
        self.registres = new_registres
    
    def next(self):
        # Execute the next task in the tasks list
        if self.pos < len(self.tasks):
            com, args = self.tasks[self.pos]
            self.pos = com(args)
            return True
        else:
            print("Machine Universel : End of program")
            return False

    def __get_value(self, arg) -> int:
        # Helper function to get the value of an argument
        if isinstance(arg, str):
            arg = self.registres.get_registre(arg)
        return arg
    
    def __ADD(self, args):
        # ADD instruction
        self.registres.set_registre(args[2], self.__get_value(args[0]) + self.__get_value(args[1]))
        return 1

    def __SUB(self, args):
        # SUB instruction
        self.registres.set_registre(args[2], self.__get_value(args[0]) - self.__get_value(args[1]))
        return 1

    def __MULT(self, args):
        # MULT instruction
        self.registres.set_registre(args[2], self.__get_value(args[0]) * self.__get_value(args[1]))
        return 1

    def __DIV(self, args):
        # DIV instruction
        self.registres.set_registre(args[2], self.__get_value(args[0]) // self.__get_value(args[1]))
        return 1

    def __MOD(self, args):
        # MOD instruction
        self.registres.set_registre(args[2], self.__get_value(args[0]) % self.__get_value(args[1]))
        return 1
    
    def __JUMP(self, args):
        # JUMP instruction
        return args[0]
    
    def __JE(self, args):
        # JE instruction
        return args[2] if self.__get_value(args[0]) == self.__get_value(args[1]) else 1
    
    def __JLT(self, args):
        # JLT instruction
        return args[2] if self.__get_value(args[0]) < self.__get_value(args[1]) else 1
    
    def __JGT(self, args):
        # JGT instruction
        return args[2] if self.__get_value(args[0]) > self.__get_value(args[1]) else 1
    
    def start(self):
        # Start the machine
        number_of_tasks = len(self.tasks)
        print("Machine Universel : Start of program")
        t0 = time()
        while self.pos < number_of_tasks:
            com, args = self.tasks[self.pos]
            self.pos += com(args)
        print(f"Machine Universel : Program finished in {round((time()-t0)*1000,1)}ms")
        print(self.registres)

    def build(self, path_of_ram_machine:str="example.ram"):
        """Build RAM Machine from .ram file"""
        print("Machine Universel : Build Started")
        t0 = time()
        self.path = path_of_ram_machine
        command_finder = re.compile(r'[A-Z][A-Z]+')
        parenthese_finder = re.compile(r'\(|\)')
        integer_finder = re.compile(r'^[0-9]+$|^-[0-9]+$')
        with open(path_of_ram_machine,"r") as f:
            nodes = dict()
            while (line:=f.readline()) != "":
                line = line.replace('\n','')
                x,y = command_finder.search(line).span()
                args = parenthese_finder.sub('',line[y:]).split(',')
                for i in range(len(args)):
                    if integer_finder.fullmatch(args[i]):
                        args[i] = int(args[i])
                command = line[x:y]
                noeud = len(self.tasks)
                match command:
                    case 'ADD':
                        command = self.__ADD
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-ADD",[(noeud+1).__repr__()])
                    case 'SUB':
                        command = self.__SUB
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-SUB",[(noeud+1).__repr__()])
                    case 'MULT':
                        command = self.__MULT
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-MULT",[(noeud+1).__repr__()])
                    case 'DIV':
                        command = self.__DIV
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-DIV",[(noeud+1).__repr__()])
                    case 'MOD':
                        command = self.__MOD
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-MOD",[(noeud+1).__repr__()])
                    case 'JUMP':
                        command = self.__JUMP
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-JUMP",[(noeud+args[0]).__repr__()])
                    case 'JE':
                        command = self.__JE
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-JE",[(noeud+1).__repr__(), (noeud+args[2]).__repr__()])
                    case 'JLT':
                        command = self.__JLT
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-JLT",[(noeud+1).__repr__(), (noeud+args[2]).__repr__()])
                    case 'JGT':
                        command = self.__JGT
                        nodes[noeud.__repr__()] = (f"{noeud.__repr__()}-JGT",[(noeud+1).__repr__(), (noeud+args[2]).__repr__()])
                task = (command, args)
                self.tasks.append(task)
        self.nodes = nodes
        print(f"Machine Universel : Build finished in {round((time()-t0)*1000,1)}ms")


class RAMGraphBuilder:
    """Builds a directed graph from a RAM machine code file and provides methods to manipulate the graph."""

    def __init__(self):
        pass

    def create_ram_graph(self, code):
        """Creates a directed graph from a RAM machine code file."""
        graph = nx.DiGraph()
        command_finder = re.compile(r'[A-Z][A-Z]+')
        parenthese_finder = re.compile(r'\(|\)')
        integer_finder = re.compile(r'^[0-9]+$|^-[0-9]+$')
        prev_command_param = 0

        with open(code, "r") as f:
            nodes = dict()
            line_number = 0
            prev_node = None
            for line in f:
                line = line.strip()
                x, y = command_finder.search(line).span()
                args = parenthese_finder.sub('', line[y:]).split(',')
                for i in range(len(args)):
                    if integer_finder.fullmatch(args[i]):
                        args[i] = int(args[i])
                command = line[x:y]
                node_id = line_number

                # Add node for the current instruction
                graph.add_node(node_id, command=command, args=args)

                # Connect nodes based on instruction type
                if prev_node is not None:
                    if command in ['ADD', 'SUB', 'MULT', 'DIV', 'MOD', 'JUMP']:
                        if prev_command_param == 1 or prev_command_param == 0:
                            graph.add_edge(prev_node, node_id)
                            prev_command_param = 0
                            if command == 'JUMP':
                                target_node_id = line_number + args[0]
                                graph.add_edge(node_id, target_node_id)
                                prev_command_param += int(args[0])
                        else:
                            prev_command_param = 0
                    elif command in ['JE', 'JLT', 'JGT']:
                        target_node_id = line_number + args[-1]
                        graph.add_edge(prev_node, node_id)
                        graph.add_edge(node_id, target_node_id)

                # Update the previous node
                prev_node = node_id
                line_number += 1

        return graph, nodes

    # inspirations from BFS algorithm
    def delete_unreachable_nodes(self, graph, ram_file):
        """Deletes unreachable nodes from the graph and writes a new RAM file without the deleted nodes."""
        if len(graph) == 0:
            return False  # No deletions were made

        reachable_nodes = set()
        visited = set()
        queue = deque([next(iter(graph))])  # Start BFS from the first node

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                reachable_nodes.add(node)
                queue.extend(graph.neighbors(node))

        # Remove nodes not in reachable_nodes
        nodes_to_remove = [n for n in graph.nodes() if n not in reachable_nodes]
        # Keep track of the edges to remove
        edges_to_remove = [(n1, n2) for n1, n2 in graph.edges() if n1 in nodes_to_remove or n2 in nodes_to_remove]
        graph.remove_nodes_from(nodes_to_remove)
        # Remove edges connected to removed nodes
        graph.remove_edges_from(edges_to_remove)

        # Rewrite RAM file without the deleted lines
        if nodes_to_remove:
            modified_ram_file = "modified_" + os.path.basename(ram_file)
            with open(ram_file, "r") as f:
                lines = f.readlines()

            # Rewrite the RAM file excluding the lines corresponding to the deleted nodes
            with open(modified_ram_file, "w") as f:
                for i, line in enumerate(lines):
                    if i not in nodes_to_remove:
                        f.write(line)

            print(f"Deleted {len(nodes_to_remove)} unreachable nodes from the graph. New RAM file created: {modified_ram_file}")
            return modified_ram_file  # Return the modified RAM file name
        else:
            print("No unreachable nodes found in the graph. No deletions were made. No new RAM file was created.")
            return False  # No deletions were made

    def combine_instructions(self, graph, ram_file):
        """Combines consecutive instructions with the same command and register in the RAM file."""
        combined_instructions = []
        prev_instruction = None  # Track the previous instruction

        for node in graph.nodes():
            command = graph.nodes[node]['command']
            args = graph.nodes[node]['args']

            if command not in ['JUMP', 'JE', 'JLT', 'JGT']:
                if prev_instruction and prev_instruction[0] == command and prev_instruction[1][2] == args[2]:
                    # Combine consecutive instructions with the same command and register
                    combined_args = [prev_instruction[1][0] + args[0], args[1], args[2]]
                    combined_instructions.pop()  # Remove the previous instruction from the list
                    combined_instructions.append((command, combined_args))
                else:
                    # Keep the current instruction as it is
                    combined_instructions.append((command, args))
            else:
                # Keep jump instructions as they are
                combined_instructions.append((command, args))

            prev_instruction = (command, args)  # Update the previous instruction

        # Write the new RAM file with combined instructions
        new_ram_file = "combined_" + os.path.basename(ram_file)
        with open(ram_file, "r") as f:
            lines = f.readlines()

        with open(new_ram_file, "w") as f:
            for command, args in combined_instructions:
                args_str = ','.join(map(str, args))
                f.write(f"{command}({args_str})\n")

        print(f"Combined instructions and wrote new RAM file: {new_ram_file}")
        return new_ram_file  # Return the new RAM file name


if __name__ == "__main__":
    print("classes.py : Nothing to run from here.")