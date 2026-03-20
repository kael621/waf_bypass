#!/usr/bin/env python3

import requests
import re
import sys
import socket
import os
import json
import urllib3
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

urllib3.disable_warnings()

R  = "\033[91m"
Y  = "\033[93m"
G  = "\033[92m"
B  = "\033[94m"
C  = "\033[96m"
M  = "\033[95m"
W  = "\033[0m"
BD = "\033[1m"
DM = "\033[2m"

def clr(text, *codes):
    return f"\033[{';'.join(str(x) for x in codes)}m{text}\033[0m"

def clear():
    os.system("clear" if os.name != "nt" else "cls")
def banner():
    print(clr("""
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡿⠇⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠀⠀⠀⡸⣞⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⢀⣧⢿⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢴⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⣼⣞⡿⣞⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀⣰⣟⢾⣽⢫⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣠⢤⣶⡻⣞⣿⣺⢯⣽⣳⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⣄⡀⠀⠀⠀⠀⠙⢦⡀⠀⠀⠀⠀⣀⣠⣤⣿⣽⣻⢾⣽⣷⣾⣽⣻⣞⣷⣳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⣿⣶⣄⡀⠀⠀⠀⣉⣲⣴⢶⣞⡿⣽⣞⡷⣯⢿⡽⣞⣿⠟⠋⠁⠉⠈⠳⣟⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⢶⣾⣿⡽⣯⣟⡾⣽⡷⣯⣟⡽⡾⣽⡯⠁⠀⠀⠀⠀⠀⠀⢮⣭⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢞⣿⣿⢯⡿⣿⣯⣟⣷⣯⢿⣳⣟⡷⣽⣼⣻⣽⠀⠀⠀⠀⠀⠀⠀⢀⣼⡯⡗⠋⠤⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⣯⣽⣾⣿⣾⣗⡿⣯⡷⣯⣟⡷⣞⣼⣿⣀⠀⠀⠀⠀⢀⣠⡿⣏⡗⠈⠐⠈⠅⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠛⠏⠉⠉⠽⢟⢿⣿⣿⣿⣿⣷⣻⢾⡽⣞⡷⠄⡹⣶⢿⣻⢿⣻⡽⢯⣼⢦⠶⠁⠈⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣯⠇⠀⠀⠀⠀⠀⠁⣽⣿⣿⣿⣷⣯⣿⣽⣛⡦⠀⠀⢩⣿⣹⢯⣷⢻⣟⠺⢣⡖⣘⠤⠓⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢈⣿⡃⠁⠀⠀⠀⢀⣤⣾⣟⢿⣻⣿⣿⣟⡾⣽⡳⠄⠎⢳⣯⢯⣟⡾⢯⣞⣯⣓⠉⢀⠀⠀⡄⢢⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣷⣷⣶⣳⣶⣺⣿⣿⣳⢯⣟⣿⣿⣳⢯⠛⠅⠃⠀⠀⣴⣿⡿⣬⢶⠾⠙⣊⣥⠾⡒⠊⢁⢠⠣⣌⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⡽⣾⡽⣯⣟⣿⡿⣯⣿⣿⣾⢿⣿⠳⢏⣈⢠⠀⠀⣰⢿⡿⣽⣉⡶⠌⠋⠉⣀⡀⠁⠀⠀⠀⣘⡐⣂⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣽⣳⣟⣳⣟⣾⣽⣿⣿⣿⣿⣿⣦⣜⡻⡽⠆⠧⣴⡟⣯⢟⡳⣭⠲⠄⠐⠀⠀⠀⠈⠁⠉⠑⢊⡕⢃⠄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣾⣿⣯⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣾⢧⠀⠹⠾⡵⡞⡽⢢⣃⠐⠀⠀⠄⡐⠀⠀⠀⡘⢦⠘⣌⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠒⡈⠀⡀⠄⡑⠢⣉⠴⣈⣆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢯⣏⡴⣶⣵⣢⢤⢠⡀⡄⢠⠐⡰⢌⡱⠀⡁⡀⠆⡥⠆⡥⣛⡽⣾
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠔⠉⠀⠀⢽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣻⢷⣯⡽⣞⣷⣻⡼⣡⢋⡔⠣⠜⡐⢐⠠⡓⣤⣙⣲⣽⣻⢷
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡿⣽⣞⣷⣻⡴⣣⢜⡱⣊⡕⣊⠠⡙⡰⣭⢷⣯⣿⢿    """, 96, 1))
    print(clr("  WAF / CDN Bypass — Real IP Discovery Tool", 93, 1))
    print(clr("  ─────────────────────────────────────────────────────────────────────", 90))
    print(clr("  Shodan · SecurityTrails · CRT.sh · DNS History · MX · SPF · Favicon", 2))
    print()



def section(title):
    bar = "─" * 64
    print(f"\n{clr('┌' + bar + '┐', 96)}")
    pad = 64 + 14
    print(f"{clr('│', 96)}  {clr(title, 93, 1):<{pad}}{clr('│', 96)}")
    print(f"{clr('└' + bar + '┘', 96)}")

def ask(prompt, default=""):
    arrow = clr("  ❯ ", 96)
    d = clr(f"  [{default}]", 2) if default else ""
    try:
        val = input(f"{arrow}{clr(prompt, 97, 1)}{d} : ").strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{Y}  Saliendo...{W}\n")
        sys.exit(0)
    return val if val else default

def log_find(ip, source, detail="", confidence="medium"):
    conf_colors = {"high": (R, "★★★ HIGH"), "medium": (Y, "★★☆ MED "), "low": (G, "★☆☆ LOW ")}
    color, label = conf_colors.get(confidence, (W, "???"))
    print(f"  {clr('►', 91, 1)} {clr(ip, 97, 1):<18} {color}{label}{W}  {clr(f'[{source}]', 96):<30} {clr(detail, 2)}")

def log_info(msg, color=DM):
    print(f"  {clr('·', 90)} {color}{msg}{W}")

def log_warn(msg):
    print(f"  {clr('⚠', 93)}  {Y}{msg}{W}")

def log_ok(msg):
    print(f"  {clr('✔', 92)}  {G}{msg}{W}")


BROWSER_UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0"}

CDN_RANGES = {
    "Cloudflare":   ["173.245.48.0/20","103.21.244.0/22","103.22.200.0/22","103.31.4.0/22",
                     "141.101.64.0/18","108.162.192.0/18","190.93.240.0/20","188.114.96.0/20",
                     "197.234.240.0/22","198.41.128.0/17","162.158.0.0/15","104.16.0.0/13",
                     "104.24.0.0/14","172.64.0.0/13","131.0.72.0/22"],
    "Akamai":       ["23.0.0.0/8","23.192.0.0/11","104.64.0.0/10","2.16.0.0/13","96.6.0.0/15"],
    "Fastly":       ["23.235.32.0/20","43.249.72.0/22","103.244.50.0/24","103.245.222.0/23",
                     "104.156.80.0/20","151.101.0.0/16","157.52.64.0/18","167.82.0.0/17",
                     "172.111.64.0/18","185.31.16.0/22","199.27.72.0/21","199.232.0.0/16"],
    "Sucuri":       ["192.88.134.0/23","185.93.228.0/22","66.248.200.0/22","208.109.0.0/18"],
    "Incapsula":    ["199.83.128.0/21","198.143.32.0/19","149.126.72.0/21","103.28.248.0/22",
                     "45.64.64.0/22","185.11.124.0/22","192.230.64.0/18"],
    "AWS CloudFront":["13.32.0.0/15","13.35.0.0/16","52.84.0.0/15","54.182.0.0/16",
                      "54.192.0.0/16","54.230.0.0/16","54.239.128.0/18","99.84.0.0/16",
                      "205.251.192.0/19","216.137.32.0/19"],
    "Google":       ["34.0.0.0/8","35.0.0.0/8","130.211.0.0/22","35.191.0.0/16"],
}

def detect_cdn(ip):
    try:
        addr = ipaddress.ip_address(ip)
        for cdn, ranges in CDN_RANGES.items():
            for cidr in ranges:
                if addr in ipaddress.ip_network(cidr, strict=False):
                    return cdn
    except:
        pass
    return None


def get_current_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None


def check_shodan(domain, api_key=None):
    found = []
    if not api_key:
        try:
            r = requests.get(
                f"https://www.shodan.io/search?query=hostname%3A{domain}",
                timeout=10, headers=BROWSER_UA)
            ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', r.text)
            for ip in set(ips):
                if not detect_cdn(ip):
                    found.append((ip, "Shodan Web", "found in page source"))
        except:
            pass
    else:
        try:
            r = requests.get(
                f"https://api.shodan.io/shodan/host/search?key={api_key}&query=hostname:{domain}",
                timeout=10)
            data = r.json()
            for match in data.get("matches", []):
                ip = match.get("ip_str", "")
                org = match.get("org", "")
                port = match.get("port", "")
                if ip and not detect_cdn(ip):
                    found.append((ip, "Shodan API", f"org={org} port={port}"))
        except:
            pass
    return found


def check_censys(domain):
    found = []
    try:
        r = requests.get(
            f"https://search.censys.io/api/v1/search/certificates?q={domain}&fields=parsed.subject_dn,ip_addresses",
            timeout=10, headers=BROWSER_UA)
        ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', r.text)
        for ip in set(ips):
            if not detect_cdn(ip):
                found.append((ip, "Censys", "SSL cert match"))
    except:
        pass
    return found


def check_crtsh_ips(domain):
    found = []
    try:
        r = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=15, headers=BROWSER_UA)
        subdomains = set()
        for e in r.json():
            for s in e.get("name_value", "").split("\n"):
                s = s.strip().lstrip("*.").lower()
                if s.endswith(domain):
                    subdomains.add(s)
        for sub in list(subdomains)[:30]:
            try:
                ip = socket.gethostbyname(sub)
                cdn = detect_cdn(ip)
                if not cdn:
                    found.append((ip, "CRT.sh subdomain", f"via {sub}"))
            except:
                pass
    except:
        pass
    return found


def check_dns_history(domain):
    found = []
    sources = [
        f"https://api.hackertarget.com/hostsearch/?q={domain}",
        f"https://api.hackertarget.com/dnslookup/?q={domain}",
    ]
    for url in sources:
        try:
            r = requests.get(url, timeout=10, headers=BROWSER_UA)
            ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', r.text)
            for ip in set(ips):
                if not detect_cdn(ip) and not ip.startswith(("127.", "0.", "255.")):
                    found.append((ip, "HackerTarget DNS", f"from {url.split('?')[0].split('/')[-1]}"))
        except:
            pass

    try:
        r = requests.get(
            f"https://viewdns.info/iphistory/?domain={domain}",
            timeout=10, headers=BROWSER_UA)
        ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', r.text)
        for ip in set(ips):
            if not detect_cdn(ip) and not ip.startswith(("127.", "0.", "255.")):
                found.append((ip, "ViewDNS History", "historical DNS record"))
    except:
        pass

    return found


def check_mx_spf(domain):
    found = []
    try:
        r = requests.get(f"https://api.hackertarget.com/dnslookup/?q={domain}", timeout=10, headers=BROWSER_UA)
        for line in r.text.splitlines():
            if " MX " in line or " A " in line or " TXT " in line:
                ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', line)
                for ip in ips:
                    if not detect_cdn(ip) and not ip.startswith(("127.", "0.", "255.")):
                        record_type = "MX" if "MX" in line else ("SPF" if "TXT" in line else "A")
                        found.append((ip, f"DNS {record_type} Record", line.strip()[:60]))
    except:
        pass

    try:
        r = requests.get(f"https://api.hackertarget.com/dnslookup/?q=mail.{domain}", timeout=8, headers=BROWSER_UA)
        ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', r.text)
        for ip in ips:
            if not detect_cdn(ip) and not ip.startswith(("127.", "0.", "255.")):
                found.append((ip, "Mail subdomain", f"mail.{domain}"))
    except:
        pass

    return found


def check_favicon(domain):
    found = []
    try:
        r = requests.get(f"https://{domain}/favicon.ico", timeout=8,
                         headers=BROWSER_UA, verify=False, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 0:
            import hashlib
            import struct
            import base64
            raw = r.content
            m = hashlib.md5(raw).hexdigest()
            b64 = base64.encodebytes(raw).decode().strip()
            h = 0
            for i in range(0, len(b64), 4):
                chunk = b64[i:i+4]
                try:
                    val = struct.unpack('>I', bytes(chunk.encode('utf-8').ljust(4, b'\x00')))[0]
                    h = (h * 37 + val) & 0xFFFFFFFF
                except:
                    pass

            shodan_hash_url = f"https://www.shodan.io/search?query=http.favicon.hash:{h}"
            found.append((shodan_hash_url, "Favicon Hash", f"MD5={m[:12]}... → search in Shodan"))
    except:
        pass
    return found


def check_securitytrails(domain):
    found = []
    try:
        r = requests.get(
            f"https://securitytrails.com/domain/{domain}/history/a",
            timeout=10, headers=BROWSER_UA)
        ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', r.text)
        for ip in set(ips):
            if not detect_cdn(ip) and not ip.startswith(("127.", "0.", "255.")):
                found.append((ip, "SecurityTrails", "DNS A record history"))
    except:
        pass
    return found


def check_wayback_ip(domain):
    found = []
    try:
        r = requests.get(
            f"http://web.archive.org/cdx/search/cdx?url={domain}&output=json&fl=original,statuscode,timestamp&limit=20&filter=statuscode:200",
            timeout=15, headers=BROWSER_UA)
        data = r.json()
        for row in data[1:]:
            url = row[0]
            ips = re.findall(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', url)
            for ip in ips:
                if not detect_cdn(ip):
                    found.append((ip, "Wayback Machine", f"found in archived URL"))
    except:
        pass
    return found


def check_subdomain_direct(domain):
    found = []
    common_subs = [
        "mail", "smtp", "ftp", "cpanel", "whm", "webmail", "direct",
        "origin", "backend", "api", "dev", "staging", "test", "old",
        "admin", "portal", "vpn", "remote", "git", "jenkins",
        "autodiscover", "autoconfig", "ns1", "ns2", "mx", "mx1", "mx2",
    ]
    for sub in common_subs:
        host = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(host)
            cdn = detect_cdn(ip)
            if not cdn:
                found.append((ip, "Direct subdomain", f"{host} → not behind CDN"))
        except:
            pass
    return found


def verify_ip(ip, domain):
    results = []
    for scheme in ["https", "http"]:
        for host_header in [domain, f"www.{domain}"]:
            try:
                r = requests.get(
                    f"{scheme}://{ip}",
                    headers={**BROWSER_UA, "Host": host_header},
                    timeout=6, verify=False, allow_redirects=False)
                code = r.status_code
                server = r.headers.get("Server", "")
                loc = r.headers.get("Location", "")
                cookie = r.headers.get("Set-Cookie", "")

                domain_in_cookie = domain in cookie
                domain_in_loc    = domain in loc

                cdn_server = any(c in server.lower() for c in
                                 ["cloudfront", "cloudflare", "akamai", "fastly",
                                  "incapsula", "imperva", "edgecast"])
                confidence = "low"
                if cdn_server:
                    confidence = "low"
                elif domain_in_cookie or domain_in_loc:
                    confidence = "high"
                elif code in [200, 301, 302, 403]:
                    confidence = "medium"

                results.append({
                    "ip": ip, "scheme": scheme, "host_header": host_header,
                    "status": code, "server": server, "location": loc[:80],
                    "domain_in_response": domain_in_cookie or domain_in_loc,
                    "confidence": confidence
                })
                break
            except:
                continue
        if results:
            break
    return results


def whois_org(ip):
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=6, headers=BROWSER_UA)
        d = r.json()
        return d.get("org", ""), d.get("country", ""), d.get("city", "")
    except:
        return "", "", ""


def run_all(domain, shodan_key):
    section("① Detectando CDN/WAF actual")
    current_ip = get_current_ip(domain)
    if current_ip:
        cdn = detect_cdn(current_ip)
        if cdn:
            log_warn(f"Dominio protegido por {cdn} → IP actual: {current_ip}")
        else:
            log_ok(f"No se detectó CDN conocido → IP actual: {current_ip}")
    else:
        log_warn("No se pudo resolver el dominio")
        return {}

    all_candidates = {}

    def add(findings, source_label):
        for item in findings:
            ip, source, detail = item
            if ip not in all_candidates:
                all_candidates[ip] = {"source": source, "detail": detail}

    section("② Buscando IP real — fuentes pasivas")

    checks = [
        ("Shodan",           lambda: check_shodan(domain, shodan_key)),
        ("SecurityTrails",   lambda: check_securitytrails(domain)),
        ("CRT.sh IPs",       lambda: check_crtsh_ips(domain)),
        ("DNS History",      lambda: check_dns_history(domain)),
        ("MX / SPF Records", lambda: check_mx_spf(domain)),
        ("Wayback Machine",  lambda: check_wayback_ip(domain)),
        ("Subdomain Direct", lambda: check_subdomain_direct(domain)),
        ("Censys",           lambda: check_censys(domain)),
    ]

    for label, fn in checks:
        print(f"  {C}◌{W} {label:<25}", end="", flush=True)
        try:
            results = fn()
            unique = list({r[0]: r for r in results}.values())
            for item in unique:
                add([item], label)
            status = clr(f"{len(unique)} encontradas", 92, 1) if unique else clr("0", 90)
            print(f"\r  {G}✔{W} {label:<25} {status}")
        except Exception as e:
            print(f"\r  {Y}⚠{W} {label:<25} {clr('error', 91)}")

    favicon_results = check_favicon(domain)
    if favicon_results:
        section("③ Favicon Hash")
        for url, source, detail in favicon_results:
            print(f"  {C}►{W} {detail}")
            print(f"    {clr('→ Busca en Shodan:', 93)} {clr(url, 96)}")

    return all_candidates


def verify_candidates(candidates, domain):
    section("④ Verificando candidatos contra el dominio")
    if not candidates:
        log_warn("No se encontraron IPs candidatas fuera del CDN")
        return []

    print(f"  {C}◌{W} Verificando {clr(str(len(candidates)), 97)} IPs con Host header {clr(domain, 93)}...\n")
    confirmed = []

    for ip, meta in candidates.items():
        org, country, city = whois_org(ip)
        verifications = verify_ip(ip, domain)

        for v in verifications:
            conf = v["confidence"]
            detail = f"HTTP {v['status']} | Server: {v['server']}" + (f" | Loc: {v['location']}" if v["location"] else "")
            log_find(ip, meta["source"], detail, conf)
            if org:
                log_info(f"  ASN/Org: {org} | {city}, {country}", DM)
            if v["domain_in_response"]:
                print(f"    {clr('✓ Dominio encontrado en la respuesta — Alta confianza', 92, 1)}")
            confirmed.append({**v, "ip": ip, "org": org, "country": country, "source": meta["source"]})
            break

    return confirmed


def save_report(domain, confirmed, all_candidates):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"waf_bypass_{domain}_{ts}.txt"
    with open(fname, "w") as f:
        f.write(f"WAF Bypass Report — {domain} — {datetime.now()}\n")
        f.write("=" * 70 + "\n\n")
        f.write("ALL CANDIDATE IPs (non-CDN):\n")
        for ip, meta in all_candidates.items():
            org, country, city = whois_org(ip)
            f.write(f"  {ip:<20} [{meta['source']}] {meta['detail']} | {org} {city} {country}\n")
        f.write("\nVERIFIED CANDIDATES:\n")
        for v in confirmed:
            f.write(f"  {v['ip']:<20} {v['confidence'].upper():<6} HTTP {v['status']} | {v['server']} | {v['org']}\n")
            if v["location"]:
                f.write(f"    Location: {v['location']}\n")
    return fname


def summary(domain, all_candidates, confirmed, fname):
    section("⑤ Resumen")
    high   = [v for v in confirmed if v["confidence"] == "high"]
    medium = [v for v in confirmed if v["confidence"] == "medium"]
    low    = [v for v in confirmed if v["confidence"] == "low"]

    print(f"  {R}★★★{W}  Confirmadas (alta)    {clr(str(len(high)), 91, 1)}")
    print(f"  {Y}★★☆{W}  Probables (media)     {clr(str(len(medium)), 93, 1)}")
    print(f"  {G}★☆☆{W}  Posibles (baja)       {clr(str(len(low)), 92, 1)}")
    print(f"  {B}»{W}   Total candidatas     {clr(str(len(all_candidates)), 97, 1)}")
    print(f"  {C}»{W}   Reporte guardado     {clr(fname, 96)}")

    if high:
        print(f"\n  {clr('IPs de alta confianza:', 92, 1)}")
        for v in high:
            print(f"    {clr('►', 91, 1)} {clr(v['ip'], 97, 1)}  {clr(v['org'], 2)}")
        print()
        print(f"  {clr('Verifica manualmente:', 93, 1)}")
        for v in high:
            ip_val = v["ip"]
            cmd = f'curl -sk -H "Host: {domain}" https://{ip_val} -I'
            print(f"    {clr(cmd, 96)}")
    print()


def main():
    clear()
    banner()
    section("⚙  Configuración")
    print()

    raw = ask("URL o dominio objetivo  (ej: tesla.com  o  https://tesla.com)")
    if not raw:
        print(R + "  Error: introduce un dominio." + W)
        sys.exit(1)

    domain = raw.replace("https://", "").replace("http://", "").split("/")[0].strip().lower()
    if domain.startswith("www."):
        domain = domain[4:]

    print(f"\n  {G}✔{W} Target: {clr(domain, 97, 1)}\n")

    print(f"  {clr('Shodan API Key (opcional — mejora resultados):', 97, 1)}")
    print(f"  {DM}  Déjalo vacío para usar scraping web básico{W}")
    shodan_key = ask("  Shodan API Key", "")
    print()

    clear()
    banner()
    print(f"  {G}▶{W} Buscando IP real de {clr(domain, 97, 1)}\n")

    all_candidates = run_all(domain, shodan_key)
    confirmed      = verify_candidates(all_candidates, domain)
    fname          = save_report(domain, confirmed, all_candidates)
    summary(domain, all_candidates, confirmed, fname)


if __name__ == "__main__":
    main()
