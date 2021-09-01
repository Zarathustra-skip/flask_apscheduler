#encoding=utf8
import base64

string = "guest:guest".encode('utf-8')

a = base64.b64encode(string)
# print(a)
# b'Z3Vlc3Q6Z3Vlc3Q='
print(b"basic " + a)  # 最后必须拼接上basic
# b'basic Z3Vlc3Q6Z3Vlc3Q='