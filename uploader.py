import socket
import os
import argparse

import buffer


parser = argparse.ArgumentParser('File process server')
parser.add_argument("-h", "--host")
parser.add_argument("-p", "--port", type=int)
parser.add_argument("-f", "--file_path")
args = parser.parse_args()

host = args.host
port = args.port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

with s:
    sbuf = buffer.Buffer(s)
    hash_type = args.hash_type
    message_type = sbuf.get_utf8()
    file_path = args.file_path
    file_name = os.path.basename(file_path)
    print(file_name)
    sbuf.put_utf8(hash_type)
    sbuf.put_utf8(file_name)

    file_size = os.path.getsize(file_path)
    sbuf.put_utf8(str(file_size))

    with open(file_path, 'rb') as f:
        sbuf.put_bytes(f.read())
    print('File Sent')
