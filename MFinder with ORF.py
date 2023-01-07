import sys

sequence_dict = {}
dna_Dict = {"G":"C","A":"T","C":"G","T":"A"}
startCodon = "ATG"
stopCodons = ["TGA","TAG","TAA"]
motif = ""
validMotif = False
while not validMotif:
    motif = input("Insert a motif:").upper()
    validMotif = True
    for letter in motif:
        if not letter in dna_Dict.keys():
            validMotif = False
            print("Invalid base in motif!")
            break
    if motif == "":
        validMotif = False
        print("Must specify a motif!")
    elif len(motif) < 5:
        validMotif = False
        print("Motif must be at least 5bp long!")

with open(sys.argv[1]) as fasta_sequence:
    dnaFound = False
    speciesName = ""
    dnaSequence = ""
    for line in fasta_sequence.readlines():
        line = line.replace("\n", "")
        if line.startswith(">"):
            speciesName = line[1:]
            dnaFound = True
        elif line == "":
            sequence_dict.update({speciesName:dnaSequence})
            dnaFound = False
            speciesName = ""
            dnaSequence = ""
        else :
            dnaSequence += line

motifFound = False
for key in sorted(sequence_dict):
    dna_sequence = sequence_dict.get(key)
    index = 0
    sign = "+"
    orfStart = 0
    orfEnd = 0
    while index <= len(dna_sequence) - len(motif):
        aminoAcid = dna_sequence[index:index+3]
        if orfStart == 0:
            if aminoAcid == startCodon:
                orfStart = index + 1
        else:
            if (index + 1 - orfStart) % 3 == 0 and aminoAcid in stopCodons:
                orfEnd = index + 1
        if orfStart != 0:
            if motif == dna_sequence[index:index+len(motif)]:
                motifFound = True
                position = index+1
                if sign == "-":
                    position = len(dna_sequence) - index + 1 - len(motif)
                frame = (index + 1 - orfStart) % 3 + 1
                print(f"{key}\t{len(dna_sequence)}\t{position}\t{sign}{frame}")
            if orfEnd == index + 1 or index == len(dna_sequence) - len(motif):
                orfStart = 0
                orfEnd = 0
        if index == len(dna_sequence) - len(motif) and sign == "+":
                index = 0
                sign = "-"
                dna_sequence = dna_sequence.replace("G","1").replace("A","2").replace("C","G").replace("T","A").replace("1","C").replace("2","T")[::-1]
        index += 1
if not motifFound:
    print("Motif not found!")
