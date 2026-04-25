def analyze_logs():
    try:
        with open("app.log", "r") as f:
            lines = f.readlines()

        recent_logs = lines[-50:]  # analyze last 50 logs

        error_count = 0
        error_types = {
            "database": 0,
            "timeout": 0,
            "other": 0
        }

        severity_score = 0  # 🔥 weighted scoring

        for line in recent_logs:
            if "ERROR" in line:
                error_count += 1

                # -----------------------------
                # 🔹 Classify + weight errors
                # -----------------------------
                if "Database" in line:
                    error_types["database"] += 1
                    severity_score += 3   # DB issues are critical

                elif "Timeout" in line:
                    error_types["timeout"] += 1
                    severity_score += 2   # medium severity

                else:
                    error_types["other"] += 1
                    severity_score += 1   # low severity

        # -----------------------------
        # 🔹 Error rate calculation
        # -----------------------------
        total_logs = len(recent_logs)
        error_rate = error_count / total_logs if total_logs > 0 else 0

        # -----------------------------
        # 🔥 Intelligent decision logic
        # -----------------------------
        if error_count == 0:
            status = "healthy"

        elif error_rate < 0.1 and severity_score < 5:
            status = "warning"

        else:
            status = "critical"

        return {
            "status": status,
            "error_count": error_count,
            "error_rate": round(error_rate, 2),
            "severity_score": severity_score,
            "error_types": error_types,
            "analyzed_logs": total_logs
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }