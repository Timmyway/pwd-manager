import requests

def post(url, payload={}, header={}):
    print(payload)
    r = requests.post(url, data=payload, headers=header)
    print(f'|Status code|-> {r.status_code}')
    print(f'|Result text| {r.text}')
    if r.status_code < 400:
        print('Status code is lower that 400')
        print(r.json)
        return r.json


if __name__ == '__main__':
    datas = {}
    datas['service'] = 'Konticrea'
    datas['username'] = 'fr2kontiki@gmail.com'
    datas['pwd'] = 'H9BcsHNZ67vBkJvT'
    post('http://localhost:5000/pwd', datas, header={'Content-Type': 'application/json'})