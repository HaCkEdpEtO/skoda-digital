import socket
import time

def receive_udp_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", 12345))
    packet_count = 0
    delays = []

    try:
        while True:
            data, addr = sock.recvfrom(1024)
            packet_count += 1
            current_time = time.time()
            delays.append(current_time - float(data.decode()))

    except KeyboardInterrupt:
        pass

    sock.close()
    print("received datagrams:", packet_count)
    if delays:
        print("delay min/max: {:.2f}/{:.2f} ms".format(min(delays) * 1000, max(delays) * 1000))

if __name__ == "__main__":
    receive_udp_packets()
