import os
def format(ipver,v):
    line=""
    for i in ipver.items():
        asystem, neighbor = list(i)
        line += f"=|{v}|{asystem}|"
        for n in neighbor:
            line += f"{n} "
        line=line[:-1]+"\n"
    return line

def txt(ipv4,ipv6,file):
    path = os.path.join("result",f"Scan_{file}")
    os.makedirs("result",exist_ok=True)
    if os.path.exists(path): os.remove(path)
    with open(path,"w") as f:  
        f.write(format(ipv4,v="ipv4"))
        f.write(format(ipv6,v="ipv6"))

# ipv4,ipv6 = dict of all ASes based on ipversion      
def summary(ipv4,ipv6,file):
    path = os.path.join("result",f"Summary_{file}")
    os.makedirs("result",exist_ok=True)
    if os.path.exists(path): os.remove(path)

    common_AS = set(ipv4.keys()) & set(ipv6.keys())
    v4_only = set(ipv4.keys()) - set(ipv6.keys())
    v6_only = set(ipv6.keys()) - set(ipv4.keys())

    with open(path,"w") as f:  
        for v4 in v4_only:
            line = f"=|{v4}|{len(ipv4[v4])}|0|0|0|0|0\n"
            f.write(line)
        for v6 in v6_only:
            line = f"=|{v6}|0|{len(ipv6[v6])}|0|0|0|0\n"
            f.write(line)
        for key in common_AS:
            intersection = set(ipv4[key]) & set(ipv6[key])
            union = set(ipv4[key]) | set(ipv6[key])
            v4_diff = set(ipv4[key]) - set(ipv6[key])
            v6_diff = set(ipv6[key]) - set(ipv4[key])
            line = f"=|{key}|{len(ipv4[key])}|{len(ipv6[key])}|{len(intersection)}|{len(union)}|{len(v4_diff)}|{len(v6_diff)}\n"
            f.write(line)
