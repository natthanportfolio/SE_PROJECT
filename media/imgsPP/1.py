a=int(input())
for i in range(1,a+1):
    print(" "*(a-i)+"*"*(i*2-1))

i=1
for j in range(a,0,-2):
    print(" "*(i)+"*"*(j))
    i=i+1
