# This script automates ribs download.

import subprocess
month = ["01","04","07","10"]
year = 2015
day = "15.0000.bz2"
for _ in range(8):
    for m in month:
        # url = f"https://archive.routeviews.org/route-views2.saopaulo/bgpdata/{str(year)}.{m}/RIBS/rib.{str(year)}{m}{day}"
        url = f"https://archive.routeviews.org/route-views.sg/bgpdata/{str(year)}.{m}/RIBS/rib.{str(year)}{m}{day}"
        output = f"data/rib.{str(year)}{m}{day}"
        command = ["wget", url, "-O", output]
        result = subprocess.run(command, check=True, capture_output=True, text=True)
    year+=1
