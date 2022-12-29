import network, umail, time

# Networks = [{'SSID':'cooper', 'Pass':'01211974'}, {'SSID':'Marist_Student', 'Pass':'MCHS1MCHS'}]

raise OSError

sta_if = network.WLAN(network.STA_IF)

sta_if.active(True)

sta_if.connect('cooper', '01211974')

while not sta_if.isconnected():
	print('NoConn, delaying')
	time.sleep(0.1)

smtp = umail.SMTP('smtp.gmail.com', 587, username='jimmy.l.smythe@gmail.com', password='klralwdsexpaeoba')

smtp.to('smythe1jh@marisths.net')

smtp.write("From: Jimmy <jimmy.l.smythe@gmail.com>\n")
smtp.write("To: Jimmy <smythe1jh@marisths.net>\n")
smtp.write("Subject: Test Of Function\n\n")
smtp.write("This would be line one,\n")
smtp.write("This would be two.\n")
smtp.write("If this works first try, \n")
smtp.write("I'll eat my shoe.\n")
smtp.write("...\n")
smtp.send()
smtp.quit()