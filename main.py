from rib import rib
from wgetRibs import downloadRibs
import run_tty as tty
import os
if __name__ == "__main__":
    print("Downloading Ribs")
    downloadRibs(month = ["01","04","07","10"],year = 2019,day = "15.0000.bz2",final_year=2023)
    directory = "data"
    zipfiles = tty.scan_directory(directory)
    zipfiles= sorted(zipfiles)
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