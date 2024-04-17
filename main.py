from bottle import route, run, request,redirect
import requests

@route('/')
def index():
    x_forwarded_for = request.environ.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0] 
    else:
        ip_address = request.environ.get('REMOTE_ADDR')

    url = f"https://api.ipapi.is/?q={ip_address}"

    response = requests.get(url)
    data = response.json()

    detect = None
    if data['is_vpn'] == True:
      detect = "VPN"
    elif data['is_proxy'] == True:
      detect = "Proxy"
    elif data['is_tor'] == True:
      detect = "Tor"
    else:
      redirect('https://discord.gg/mbed')

    return f"{detect}の使用を検出しました。\nお手数ですが{detect}を切断してやり直してください。"

run(host='0.0.0.0',port=8080)
