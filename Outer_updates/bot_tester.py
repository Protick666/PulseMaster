import dns.resolver
from multiprocessing.dummy import Pool as ThreadPool
query = "12345a12asdas44saadfsdfsdafdsfasfsasdsdfdsf.zeus_reload_19.60.121.1.securekey.app"

ip_list = [
    "8.8.8.8",
    "9.9.9.9",
    "208.67.222.222",
    "1.1.1.1",
    "185.228.168.9",
    "76.76.19.19",
    "94.140.14.14",
    "84.200.69.80",
    "8.26.56.26",
    "205.171.3.65",
    "149.112.121.10",
    "195.46.39.39",
    "159.89.120.99",
    "216.146.35.35",
    "77.88.8.8",
    "74.82.42.42",
    "64.6.64.6"
]

final_ip_list = ip_list + ip_list


def make_dns_req(ip):
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]
        answer = resolver.resolve(query)
        rrs = list(answer.rrset.items)
        rrs = [str(e) for e in rrs]
        return {ip: rrs}
    except:
        return {ip: None}

pool = ThreadPool(15)
results = pool.map(make_dns_req, final_ip_list)
pool.close()
pool.join()
a = 1
from collections import defaultdict
ans = defaultdict(lambda : list())
for d in results:
    for key in d:
        try:
            ans[key] = ans[key] + d[key]
        except:
            pass

a = 1
