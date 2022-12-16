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
            idx = index[e]
            start_string = e
            end_string = e
            for tpl in somme :
                if tpl[0]<L[e]:
                    prev = tpl[1]

            e = prev + idx[1] - 1
            i -= 1
        idx = index[e]
        start_string = e
        end_string = e
    if i < 1 :
        pattern_in_S = True
    return pattern_in_S,start_string,end_string
