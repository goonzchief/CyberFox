import socket
import dns.resolver
import requests
import logging
import argparse
import shodan
import ssl
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from io import BytesIO
from OpenSSL import crypto
from base64 import b64decode

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_subdomains(domain, subdomains):
    ips = {}
    for sub in subdomains:
        subdomain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(subdomain)
            ips[subdomain] = ip
        except socket.gaierror:
            logging.debug(f"{subdomain} not found.")
    return ips

def fetch_ssl_certificates(domain):
    crtsh_url = f"https://crt.sh/?q={domain}&output=json"
    try:
        response = requests.get(crtsh_url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch SSL data: {e}")
        return []

def parse_certificates(certificates):
    for cert in certificates:
        logging.info(f"Issued To: {cert.get('common_name')}")
        logging.info(f"Issued By: {cert.get('issuer_name')}")
        logging.info(f"Serial Number: {cert.get('serial_number')}")
        logging.info("-" * 40)

def search_shodan(api_key, domain):
    api = shodan.Shodan(api_key)
    try:
        results = api.search(domain)
        logging.info(f"Total results: {results['total']}")
        for result in results['matches']:
            logging.info(f"IP: {result['ip_str']} | Port: {result['port']} | Org: {result.get('org', 'N/A')}")
    except shodan.APIError as e:
        logging.error(f"Shodan error: {e}")

def reverse_dns_lookup(ip):
    try:
        result = socket.gethostbyaddr(ip)
        return result[0]
    except socket.herror:
        return None

def attempt_zone_transfer(domain):
    try:
        ns_records = dns.resolver.resolve(domain, 'NS')
        for ns in ns_records:
            ns_ip = dns.resolver.resolve(ns.target, 'A')[0].to_text()
            logging.info(f"Attempting zone transfer on {ns.target} ({ns_ip})")
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_ip, domain))
                for name in zone.nodes.keys():
                    logging.info(f"Record found: {name}.{domain}")
            except Exception as e:
                logging.error(f"Zone transfer failed on {ns.target} ({ns_ip}): {e}")
    except Exception as e:
        logging.error(f"DNS resolution error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Investigate a domain's real IP behind a CDN.")
    parser.add_argument('domain', type=str, help='Target domain name')
    parser.add_argument('--shodan_api_key', type=str, help='API key for Shodan search')
    args = parser.parse_args()

    domain = args.domain

    logging.info(f"Finding subdomain IPs for {domain}")
    subdomains = ['www', 'api', 'mail', 'ftp', 'dev', 'test', 'staging', 'admin', 'cpanel', 'blog']
    subdomain_ips = check_subdomains(domain, subdomains)
    for subdomain, ip in subdomain_ips.items():
        logging.info(f"{subdomain}: {ip}")

    logging.info(f"Fetching SSL certificates for {domain}")
    certificates = fetch_ssl_certificates(domain)
    parse_certificates(certificates)

    if args.shodan_api_key:
        logging.info(f"Searching Shodan for {domain}")
        search_shodan(args.shodan_api_key, domain)
    else:
        logging.info("No Shodan API key provided, skipping Shodan search.")

    for subdomain, ip in subdomain_ips.items():
        reverse_dns = reverse_dns_lookup(ip)
        if reverse_dns:
            logging.info(f"Reverse DNS for {ip}: {reverse_dns}")
        else:
            logging.info(f"No reverse DNS record for {ip}")

    logging.info(f"Attempting zone transfer for {domain}")
    attempt_zone_transfer(domain)

if __name__ == "__main__":
    main()
