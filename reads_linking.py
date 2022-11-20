
def link_reads (l_pos_kmer,k):
    """
    Links the kmer of the reads
    Args:
        l_pos_kmer : list of tuple : (kmer, position in the genom)
        k : length of kmers
    Return:
        ?
    """

    l_pos_kmer.sort(key=lambda x: x[1]) #sort by position

    list_reads_pos=[]

    tuple_pos=0
    while ((tuple_pos+1)<len(l_pos_kmer)) : # while we have not seen each tuple of the list
        word=l_pos_kmer[tuple_pos][0] # add the kmer to the word we want to add
        pos_word=l_pos_kmer[tuple_pos][1] # take the position of the word
        next_pos=l_pos_kmer[tuple_pos][1]+k  #position of the next kmer
        tuple_pos+=1
        while (next_pos==l_pos_kmer[tuple_pos][1])  :
            word+=l_pos_kmer[tuple_pos][0]
            next_pos=l_pos_kmer[tuple_pos][1]+k
            tuple_pos+=1
            if((tuple_pos+1)==(len(l_pos_kmer))): #case in which the next element is the last longueur
                word+=l_pos_kmer[tuple_pos][0]
                break
        list_reads_pos.append((word,pos_word))
        if((tuple_pos+1)==(len(l_pos_kmer))):
            break

# un do while serait préférable ??
    return(list_reads_pos)

tab_pos=[('TT',1),('AT',13),('CC',3),('CA',15),('AA',5),('AG',17),('TT',7)]

print(link_reads(tab_pos,2))


### Attention pour l'instant je suppose que chaque kmer a la même longueur (bout de chaine à voir) et qu'il n'y a pas plusieurs kmer
## à la même position

#test
T = "TTTCCAATTAATTATCAAGTCTGTTTTGGGTTTCCAATTAATTATCACCAGTCTGTTTTGGGACTCTGCACCTAATCCCCAACACTTTGAGAAACACTTTGAG"



# reads 1 : TT CC AA TT
# reads 2 :  AT CA AG
