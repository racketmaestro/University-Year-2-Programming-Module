from dna_oop import *
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

