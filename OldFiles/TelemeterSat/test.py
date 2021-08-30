import TelemeterSat.telemeter as telemeter


if __name__ == '__main__':
    ##### 测试遥测包初始值是否正确
    t1 = telemeter.Telemeter()
    print(t1.__dict__)
