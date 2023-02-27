import requests
import json
from bs4 import BeautifulSoup
import schedule
import time


def get_earthquake_kandilli():
    array = []
    url = 'http://www.koeri.boun.edu.tr/scripts/lst9.asp'
    code = requests.get(url)
    plain = code.content
    soup = BeautifulSoup(plain, 'html.parser')
    plain_data = soup.find_all('pre')
    plain_data = str(plain_data).strip().split('--------------')[2]

    plain_data = plain_data.split('\n')
    plain_data.pop(0)
    plain_data.pop()
    plain_data.pop()
    for index in range(len(plain_data)):
        element = str(plain_data[index].rstrip())
        element = element.replace('(', " ")
        element = element.replace(')', " ")
        data = element.split()
        json_data = json.dumps({
            "id": index + 1,
            "date": data[0] + " " + data[1],
            "latitude": float(data[2]),
            "longitude": float(data[3]),
            "depth": float(data[4]),
            "magnitude": {
                "md": float(data[5].replace('-.-', '0')),
                "ml": float(data[6].replace('-.-', '0')),
                "mw": float(data[7].replace('-.-', '0'))
            },
            "location": ' '.join(s for s in data[8:-1]),
            "attribute": data[-1]
        }, sort_keys=False)

        json_data = json.loads(json_data)
        array.append(json_data)
    return array


def get_greater_3():
    data = get_earthquake_kandilli()
    for item in data:
        if (int(item['magnitude']['ml']) >= 3.0):
            print(item)


if __name__ == '__main__':
    schedule.every(15).seconds.do(get_greater_3)
    while True:
        schedule.run_pending()
        time.sleep(1)
