import pyshark

key_string = "AAAAAA85783cc847fb84e7ba9c1c727099c9040fe086fab96857227bedc4b3967ec978"
key_bytes = key_string.encode('utf-8')

target_filter = 'tcp.stream eq 78 and ip.src == 161.35.16.97 && tcp.len > 0'

cap = pyshark.FileCapture('chall.pcapng', display_filter=target_filter)

content = bytearray()

for pkt in cap:
    try:
        payload_hex = pkt.tcp.payload.replace(':','')
        payload_bytes = bytes.fromhex(payload_hex)
        content = [chr(kb ^ pb)   for kb,pb in zip(key_bytes,payload_bytes)]
        flag = ''.join(content)
        print(flag)
    except AttributeError:
        continue
