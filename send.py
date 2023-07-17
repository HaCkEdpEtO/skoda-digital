import socket
import sys
import time

def send_udp_packets(target_ip, period):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet_count = 0

    while True:
        try:
            current_time = time.time()
            sock.sendto(str(current_time).encode(), (target_ip, 12345))
            packet_count += 1
            time.sleep(period / 1000)
        except KeyboardInterrupt:
            break

    sock.close()
    print("sent datagrams:", packet_count)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: send.py <target_ip> <period_ms>")
        sys.exit(1)

    target_ip = sys.argv[1]
    period = int(sys.argv[2])
    send_udp_packets(target_ip, period)
