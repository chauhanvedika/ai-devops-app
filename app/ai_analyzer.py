import time

def analyze_logs():
    with open("app.log", "r") as f:
        lines = f.readlines()

    error_count = 0

    for line in lines[-20:]:  # last 20 logs
        if "ERROR" in line:
            error_count += 1

    if error_count > 3:
        print("🚨 ALERT: High error rate detected!")
    else:
        print("✅ System looks healthy")

while True:
    analyze_logs()
    time.sleep(10)