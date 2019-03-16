a = 5
b = 20
c = 'AB'
d = 'CDEFG'
e = [1,2,3]
f = ['a','b','c']

#足し算
print(a + b)
print(c + d)
print(e + f)
print()

#len()関数
print(len(e))
print(len(d))
print()

#str()関数でのキャスト
strtest = d + str(b)
print(strtest)
print()

#range()関数
number_0to10 = range(10)
number_1to11 = range(1,11)
number_2to21 = range(2,22)
#python2ではrange()だけで表示できたが、python3はlistを使わないとならない
print(list(number_0to10))
print(list(number_1to11))
print(list(number_2to21))
print()

#Stringの持つ活用
address = 'Tokyo,Japan'
print(address)
print(address.split(',')[0],address.split(',')[1])
print(address.upper())