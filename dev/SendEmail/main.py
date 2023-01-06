import network, umail, time

sta_if = network.WLAN(network.STA_IF)

sta_if.active(True)

sta_if.connect('SSID', 'PASS')

while not sta_if.isconnected():
	print('NoConn, delaying')
	time.sleep(0.1)

smtp = umail.SMTP('smtp.gmail.com', 587, username=f'{From}', password='???????????')

smtp.to(f'{To}')

smtp.write(f"From: {From}\n")
smtp.write(f"To: {To}\n")
smtp.write("Subject: Test Of Function\n\n")
smtp.write("This would be line one,\n")
smtp.write("This would be two.\n")
smtp.write("If this works first try, \n")
smtp.write("I'll eat my shoe.\n")
smtp.write("...\n")
smtp.send()
smtp.quit()
