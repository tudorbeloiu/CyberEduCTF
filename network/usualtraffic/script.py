import pyshark

cap = pyshark.FileCapture('traffic.pcapng', display_filter='bgp.type == 2')

field_name = 'nlri_prefix'
enc = ""
enc_iv = ""
for i,pkt in enumerate(cap,start = 1):
    ip_src = pkt.ip.src
    ip_dest = pkt.ip.dst

    if ip_src == "10.10.10.1":
        nlri = pkt.bgp.get_field_value(field_name)
        if i != 1:
            num_list = nlri.split(".")
            s = ''.join([chr(int(n)) for n in num_list])
            enc = enc + s
    else:
        nlri = pkt.bgp.get_field_value(field_name)
        if i != 2:
            iv_list = nlri.split(".")
            iv_s = ''.join([chr(int(n)) for n in iv_list])
            enc_iv = enc_iv + iv_s

        


print(enc)
print(enc_iv)

cap.close()