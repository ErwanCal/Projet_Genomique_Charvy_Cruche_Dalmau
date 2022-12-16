
from Bio import SeqIO


list_genom=[]
for record in SeqIO.parse("GCF_000002765.5_GCA_000002765_genomic.fna","fasta"):
    list_genom.append((str(record.seq).upper(),record.description[-14:])) # attention le marquage est à changer pour la dernière séquence


list_reads=[]
for record in SeqIO.parse("single_Pfal_dat.fq","fastq"):
    list_reads.append((str(record.seq).upper(),record.description))


print(list_reads[0:6])
