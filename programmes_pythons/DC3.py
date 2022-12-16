import radix_DC3_tuples as rd
import numpy as np

def DC3(S, P_12_base = []) :
    """
    Create the suffix array from DC3 algorithm, could be recursive if needed
    
    Args:
        S (str): string
        P_12_base : store P1+2 from recursion to map correctly recursivity
    
    Return:
        index_012 : suffix array of S
        order_12 : order of the next recursion to map correctly recursivity
    """
    
    DC3_table = np.zeros((3,len(S) + 3), dtype=int) # On crée un tableau de taille longeur de la séquence + 3 caractères sentinelles
    """
    Table de DC3 qui contient en chaque ligne : 
    Ligne 0 : indice du caractère ( ducoup optionel si on veut )
    Ligne 1 : conversion du caractère en nombre
    Ligne 2 : Ordre de l'indice du caractère
    
    """
    for i in range(len(S) + 3) :
            DC3_table[0][i] =  i # On initialise les indices
    
    #print(DC3_table)
    
    
    # String conversion : !!!!! à n'executer que lors de la première récursion !!!!!
    if type(S) == str :
        S_l = [*S] # On sépare caractère par caractère : "ATGC" devient ["A","T","G","C"]
        for i in range(len(S_l)) :
            DC3_table[1][i] =  ord(S_l[i]) # On rempli le caractère par son code Ascii dans la table
    else :
         for i in range(len(S)) :
            DC3_table[1][i] =  S[i] # Cas où l'on rentre dans la boucle une deuxième fois ou plus, pas de conversion
    
    # Cas où la chaine n'est composé que d'une seule lettre : trivial car DC3 = ordre des indices en décroissant
    equal = True
    for i in range(len(S)) :
        if DC3_table[1][0] != DC3_table[1][i] :
            equal = False
            break # On teste si la chaine n'est composé que d'une seule lettre
    if equal == True :
         return [*range(len(S)-1,-1,-1)]
    
    
    """
    for i in range(len(S), len(S) + 3, 1) :
        conversion_l.append(0) # Ajout des 3 caractères sentinelles # A garder si pas tables de 0
    """
    
    # On crée P0, P1, P2 et P1+P2 :
    
    P0 = [*range(0,len(S)+1,3)] 
    P1 = [*range(1,len(S)+1,3)]
    P2 = [*range(2,len(S)+1,3)]
    
    P_12 = P1 + P2
    #print(P0, P1, P2)
    #print(P_12)
    
    #Obtention des triplets à partir de P1+P2 :
    
    R_12 = []
    for val in P_12 :
        R_12.append([list(DC3_table[1][val:val+3]), val])

    print(R_12)
    
    rd.radix_sort(R_12,3) # On trie les triplets
    
    print(R_12)
    
    index_12 = [] # Liste des indexes de R12 trié
    order_count = 1 # Compteur pour remplir l'ordre
    recur = False # Etat de la récursion tourné True si on a des égalités d'ordre
    for j in range(len(R_12)) : # On parcours tous les triplets triés
        index_12.append(R_12[j][1]) # ... pour lui attribuer son index depuis P_12
        DC3_table[2][R_12[j][1]] = order_count # Et on ajoute l'ordre dans la table
        if j < len(R_12)-1 :
            if R_12[j][0] != R_12[j+1][0] : # On teste l'égalité des triplets pour mettre l'ordre
                order_count += 1
            else :
                recur = True # On a égalité, donc on doit relancer l'algorithme à la fin des for
        else :
            order_count += 1
    
    #print(DC3_table, index_12)
    
    if recur == True :
        new_S = [] # On crée T' la séquence des orders suivant l'ordre de P12
        for l in P_12 :
            new_S.append(DC3_table[2][l])
        #print(new_S)
        index_012 = DC3(new_S, P_12) # On doit récupérer ces deux paramètres sinon ça marche pas
        index_12 = []
        for ind,val in index_012 :
            DC3_table[2][ind] = val
            index_12.append(ind)
            
        print(DC3_table)
    
    R_0 = [] # On crée la dernière partie à trier
    for val in P0 :
        R_0.append([[int(DC3_table[1][val]), DC3_table[2][val + 1]], val]) # On crée R0 avec son indice
        
    print(R_0)
    
    rd.radix_sort(R_0,2)
    
    print(R_0)
    
    index_0 = [] # Liste des indexes de R0 trié
    for k in range(len(R_0)) : # On parcours tous les doublets triés
       index_0.append(R_0[k][1]) # On récupère l'indice
    
    #print(DC3_table[0:2], index_0, index_12)
    
    index_012 = [] # On crée l'index final en ordonant 0 et 1,2
    i_0 = 0
    i_12 = 0
    
    index_12_dict = {}
    for i in range(len(index_12)) :
        index_12_dict[index_12[i]] = i
        
    while (i_0 < len(index_0) and i_12 < len(index_12)) : # On prends tout les éléments : on vide index 0 ou 12
        val_i0 = index_0[i_0]
        val_i12 = index_12[i_12]
        
        if DC3_table[1][val_i0] > DC3_table[1][val_i12] : # Cas où index 12 arrive avant index 0
            index_012.append(index_12[i_12])
            i_12 += 1
        elif DC3_table[1][val_i0] < DC3_table[1][val_i12] : # Cas où index 0 arrive avant index 12
            index_012.append(index_0[i_0])
            i_0 += 1
        else : # Cas d'égalité sur l'indice : si les 2 indexes renvoient le même nombre 
            if index_12[i_12] % 3 == 1 :
                if index_12_dict[val_i0 + 1] > index_12_dict[val_i12 + 1] : # Cas où index 12 au deuxième terme arrive avant index 0 au deuxième terme
                    index_012.append(index_12[i_12])
                    i_12 += 1
                else : # Cas où index 0 au deuxième terme arrive avant index 12 au deuxième terme
                    index_012.append(index_0[i_0])
                    i_0 += 1
            else :
                if DC3_table[1][val_i0 + 1] > DC3_table[1][val_i12 + 1] : # On teste dabord cas où index 12 + 1 arrive avant index 0 + 1
                    index_012.append(index_12[i_12])
                    i_12 += 1
                elif DC3_table[1][val_i0 + 1] < DC3_table[1][val_i12 + 1] : # Cas où index 0 + 1 arrive avant index 12 + 1
                    index_012.append(index_0[i_0])
                    i_0 += 1
                elif index_12_dict[val_i0 + 2] > index_12_dict[val_i12 + 2] : # Cas où index 12 au deuxième terme arrive avant index 0 au troisième terme
                    index_012.append(index_12[i_12])
                    i_12 += 1
                else : # Cas où index 0 au troisième terme arrive avant index 12 au deuxième terme
                    index_012.append(index_0[i_0])
                    i_0 += 1
    
    index_012.extend(index_12[i_12:]) # Si 1 des deux index est encore plein, on ajoute son contenu
    index_012.extend(index_0[i_0:])
    """
    while (i_0 < len(index_0) or i_12 < len(index_12)) : # On prends tout les éléments : on vide index 0 et 12
        if i_0 == len(index_0) : # Cas où index 0 est vide, on rempli avec index 12
            index_012.extend(index_12[i_12:])
            i_12 += len(index_12)
        elif i_12 == len(index_12) : # Cas où index 12 est vide, on rempli avec index 0
            index_012.extend(index_0[i_0:])
            i_0 += len(index_0)
        elif DC3_table[1][index_0[i_0]] > DC3_table[1][index_12[i_12]] : # Cas où index 12 arrive avant index 0
            index_012.append(index_12[i_12])
            i_12 += 1
        elif DC3_table[1][index_0[i_0]] < DC3_table[1][index_12[i_12]] : # Cas où index 0 arrive avant index 12
            index_012.append(index_0[i_0])
            i_0 += 1
        else : # Cas d'égalité sur l'indice : si les 2 indexes renvoient le même nombre 
            if index_12[i_12] % 3 == 1 :
                if index_12.index(index_0[i_0] + 1) > index_12.index(index_12[i_12] + 1) : # Cas où index 12 au deuxième terme arrive avant index 0 au deuxième terme
                    index_012.append(index_12[i_12])
                    i_12 += 1
                else : # Cas où index 0 au deuxième terme arrive avant index 12 au deuxième terme
                    index_012.append(index_0[i_0])
                    i_0 += 1
            else :
                if DC3_table[1][index_0[i_0] + 1] > DC3_table[1][index_12[i_12] + 1] : # On teste dabord cas où index 12 + 1 arrive avant index 0 + 1
                    index_012.append(index_12[i_12])
                    i_12 += 1
                elif DC3_table[1][index_0[i_0] + 1] < DC3_table[1][index_12[i_12] + 1] : # Cas où index 0 + 1 arrive avant index 12 + 1
                    index_012.append(index_0[i_0])
                    i_0 += 1
                elif index_12.index(index_0[i_0] + 2) > index_12.index(index_12[i_12] + 2) : # Cas où index 12 au deuxième terme arrive avant index 0 au troisième terme
                    
                    index_012.append(index_12[i_12])
                    i_12 += 1
                else : # Cas où index 0 au troisième terme arrive avant index 12 au deuxième terme
                    index_012.append(index_0[i_0])
                    i_0 += 1
    #print(index_012)
    """
    
    if int(DC3_table[1][index_012[0]]) == 0 : # On enlève le terme sentinel s'il est présent
        index_012 = index_012[1:]
        
    #print(index_012)
    
    if len(P_12_base) > 0 : # Mapping sur recursion -1 si existe
        new_index_012 = []
        for n in range(len(index_012)) :
            new_index_012.append([P_12_base[index_012[n]], n])
        #print(new_index_012)
        index_012 = new_index_012
   
    

    return index_012 # Retourne le suffix array si dernière récursion


print(DC3("abcabcacab"))
