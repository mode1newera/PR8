import os
import requests
BASE = os.environ.get("VIS_SERVER", "http://127.0.0.1:5000").rstrip("/")

def main():
    r = requests.get(BASE + "/",timeout=3)
    print("H1:",r.status_code,type(r.text),type(r.json()),r.json()["service"])
    r = requests.get(BASE + "/anketi",timeout=3)
    print("H2:",len(r.json()),r.json()[0]["fio"])
    r = requests.get(BASE + "/anketi/99",timeout=3)
    print("H3:",r.status_code,r.ok,r.json()["oshibka"])
    r = requests.get(BASE + "/anketi",params={"tip":"t"},timeout=3)
    print("H4:",r.url)
    for p in r.json():
        print(p["fio"],p["kafedra"])
    for mail in ["ivanov@mail.ru","kuznetsov.mail.ru"]:
        r = requests.post(BASE + "/proverka",json={"mail":mail},timeout=3)
        print("H5:",mail,r.status_code,r.json()["prinyato"])

if __name__ == "__main__":
    main()
