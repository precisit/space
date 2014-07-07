space
=====

Space Repo

Test

    HTTPRequest(protocol='http', host='hampus.simulations.io', method='POST', uri='/test', version='HTTP/1.0', remote_ip='127.0.0.1', headers={'Content-Length': '127', 'X-Forwarded-For': '172.31.37.169', 'Host': 'hampus.simulations.io', 'Accept': '*/*', 'User-Agent': 'curl/7.26.0', 'Connection': 'close', 'X-Real-Ip': '172.31.37.169', 'Content-Type': 'application/x-www-form-urlencoded'})
    Traceback (most recent call last):
      File "/usr/local/lib/python2.7/dist-packages/tornado/web.py", line 1346, in _when_complete
        callback()
      File "/usr/local/lib/python2.7/dist-packages/tornado/web.py", line 1367, in _execute_method
        self._when_complete(method(*self.path_args, **self.path_kwargs),
      File "server.py", line 33, in post
        response = mainschilling.Tmix(indata)
      File "/home/hampus/space/Schilling python/mainschilling.py", line 22, in Tmix
        rockPar["deltaVp"], rockPar["Isp1V"], rockPar["A0"], rockPar["ssT"])
      File "/home/hampus/space/Schilling python/ascTime.py", line 26, in Tmix
        return 0.405*Ta(m1b, Isp1SL, T1, m2b, Isp2V, T2, ssT) + 0.595*T3s(deltaVp, Isp1V, A0)
      File "/home/hampus/space/Schilling python/ascTime.py", line 11, in Ta
        t1 = m1b*Isp1SL*9.81/T1
    TypeError: unsupported operand type(s) for /: 'float' and 'list'
