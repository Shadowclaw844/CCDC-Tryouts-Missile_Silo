from datetime import datetime, timedelta
import psycopg2
import paramiko
import os

class hostinfo():
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password





def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='missile_silo',
                            user='silo_admin',
                            password='NebulaNumber1!')
    return conn

def order66(target):
    # Host information
    # Linux
    #debian = hostinfo('127.0.0.1', 'adminuser', 'admin')
    debian_root = hostinfo('127.0.0.1','root', 'NebulaNumber1!')

    #centos = hostinfo('','nebula','nebula')
    centos_root = hostinfo('192.168.1.120','root','NebulaNumber1!')
    
    # Windows
    win10 = hostinfo('','NEBULA/administrator','NebulaNumber1!')
    
    win2016 = hostinfo('','administraotr','NebulaNumber1!')




    if target == 'debian':
        print('Goodbye Debian')
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Could implement feature to test normal user and sudo as well as root cred, but eh
        ssh.connect(debian_root.host, username=debian_root.username, password=debian_root.password)
        ssh.exec_command('wall zzz lmao', get_pty=True)
        ssh.close()



    if target == 'centos':
        print('Goodbye Centos')
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(centos_root.host, username=centos_root.username, password=centos_root.password)
        # Centos may require just shutdown now
        ssh.exec_command('wall zzz lmao', get_pty=True)
        ssh.close()

    if target == 'win10':
        print('Goodbye Windows 10')
        # Put the venvs in the root user
        command = '/root/venvs/impacket/bin/wmiexec.py {}:{}@{} "whoami"'.format(win10.username,win10.password,win10.host)
        os.system(command)

    if target == 'win2016':
        print('Goodbye Windows Server 2016')
        command = '/root/venvs/impacket/bin/wmiexec.py {}:{}@{} "whoami"'.format(win2016.username,win2016.password,win2016.host)
        os.system(command)




def main():
    targets = []
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM rockets WHERE active=true')
    results = cur.fetchall()
    #print(results)
    for rocket in results:
        #Time delta thing not working. Needs fixing
        if rocket[1] < datetime.now() + timedelta(seconds=-20): 
            print('We found one')
            print(rocket[0])
            cur.execute('UPDATE rockets SET active=false WHERE ID={}'.format(rocket[0]))
            conn.commit()
            targets.append(rocket[2])
    cur.close()
    conn.close()
    for i in targets:
        order66(i)
    

if __name__ == '__main__':
    main()