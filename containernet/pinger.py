import subprocess

def send_ping(ip_address):
    try:
        subprocess.run(['ping', '-c', '1', ip_address], check=True)
        print(f"Ping sent to {ip_address}")
    except subprocess.CalledProcessError:
        print(f"Failed to send ping to {ip_address}")

if __name__ == "__main__":
    target_ip = '10.0.0.252'
    send_ping(target_ip)
