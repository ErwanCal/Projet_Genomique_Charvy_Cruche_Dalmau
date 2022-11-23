import functools as ft
def flatten(arr):
    return ft.reduce(lambda x, y: x + y, arr)

def counting_sort(array,digit,p): ##The counting sort is a stable sort used in the radic sort
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
def radix_sort(array,p):##Here the radix sort is modified to work with the triplet list sent by the DC3
##The code is not flexible enough to compute all characters in the ascii table, but it's enough for the use needed
    ##1) we search for the max in the nuplets
    max = 0
    if p == 3 : ##we take max = 100 because A T C G are all below 100 in ascii code
        mx = 100
    else :
        for tpl in array:
            n_uplet = tpl[0]
            if n_uplet[-1] > mx :
                mx = n_uplet[-1]
    '''##2) to know how many loops we have to do, we will use a variable to represent,
    the digit we are currently in'''
    for i in reversed(range(0,p)):
        digit = 1 ##starts at one for units
        while mx - digit > 0 :##when all the digits are checked, digit will be greater than the maximum
            counting_sort(array,digit,i)
            digit *= 10 ##digit will go to the tens, the hundreds, the thousands...

'''import time
import listest
print("Hello")
'''

'''lis_test= listest.listest()
t0= time.perf_counter()
radix_sort(lis_test,3)
t1 = time.perf_counter() - t0
print("Time elapsed: ", t1) # CPU seconds elapsed (floating point
##print(lis_test)'''
'''lis_test=[([98,99],1),([98,99],2),([99,97],3),([0,0],4),([99,98],5),([99,197],6),([97,98],7)]
radix_sort(lis_test,2)
print(lis_test)'''
