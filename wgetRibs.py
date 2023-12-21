# This script automates ribs download.

import subprocess
def downloadRibs(year, month,day,final_year):
    for _ in range(final_year - year):
        for m in month:
            url = f"https://archive.routeviews.org/route-views2.saopaulo/bgpdata/{str(year)}.{m}/RIBS/rib.{str(year)}{m}{day}"
            output = f"data/rib.{str(year)}{m}{day}"
            command = ["wget", url, "-O", output]
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        year+=1
