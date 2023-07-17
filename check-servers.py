import os
import sys
import platform
import time
import signal

def ping_server(server):
    if platform.system().lower() == 'windows':
        response = os.system(f"ping -n 1 -w 1000 {server} > nul 2>&1")
    else:
        response = os.system(f"ping -c 1 -W 1 {server} > /dev/null 2>&1")
    
    if response == 0:
        return 'OK'
    else:
        return 'UNREACHABLE'

def check_servers(servers):
    count = 1
    while True:
        results = []
        start_time = time.time()
        for server in servers:
            result = ping_server(server)
            results.append(result)

        elapsed_time = time.time() - start_time
        print(','.join([str(count)] + results))
        count += 1
        if elapsed_time < 1:
            time.sleep(1 - elapsed_time)

def signal_handler(signal, frame):
    print('Ctrl-C pressed. Exiting...')
    sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python check-servers.py server1 server2 ...')
        sys.exit(1)

    servers = sys.argv[1:]
    signal.signal(signal.SIGINT, signal_handler)
    check_servers(servers)
