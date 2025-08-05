import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime

def check_iban_validation(iban):
    url = "https://www.iban-rechner.de/iban_validieren.html"
    payload = {
        "tx_valIBAN_pi1[iban]": iban,
        "tx_valIBAN_pi1[fi]": "fi",
        "no_cache": "1",
        "Action": "IBAN prüfen und BIC-Code suchen"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    result_fieldset = None
    for fs in soup.find_all("fieldset"):
        legend = fs.find("legend")
        if legend and "Ergebnis" in legend.text:
            result_fieldset = fs
            break
    if not result_fieldset:
        print("No result found.")
        return
    final_msg = None
    for p in result_fieldset.find_all("p"):
        b_tag = p.find("b")
        if b_tag and "Diese IBAN" in b_tag.text:
            final_msg = p.get_text(strip=True)
            break
    if not final_msg:
        print("Validation message not found.")
        return
    green = "\033[92m"
    red = "\033[91m"
    reset = "\033[0m"
    msg_lower = final_msg.lower()
    if ("nicht korrekt" in msg_lower) or ("falsch" in msg_lower): 
        print(f"{red}{iban} - Incorrect{reset}")
        return False
    elif ("korrekt" in msg_lower) or ("correct" in msg_lower): 
        print(f"{green}{iban} - Correct{reset}")
        return True
    else: 
        print(f"{red}{iban} - {final_msg}{reset}")
        return False

absolute_path = input("Enter the absolut path to the .txt file that contains the IBANs on different lines (Use '/' and not '\\'): ")
input("Press ENTER to start the process: ")
try:
    with open(absolute_path, "r", encoding = "utf-8") as ibans_file:
        ibans_file_checked_absolute_path = os.path.dirname(absolute_path) + "/" + os.path.splitext(os.path.basename(absolute_path))[0] + "_checked.txt"
        with open(ibans_file_checked_absolute_path, "w", encoding = "utf-8") as checked_file:
            checked_file.write(f"\n\n- {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} -\n\n")
            for iban in ibans_file:
                state = check_iban_validation(iban.strip())
                if state: checked_file.write(iban.strip() + " - Correct.\n")
                time.sleep(3)
except Exception as e:
    print("Something went wrong with the process: " + str(e))
print(f"A log file for correct IBANs had been created: {ibans_file_checked_absolute_path}")
input("Press ENTER to end the process: ")
