import DC3

def BWT(T):
    """
    Compute the BWT from the suffix table

    Args:
        T (str): string
        end_of_string (char): end of string character to append

    Return:
        bwt (str): BWT
    """
    bwt = ""
    text= T ##+ "$"
    sf_tab = DC3.DC3(text)
    for i in range(len(sf_tab)):
        crt = sf_tab[i]
        bwt += text[crt-1]
    ###################
    # Write your code
    ###################
    return(bwt)

def pattern_matching_BWT(S,pattern):
    """
    Search a pattern in a String using the BWT

    Args:
        S (str): string
        pattern (str): pattern

    Return:
        bool: true if the pattern is in the string
    """
    S = S ##+ "$"
    pattern_in_S = False
    L = list(BWT(S))
    LS = L + []
    LS.sort()
    lpattern = list(pattern)
    ##initialisation de l'alphabet, de l'index et du compteur total de char
    alphabet = []
    for i in range(len(L)):
        if L[i] not in alphabet:
            alphabet.append(L[i])
    alphabet.sort()
    total = []
    index = L+[]
    for lett in alphabet:
        cntr = 0
        for i in range(len(L)):
            if L[i]==lett:
                cntr +=1
                index[i]=(lett,cntr)
        total.append((lett,cntr))
    somme = []
    som=0
    for tpl in total:
        som += tpl[1]
        somme.append((tpl[0],som))
    ##init des valeurs utiles pour la substring search
    e = 0
    f = len(L)
    i = len(lpattern)-1
    ##début de la boucle de recherche
    while e < f and i > 0 :
        X = lpattern[i]
        Y = lpattern[i-1]
        r = 0
        s = 0
        suite_impos = True
        for tpl in somme :
            if tpl[0]<X:
                r = tpl[1] ##donne place du premier char dans la liste ordonnée
            if tpl[0]==X:
                s = tpl[1]-1 ##donne place du dernier char
        if e>r:
            r = e
        if f<s:
            s = f
        for u in range(r,s+1):
            if L[u]==Y:
                suite_impos= False
                prev = 0
                id = index[u]
                for tpl in somme :
                    if tpl[0]<Y:
                        prev = tpl[1]
                e = prev + id[1]-1
            if(suite_impos==False):
                break
        char_found = False
        for u in reversed(range(r,s+1)):
            if L[u]==Y:
                char_found = True
                prev = 0
                id = index[u]
                for tpl in somme :
                    if tpl[0]<Y:
                        prev = tpl[1]
                f = prev + id[1]-1
            if(char_found):
                break
        if suite_impos :
            break
        i-=1
    ##dans le cas où e = f, il faut vérifier que le reste du substring est bon
    if i > 0 :
        while i > 0 :
            if L[e] != lpattern[i-1]:
                break
            prev = 0
            id=index[e]
            for tpl in somme :
                if tpl[0]<L[e]:
                    prev = tpl[1]

            e = prev + id[1]-1
            i -= 1
    if i < 1 :
        pattern_in_S = True
    if suite_impos:
        i = 0
        pattern_in_S = False
    return pattern_in_S

T = "TTTCCAATTAATTATCAAGTCTGTTTTCCAATTAATTATCAAGTCTGTTTTGGGTTTCCAATTAATTATCAAGTTTCCAATTAATTATCAAGTCTGTTTTGGGTTTCCAATTAATTATCAAGTCTGTTTTGGGACTCTGCATCTGTTTTGGGACTCTGCATTTGGGTTTCCAATTAATTATCAAGTCTGTTTTGGGACTCTGCA"
T2 = "TTTCCAATTAATTATCAAGTCTGTTTTGGGTTTCCAATTAATTATCACCAGTCTGTTTTGGGACTCTGCACCTAATCCCCAACACTTTGAGAAACACTTTGAG"
patt2 = "ATCAA"
patt1 = "TGCACC"
print(len(T))
pat = pattern_matching_BWT(T2,patt2)
print(pat)
##print(BWT(T))
##le dollar permet d'eviter pattern sur fin/debut (chevauchement)
