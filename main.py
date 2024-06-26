from bottle import route, run, request, redirect
import requests
import os

@route('/')
def index():
    x_forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0] 
    else:
        ip_address = request.environ.get('REMOTE_ADDR')

    detect = None
    try:
      API_KEY = os.getenv("VPNAPIIO_KEY")

      url = f"https://vpnapi.io/api/{ip_address}?key={API_KEY}"
      response = requests.get(url)
      data = response.json()

      if data['security']['vpn'] == True:
        detect = "VPN"
      elif data['security']['proxy'] == True:
        detect = "Proxy"
      elif data['security']['tor'] == True:
        detect = "Tor"
    except:
      url = f"https://api.ipapi.is/?q={ip_address}"

      response = requests.get(url)
      data = response.json()

      if data['is_vpn'] == True:
        detect = "VPN"
      elif data['is_proxy'] == True:
        detect = "Proxy"
      elif data['is_tor'] == True:
        detect = "Tor"

    print(ip_address)
    print(detect)
    if detect == None:
      redirect('https://discord.com/invite/mbed')

    return f"{detect}の使用を検出しました。お手数ですが{detect}を切断してやり直してください。<br><br>{detect} use detected. Please disconnect the {detect} and try again."

run(host='0.0.0.0',port=8080)
