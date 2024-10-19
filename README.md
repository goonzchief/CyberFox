# 🔍 **CyberFox** 🦊
> **A clever fox sniffing out the real IP behind CDNs and more!**

Welcome to **CyberFox**, where curiosity meets powerful network investigation tools. Whether you're hunting down subdomains, searching for SSL certs, or even poking around with zone transfers, **CyberFox** is here to help you **unveil the hidden**. Get ready for some serious sniffing! 🦊✨

![CyberFox Banner](https://media.giphy.com/media/fAxxeV0wX6T44/giphy.gif)

---

## **Features** 🚀

- 🕵️ **Subdomain Hunter**: Discover the hidden IPs behind popular subdomains.
- 🔐 **SSL Cert Tracker**: Fetch SSL certificate data to dig deeper into the domain’s secrets.
- 🌍 **Shodan Digger**: Integrate with Shodan to explore even more about the target (if you’ve got the API key).
- 🧑‍💻 **Reverse DNS Sleuth**: Perform reverse DNS lookups for that extra bit of intel.
- 🌐 **Zone Transfer Attempt**: Try your luck at getting domain zone transfers (careful now! 😉).

---

## **How to Use** 💻

1. Clone the repo:
    ```bash
    git clone https://github.com/goonzchief/cyberfox.git
    cd cyberfox
    ```

2. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the **CyberFox** 🦊 script:
    ```bash
    python cyberfox.py <your-domain> --shodan_api_key <your-shodan-api-key>
    ```

    *Example:*
    ```bash
    python cyberfox.py example.com --shodan_api_key your_shodan_key
    ```

    If you don't have a Shodan key, no worries! You can still use the subdomain, SSL cert, reverse DNS, and zone transfer features without it.

---


## **Under the Hood** 🛠️

**CyberFox** utilizes some of the best-in-class tools to get you results:
- 🦊 **DNS Resolution** with `socket` and `dns.resolver`
- 🔒 **SSL Cert Retrieval** via `crt.sh`
- 🌐 **Shodan** search integration
- 🔎 **Reverse DNS** using `socket.gethostbyaddr`
- 🧠 **Zone Transfer Attempts** with `dns.query`

---

## **Contributing** 🤝

Want to help the fox get even cleverer? Contributions are welcome!

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-branch`).
3. Submit a pull request, and we'll review it together!

---

## **License** 📜

MIT License - Do whatever you want but don’t blame the fox 🦊.

---

## **Stay Updated!** 🌟

Follow this repo to stay updated on all future **CyberFox** features and improvements!

---

**Let the hunt begin with CyberFox!** 🦊
