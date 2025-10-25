import socket

HOST = '34.185.180.177'
PORT = 31060


sock = socket.socket()
sock.connect((HOST,PORT))


caz = 0

while caz < 3:

    response = sock.recv(4096)
    str_response = repr(response)

    idxSt = str_response.find('<') + 2
    idxDr = str_response.find('>')

    numar = str_response[idxSt:idxDr]

    if caz == 0:
        response_corect = str(hex(int(numar)))
    elif caz == 1:
        #hex to ascii
        response_corect = bytes.fromhex(numar).decode("utf-8")
    else:
        #oct to ascii
        response_splitted = numar.split(' ')
        response_corect = ""
        for i in response_splitted:
            converted_in_oct = chr(int(i,8))
            response_corect += converted_in_oct


    response_final = response_corect + '\n'

    print(response)
    print(response_final)

    sock.send(bytes(response_final,'utf8'))
    caz = caz + 1


response = sock.recv(4096)
print(response)

sock.close()

