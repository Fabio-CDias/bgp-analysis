import subprocess
import os
def scan_directory(directory):
    files = []
    for filename in os.listdir(directory):
        path = os.path.join(directory,filename)
        if ".bz2" in filename and os.path.isfile(path):
            files.append(path)
    return files

def run_bgpscanner(input_filename):
    output_filename = f"{input_filename[:-4]}.txt"
    command = ["bgpscanner", input_filename]
    if os.path.exists(output_filename): os.remove(output_filename)
    with open(output_filename, 'w') as output_file:
        subprocess.run(command, stdout=output_file)
    return os.path.basename(output_filename)
