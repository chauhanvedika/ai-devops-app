def analyze_logs():
    try:
        with open("app.log", "r") as f:
            lines = f.readlines()

        recent_logs = lines[-50:]  # analyze last 50 logs
        error_count = 0
        error_types = {}

        for line in recent_logs:
            if "ERROR" in line:
                error_count += 1

                # classify errors
                if "Database" in line:
                    error_types["database"] = error_types.get("database", 0) + 1
                elif "Timeout" in line:
                    error_types["timeout"] = error_types.get("timeout", 0) + 1
                else:
                    error_types["other"] = error_types.get("other", 0) + 1

        # -----------------------------
        # 🔥 Intelligent decision logic
        # -----------------------------
        if error_count == 0:
            status = "healthy"
        elif error_count <= 3:
            status = "warning"
        else:
            status = "critical"

        return {
            "status": status,
            "error_count": error_count,
            "error_types": error_types,
            "analyzed_logs": len(recent_logs)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
        