#20170528

import sys
import urllib

# Free mobile credentials
free_user = "XXXXXXXXXX"
free_pass = "XXXXXXXXXX"

# Send SMS message using free mobile API
def send_sms(msg):
  try:
    r = urllib.urlopen('https://smsapi.free-mobile.fr/sendmsg?user=%s&pass=%s&msg=%s' % (free_user, free_pass, msg))
    if r.getcode() != 200:
      print('-> [x] error sending sms. httpcode: {}', r.getcode())
    else:
      print('-> sms sent : %s' % msg)
  except:
    e = sys.exc_info()[0]
    print(str(e))

send_sms("LOVE U FOREVER")
