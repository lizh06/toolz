import paramiko

# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='linode', username='')
# client.connect(hostname='localhost') # local sshd not running!

_, out, err = client.exec_command('hostname')

print(out.readlines())
