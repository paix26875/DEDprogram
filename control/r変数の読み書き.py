
from opcua import ua, Server, Client
client = Client("opc.tcp://10.195.133.125:4840/")

try:

    client.connect()



    r0 = client.get_node("ns=2;s=/Channel/Parameter/R[0]")

    r0.set_value(ua.DataValue(100.123)) # R0に100.123を書き込む

    val = r0.get_value() # R0の値を読み出す

    print(val)



finally:

    client.disconnect()