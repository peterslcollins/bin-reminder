# 🗑️ Bin Reminder

A simple Python script that sends a daily email reminder to put the bins out, based on your council's collection schedule.

---

## 🔧 What It Does

- Scrapes your local council website to find your bin collection dates.
- Checks which bins are due **tomorrow**.
- Sends you a helpful email reminder only once per day.
- Logs errors and notifications.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/peterslcollins/bin-reminder.git
cd bin-reminder
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add config file
Create a config.json file in the root folder like this:

```json
{
  "address": "123 Street Name, Suburb, State",
  "email": {
    "sender": "your.sender@gmail.com",
    "recipient": "your.real.email@example.com",
    "app_password": "your_generated_gmail_app_password"
  }
}
```

⚠️ Tip: Don’t use your main Gmail account! Create a separate Gmail and generate an app password.

### 5. Schedule to run daily
You can use windows Task Scheduler