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
    apache_dir = "/var/log/apache2"
    dest_dir = "/net/data/dns-ttl/bind/"
    dest_dir_apache = "/net/data/dns-ttl/apache1/"
    rsa_loc = "/home/ubuntu/id_rsa"
    bash_cmd = "sudo logrotate -f /home/ubuntu/bind"
    bash_cmd_apache = "sudo logrotate -f /home/ubuntu/apache2"
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


def get_apache_access_files_only(lst):
    a = []
    for e in lst:
        if "other_vhosts" in e:
            continue
        if "access" in e:
            a.append(e)
    return a



def apache_transfer():
    send_msg("Starting apache transfer")

    files_before_log_rotate = [join(apache_dir, f) for f in listdir(apache_dir) if isfile(join(apache_dir, f))]
    files_before_log_rotate = get_apache_access_files_only(files_before_log_rotate)

    send_msg("Apache Files before:" + concat_str(files_before_log_rotate))

    if LIVE:
        execute_cmd(bash_cmd_apache)

    files_after_log_rotate = [join(apache_dir, f) for f in listdir(apache_dir) if isfile(join(apache_dir, f))]
    files_after_log_rotate = get_apache_access_files_only(files_after_log_rotate)

    send_msg("Apache Files after logrotate:" + concat_str(files_after_log_rotate))

    files_to_transfer = []
    for file in files_after_log_rotate:
        if not file.endswith("access.log"):
            files_to_transfer.append(file)

    for file in files_to_transfer:
        file_size_in_mb = getsize(file) / 1000000
        file_name = "access.log.{}{}".format(int(time.time()), randint(100, 999))

        cmd = "sudo mv {} {}".format(file, "{}/{}".format(apache_dir, file_name))
        execute_cmd(cmd)
        msg_str = "moved {} to {}, size {} MB".format(file.split("/")[-1], file_name, file_size_in_mb)
        send_msg(msg_str)
        cmd = "scp -i {} -r -P 2222 {} protick@pharah.cs.vt.edu:{}".format(rsa_loc, "{}/{}".format(apache_dir, file_name),
                                                                           dest_dir_apache)
        ans = execute_cmd(cmd)
        if ans[1] is None:
            cmd = "sudo rm {}".format("{}/{}".format(apache_dir, file_name))
            execute_cmd(cmd)


    files_at_end = [join(apache_dir, f) for f in listdir(apache_dir) if isfile(join(apache_dir, f))]
    files_at_end = get_apache_access_files_only(files_at_end)

    send_msg("Apache Files after sending:" + concat_str(files_at_end))


# bind_transfer()
scheduler = BlockingScheduler()
scheduler.add_job(bind_transfer, 'interval', minutes=20)
# scheduler.add_job(apache_transfer, 'interval', minutes=60)
scheduler.start()