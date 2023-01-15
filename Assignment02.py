from pathlib import Path
import argparse
import re
import sys
import os

class Sequence():
    dict = {}

    input_path = None
    output_path = None

    input_type = None
    output_type = None

    def __init__(self, arguments):
        if arguments.input == None and arguments.output == None: sys.exit("Must provide an input and output files!")
        if arguments.input == None: sys.exit("Must provide an input file!")
        if arguments.output == None: sys.exit("Must provide an output file!")

        self.input_path = Path(arguments.input)
        self.output_path = Path(arguments.output)

        if not self.input_path.exists(): sys.exit("Input file does not exist!")

        path_segments = str(self.output_path).split("\\")
        file_segments = path_segments[len(path_segments) - 1].split(".")
        if not self.output_path.parent.exists() or len(file_segments) == 1: self.output_path = None

        self.input_type = get_input_file_extension(self.input_path)
        self.output_type = get_output_file_extension(arguments.output)
        if self.input_type == "invalid" and self.output_type == "invalid": sys.exit("Invalid input and output files!")
        if self.input_type == "invalid": sys.exit("Invalid input file!")
        if self.output_type == "invalid": sys.exit("Invalid output file!")

    def import_data(self):
        with open(self.input_path) as open_file:
            if self.input_type == "fasta":
                dna_found = False
                species_name = ""
                dna_sequence = ""
                for line in open_file.readlines():
                    line = line.replace("\n", "")
                    if line.startswith(">"):
                        species_name = line[1:]
                        dna_found = True
                    elif line == "":
                        self.dict.update({species_name:dna_sequence})
                        dna_found = False
                        species_name = ""
                        dna_sequence = ""
                    elif dna_found: dna_sequence += line
            if self.input_type == "nexus": line_index = 7   
            if self.input_type == "phylip": line_index = 1     
            if self.input_type == "nexus" or self.input_type == "phylip":
                lines = open_file.readlines()
                while line_index < len(lines):
                    line = lines[line_index].replace("\n", "")
                    if line == ";": break
                    segmented_line = re.split(" |\t",line)
                    species_name = segmented_line[0]
                    dna_sequence = segmented_line[len(segmented_line) - 1]
                    self.dict.update({species_name:dna_sequence})
                    line_index += 1
        print(self.dict)
                    

def get_input_file_extension(input_file_dir):
    """
    Obtains the input file's type
    """
    with open(input_file_dir) as input_file:
        first_line = input_file.readline().replace("\n", "")
        if first_line.startswith(">"): return "fasta"
        if first_line.lower().startswith("#nexus"): return "nexus"
        line_args = first_line.split(" ")
        if len(line_args) == 2 and line_args[0].isdigit() and line_args[1].isdigit(): return "phylip"
        return "invalid"

def get_output_file_extension(output_file_dir):
    """
    Obtains the output file's type
    """
    output_file_array = output_file_dir.split(".")
    extension = output_file_array[len(output_file_array) - 1]
    if extension == "fasta": return "fasta"
    if extension == "nexus": return "nexus"
    if len(output_file_array) == 1:
        if extension == "phylip": return "phylip"
    else:
        if extension == "phy": return "phylip"
    return "invalid"

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file")
parser.add_argument("-o", "--output", help="Output file")
args = parser.parse_args()

sequence_holder = Sequence(args)
sequence_holder.import_data()