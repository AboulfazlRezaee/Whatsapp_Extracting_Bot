# 📥 WhatsApp Group Member Extractor

A **Python + Selenium** tool to automatically extract all member phone numbers from a selected WhatsApp group via [web.whatsapp.com](https://web.whatsapp.com) and export them into an **Excel file** (`.xlsx`).

---

## 🚀 Features

* ✅ Logs in via WhatsApp Web (QR Code)
* 📂 Lists all available chats/groups
* 🔍 Lets you select a group by number
* 👥 Extracts phone numbers of group participants
* 📊 Saves results into an Excel file (`group.xlsx`)
* 📈 Shows progress until full extraction (100%)

---

## 🛠️ Requirements

* Python 3.9+
* Google Chrome
* ChromeDriver matching your Chrome version
* WhatsApp account with active groups

Install all Python requirements using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 📆 Installation

```bash
git clone https://github.com/AboulfazlRezaee/Whatsapp_Extracting_Bot.git
cd Whatsapp_Extracting_Bot
pip install -r requirements.txt
```

Make sure you place `chromedriver.exe` in the project root or update the path in the script.

---

## ⚙️ Usage

1. Run the script:

```bash
python whatsapp_group_extractor.py
```

2. Scan the QR code when prompted
3. Choose the group you want to extract
4. Let the script scroll, load, and extract the members
5. Find your output in the generated `group.xlsx` file

---

## 📁 Output

Your exported Excel file will look like this:

| Phone Number  |
| ------------- |
| +989123456789 |
| +989876543210 |

---

## 🧐 How It Works

* Uses **Selenium** to control the browser
* Injects **JavaScript** for efficient data scraping from the DOM
* Extracts numbers only (`+98` prefix used as default, can be changed)
* Handles pagination to scroll through all group members
* Saves the results in an Excel file using **Pandas**

---

## ⚠️ Notes

* This tool **only works for groups where you are a participant**
* Phone numbers are visible only for public or saved contacts, as per WhatsApp's privacy policies
* **Do not use for spam or unsolicited messaging** – this violates WhatsApp’s terms of service

---



## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## ⭐️ Give it a star if you like it!
