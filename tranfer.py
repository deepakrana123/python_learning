import paramiko 



def transferData():
    # try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(hostname="localhost")
        print("connected")
    # except:
    #     print("not worring")


transferData()