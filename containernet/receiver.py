import socket
import struct

def receive_ping():
    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        try:
            while True:
                packet_data, address = sock.recvfrom(1024)
                icmp_header = struct.unpack('!BBHHH', packet_data[20:28])
                if icmp_header[0] == 8:
                    print(f"Ping received from {address[0]}")
        except KeyboardInterrupt:
            print("Ping listener stopped.")

if __name__ == "__main__":
    receive_ping()
