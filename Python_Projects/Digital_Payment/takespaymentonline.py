import qrcode 

# taking UPI ID AS a input 

upi_id = input("Enter your UPI ID= ")

# upi://pay?pa=UPI_ID&pn=NAME&am=Amount%cu=CURRENCY&tn=MESSAGE

# pa(upi_id),pn(reciept_name),am(amount),cu(currency),tn(message box after payment ) Is All  PARAMETER


# Defining the payment URL based on the UPI and the payment app
# You can modify this URLs based  on the payment apps you want  to support 

phone_pay_url = f'upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234'
paytem_url = f'upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234'
google_pay_url = f'upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234'


# Create QR codes for each payment app

phone_pay_qr = qrcode.make(phone_pay_url)
paytem_qr = qrcode.make(paytem_url)
google_pay_qr = qrcode.make(google_pay_url)

# saved the qr code to image file (optional)
phone_pay_qr.save('phonepay_qr.png')
paytem_qr.save('paytem_qr.png')
google_pay_qr.save('googlepay_qr.png')



# pillow library is used for image processing 
phone_pay_qr.show()
paytem_qr.show()
google_pay_qr.show()