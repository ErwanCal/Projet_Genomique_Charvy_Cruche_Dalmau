import DC3

def BWT(text,suffix_table):
    """
    Compute the BWT from the suffix table

    Args:
        T (str): string
        end_of_string (char): end of string character to append

    Return:
        bwt (str): BWT
    """
    bwt = ""
    sf_tab = suffix_table
    for i in range(len(sf_tab)):
        crt = sf_tab[i]
        bwt += text[crt-1]
    ###################
    # Write your code
    ###################
    return(bwt)
'''
clean
'''
def pattern_matching_BWT(S,pattern,bwt,index,somme):
    """
    Search a pattern in a String using the BWT

    Args:
        S (str): string
        pattern (str): pattern
        bwt : the bwt of the text (to not compute it each time)

    Return:
        bool: true if the pattern is in the string
        int : position of the first occurence of the pattern in the ordered text
        int : position of the last occurence of the pattern in the ordered text
    """
    pattern_in_S = False
    L = list(bwt)
    lpattern = list(pattern)
    start_string = -1
    end_string = -1
    e = 0
    f = len(L)
    ##init des valeurs utiles pour la substring search
    i = len(lpattern)-1
    X = lpattern[i]
    for tpl in somme :
        if tpl[0]<X:
            e = tpl[1]+1 ##donne place du premier char dans la liste ordonnée
        if tpl[0]==X:
            f = tpl[1]-1 ##donne place du dernier char

    while e < f and i > 0 :
        X = lpattern[i]
        Y = lpattern[i-1]
        suite_impos = True
        r = e
        s = f
        for u in range(r,s+1):
            if(suite_impos==False):##we use the boolean to exit the loop early
                break
            if(L[u]==Y):
                suite_impos= False
                prev = 0
                idx = index[u]
                for tpl in somme :
                    if tpl[0]<Y:
                        prev = tpl[1]
                e = prev + idx[1] -1 ##car l'index commence à 1 et non 0
                start_string = e

        char_found = False
        for u in reversed(range(r,s+1)):
            if(char_found or suite_impos):
                break
            if(L[u]==Y):
                char_found = True
                prev = 0
                idx = index[u]
                for tpl in somme :
                    if tpl[0]<Y:
                        prev = tpl[1]
                f = prev + idx[1] -1 ##car l'index commence à 1 et non 0
                end_string = f
        if suite_impos :## this will stop the loop if no char has been found in the previous one
            break
        i -= 1
    if suite_impos:
        i = 0
        pattern_in_S = False
        return pattern_in_S,start_string,end_string
    ##dans le cas où e = f, il faut vérifier que le reste du substring est bon
    if i > 0 :
        while i > 0 :
            if L[e] != lpattern[i-1]:
                break
            prev = 0
            id=index[e]
            start_string = e
            end_string = e
            for tpl in somme :
                if tpl[0]<L[e]:
                    prev = tpl[1]

            e = prev + id[1]
            i -= 1
    if i < 1 :
        pattern_in_S = True
    return pattern_in_S,start_string,end_string
'''
clean
'''

def string_location(text,string,matches,suffix_table):
    '''
    Gives the position of each occurence of the substring in the text

    Args :
        text (string) : the text to search in
        string (string) : the substring to be searched

    Return :
        ???
    '''
    list_occur = []
    print(suffix_table,"res")

    if matches[0] == False :
        print("No occurence of the substring was found")
        list_occur.append(-1)
    else :
        for idx in suffix_table[matches[1]:(matches[2]+1)]:
            print(idx)
            list_occur.append(idx)
            print(T[idx:idx+len(string)])
    return(list_occur)

def k_positioning(text,pattern,bwt,suffix_table):##permet d'obtenir la liste des positions
    ##initialisation de l'alphabet, de l'index et du compteur total de char
    L = list(bwt)
    alphabet = ['$','A','C','G','T']
    total = []
    index = L+[]
    for lett in alphabet:
        cntr = 0
        for i in range(len(L)):
            if L[i]==lett:
                cntr +=1
                index[i]=(lett,cntr)
        total.append((lett,cntr))##le faire en une liste somme et total
    somme = []
    som=0
    for tpl in total:
        som += tpl[1]
        somme.append((tpl[0],som))
    ##recuperation des positions des premiers et derniers patterns trouvés
    mat = pattern_matching_BWT(T,patt,bwt,index,somme)
    ##recupération et renvoi des positions de tout les patterns
    return string_location(T,patt,mat,suffix_table)

T = "TTTCCAATTAATTATCAAGTCTGTTTTCCAATACTAGCTGCATCGATCGTAAGCATCAAGTCTGTTTTGGGTTTCCAATTAATTATCAAGTTTCCAATTAATTATCAAGTCTGTTTTGGGTTTCCAATTAATTATCAAGTCTGTTTTGGGACTCTGCATCTGTTTTGGGACTCTGCATTTGGGTTTCCAATTAATTATCAAGTCTGTTTTGGGACTCTGCA"
T2 = "TTTCCAATTAATTATCAAGTCTGTTTTGGGTTTCCAATTAATTATCACCAGTCGTATTTTGGGACTCTGCACCTAATCCCCAACACTTTGTCGTAGAAACACTTTGAG"
patt = "ATCAAG"
patt5 = "AGTCGTA"
patt4 = "AGTCGT"
patt2 = "TGCACC"
text= T + '$'

sf_tab = DC3.DC3(text)
'''
for i in sf_tab[33:38]:
    print(i)
    print(T[i:i+len(patt)])
'''
print(len(T))
sft=DC3.DC3(T)
print("aaaa",sf_tab[33:38+1])
bwt = BWT(text,sf_tab)
print(sf_tab,"resdehors")
##counts = Counter(bwt)
##print(counts)
print(k_positioning(text,patt,bwt,sf_tab))


##print(BWT(T))
##le dollar permet d'eviter pattern sur fin/debut (chevauchement)
