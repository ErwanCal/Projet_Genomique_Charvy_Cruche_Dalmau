def link_reads_new (data,k):
    """
    give_position of each read
    Args:
        data :List containing the treatment of kmer by mapping :
        (kmer_seq, seq_name, kmer_pos, pos_genom_list)
        kmer_seq : kmer,
        seq_name : read containing the kmer,
        kmer_pos : position of the kmer in the read,
        pos_genom_list : possible positions of the kmer in the genom
        k : length of kmers

    Return:
        ?
    """
    


    l_pos=[]##creating a list of positions according to the read name with the position in the read
    stock_seq_name=data[0][1] #we take the first name in the list to initialize
    for kmer_seq, seq_name, kmer_pos, pos_genom_list in data :
        if (l_seq_name==stock_seq_name):
            l_pos.append(kmer_pos, pos_genom_list)
        else :
            l_pos = []


    return(list_reads_pos)
