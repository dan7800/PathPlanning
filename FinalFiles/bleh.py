# s, e = 100, 999
# count =0
# for i in range(s, e+1):
#     if i % 3 == 0 or i % 4 == 0:
#         count+= 1
#
# print(count)
def no_course():
    count = 0
    for i in range(1, 121):
        if(i % 2 == 0 or i % 5 == 0 or i % 7 == 0):
            count += 1
    return 120 - count

print(no_course())

def sortByParity(A):
    counter = 0

    for i in range(0 , len(A)):
        if A[i] % 2 == 0:
            temp = A[counter]
            A[counter] = A[i]
            counter += 1
            A[i] = temp
    return counter

print(sortByParity([0,1,2,3,4,5,6,7,8]))



def KellyAsha(A, K, P):
    if K <= A:
        return -1

    return P//(K - A) + 1

print(KellyAsha(3,5,5))

def overlappingmatrix(upRight):
    grid =[]





