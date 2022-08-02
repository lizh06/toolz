import execnet as _en

gw = _en.makegateway()
ch = gw.remote_exec('channel.send(channel.receive() + 1)')
ch.send(1)
print(ch.receive())
