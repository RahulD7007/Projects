# """
# Dictionary 

# collection - key+value = pair = data1

# left_side = key 
# Rigth_side = value
# {key1:value1,key2:value2}


# crud operation = ADD ,UPDATE,DELETE,VIEW,EXIT 



# """
# # how to create dictionary 

# Student = {
#     'Pankaj':95,
#     'Kiran':85
#     }

# key pass element
# print (Student['Pankaj'])

# update  the value 
# Student['Pankaj'] = 75
# print (Student)


# delete 
# del Student['Kiran']
# print(Student) 







# i = 1
# while i <= 5 :
#     print (i)
#     i += 1  



# a=list(range(1,101,1))
# print (a)

# a=tuple(range(1,101,1))
# print (a)

# for i in range (1,3):
#  for j in range (3,6):
#     print(f'{i},{j}') 


# for num in range(1,10,1):
#     if num == 5:
#         break
#     print (num)




# for num in range (1,5):
#     if num ==3:
#         continue
#     print(num)


# for num in range (1,10):
#     if num == 3:
#         pass
#     print (num)





# questions 
'''
1-10 
even numbers display 

%2 ==0 
'''


# for i  in range (1,11):
#     if  i % 2 == 0 :
#        print (f'even number',i)


'''
1-10 
odd number 

%2 == 1

'''

# for i in range (1,11):
#     if i % 2 == 1:
#         print(f'odd number',i)


# --------------------------------------------------

# for i  in range (1,11):
#     if  i % 2 == 0 :
#        print (f'even number',i)
#     else:
#           print(f'odd number',i)

# ----------------------------------------------------


# start = int (
#     int(
#         input('enter start = ')
#     )
# )

# stop =  int (
#     int(
#         input('enter stop = ')
#     )
# )



# skip = int (
#     input
#    ( 'number you want to skip = ') )
# for i in range (start,stop):
#     if i == skip:
#         continue 
#     print (i)




# ------------------------------------------------
# string  and character 

'''
numbers 
a-z A-Z !@#$%
white space 
'''




# name = 'root'
# print(name)

# name2 = "root"
# print (name2)

# name_3 = '''root'''
# print (name_3)


# name_4 = """root"""
# print (name_4)



# --------------------------------------
# 3 characterstics

# 1- mutable (declare data change)
# 2- immutable (declare data not change)



# indexed
# a = ('sharvil')
# print (a[2])


# len{} integer 
# str = "python"
# print (len(str))




# square = lambda x: x ** 2
# print(square(5))


# import logging
# logging.basicConfig(level=logging.INFO)
# logging.info('This is an info message')


# import pdb
# pdb.set_trace()







'''
Practice Questions

Write a Python program to find the factorial of a number using recursion.

Implement a program to check if a string is a palindrome.

Write a function to count the frequency of each word in a string.

Create a class to implement a bank account with deposit and withdrawal functionalities.

Explain the difference between is and == in Python.

Write SQL queries to fetch data from a database using Python.

'''


# slicng      
# text = "helloamroot"


# print(text[ : :-2])


# LOWER
# str = input("enter your name= ").lower()
# print(str)

# UPPER
# str = input("enter your name= ").upper()
# print(str)


# capitalize 
# str = input("enter your name= ").capitalize()
# print(str)


# title 
# str = input("enter your name= ").title()
# print(str)

# swapcase 
# str = input("enter you names= ").swapcase()
# print (str)




# text ="python program "
# print(text.find("p"))



# text ="python program "
# print(text.replace("python","java"))




"""
# splitting
str="a,b,c"
print(str.split(","))

-------------------------------
# join
str="a,b,c"
s= str.split(",")
print("after splitting",s)

# join 
result = ",".join(s)
print (result)

# another way 

str=['a','b','c']
print(",".join(str))
"""


'''
# checking methods  (returns boolean) and (case sensetive)
# startswith method 
str ="Python"
print(str.startswith('P'))
ans-True

 

# endswith method
str ="Python"
print(str.endswith('o'))
ans- False

# isalpha 
str ="Python"
print(str.isalpha())
ans- True

# isdigit
str ="Python"
print(str.isdigit())

# isalnum  (is alpa numeric methods)
str ="Python"
print(str.isalnum())

'''