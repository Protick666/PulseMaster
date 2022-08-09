
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import subprocess


from PulseMaster.settings import LOCAL

if LOCAL:
    zone_path = '/Users/protick.bhowmick/zones'
    bash_cmd = 'ls -l'
else:
    zone_path = '/etc/bind/zones'
    bash_cmd_init = 'sudo service bind9 restart'
    bash_cmd_edit = 'sudo rndc reload'

BASE_FILE_NAME = 'db.exp.net-measurement.net'
base_domain = 'ttlexp.exp.net-measurement.net.'

first_web_ip = '52.44.221.99'
second_web_ip = '3.220.52.113'


class BindUpdateView(APIView):
    def get(self, request):
        try:
            file_version = request.GET.get('file_version', None)
            bucket_id = request.GET.get('bucket_id', None)
            if bucket_id is None:
                raise Exception
            # ttl = int(request.GET.get('ttl', None))

            if file_version not in ['first', 'second', 'remove']:
                raise Exception
            dest_file = zone_path + "/" + BASE_FILE_NAME

            lines_to_write = []
            substring_to_look_for = '.{}.{}'.format(bucket_id, base_domain)
            with open(dest_file) as f1:
                for line in f1:

                    if substring_to_look_for in line:
                        if file_version == 'first':
                            line_temp = "*.{}.{}  IN A {}\n".format(bucket_id, base_domain, first_web_ip)
                        elif file_version == 'second':
                            line_temp = "*.{}.{}  IN A {}\n".format(bucket_id, base_domain, second_web_ip)
                        elif file_version == 'remove':
                            line_temp = ";{}".format(line)
                        lines_to_write.append(line_temp)
                    else:
                        lines_to_write.append(line)

            with open(dest_file, "w") as f1:
                for line in lines_to_write:
                    f1.write(line)

            bashCommand = bash_cmd_edit
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                raise Exception

            a = 1
            return Response({'success': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BindInitView(APIView):
    def get(self, request):
        try:
            bucket_number = int(request.GET.get('total', None))
            ttl = int(request.GET.get('ttl', None))

            dest_file = zone_path + "/" + BASE_FILE_NAME

            lines_to_write = []
            substring_to_look_for = "Other A records"
            with open(dest_file) as f1:
                for line in f1:
                    if '$TTL' in line:
                        line_temp = '$TTL\t{}\n'.format(ttl)
                        lines_to_write.append(line_temp)
                    elif substring_to_look_for in line:
                        lines_to_write.append(line)
                        for bucket_index in range(1, bucket_number + 1):
                            line_temp = "*.{}.{}  IN A {}\n".format(bucket_index, base_domain, first_web_ip)
                            lines_to_write.append(line_temp)
                        line_temp = "* IN A {}\n".format(first_web_ip)
                        lines_to_write.append(line_temp)
                        break

                    else:
                        lines_to_write.append(line)

            with open(dest_file, "w") as f1:
                for line in lines_to_write:
                    f1.write(line)

            bashCommand = bash_cmd_init
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                raise Exception

            a = 1
            return Response({'success': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DemoView(APIView):
    def get(self, request):
        try:
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False, 'error': "error"}, status=status.HTTP_400_BAD_REQUEST)

