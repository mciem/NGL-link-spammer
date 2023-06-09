from uuid       import uuid4
from tls_client import Session
from time       import time
from threading  import Thread

class NGL:
    def __init__(self, username: str, proxy: str) -> None:
        self.deviceId = str(uuid4())
        self.username = username

        self.client = Session(client_identifier="chrome_114", random_tls_extension_order=True)
        self.client.proxies = proxy
        
        #self.client.get(f"https://ngl.link/{username}")
        self.client.headers = self.__headers()
    
    def __headers(self):
        return {
            "accept": "*/*",
            "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            #"cookie": "; ".join(f"{k}={v}" for k,v in self.client.cookies.items()),
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "host": "ngl.link",
            "origin": "https://ngl.link",
            "referer": f"https://ngl.link/{self.username}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }

    def send(self, question: str):
        data = f"username={self.username}&question={question}&deviceId={self.deviceId}gameSlug=&referrer"

        return self.client.post("https://ngl.link/api/submit", data=data)

if __name__ == "__main__":
    stats = {
        "sent": 0,
        "failed": 0,
        "start": time()
    }

    proxy = "http://"
    

    threads  = input("Threads > ")
    username = input("Username > ")
    question = input("Qustion > ")

    def n():
        while True:
            s = NGL(username, proxy)

            ss = s.send(question)
            js = ss.json()
            
            if js.get("questionId") is not None:
                stats["sent"] += 1
            else:
                stats["failed"] += 1

    for _ in range(int(threads)):
        Thread(target=n).start()

    while True:
        uptime = round(time() - stats["start"], 2)
        perm   = round((stats["sent"]/uptime)*60)
        print(f'\rSent: {stats["sent"]} | Failed: {stats["failed"]} | PerM: {perm} | Uptime: {uptime}s', end='', flush=True)
