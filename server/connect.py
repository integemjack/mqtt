from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess, os
import urllib
import uuid
import signal

host = ('', 80)
pid = 0
 
class Resquest(BaseHTTPRequestHandler):
    timeout = 5
    server_version = "ROS"
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()

        paths = self.path.split('?',1)
        print(paths)
        path = paths[0]
        if len(paths) == 1:
            return self.wfile.write('No this function!'.encode())
        self.queryString=urllib.parse.unquote(paths[1])       
        params=urllib.parse.parse_qs(self.queryString)     
        print(params)

        topic = params['machineid'][0]
        ips = params['mqtt_ip'][0].split(':',1)
        ip = ips[0]
        port = ips[1]
        global pid

        buf = 'no function'
        print('machineId: "', machineId(), '"  topic: ', topic)
        if machineId() != topic:
            return self.wfile.write('No this device!'.encode())

        if path == '/connect':
            cmd = "sed -i \"s/host: localhost/host: {}/g\" /home/nvidia/mqtt_ws/src/mqtt/config/demo_params.yaml && sed -i \"s/port: 1883/port: {}/g\" /home/nvidia/mqtt_ws/src/mqtt/config/demo_params.yaml && chmod +x -R /home/nvidia/mqtt_ws && cd /home/nvidia/mqtt_ws/devel && source setup.bash && roslaunch mqtt_bridge demo.launch".format(
                ip, port)
            print("Command: ", cmd)
            self.proc = subprocess.Popen(
                cmd, shell=True, executable="/bin/bash", preexec_fn=os.setsid)
            buf = 'ok'
            pid = self.proc.pid

        elif path == '/stop':
            print("pid", pid)
            try:
                # print("id:", self.proc)
                # self.proc.terminate()
                # self.proc.wait()
                if pid != 0:
                  os.killpg(pid, signal.SIGTERM)
                  print("stoped!")
                  buf = 'ok'
                else:
                  print("no stop!")
                  buf = 'no stop!'
            except:
                print("no ros to stop...")
                buf = 'no ros to stop...'

        elif path == '/status':
            buf = 'ok'

        self.wfile.write(buf.encode())
 
    def do_POST(self):
        # datas = self.rfile.read(int(self.headers['content-length']))
        #datas = urllib.unquote(datas).decode("utf-8", 'ignore')
 
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.end_headers()
 
        html = '''No Data!!!'''
        self.wfile.write(html.encode())

def readFile(file):
  file_object = open(file)
  try:
    all_the_text = file_object.read()
  finally:
    file_object.close()
  return all_the_text

def writeFile(file, all_the_text):
  file_object = open(file, 'w')
  file_object.write(all_the_text)
  file_object.close()

def machineId():
  try:
    mid = readFile('/machineId')
  except:
    mid = uuid.uuid4()
    writeFile('/machineId', str(mid) + '')

  if (mid == ''):
    mid = uuid.uuid4()
    writeFile('/machineId', str(mid) + '')
  return mid.strip()

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()