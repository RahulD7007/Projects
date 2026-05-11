# Inputs we need from the user 
# total rent 
# Total food ordered for snacking 
# Electricity units spend
# Charge per unit 
# person leaving in flat



# output 
# Total amount you've to pay is 
persons =int(input ("Enter the Number  of person  in Flat= "))
rent =int(input ("Enter your Flat rent = "))
maintanace = int(input("Enter the amount of maintanance = "))
electricity_bill = int(input("Enter the total of electricity spent =  "))
# charge_per_unit = int(input("Enter the charge per unit= "))

# total_bill= electricity_spent*charge_per_unit
output = (rent+electricity_bill+maintanace) //persons
print ("Each person will pay= ",output)