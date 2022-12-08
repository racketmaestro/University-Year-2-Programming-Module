import copy
import csv

class Dna:
    
    with open('dna2protein.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        lookup = {}
        for row in reader:
            codon = row[0] + row[1] + row[2]
            amino_acid = row[4]
            new_dict_entry = {codon: amino_acid}
            lookup.update(new_dict_entry)

    
    def print_pro_seq(self):
        seq_str = ''.join(self.seq)
        codon_list = [seq_str[i:i+3] for i in range(0,int(len(seq_str)  ),3)]
        print(codon_list)
        protein_seq = []
        for i in codon_list:
            protein_seq.append(self.lookup[i])
        protein_seq = ''.join(protein_seq)
        print(protein_seq)
            
    # @property
    # def print_pro_seq(self):


    @classmethod  # takes cls as the first argument
    def update_lookup(cls, nuc_seq, amino_acid):
        if nuc_seq not in cls.lookup:
            new_entry = {nuc_seq, amino_acid}
            cls.lookup.update(new_entry)
        else: 
            cls.lookup[nuc_seq] = amino_acid   
        print(cls.lookup)                                                          

    @staticmethod  # static methods do not need creation of the instance. Bound to a class rather than the object
    def find_point_mutation(self,other):
        mismatch = [i for i in range(len(self.seq)) if self.seq[i] != other.seq[i]]
        for i in mismatch:
            print(f'point mutation at index {i}: {self.seq[i]}->{other.seq[i]}' )


    def __init__(self, seq = None, info=''):
        if seq is None:
            self.seq = []
        elif isinstance(seq, list):
            self.seq = seq
            self.info = info
        elif isinstance(seq, str):
            self.seq = list(seq)
            self.info = info
        
    def __str__(self) -> str:
        seq_str = ''.join(self.seq)
        return f"{seq_str}"

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
    

    def __getitem__(self,idx):
        new_seq = ''.join(self.seq[idx])
        return new_seq

    def load(self,file_name):
        fin = open(file_name,'r')
        self.seq = list()
        line = fin.readline().strip()
        print(line)
        if line.startswith('>'):
            self.info = line.replace('>','').strip()
            line = fin.readline().strip().upper()
            while line:
                for ch in line:
                    self.seq.append(ch)
                    
                line = fin.readline().strip().upper()
                
        fin.close()


        
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

    


# from dna_oop import *
# print('=== assignments ==')
# dna1 = Dna()
# print(dna1) # empty line
# dna1 = Dna('TTT')
# print(dna1)
# dna2 = Dna('ACTGGCTAA')
# print(dna2)
# dna3 = dna2
# print(dna3)
# print('=== concatenations ===')
# dna4 = dna1+dna2
# dna5 = dna1+'GGG'
# dna6 = 'CCC' + dna1
# print(dna4)
# print(dna5)
# print(dna6)
# print('=== indexing ===')
# print(dna6[2:6])
# for nt in dna6:
#  print(nt)
# dna5 = dna2[2:6]
# print(dna5)
# print('=== loading from file ===')
# dna6 = Dna()
# dna6.load('BRCA1.fna')
# print(dna6[0:80])
# print('=== stats ===')
# print(dna6.stats())
def main():

    dna1 = Dna()
    print(dna1)
    dna1 = Dna('TTT')
    print(dna1)
    dna2 = Dna('ACTGGCTAA')
    print(dna2)
    dna3 = Dna('ACTGGCGAA')
    print(dna3)
    print(dna2.lookup)
    dna2.print_pro_seq()
    dna1.update_lookup('TAA','T')
    dna2.print_pro_seq()
    Dna().find_point_mutation(dna2,dna3)
if __name__ == '__main__':
    main()

