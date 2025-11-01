from scapy.all import rdpcap, TCP
import re

def user_agents(file_name):
    user_agents = []
    packages = rdpcap(file_name) #reads my pcapng file and returns all the packages

    for package in packages:
        if package.haslayer(TCP) and package.haslayer('Raw'):
            payload = package['Raw'].load.decode(errors='ignore')
            # package['Raw'].load is in bytes and it s converted to strings

            match = re.search(r'User-Agent:\s*(.+)', payload)
            if match:
                searched_value = re.sub(r'curl/', '', match.group(1))
                searched_value = re.sub(r'\n', '', searched_value)
                searched_value = re.sub(r'\r', '', searched_value)
                user_agents.append(searched_value)

    return user_agents

file_name = "captura.pcapng"

ua = user_agents(file_name)
result = ''.join(ua)

with open("user_agents.txt", "w") as g:
    g.write(result)

g.close()
