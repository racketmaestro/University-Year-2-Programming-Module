# write a DNA database
import copy

class Dna:

    def __init__(self, seq = None, info=''):
        if seq is None:
            self.seq = []
        elif isinstance(seq, list):
            self.seq = seq
            self.info = info
        elif isinstance(seq, str):
            self.seq = list(seq)
            self.info = info

    def __add__(self, dna):
        dna_new = Dna(''.join(self.seq))

        if isinstance(dna, Dna):
            for nt in dna.seq:
                dna_new.seq.append(nt)
        elif isinstance(dna, str):
            for nt in dna:
                dna_new.seq.append(nt)
        else:
            print('data type not recognised')

        return dna_new

    def __radd__(self, dna):

        if isinstance(dna, Dna):
            dna_new = copy.deepcopy(dna)
            for nt in self.seq:
                dna_new.seq.append(nt)
        elif isinstance(dna, str):
            dna_new = Dna(dna)
            for nt in self.seq:
                dna_new.seq.append(nt)
        else:
            print('data type not recognised')

        return dna_new

    def __str__(self):
        return ''.join(self.seq)

    def __getitem__(self, key):
        dna_new = copy.deepcopy(self)
        dna_new.seq = self.seq[key]
        return dna_new

    def __eq__(self, dna):
        if isinstance(dna, Dna):
            return self.seq == dna.seq
        elif isinstance(dna, str):
            return self.seq == list(dna.seq)
        else:
            print('data type not recognised')

    def load(self, file_name):
        try:
            fin = open(file_name, 'r')
            self.seq = list()
            line = fin.readline().strip()
            if line.startswith('>'):
                self.info = line.replace('>','').strip()
                line = fin.readline().strip().upper()
                while line:
                    for ch in line:
                        self.seq.append(ch)
                    line = fin.readline().strip().upper()
            fin.close()
        except FileNotFoundError:
            self.seq = list()
            self.info = 'file was not loaded'

    def stats(self):
        table = dict()

        for nt in 'ACGTNUKSYMWRBDHV-':
            table[nt]=0
        table['other'] = 0

        for nt in self.seq:
            if nt.upper() in 'ACGTNUKSYMWRBDHV-':
                table[nt]+=1
            else:
                table['other']+=1

        return table

    def find(self, dna):
        index = []
        match = False
        if isinstance(dna, Dna):
            for i, b in enumerate(self.seq):
                for j, c in enumerate(dna):
                    if i+j < len(self.seq):
                        if self.seq[i+j] == dna[j]:
                            match = True
                        else:
                            match = False
                            break
                    else:
                        match = False
                        break
                if match == True:
                    index.append(i)

        elif isinstance(dna,str):
            for i, b in enumerate(self.seq):
                for j, c in enumerate(dna):
                    if i+j < len(self.seq):
                        if self.seq[i+j] == dna[j]:
                            match = True
                        else:
                            match = False
                            break
                    else:
                        match = False
                        break
                if match == True:
                    index.append(i)
        return index

def main():

    print('=== assignments ==')

    dna1 = Dna()
    print(dna1)

    dna1 = Dna('TTT')
    print(dna1)

    dna2 = Dna('ACTGGCTAA')
    print(dna2)

    dna3 = dna2
    print(dna3)

    print('=== concatenations ===')
    
    dna4 = dna1+dna2
    dna5 = dna1+'GGG'
    dna6 = 'CCC' + dna1

    print(dna4)
    print(dna5)
    print(dna6)

    print('=== indexing ===')
    
    print(dna6[2:6])
    for nt in dna6:
        print(nt)

    dna5 = dna2[2:6]
    print(dna5)

    print('=== loading from file ===')

    dna6 = Dna()
    dna6.load('BRCA1.fna')
    print(dna6[0:80])

    print('=== stats ===')

    print(dna6.stats())

if __name__ == '__main__':
    main()
    
