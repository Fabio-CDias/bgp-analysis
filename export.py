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
# v4,v6,both = only ipv4, only ipv6, both ipversion Keys
def summary(ipv4,ipv6,v4_key,v6_key,both_key,file):
    path = os.path.join("result",f"Summary_{file}")
    os.makedirs("result",exist_ok=True)
    if os.path.exists(path): os.remove(path)
    with open(path,"w") as f:  
        for v4 in v4_key:
            line = f"=|{v4}|{len(ipv4[v4])}|0|0\n"
            f.write(line)
        for v6 in v6_key:
            line = f"=|{v6}|0|{len(ipv6[v6])}|0\n"
            f.write(line)
        for both in both_key:
            equal = set(ipv4[both]) & set(ipv6[both])
            line = f"=|{both}|{len(ipv4[both])}|{len(ipv6[both])}|{len(equal)}\n"
            f.write(line)
       






















# import json

# def json(ipv4,ipv6,savefile):
#     data = []
#     if os.path.exists(f"{savefile}.json"): os.remove(f"{savefile}.json")
#     # with open(f"{savefile}.json","w") as f:
#     for i in ipv4.items():
#         asystem, neighbor = list(i)
#         neighbor = tuple(neighbor)
#         data.append({"Asyncronous system": asystem,"Neighborhood": neighbor,"Type": "ipv4"})
#     for i in ipv6.items():
#         asystem, neighbor = list(i)
#         neighbor = tuple(neighbor)
#         data.append({"Asyncronous system": asystem,"Neighborhood": neighbor,"Type": "ipv6"})
    
#     json.dumps(data,indent=2)