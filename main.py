from rib import rib
import run_tty as tty
import os
if __name__ == "__main__":
    directory = "data"
    zipfiles = tty.scan_directory(directory)
    s = len(zipfiles)
    for file in zipfiles:
        print(s,"N of files")
        print(f"Unpacking - {file}")
        filename = tty.run_bgpscanner(file)
        print(f"Processing - {filename}\n")
        rib(directory,filename)
        s-=1
        os.remove(os.path.join(directory,filename))
    print("All done!")