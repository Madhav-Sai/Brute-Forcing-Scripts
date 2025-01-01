# Brute Forcing Scripts

This repository contains Python scripts for performing **brute-force attacks** and **dictionary attacks**. These scripts are designed for **educational purposes** to demonstrate the importance of strong security practices and the vulnerabilities of weak authentication mechanisms.

---

## Scripts Included

1. **PIN Brute Forcing Script**:
   - Tests all 4-digit numeric PINs (0000–9999).
   - Uses asynchronous requests to speed up the brute-forcing process.

2. **Dictionary Attack Script**:
   - Tests a list of common passwords from the [SecLists GitHub repository](https://github.com/danielmiessler/SecLists).
   - Utilizes concurrency to enhance efficiency and halts execution upon finding the correct password.

---

## Dictionary Attack Script

### Features

- **Dynamic Password List**: Downloads the latest list of common passwords from the web.
- **Asynchronous Execution**: Leverages `aiohttp` and `asyncio` to perform multiple requests concurrently.
- **Concurrency Management**: Limits the number of concurrent requests to avoid overwhelming the server.
- **Early Termination**: Stops the attack once the correct password is found.

---

### Prerequisites

1. **Python 3.7+**: Ensure Python is installed on your system. Check the version using:
   ```bash
   python --version
   ```
2. **Install Dependencies**: Use `pip` to install the required library:
   ```bash
   pip install aiohttp
   ```

---

### How to Run

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Madhav-Sai/Brute-Forcing-Scripts.git
   cd Brute-Forcing-Scripts
   ```

2. **Edit Script**:
   Update the `ip` and `port` variables in the script with the target server details.

3. **Run the Script**:
   Execute the script from the terminal:
   ```bash
   python dictionary_attack.py
   ```

---

### Example Output

```plaintext
🚀 Starting dictionary attack...
🔄 Downloading password list...
✅ Password list downloaded: 500 passwords.
Attempted password: 123456
Attempted password: password
✅ Correct password found: qwerty
🏴 Flag: {example_flag_here}
🎯 Attack completed.
```

---

## Legal Disclaimer

This repository is intended for **educational purposes only**. Use these scripts **only** on systems where you have explicit permission to perform penetration testing. Unauthorized use of these scripts is illegal and unethical.

---




