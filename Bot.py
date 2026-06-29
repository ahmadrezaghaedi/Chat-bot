import requests,time,json,threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

B="8455396477:AAEX0S9wL5Jh6y70ZaGUx83HCMY0eRYDM8w"
A=8822316542
C="@RayniStorm"
E="https://t.me/RayniStorm"
F=f"https://api.telegram.org/bot{B}"
USERS={}
CHATS={}

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Running!")

def WS():
    port=int(os.environ.get('PORT',8000))
    HTTPServer(('0.0.0.0',port), H).serve_forever()

threading.Thread(target=WS, daemon=True).start()

def LD():
    global USERS,CHATS
    try:
        with open("users.json","r") as f:
            d=json.load(f)
            USERS=d.get("users",{})
            CHATS=d.get("chats",{})
    except:pass

def SV():
    with open("users.json","w") as f:
        json.dump({"users":USERS,"chats":CHATS},f)

LD()

def U():
    try:
        r=requests.get(f"{F}/getUpdates?timeout=5")
        return r.json().get("result",[])
    except:return[]

def SM(c,t,k=None):
    d={"chat_id":c,"text":t}
    if k:d["reply_markup"]=json.dumps(k)
    try:requests.post(f"{F}/sendMessage",json=d)
    except:pass

def CK(u):
    try:
        r=requests.get(f"{F}/getChatMember?chat_id={C}&user_id={u}")
        s=r.json().get("result",{}).get("status","")
        return s in["member","administrator","creator"]
    except:return False

def handle(m):
    c=m["chat"]["id"]
    u=m["from"]["id"]
    t=m.get("text","").strip()
    n=m["from"].get("first_name","User")
    uid=str(u)
    
    if t=="/start"or t=="برگشت":
        if CK(u):
            USERS[uid]=n
            if uid+"_target"in USERS:del USERS[uid+"_target"]
            if uid in CHATS:del CHATS[uid]
            SV()
            SM(c,"سلام "+n+"!\n\nعضو کانال هستی!\n\nآیدی عددی طرف رو بفرست:\n(از @userinfobot بگیر)\nمثال: 123456789\n\nبعدش پیام بده تا براش بره.\n\nبرای برگشت از اول: برگشت")
        else:
            SM(c,"سلام "+n+"!\n\nباید عضو کانال باشی:\n"+E+"\n\nبعد عضو شدن /start بزن.",{"inline_keyboard":[[{"text":"عضویت","url":E}]]})
        return
    
    if not CK(u):
        SM(c,"عضو کانال نیستی!")
        return
    
    if uid not in USERS:
        USERS[uid]=n
        SV()
    
    if t.startswith("/send ")and u==A:
        parts=t.split(maxsplit=2)
        if len(parts)>=3:
            target=parts[1]
            msg=parts[2]
            try:SM(int(target),msg)
            except:pass
            SM(c,"ارسال شد")
        return
    
    if t=="/stats"and u==A:
        SM(c,"اعضا: "+str(len(USERS)))
        return
    
    if t.isdigit() and len(t)>=7:
        USERS[uid+"_target"]=t
        CHATS[uid]=t
        CHATS[t]=uid
        SV()
        SM(c,"طرف: "+t+"\n\nحالا پیام بده تا براش بره.\n\nبرای برگشت: برگشت")
        try:SM(int(t),"📩 یه نفر بهت پیام داده!\nجواب بده همینجا.\nبرای برگشت: برگشت")
        except:pass
        return
    
    if uid+"_target"in USERS:
        target=USERS[uid+"_target"]
        try:
            SM(int(target),"📩 "+n+":\n\n"+t)
            SM(c,"✅ ارسال شد!")
        except:
            SM(c,"❌ طرف ربات رو استارت نزده!")
        return
    
    if uid in CHATS:
        other=CHATS[uid]
        try:
            SM(int(other),"📩 "+n+":\n\n"+t)
            SM(c,"✅ ارسال شد!")
        except:
            SM(c,"❌ طرف آنلاین نیست!")
        return
    
    SM(c,"لطفاً اول آیدی عددی طرف رو بفرست.\nاز @userinfobot بگیر.\n\nبرای برگشت: برگشت")

print("BOT READY")

last_id=0
while True:
    try:
        ups=U()
        for up in ups:
            uid=up["update_id"]
            if uid>last_id:
                last_id=uid
                if"message"in up and"text"in up["message"]:
                    handle(up["message"])
                    requests.get(f"{F}/getUpdates?offset={uid+1}")
        time.sleep(0.5)
    except KeyboardInterrupt:
        break
    except:
        time.sleep(1)
