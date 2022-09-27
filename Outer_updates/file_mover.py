import subprocess
import requests
import time
from os import listdir
from os.path import isfile, join, getsize
from random import randint
from apscheduler.schedulers.blocking import BlockingScheduler

LIVE = True


def send_msg(text):
   token = "5041433919:AAGNTUiAjLRFSHdbiqD6v-DJakxBNN_kQFY"
   chat_id = "1764697018"
   url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
   results = requests.get(url_req)
   print(results.json())


if LIVE:
    bind_dir = "/var/log/bind"
    dest_dir = "/home/protick/ocsp_dns_django/ttldict/logs_final_v2/bind/bind/"
    rsa_loc = "/home/ubuntu/id_rsa"
    bash_cmd = "sudo logrotate -f /home/ubuntu/bind"
else:
    bind_dir = "/Users/protick.bhowmick/PriyoRepos/PulseMaster/bind"
    dest_dir = "/home/protick/false_dir/"
    rsa_loc = "/Users/protick.bhowmick/id_rsa"


def concat_str(lst):
    init_str = ""
    for e in lst:
        init_str = init_str + " " + e.split("/")[-1]

    return init_str


def execute_cmd(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # time.sleep(5)
    return output, error

# TODO check files


def bind_transfer():
    send_msg("Starting bind transfer")

    files_before_log_rotate = [join(bind_dir, f) for f in listdir(bind_dir) if isfile(join(bind_dir, f))]

    send_msg("Files before:" + concat_str(files_before_log_rotate))

    if LIVE:
        execute_cmd(bash_cmd)

    files_after_log_rotate = [join(bind_dir, f) for f in listdir(bind_dir) if isfile(join(bind_dir, f))]

    send_msg("Files after logrotate:" + concat_str(files_after_log_rotate))

    files_to_transfer = []
    for file in files_after_log_rotate:
        if not file.endswith("query.log"):
            files_to_transfer.append(file)

    for file in files_to_transfer:
        file_size_in_mb = getsize(file) / 1000000
        file_name = "query.log.{}{}".format(int(time.time()), randint(100, 999))

        cmd = "sudo mv {} {}".format(file, "{}/{}".format(bind_dir, file_name))
        execute_cmd(cmd)
        msg_str = "moved {} to {}, size {} MB".format(file.split("/")[-1], file_name, file_size_in_mb)
        send_msg(msg_str)
        cmd = "scp -i {} -r -P 2222 {} protick@pharah.cs.vt.edu:{}".format(rsa_loc, "{}/{}".format(bind_dir, file_name),
                                                                           dest_dir)
        ans = execute_cmd(cmd)
        if ans[1] is None:
            cmd = "sudo rm {}".format("{}/{}".format(bind_dir, file_name))
            execute_cmd(cmd)


    files_at_end = [join(bind_dir, f) for f in listdir(bind_dir) if isfile(join(bind_dir, f))]
    send_msg("Files after sending:" + concat_str(files_at_end))


# bind_transfer()
scheduler = BlockingScheduler()
scheduler.add_job(bind_transfer, 'interval', minutes=30)
scheduler.start()






