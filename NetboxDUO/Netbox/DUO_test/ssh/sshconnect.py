import paramiko


def commend(cmd):
    # for i in range (1):
    #     ip=get_ip('config')
    #     print(ip)
    #     break
    for i in range(10):
        try:
            # 创建SSH对象
            global ssh
            ssh = paramiko.SSHClient()

            # 把要连接的机器添加到known_hosts文件中
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # 连接服务器
            ssh.connect(hostname='192.168.10.1', port=22, username='root', password='ubt3018',)
            break
        except AssertionError as e:
            raise e
    # self.cmd = cmd
    #cmd = 'ls -l;ifconfig'       #多个命令用;隔开
    stdin, stdout, stderr = ssh.exec_command(cmd)

    result = stdout.read()

    if not result:
        result = stderr.read()
    ssh.close()

    return result.decode()
def close():
    ssh.close()