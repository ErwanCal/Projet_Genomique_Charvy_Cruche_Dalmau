def counting_sort(array,digit,p): ##The counting sort is a stable sort used in the radic sort
    ##here the counting sort needs to be adapted to look at only one digit of each number (for radix)
    ##we also added the parameter p to be able to read the triplets (more info below)
    arr_ord = [0]*len(array)
    ##1) since we only sort single digits, the max will always be smaller than 10
    ##2) create count index (that will have the cumulative index in the end)
    count_list = [0]*10
    for tpl in array :
        n_uplet = tpl[0]##we take the first element of the tuple, the n-uplet
        num = n_uplet[p] // digit ##we cut off the digits to the right by getting the quotient of the euclidian division
        ##p is the index of the number studied in the triplet
        count_list[num%10]+=1##we cut off the digits to the left by getting the remainder of the euclidian division
    sum = 0
    for i in range(len(count_list)):
        sum += count_list[i]
        count_list[i]=sum
    ##3) Get the ordered array using the cumulative count indexes
    for tpl in reversed(array):
        n_uplet = tpl[0]
        num = n_uplet[p] // digit
        id = count_list[num%10]-1
        arr_ord[id]=tpl
        count_list[num%10] -=1

    for i in range(len(array)):##we change the base array to allow the radix sort to loop easily
        array[i] = arr_ord[i]
def radix_sort(array,p):##Here the radix sort is modified to work with the triplet list sent by the DC3
##The code is not flexible enough to compute all characters in the ascii table, but it's enough for the use needed
    ##1) we take max = 100 because A T C G are all below 100 in ascii code
    mx = 100
    '''##2) to know how many loops we have to do, we will use a variable to represent,
    the digit we are currently in'''
    for i in reversed(range(0,p)):
        digit = 1 ##starts at one for units
        while mx - digit > 0 :##when all the digits are checked, digit will be greater than the maximum
            counting_sort(array,digit,i)
            digit *= 10 ##digit will go to the tens, the hundreds, the thousands...

lis_test=[([98,99,97],3),([98,99,97],4),([99,97,98],2),([0,0,0],5),([99,97,98],1),([99,97,99],6),([97,98,0],7)]
radix_sort(lis_test,3)
print(lis_test)
lis_test=[([98,99],1),([98,99],2),([99,97],3),([0,0],4),([99,97],5),([99,97],6),([97,98],7)]
radix_sort(lis_test,2)
print(lis_test)
