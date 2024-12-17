# chartink-stock-scanner
A Python automation project to scan high-momentum stocks on Chartink and add them to a TradingView watchlist.
# Chartink Stock Scanner Automation

🚀 **Automates high-momentum stock scanning and TradingView watchlist creation**.

# Chartink Stock Scanner Automation 🚀

## **Overview**
This Python project automates stock scanning on **Chartink** and adds high-momentum stocks to a **TradingView** watchlist. It helps traders capture quick gains within the first 15 minutes of market opening.

---

## **Problem**
Manually scanning and transferring stocks wastes time. This project:
- Runs three **Chartink scanners** simultaneously.
- Sorts stocks by **Volume**.
- Adds the top 15 stocks (5 from each scanner) to TradingView automatically.

---

## **Features**
- 🕒 **Speed**: Executes scans and updates watchlist within 2 minutes.
- 🔎 **Automation**: Reduces manual effort in scanning and adding stocks.
- 📊 **Integration**: Supports Chartink scanners and TradingView.

---

## **Technologies Used**
- **Python**
- **Selenium** (Web Automation)
- **Subprocess**
- **ActionChains** (Selenium for mouse actions)

---

## **Setup**

### Prerequisites:
- Install Python 3 and ChromeDriver.
- Install required libraries:
   ```bash
   pip install selenium pyperclip
