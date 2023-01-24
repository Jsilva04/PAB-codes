import sys

motifFound = False
while not motifFound:
    motif = ""
    validMotif = False
    while not validMotif:
        motif = input("Insert a motif:").upper()
        validMotif = True
        for letter in motif:
            if not letter in ["G","A","C","T"]:
                validMotif = False
                print("Invalid base in motif!")
                break
        if motif == "":
            validMotif = False
            print("Must specify a motif!")
        elif validMotif and len(motif) < 5:
            validMotif = False
            print("Motif must be at least 5bp long!")

    sequence_dict = {}
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
            elif dnaFound: dnaSequence += line
                
    motifFound = False
    for key in sorted(sequence_dict):
        dna_sequence = sequence_dict.get(key)
        motifCopy = motif
        index = 0
        sign = 1
        while index <= len(dna_sequence) - len(motif):
            if motifCopy == dna_sequence[index:index+len(motif)]:
                motifFound = True
                position = index + 1
                frame = index % 3 + 1 if sign > 0 else (len(dna_sequence) - index - len(motif)) % 3 + 1
                print(f"{key}\t{len(dna_sequence)}\t{position}\t{sign*frame}")
            index += 1
            if index > len(dna_sequence) - len(motif) and sign > 0:
                    index = 0
                    sign = -1
                    motifCopy = motif[::-1].replace("G","1").replace("A","2").replace("C","G").replace("T","A").replace("1","C").replace("2","T")
    if not motifFound:
        print("Motif not found!")
