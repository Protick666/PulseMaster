
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
    bash_cmd = 'sudo service bind9 restart'

BASE_FILE_NAME = 'db.exp.net-measurement.net'

class BindUpdateView(APIView):
    def get(self, request):
        try:
            file_version = request.GET.get('file_version', None)
            ttl = int(request.GET.get('ttl', None))

            if file_version not in ['first', 'second']:
                raise Exception
            source_file = "{}/{}.{}".format(zone_path, BASE_FILE_NAME, file_version)
            dest_file = zone_path + "/" + BASE_FILE_NAME

            with open(source_file) as f:
                with open(dest_file, "w") as f1:
                    for line in f:
                        if '$TTL' in line:
                            line_temp = '$TTL\t{}\n'.format(ttl)
                            f1.write(line_temp)
                        else:
                            f1.write(line)

            bashCommand = bash_cmd
            process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()

            if error is not None:
                raise Exception

            a = 1
            return Response({'success': True}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


