import logging

from django.http import HttpResponse
from django.template import loader
from PulseMaster.settings import *

logger = logging.getLogger('spf_referral_vulnerability_checker')
cache = {}


def home(request):
    import json
    f = open("data/context.json")
    context = json.load(f)
    # logger.debug('this is a debug message!')
    template = loader.get_template('../templates/spf_referral_vulnerability_check/index.html')
    return HttpResponse(template.render(context, request))


def make_arr(resolver_ip_to_verdict_list):
    count = 0
    tot = 0
    for resolver_ip in resolver_ip_to_verdict_list:

        good_len = len(resolver_ip_to_verdict_list[resolver_ip]["g"])
        bad_len = len(resolver_ip_to_verdict_list[resolver_ip]["b"])
        if good_len + bad_len == 0:
            continue
        tot += 1
        if (bad_len / (good_len + bad_len) == 1):
            count += 1
    return tot, count


def contact(request):
    allowed_ttl = [1, 5, 15, 30, 60]
    import json

    # f = open("data/context.json")
    # context = json.load(f)

    import json
    f = open("data/mother_info.json")
    d = json.load(f)
    # time_of_parse = int(d['time_of_parse'])
    from datetime import datetime
    dd = datetime.now()
    parse_day = dd.strftime("%m/%d/%Y")
    a = 1
    ans = []
    for ttl1 in allowed_ttl:
        ttl = str(ttl1)
        meta = d[ttl]
        local_list = []

        resolver_ip_to_verdict_list_dump = meta["resolver_ip_to_verdict_list_dump"]
        tot, cnt = make_arr(resolver_ip_to_verdict_list_dump)

        local_list.append(ttl)
        local_list.append(tot)
        local_list.append(meta["total_asns"])
        print(ttl1, meta["total_asns"])
        local_list.append(meta["total_exitnodes"])

        local_list.append("{} ({}%)".format(cnt, "{:.2f}".format((cnt * 100)/meta["total_resolvers"]) ))
        ans.append(local_list)
    local_list = []
    local_list.append("Overall")
    local_list.append(d["global"]["total_resolvers"])
    local_list.append(d["global"]["total_asns"])
    local_list.append(d["global"]["total_exitnodes"])
    local_list.append("-")
    ans.append(local_list)

    template = loader.get_template('../templates/spf_referral_vulnerability_check/contact.html')
    context = {"lst": ans, "day": parse_day}

    with open("data/context.json", "w") as ouf:
        json.dump(context, fp=ouf)

    return HttpResponse(template.render(context, request))

