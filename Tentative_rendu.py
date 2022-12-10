from Bio import SeqIO # Permet l'import de la fonction parse
from Bio.Seq import Seq # Permet la transformation en complémentaire inverse
from Bio.SeqIO.QualityIO import FastqGeneralIterator # Permet un parse plus rapide lorsque beaucoup de séquences (fastaq uniquement sinon voir site biopython pour fasta)
import functools as ft # Permet de regrouper des listes pour radix sort
from collections import Counter # Demander à Erwan
import numpy as np

from tqdm import tqdm # Permet d'estimer le temps d'éxécution sur un boucle
from datetime import datetime # Permet de comparer la vitesse de 2 programmes 
#%load_ext snakeviz # temps de calcul

def import_DC3(filename) :
    """
    Fonction qui importe depuis un fichier texte la table des suffixes du génome par DC3 et la stocke dans une liste
    """
    filename = "DC3_save/" + filename
    with open(filename, 'r') as f:
        text = f.readline()
        data = text.split(" ")[:-1]
        for i in range(len(data)) :
            data[i] = int(data[i])
        return(data)

def genome_import() :
    """
    Fonction qui importe depuis un fichier fasta la séquence du génome dans une liste contenant ["seq", "n°k"]
    """
    list_genom=[]
    for record in SeqIO.parse("GCF_000002765.5_GCA_000002765_genomic.fna","fasta"):
        list_genom.append([str(record.seq).upper(),record.description[-14:]]) # attention le marquage est à changer pour la dernière séquence
    
    return list_genom
    
def reads_import_cuts(k) :
    """
    Fonction qui importe depuis un fichier fasta les séquences des reads et les coupes en les rangeant
    dans une liste contenant ["seq", "nom", "n°kmer"]
    
    Entrée : k, int : longueur du kmer
    
    Sortie : list_reads : liste de tous les read découpés en kmers
    """
    list_reads=[]
    with open("single_Pfal_dat.fq") as in_handle:
        for title, seq, qual in tqdm(FastqGeneralIterator(in_handle), desc = "Import sequence"):
            i = 1    # Incrémenteur du nombre de k-mer
            while len(seq) >= 1 : # On parcoure toute la séquence
                if len(seq) > k : # Cas où le k-mer est entier
                    list_reads.append([str(seq[0:k]).upper(),title, i])
                    i += 1
                    seq = seq[k:]
                else : # Cas où le dernier k-mer n'est pas entier
                    list_reads.append([str(seq).upper(),title, i])
                    seq = ""
            
    return list_reads
def flatten(arr):
    """
    Nécessaire pour le radix sort, je te le laisse Erwan
    """
    return ft.reduce(lambda x, y: x + y, arr)

def counting_sort(array,digit,p): 
    """
    Nécessaire pour le radix sort, je te le laisse Erwan
    """
    ##The counting sort is a stable sort used in the radic sort
    ##here the counting sort needs to be adapted to look at only one digit of each number (for radix)
    ##we also added the parameter p to be able to read the triplets (more info below)
    ##1) since we only sort single digits, the max will always be smaller than 10
    ##2) create count index (that will have the cumulative index in the end)
    count_list = [[]for i in range(10)]
    for tpl in array :
        n_uplet = tpl[0]##we take the first element of the tuple, the n-uplet
        num = n_uplet[p] // digit ##we cut off the digits to the right by getting the quotient of the euclidian division
        ##p is the index of the number studied in the triplet
        count_list[num%10].append(tpl)##we cut off the digits to the left by getting the remainder of the euclidian division
    arr_ord = flatten(count_list)

    for i in range(len(array)):##we change the base array to allow the radix sort to loop easily
        array[i] = arr_ord[i]
        
def radix_sort(array,p):
    """
    Prend en entrée un tableau de valeur de valeur et le trie en foncion de la première composante
    selon l'algorithm du radix sort
    
    Entrée : array à trier
             p : nombre de cases à trier p-uplets
    
    Sortie : array trié
    """
    ##Here the radix sort is modified to work with the triplet list sent by the DC3
    ##The code is not flexible enough to compute all characters in the ascii table, but it's enough for the use needed
    ##1) we search for the max in the nuplets
    mx = (max(array)[0])[0]+1
    if p != 3 : ##we take max = 100 because A T C G are all below 100 in ascii code
        for tpl in array:
            n_uplet = tpl[0]
            if n_uplet[-1] > mx :
                mx = n_uplet[-1]+1
    '''##2) to know how many loops we have to do, we will use a variable to represent,
    the digit we are currently in'''
    for i in reversed(range(0,p)):
        digit = 1 ##starts at one for units
        while mx - digit > 0 :##when all the digits are checked, digit will be greater than the maximum
            counting_sort(array,digit,i)
            digit *= 10 ##digit will go to the tens, the hundreds, the thousands...
            
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
    
    DC3_table = np.zeros((3,len(S) + 3), dtype=int) # Les caractères sentinelles sont déja là !
    """
    Table de DC3 qui contient en chaque ligne : 
    Ligne 0 : indice du caractère
    Ligne 1 : conversion du caractère en nombre
    Ligne 2 : Ordre de l'indice du caractère
    
    """

    for i in range(len(S) + 3) :
            DC3_table[0][i] =  i # On remplace le caractère par son code Ascii
    
    # String conversion : !!!!! à n'executer que lors de la première récursion !!!!!
    if type(S) == str :
        S_l = [*S] # On sépare caractère par caractère : "ATGC" devient ["A","T","G","C"]
        for i in range(len(S_l)) :
            DC3_table[1][i] =  ord(S_l[i]) # On rempli le caractère par son code Ascii dans la table
    else :
         for i in range(len(S)) :
            DC3_table[1][i] =  S[i] # Cas où l'on rentre dans la boucle une deuxième fois ou plus, pas de conversion
    """
    # Cas où la chaine n'est composé que d'une seule lettre : trivial car DC3 = ordre des indices en décroissant
    equal = True
    for i in range(len(S)) :
        if DC3_table[1][0] != DC3_table[1][i] :
            equal = False
            break # On teste si la chaine n'est composé que d'une seule lettre
    if equal == True :
         return [*range(len(S)-1,-1,-1)]
    """
    
    # On crée P0, P1, P2 et P1+P2 :    
    P0 = [*range(0,len(S)+1,3)] 
    P1 = [*range(1,len(S)+1,3)]
    P2 = [*range(2,len(S)+1,3)]
    
    P_12 = P1 + P2
    

    #Obtention des triplets à partir de P1+P2 :
    R_12 = []
    for val in P_12 :
        R_12.append([list(DC3_table[1][val:val+3]), val])
    
    radix_sort(R_12,3) # On trie les triplets

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

    if recur == True :
        new_S = [] # On crée T' la séquence des orders suivant l'ordre de P12
        for l in P_12 :
            new_S.append(DC3_table[2][l])
        index_012 = DC3(new_S, P_12) # On doit récupérer ces deux paramètres sinon ça marche pas
        index_12 = []
        for ind,val in index_012 :
            DC3_table[2][ind] = val
            index_12.append(ind)
    
    R_0 = [] # On crée la dernière partie à trier
    for val in P0 :
        R_0.append([[int(DC3_table[1][val]), DC3_table[2][val + 1]], val]) # On crée R0 avec son indice
    
    
    radix_sort(R_0,2)
    
    index_0 = [] # Liste des indexes de R0 trié
    for k in range(len(R_0)) : # On parcours tous les doublets triés
       index_0.append(R_0[k][1]) # On récupère l'indice
    
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

    if int(DC3_table[1][index_012[0]]) == 0 : # On enlève le terme sentinel s'il est présent
        index_012 = index_012[1:]

    if len(P_12_base) > 0 : # Mapping sur recursion -1 si existe
        new_index_012 = []
        for n in range(len(index_012)) :
            new_index_012.append([P_12_base[index_012[n]], n])
        index_012 = new_index_012
   

    return index_012 # Retourne le suffix array si dernière récursion

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
    return(bwt)

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
                e = prev + idx ##car l'index commence à 1 et non 0
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
                f = prev + idx ##car l'index commence à 1 et non 0
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

            e = prev + idx
            i -= 1
        idx = index[e]
        start_string = e
        end_string = e
    if i < 1 :
        pattern_in_S = True
    return pattern_in_S,start_string,end_string

def string_location(text,string,matches,suffix_table):
    '''
    Gives the position of each occurence of the substring in the text

    Args :
        text (string) : the text to search in
        string (string) : the substring to be searched

    Return :
        ???
    '''
    result = matches
    #print(result[1],result[2])
    sft = suffix_table
    list_occur = []
    if result[0] == False :
        #print("No occurence of the substring was found")
        list_occur.append(-1)
    else :
        for i in range(result[1],(result[2]+1)):
            ##print(text[sft[i-1]-1],"ici")
            idx = sft[i]
            list_occur.append(idx)
            #print(text[idx:idx+len(string)])
    return(list_occur)

def k_positioning(text,patt,bwt,suffix_table,index,somme):##permet d'obtenir la liste des positions
    ##recuperation des positions des premiers et derniers patterns trouvés
    mat = pattern_matching_BWT(text,patt,bwt,index,somme)
    ##recupération et renvoi des positions de tout les patterns
    return string_location(text,patt,mat,suffix_table)

def prepare_reads(data,k):
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
   
    read_pos=[]##creating a list of positions according to the read name with the position in the read
    stock_seq_name= data[0][1] #we take the first name in the list to initialize
    pres_list = []
    i = 0
    temp_pres_list = []
    for kmer_seq, seq_name, kmer_pos, pos_genom_list in tqdm(data, desc = "Liaison des kmer de séquence n°") :
        if (seq_name==stock_seq_name):
            read_pos.append(pos_genom_list)
        else :
            for j in range(len(pos_genom_list)) :
                list_for_k = [read_pos[0][j], read_pos[1][j], read_pos[2][j], read_pos[3][j],
                              read_pos[4][j], read_pos[5][j], read_pos[6][j], read_pos[7][j],
                              read_pos[8][j], read_pos[9][j]]
                #print(list_for_k)
                
                temp_pres_list.append(list(link_reads(list_for_k,k)))
            
            read_pos = [pos_genom_list]
            pres_list.append([stock_seq_name, temp_pres_list])
            stock_seq_name= data[i + 1][1]
            temp_pres_list = []
        i +=1
    
    pres_list.append([stock_seq_name, temp_pres_list])
    
    return pres_list
    
    
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
                        valid = True
                        break

    return (valid, val_pos,comment)


def export_result(result, list_genom) :
    """
    Ecrit les r�sultats obtenus du mapping pour chaque read dans un fichier texte
    """
    longueur_read = 100 #Ici on sait que c'est 100, changer en detection automatique si j'ai le temps
    with open("result.txt", 'w') as f: # On ouvre le fichier r�sultat
            f.write("Name_seq" + "\t" + "\t" + "Find ?" + "\t" + "Where : n� chromosome brin : start" + "\n") # On �crit le header
            for i in range(len(result)) :
                line = result[i][0]
                find = False
                pos = ""
                for j in range(len(result[i][1])) :
                    if result[i][1][j][0] == True :
                        find = True
                        for el in result[i][1][j][1] :
                            if j+1 > 15 :
                                if result[i][1][j][2] == "possible mutation" :
                                    pos += str(j-15+1) + " - : " + "~" + str(len(list_genom[j-15][0]) - longueur_read - el + 1 ) + "\t"
                                else :
                                    pos += str(j-15+1) + " - : " + str(len(list_genom[j-15][0]) - longueur_read - el + 1 ) + "\t"
                            else :
                                if result[i][1][j][2] == "possible mutation" :
                                    pos += str(j+1) + " + : " + "~" + str(el + 1) + "\t"
                                else :
                                    pos += str(j+1) + " + : " + str(el + 1) + "\t"
                if find == False :
                    line += "\tFalse"
                else :
                    line += "\tTrue" + "\t" + pos
                f.write(line + "\n")


now = datetime.now()

k = 10 # On défini k, la longueur de chaque kmers
by_DC3 = False # True : on calcule la DC3 depuis les données, False : on la récupère depuis le fichier de sauvegarde

list_genom = genome_import() # On récupère la séquence du génome, chaque chromose étant compartimenté dans la liste

list_reads= reads_import_cuts(k) # On récupère les reads obtenu lors du séquençage et on les découpes, chaque élément de la liste correspond à 1 kmer

# On crée le brin inverse complémentaire du génome :
list_genom_inv = []
for data in list_genom :
    genom = Seq(data[0])
    genom = genom.reverse_complement()
    list_genom_inv.append([str(genom), data[1] + " : compl inv"])

# On calcule/importe la table des suffixes pour les génomes  

if by_DC3 == True :
    # Brin sens
    for i in tqdm(range(len(list_genom)), desc = "Calcul DC3") :
        data = DC3(list_genom[i][0] + "$")
        list_genom[i].append(data)
    # Brin anti-sens
    for i in tqdm(range(len(list_genom_inv)), desc = "Calcul DC3 brin compl�mentaire inverse") :
        data = DC3(list_genom_inv[i][0] + "$")
        list_genom_inv[i].append(data)
    
else :
    # Brin sens
    for i in range(len(list_genom)) :
        filename1 = "DC3_chrom"
        filename3 = ".txt"
        filename = filename1 + str(i+1) + filename3

        list_genom[i].append(import_DC3(filename))
    # Brin anti-sens
    for i in range(len(list_genom)) :
        filename1 = "DC3_chrom"
        filename3 = ".txt"
        filename = filename1 + str(i+1) + "_inv" + filename3

        list_genom_inv[i].append(import_DC3(filename))

# On effectue le mapping et on le stocke dans une liste

full_mapping = [] # Liste totale de mapping qui regroupe tous les chromosomes
actual_mapping = [] # Liste temporaire qui accueille le mapping de chaque kmer par chromosome

for i in tqdm(range(len(list_genom)), desc = "Mapping sur chromosome brin sens") :
    bwt = BWT(list_genom[i][0] + "$",list_genom[i][2])
    ##initialisation de l'alphabet, de l'index et du compteur total de char
    L = list(bwt)
    alphabet = ['$','A','C','G','T']
    index = []
    char_index = {}
    for char in L:
        if char not in char_index: 
            char_index[char] = 0
        index.append(char_index[char])
        char_index[char] += 1
    total = Counter(list_genom[i][0] + "$")
    som = 0
    somme = []
    for char in alphabet:
        som += total[char]
        somme.append((char,som))
    for j in range(100000,200200,1) : # vrai code : len(list_reads[100000:200000])
        actual_mapping.append([list_reads[j][2], k_positioning(list_genom[i][0] + "$",list_reads[j][0], bwt,list_genom[i][2],index,somme)])
    full_mapping.append(actual_mapping)
    actual_mapping = []

# et sur le brin complémentaire :
actual_mapping = [] # Liste temporaire qui accueille le mapping de chaque kmer par chromosome
for i in tqdm(range(len(list_genom_inv)), desc = "Mapping sur chromosome brin anti-sens") :
    bwt = BWT(list_genom_inv[i][0] + "$",list_genom_inv[i][2])
    ##initialisation de l'alphabet, de l'index et du compteur total de char
    L = list(bwt)
    alphabet = ['$','A','C','G','T']
    index = []
    char_index = {}
    for char in L:
        if char not in char_index: 
            char_index[char] = 0
        index.append(char_index[char])
        char_index[char] += 1
    total = Counter(list_genom_inv[i][0] +"$")
    som = 0
    somme = []
    for char in alphabet:
        som += total[char]
        somme.append((char,som))
    for j in range(100000,200000,1) :
        actual_mapping.append([list_reads[j][2], k_positioning(list_genom_inv[i][0] + "$",list_reads[j][0], bwt,list_genom_inv[i][2],index,somme)])
    full_mapping.append(actual_mapping)
    actual_mapping = []

    
# On réorganise les données pour associer à chaque kmer sa liste de position pour tout les chromosomes et dans les deux sens
for i in range(len(full_mapping[0])) :
    list_reads[100000 + i].append([full_mapping[0][i], full_mapping[1][i], full_mapping[2][i], full_mapping[3][i], full_mapping[4][i], full_mapping[5][i],
                          full_mapping[6][i], full_mapping[7][i], full_mapping[8][i], full_mapping[9][i], full_mapping[10][i], full_mapping[11][i],
                          full_mapping[12][i], full_mapping[13][i], full_mapping[14][i], #tout les chromosomes brin sens
                          full_mapping[15][i], full_mapping[16][i], full_mapping[17][i], full_mapping[18][i], full_mapping[19][i], full_mapping[20][i],
                          full_mapping[21][i], full_mapping[22][i], full_mapping[23][i], full_mapping[24][i], full_mapping[25][i], full_mapping[26][i],
                          full_mapping[27][i], full_mapping[28][i], full_mapping[29][i]]) #tout les chromosomes brin anti-sens

# On teste la possibilité de présence de la séquenbce :
result = prepare_reads(list_reads[100000:200000], k)

export_result(result, list_genom)

time_imp = datetime.now() - now
print("Travail effectu� en", time_imp)