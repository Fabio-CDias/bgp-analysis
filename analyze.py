# This script generates the plot images

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from run_tty import scan_directory

files= scan_directory("result/Summary",ext=".txt")
files= sorted(files)

data_ipv4 = pd.DataFrame()
data_max_ipv4 = pd.DataFrame()
data_onlyipv4 = pd.DataFrame()
data_max_onlyipv4 = pd.DataFrame()

data_ipv6 = pd.DataFrame()
data_max_ipv6 = pd.DataFrame()
data_onlyipv6 = pd.DataFrame()
data_max_onlyipv6 = pd.DataFrame()


data_intersection = pd.DataFrame()
data_max_intersection = pd.DataFrame()

data_union = pd.DataFrame()
data_max_union = pd.DataFrame()

data_diffv4v6 = pd.DataFrame()
data_max_diffv4v6 = pd.DataFrame()

data_diffv6v4 = pd.DataFrame()
data_max_diffv6v4 = pd.DataFrame()

for f in files:
    date = f[f.find(".") + 1:len(f) - 9]
    df = pd.read_csv(f, sep="|", skiprows=0, header=None)
    df = df.drop(0, axis=1)
    df = df.rename(columns={1: "AS", 2: "IPV4", 3: "IPV6", 4: "intersection_v4v6", 5: "union_v4v6", 6: "diff_v4v6", 7: "diff_v6v4"})
    df["bool_union_v4v6"] = ((df["diff_v4v6"] + df["diff_v6v4"] == df["union_v4v6"]) &
                                   (df["diff_v4v6"] + df["diff_v6v4"] > 0) &
                                   (df["union_v4v6"] > 0))
    
    df["date"] = pd.to_datetime(date, format='%Y%m%d')
    
    IPV4 = df.sort_values(by=["IPV4","date"], ascending=False)
    max_IPV4 = IPV4.iloc[:1]

    IPV6 = df.sort_values(by="IPV6", ascending=False)
    max_IPV6 = IPV6.iloc[:1]

    onlyIPV4 = df[(df["IPV4"] > 0) & (df["IPV6"] == 0)].sort_values(by="IPV4", ascending=False)
    max_onlyIPV4 = onlyIPV4.sort_values(by="IPV4",ascending=False).iloc[:1]

    onlyIPV6 = df[(df["IPV6"] > 0) & (df["IPV4"] == 0)].sort_values(by="IPV6", ascending=False)
    max_onlyIPV6 = onlyIPV6.sort_values(by="IPV6",ascending=False).iloc[:1]


    intersection = df.sort_values(by="intersection_v4v6", ascending=False)
    max_intersection = intersection.iloc[:1]

    union = df.sort_values(by=["union_v4v6","bool_union_v4v6"], ascending=False)
    max_union = union.iloc[:1]

    diff_v4v6 = df.sort_values(by="diff_v4v6", ascending=False)
    max_diff_v4v6 = diff_v4v6.iloc[:1]

    diff_v6v4 = df.sort_values(by="diff_v6v4", ascending=False)
    max_diff_v6v4 = diff_v6v4.iloc[:1]


    data_ipv4 = pd.concat([data_ipv4, IPV4[["AS","date", "IPV4"]]], ignore_index=True)
    data_max_ipv4= pd.concat([data_max_ipv4, max_IPV4[["AS","date", "IPV4"]]], ignore_index=True)
    data_onlyipv4 = pd.concat([data_onlyipv4, onlyIPV4[["AS","date", "IPV4"]]], ignore_index=True)
    data_max_onlyipv4 = pd.concat([data_max_onlyipv4, max_onlyIPV4[["AS","date", "IPV4"]]], ignore_index=True)

    data_ipv6 = pd.concat([data_ipv6, IPV6[["AS","date", "IPV6"]]], ignore_index=True)
    data_max_ipv6 = pd.concat([data_max_ipv6, max_IPV6[["AS","date", "IPV6"]]], ignore_index=True)
    data_onlyipv6 = pd.concat([data_onlyipv6, onlyIPV6[["AS","date", "IPV6"]]], ignore_index=True)
    data_max_onlyipv6 = pd.concat([data_max_onlyipv6, max_onlyIPV6[["AS","date", "IPV6"]]], ignore_index=True)

    data_intersection = pd.concat([data_intersection, intersection[["AS","date","intersection_v4v6"]]], ignore_index=True)
    data_max_intersection = pd.concat([data_max_intersection, max_intersection[["AS","date","intersection_v4v6"]]], ignore_index=True)

    data_union = pd.concat([data_union, union[["AS","date","union_v4v6"]]], ignore_index=True)
    data_max_union = pd.concat([data_max_union, max_union[["AS","date","union_v4v6"]]], ignore_index=True)

    data_diffv4v6 = pd.concat([data_diffv4v6, diff_v4v6[["AS","date","diff_v4v6"]]], ignore_index=True)
    data_max_diffv4v6 = pd.concat([data_max_diffv4v6, max_diff_v4v6[["AS","date","diff_v4v6"]]], ignore_index=True)

    data_diffv6v4 = pd.concat([data_diffv6v4, diff_v6v4[["AS","date","diff_v6v4"]]], ignore_index=True)
    data_max_diffv6v4 = pd.concat([data_max_diffv6v4, max_diff_v6v4[["AS","date","diff_v6v4"]]], ignore_index=True)

# IPV4  (TIME)
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.plot(data_max_ipv4['date'], data_max_ipv4['IPV4'], label='IPV4 Inclusive', linestyle='-')
plt.title('AS Neighbors General: IPV4 → by TIME')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
# IPV6 (TIME)
plt.subplot(2, 1, 2)
plt.plot(data_max_ipv6['date'], data_max_ipv6['IPV6'], label='IPV6 Inclusive', linestyle='-')
plt.title('AS Neighbors General: IPV6 → by TIME')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()
#plt.show()
plt.savefig("img/ipv4ipv6_time.png")

# IPV4 (AS)
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.bar(data_ipv4['AS'].head(15), data_ipv4['IPV4'].head(15), label='IPV4 Inclusive')
plt.title('AS Neighbors General: IPV4 → by AS')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#  IPV6 (AS)
plt.subplot(2, 1, 2)
plt.bar(data_ipv6['AS'].head(15), data_ipv6['IPV6'].head(15), label='IPV6 Inclusive')
plt.title('AS Neighbors General: IPV6 → by AS')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()
#plt.show()
plt.savefig("img/ipv4ipv6_AS.png")


#IPV4 ONLY (TIME)
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.plot(data_max_onlyipv4['date'], data_max_onlyipv4['IPV4'], label='IPV4 Exclusive', linestyle='-')
plt.title('AS Neighbors: Only IPV4 → by TIME')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
# IPV6 ONLY (TIME)
plt.subplot(2, 1, 2)
plt.plot(data_max_onlyipv6['date'], data_max_onlyipv6['IPV6'], label='IPV6 Exclusive', linestyle='-')
plt.title('AS Neighbors: Only IPV6 → by TIME')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()
#plt.show()
plt.savefig("img/ipv4ipv6_only_time.png")


# IPV4 ONLY (AS)
plt.figure(figsize=(20, 10))
plt.subplot(2, 1, 1)
plt.bar(data_onlyipv4['AS'].head(15), data_onlyipv4['IPV4'].head(15), label='IPV4 Exclusive')
plt.title('AS Neighbors: Only IPV4 → by AS')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
# IPV6 ONLY (AS)
plt.subplot(2, 1, 2)
plt.bar(data_onlyipv6['AS'].head(15), data_onlyipv6['IPV6'].head(15), label='IPV6 Exclusive')
plt.title('AS Neighbors: Only IPV6 → by AS')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
plt.tight_layout()
#plt.show()
plt.savefig("img/ipv4ipv6_only_AS.png")

# IPV4 intersection IPV6 (TIME)
plt.figure(figsize=(20, 10))
plt.plot(data_max_intersection['date'], data_max_intersection['intersection_v4v6'], label='IPV4 ∩ IPV6')
plt.title('Intersection: IPV4 ∩ IPV6 → by TIME')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv4_intersection_ipv6_time.png")

# IPV4 intersection IPV6 (AS)
plt.figure(figsize=(20, 10))
plt.bar(data_intersection['AS'].head(15), data_intersection['intersection_v4v6'].head(15), label='IPV4 ∩ IPV6')
plt.title('Intersection: IPV4 ∩ IPV6 → by AS')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv4_intersection_ipv6_time.png")


# IPV4 diff IPV6 (AS)
plt.figure(figsize=(20, 10))
plt.bar(data_diffv4v6['AS'].head(15), data_diffv4v6['diff_v4v6'].head(15), label='IPV4 Δ IPV6')
plt.title('Difference: IPV4 Δ IPV6 → by TIME')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv4_diff_ipv6_AS.png")

# IPV4 diff IPV6 (TIME)
plt.figure(figsize=(20, 10))
plt.plot(data_max_diffv4v6['date'], data_max_diffv4v6['diff_v4v6'], label='IPV4 Δ IPV6')
plt.title('Difference: IPV4 Δ IPV6 → by AS')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv4_diff_ipv6_time.png")


# IPV6 diff IPV4 (AS)
plt.figure(figsize=(20, 10))
plt.bar(data_diffv6v4['AS'].head(15), data_diffv6v4['diff_v6v4'].head(15), label='IPV4 Δ IPV6')
plt.title('Difference: IPV6 Δ IPV4 → by TIME)')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv6_diff_ipv4_AS.png")

# IPV4 diff IPV6 (TIME)
plt.figure(figsize=(20, 10))
plt.plot(data_max_diffv6v4['date'], data_max_diffv6v4['diff_v6v4'], label='IPV4 Δ IPV6')
plt.title('Difference: IPV6 Δ IPV4 → by AS')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv6_diff_ipv4_time.png")


# IPV4 union IPV6 (AS)
plt.figure(figsize=(20, 10))
plt.bar(data_union['AS'].head(15), data_union['union_v4v6'].head(15), label='IPV4 ∪ IPV6')
plt.title('Union: IPV4 ∪ IPV6 → by AS')
plt.xlabel('AS')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv4_union_ipv6_AS.png")

# IPV4 union IPV6 (TIME)
plt.figure(figsize=(20, 10))
plt.plot(data_max_union['date'], data_max_union['union_v4v6'], label='IPV4 ∪ IPV6')
plt.title('Union: IPV4 ∪ IPV6 → by TIME')
plt.xlabel('Date')
plt.ylabel('Neighbors')
plt.legend(fontsize="small")
#plt.show()
plt.savefig("img/ipv4_union_ipv6_time.png")

