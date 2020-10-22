-
    client = Client("opc.tcp://10.195.133.125:4840/")

    try:
        client.connect()

        methodNode = client.get_node("ns=2;s=/Methods")
        readVar = ua.QualifiedName("/Methods/ReadVar", 2) # 値を読み出す関数名、引数の2は上のns=?と同じ値。
        machineCoordinate = methodNode.call_method(readVar, "/Channel/GeometricAxis/actToolBasePos[u1,1,3]") # 機械座標の1～3軸を取得
        workCoordinate = methodNode.call_method(readVar, "/Channel/GeometricAxis/actToolEdgeCenterPos[u1,1,3]") # ワーク座標の1～3軸を取得
        print("Machine Coordinate: " + machineCoordinate)
        print("Work Coordinate: " + workCoordinate)

    finally:
        client.disconnect()
-