
def link_reads (l_pos,k):
    """
    Links the kmer of the reads
    Args:
        l_pos : list of tuple : (kmer_pos_read, kmer_pos_gen)
        kmer_pos_read : position of the kmer in the read
        kmer_pos_gen : possible position of the kmer in the genom
        k : length of kmers
    Return:

    """
    valid=False # true if there is a valid position
    val_pos=[] # list of valid starting position of the read in the genom
    comment=""
    for i in l_pos[0][1] :# for each first position,we add the next part to see if it exists
        cur_pos=1
        if(cur_pos==len(l_pos)): # if there is only one position in the list
            if (i!=-1): #if there is only a position -1 it returns False and no position
                valid=True
                val_pos.append(i)

        else :  # if there is more than 1 element iiin the list
            pos_gen=i+k # next position of the kmer of the read in the genom
            while (pos_gen in l_pos[cur_pos][1]) : # we try to find the next kmer in the next list of position of kmer
                cur_pos+=1
                if(cur_pos==len(l_pos)): # when there is the whole read in the genom
                    valid=True
                    val_pos.append(i)# to return the position of the read(s) in the genom
                    break
                else :
                    pos_gen+=k
    if(valid==False):
        for i in l_pos[0][1] :# for each first position,we look at the last kmer to see if it can correpond with the genom but with mutation between
            cur_pos=1
            if(cur_pos!=len(l_pos)):   # if there is more than 1 element in the list
                pos_gen=i+k*(len(l_pos)-1) #  position of the last kmer of the read in the genom
                if (pos_gen in l_pos[-1][1]) : # we try to find the last position in the last element of the list
                        comment+="possible mutation"
                        val_pos.append(i)# to return the position of the read(s) in the genom
                        break

    return (valid, val_pos,comment)

read=[(1,[4,9,10]),(2,[5,15,28,57]),(3,[12,15,28,57])]
read2=[(1,[-1])]
print(link_reads(read2,4))

    # attention traiter cas -1, et cas avec un seul tuple dans liste et attention position pas dans bon ordre
