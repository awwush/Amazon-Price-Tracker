# import required files and modules

import requests
from bs4 import BeautifulSoup
import smtplib
import time

# set the headers and user string
headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}

# send a request to fetch HTML of the page
response = requests.get('https://www.amazon.in/Bose-SoundLink-Wireless-Around-Ear-Headphones/dp/B0117RGG8E/ref=sr_1_11?qid=1562395272&refinements=p_89%3ABose&s=electronics&sr=1-11', headers=headers)

# create the soup object
soup = BeautifulSoup(response.content, 'html.parser')

# change the encoding to utf-8
soup.encode('utf-8')

#print(soup.prettify())

# function to check if the price has dropped below 20,000
def check_price():
  try:
    title = soup.find(id= "productTitle").get_text()
  except AttributeError :
    print("not found")
  try:
    price = soup.find(id = "priceblock_ourprice").get_text().replace(',', '').replace('₹', '').replace(' ', '').strip()
  except AttributeError :
    print("not found")
  #print(price)

  #converting the string amount to float
  converted_price = float(price[0:5])
  print(converted_price)
  if(converted_price < 20000):
    send_mail()

  #using strip to remove extra spaces in the title
  print(title.strip())




# function that sends an email if the prices fell down
def send_mail():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.ehlo()

  server.login('email@gmail.com', 'password')

  subject = 'Price Fell Down'
  body = "Check the amazon link https://www.amazon.in/Bose-SoundLink-Wireless-Around-Ear-Headphones/dp/B0117RGG8E/ref=sr_1_11?qid=1562395272&refinements=p_89%3ABose&s=electronics&sr=1-11 "

  msg = f"Subject: {subject}\n\n{body}"
  
  server.sendmail(
    'sender@gmail.com',
    'receiver@gmail.com',
    msg
  )
  #print a message to check if the email has been sent
  print('Hey Email has been sent')
  # quit the server
  server.quit()

#loop that allows the program to regularly check for prices
while(True):
  check_price()
  time.sleep(60 * 60)