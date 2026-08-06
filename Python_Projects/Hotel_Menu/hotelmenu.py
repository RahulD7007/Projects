# using dictionary datatype
 
#define the menu of restaurant 


menu ={
    'Pizza':40,
    'Pasta':50,
    'Burger':60,
    'Salad':70,
    'Coffee':80,
    'Shake':50,
    'vadapav':15,
    'Pohe':20

}



print ("Welcome To Python Restaurant")
print ("Pizza : Rs 40 \n Pasta : Rs 50 \n Burger : Rs 60 \n Salad : Rs 70\n Coffee : Rs80 \n Shake : Rs50 \n vadapav : Rs 15 \n Pohe : Rs20")


order_total = 0 
item_1 = input("Enter the name of item you want to order =  ")
if item_1 in menu:
    order_total += menu [item_1]  # 0+50 
    print (f"Your  item {item_1} has been added to your order")

else: 
    print (f"ordered item {item_1} is not available yet!")


another_order = input ("Do you want to add another item?(Yes/No) ")
if another_order == "Yes":
   item_2 = input ("Enter the name of second item = ")
   if item_2 in menu:
        order_total += menu [item_2]
        print (f"Item {item_2} has been added to order")
   else: 
       print ("Order item {item_2} is not Available!")



print (f"The total amount of items to pay is  {order_total}")