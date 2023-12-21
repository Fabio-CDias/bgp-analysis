# This script generates the plot images
import pandas as pd
import matplotlib.pyplot as plt
from run_tty import scan_directory


files= scan_directory("result/Summary",ext=".txt")
files= sorted(files)

df_AS = pd.DataFrame()
df_IPV4 = pd.DataFrame()
df_IPV6 = pd.DataFrame()
df_intersection_v4v6 = pd.DataFrame()
df_union_v4v6 = pd.DataFrame()
df_diff_v4v6 = pd.DataFrame()
df_diff_v6v4 = pd.DataFrame()

for f in files:
    date = f[f.find(".") + 1:len(f) - 9]
    df = pd.read_csv(f, sep="|", skiprows=0, header=None)
    df = df.drop(0, axis=1)
    df = df.rename(columns={1: "AS", 2: "IPV4", 3: "IPV6", 4: "intersection_v4v6", 5: "union_v4v6", 6: "diff_v4v6", 7: "diff_v6v4"})
    df["date"] = pd.to_datetime(date, format='%Y%m%d')
    df["type"],df["location"] = None,None

    df['IPV4'] = pd.to_numeric(df['IPV4'], errors='coerce')
    df['IPV6'] = pd.to_numeric(df['IPV6'], errors='coerce')
    df['intersection_v4v6'] = pd.to_numeric(df['intersection_v4v6'], errors='coerce')
    df['union_v4v6'] = pd.to_numeric(df['union_v4v6'], errors='coerce')
    df['diff_v4v6'] = pd.to_numeric(df['diff_v4v6'], errors='coerce')
    df['diff_v6v4'] = pd.to_numeric(df['diff_v6v4'], errors='coerce')

    df["bool_union_v4v6"] = ( (df["diff_v4v6"] == 0) & (df["diff_v6v4"] == 0) & (df["union_v4v6"] > 0) )

    len_AS = pd.DataFrame({"date": [df["date"].iloc[0]], "len_AS": (df["AS"]).count()})
    len_IPV4 = pd.DataFrame({"date": [df["date"].iloc[0]],"len_IPV4": ((df["IPV4"] > 0) & (df["IPV6"] == 0)).sum()})
    len_IPV6 = pd.DataFrame({"date": [df["date"].iloc[0]],"len_IPV6": ((df["IPV6"] > 0) & (df["IPV4"] == 0)).sum()})
    len_intersection_v4v6 = pd.DataFrame({"date": [df["date"].iloc[0]], "len_intersection_v4v6": (df["intersection_v4v6"]>0).sum()})
    len_union_v4v6 = pd.DataFrame({"date": [df["date"].iloc[0]],"len_union_v4v6": df.loc[df["bool_union_v4v6"], "union_v4v6"].count()})
    len_diff_v4v6 = pd.DataFrame({"date": [df["date"].iloc[0]], "len_diff_v4v6": (df["diff_v4v6"] > df["diff_v6v4"]).sum()})
    len_diff_v6v4 = pd.DataFrame({"date": [df["date"].iloc[0]], "len_diff_v6v4": (df["diff_v4v6"] < df["diff_v6v4"]).sum()})

    df_AS = pd.concat([df_AS, len_AS], ignore_index=True)
    df_IPV4 = pd.concat([df_IPV4, len_IPV4], ignore_index=True)
    df_IPV6 = pd.concat([df_IPV6, len_IPV6], ignore_index=True)
    df_intersection_v4v6 = pd.concat([df_intersection_v4v6, len_intersection_v4v6], ignore_index=True)
    df_union_v4v6 = pd.concat([df_union_v4v6, len_union_v4v6], ignore_index=True)
    df_diff_v4v6 = pd.concat([df_diff_v4v6, len_diff_v4v6], ignore_index=True)
    df_diff_v6v4 = pd.concat([df_diff_v6v4, len_diff_v6v4], ignore_index=True)

# TOTAL AS
plt.figure(figsize=(20, 10))
plt.plot(df_AS['date'], df_AS['len_AS'], label='Total ASes', linestyle='-')
plt.title('Total ASes ')
plt.xlabel('Date')
plt.ylabel('ASes')
plt.legend(fontsize="small")
# plt.show()
plt.savefig("img/ipv4ipv6_AS.png")

# IPV4 IPV6 TOTAL SIDEBYSIDE
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.plot(df_IPV4['date'], df_IPV4['len_IPV4'], label='IPV4', linestyle='-')
plt.title('Total AS Neighbors: IPV4')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()

plt.subplot(2, 1, 2)
plt.plot(df_IPV6['date'], df_IPV6['len_IPV6'], label='IPV6', linestyle='-')
plt.title('Total AS Neighbors: IPV6')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()
# plt.show()
plt.savefig("img/ipv4ipv6_total_v1.png")

# IPV4 IPV6 TOTAL TOGETHER
plt.figure(figsize=(20, 10))
plt.plot(df_IPV4['date'], df_IPV4['len_IPV4'], label='IPV4', linestyle='-')
plt.plot(df_IPV6['date'], df_IPV6['len_IPV6'], label='IPV6', linestyle='-')
plt.title('Total AS Neighbors: IPV4 and IPV6')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
# plt.show()
plt.savefig("img/ipv4ipv6_total_v2.png")

# TOTAL INTERSECTION
plt.figure(figsize=(20, 10))
plt.plot(df_intersection_v4v6['date'], df_intersection_v4v6['len_intersection_v4v6'], label='IPV4 ∩ IPV6', linestyle='-')
plt.title('Intersection: IPV4 and IPV6')
plt.xlabel('Date')
plt.ylabel('ASes')
plt.legend(fontsize="small")
# plt.show()
plt.savefig("img/ipv4ipv6_intersection.png")

# TOTAL UNION
plt.figure(figsize=(20, 10))
plt.plot(df_union_v4v6['date'], df_union_v4v6['len_union_v4v6'], label='IPV4 ∪ IPV6', linestyle='-')
plt.title('Union: IPV4 and IPV6')
plt.xlabel('Date')
plt.ylabel('ASes')
plt.legend(fontsize="small")
# plt.show()
plt.savefig("img/ipv4ipv6_union.png")

# DIFF IPV4 IPV6 TOTAL SIDEBYSIDE
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.plot(df_diff_v4v6['date'], df_diff_v4v6['len_diff_v4v6'], label='IPV4 Δ IPV6', linestyle='-')
plt.title('Difference: IPV4 > IPV6')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()

plt.subplot(2, 1, 2)
plt.plot(df_diff_v6v4['date'], df_diff_v6v4['len_diff_v6v4'], label='IPV6 Δ IPV4', linestyle='-')
plt.title('Difference: IPV6 > IPV4')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()
# plt.show()
plt.savefig("img/ipv4ipv6_diff.png")
