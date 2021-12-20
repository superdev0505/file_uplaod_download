import socket
import os

import buffer
import argparse


parser = argparse.ArgumentParser('File process server')
parser.add_argument("-h", "--host")
parser.add_argument("-p", "--port", type=int)
parser.add_argument("-c", "--file_count", type=int)
args = parser.parse_args()

try:
    os.mkdir('uploads')
except FileExistsError:
    pass

host = args.host
port = args.port
s = socket.socket()
s.connect((host, port))
print("Waiting for a connection.....")

with s:
    conn_buf = buffer.Buffer(s)
    file_count = args.file_count
    conn_buf.put_utf8(file_count)

    while True:
        hash_type = conn_buf.get_utf8()
        if not hash_type:
            break
        print('hash type: ', hash_type)

        file_name = conn_buf.get_utf8()
        if not file_name:
            break
        file_name = os.path.join('uploads', file_name)
        print('file name: ', file_name)

        file_size = int(conn_buf.get_utf8())
        print('file size: ', file_size)

        with open(file_name, 'wb') as f:
            remaining = file_size
            while remaining:
                chunk_size = 4096 if remaining >= 4096 else remaining
                chunk = conn_buf.get_bytes(chunk_size)
                if not chunk: break
                f.write(chunk)
                remaining -= len(chunk)
            if remaining:
                print('File incomplete.  Missing', remaining, 'bytes.')
            else:
                print('File received successfully.')
