import export
import os
# Adds the observed AS(current) and its neighbors, to a dict.
def add_neighbor(current,next_neighbor,prev_neighbor,ipver):
    if current not in ipver:
        ipver[current] = set()
    for value in (next_neighbor,prev_neighbor):
        if value is not None and value not in ipver[current]:
            ipver[current].add(value)

# Defines and maps the neighbors as: Previous AS | (Current AS) | Next AS
def set_neighbors(neighbor_list,ipver):
    for i in range(len(neighbor_list)):
        prev_neighbor = neighbor_list[i-1] if (i - 1 >= 0) and (neighbor_list[i-1] != neighbor_list[i]) and "{" not in neighbor_list[i-1] and "{" not in neighbor_list[i-1] else None
        next_neighbor = neighbor_list[i+1] if (i + 1 < len(neighbor_list)) and (neighbor_list[i+1] != neighbor_list[i])  and "{" not in neighbor_list[i+1] and "}" not in neighbor_list[i+1] else None
        add_neighbor(neighbor_list[i],prev_neighbor,next_neighbor,ipver)

def rib(directory,file):
    ipv4 = {}
    ipv6 = {}

    with open(os.path.join(directory,file),"r") as f:
        content = f.read().split("\n")
        for line in content:
            try:
                if len(line) > 0:
                    if line[0] == "=":
                        line = line.split("|")
                        neighbors_list = line[2].split(" ")

                        # Line[1] is either ipv4 or ipv6
                        if '.' in line[1]:
                            set_neighbors(neighbors_list,ipv4)
                        if ':' in line[1]:
                            set_neighbors(neighbors_list,ipv6)
            except ValueError:
                print("ERROR: ",ValueError)
   
    export.txt(ipv4,ipv6,file)
    export.summary(ipv4,ipv6,file) 
