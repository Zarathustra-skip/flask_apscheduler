import os


def success(path):
    cmd = "python "+path
    print(cmd)
    a = os.system(cmd)
    print(a)
