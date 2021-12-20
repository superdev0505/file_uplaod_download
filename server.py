import socket
import os
import argparse
import buffer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    parser.add_argument("-a", "--hash_type")

    args = parser.parse_args()

    host = '0.0.0.0'
    port = int(args.port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(10)

    while True:
        conn, addr = s.accept()
        sbuf = buffer.Buffer(conn)
        hash_type = args.hash_type
        message_type = sbuf.get_utf8()
        if message_type == 'download_files':
            file_count = sbuf.get_utf8()
            file_count = int(file_count)

            files = [f for f in os.listdir('./uploads') if os.path.isfile(f)]
            if len(files) > file_count:
                files = files[:file_count]

            for file_name in files:
                file_path = os.path.join('uploads', file_name)
                print(file_name)
                sbuf.put_utf8(hash_type)
                sbuf.put_utf8(file_name)

                file_size = os.path.getsize(file_name)
                sbuf.put_utf8(str(file_size))

                with open(file_path, 'rb') as f:
                    sbuf.put_bytes(f.read())
                print('File Sent')
            conn.close()
        if message_type == 'upload_file':
            hash_type = sbuf.get_utf8()
            if not hash_type:
                break
            print('hash type: ', hash_type)

            file_name = sbuf.get_utf8()
            if not file_name:
                break
            file_name = os.path.join('uploads', file_name)
            print('file name: ', file_name)

            file_size = int(sbuf.get_utf8())
            print('file size: ', file_size)

            with open(file_name, 'wb') as f:
                remaining = file_size
                while remaining:
                    chunk_size = 4096 if remaining >= 4096 else remaining
                    chunk = sbuf.get_bytes(chunk_size)
                    if not chunk: break
                    f.write(chunk)
                    remaining -= len(chunk)
                if remaining:
                    print('File incomplete.  Missing', remaining, 'bytes.')
                else:
                    print('File received successfully.')
