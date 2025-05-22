from datetime import datetime, timedelta

from src.config import load_config, NOTIFY_LOG, ERROR_LOG
from src.scraper import scrape_bin_collection
from src.log_utils import append_log, was_notified_today
from src.notify import send_email


def send_notification(bin_info, cfg):
    tomorrow = datetime.now().date() + timedelta(days=1)

    bins_due = []
    for name, info in bin_info.items():
        try:
            # Extract the date from the "next_collection" string
            date_str = info["next_collection"].split("on")[-1].strip()
            collection_date = datetime.strptime(date_str, "%d %B %Y").date()
            if collection_date == tomorrow:
                bins_due.append(name)
        except Exception as e:
            append_log(ERROR_LOG, f"Date parsing error for {name}: {e}")

    if bins_due:
        msg = "🟢 Bins to put out tomorrow:\n" + "\n".join(
            f"{b}: {bin_info[b]['next_collection']}" for b in bins_due
        )
        subject = "🚮 Bin Reminder: Take the bins out tomorrow!"
        send_email(
            subject,
            msg,
            cfg["email"]["sender"],
            cfg["email"]["recipient"],
            cfg["email"]["app_password"],
        )
        append_log(NOTIFY_LOG, f"Sent notification: {msg}")
    else:
        msg = "🟡 No bins due tomorrow. Upcoming collections:\n" + "\n".join(
            f"{b}: {info['next_collection']}" for b, info in bin_info.items()
        )
        append_log(NOTIFY_LOG, f"No notification sent. {msg}")


def run_reminder():
    cfg = load_config()

    try:
        if not was_notified_today(NOTIFY_LOG):
            bin_info = scrape_bin_collection(cfg["address"])
            send_notification(bin_info, cfg)
        else:
            print("Notification already sent today.")
    except Exception as e:
        append_log(ERROR_LOG, f"Error: {str(e)}")
        print(f"Error occurred: {e}")
