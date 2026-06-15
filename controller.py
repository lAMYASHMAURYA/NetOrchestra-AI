import subprocess
import platform
import os
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

# 1. FastAPI ऐप को इनिशियलाइज करना
app = FastAPI(title="NetOrchestra AI Engine")

# CORS ब्लॉक एरर को रोकने के लिए सिक्योरिटी सेटिंग्स
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def test_network_node(ip_address):
    is_windows = platform.system().lower() == "windows"
    flag = "-n" if is_windows else "-c"
    command = ["ping", flag, "2", ip_address]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            if "time=" in result.stdout:
                latency = result.stdout.split("time=")[1].split("ms")[0].strip()
                return f"✅ [ONLINE] Node {ip_address} is fully operational. Latency: {latency} ms"
            return f"✅ [ONLINE] Node {ip_address} is fully operational."
        else:
            return f"🚨 [OFFLINE] Target {ip_address} is down!"
    except Exception as e:
        return f"⚠️ [ERROR] Ping failed: {str(e)}"

def manage_firewall_rule(ip_address, action):
    if platform.system().lower() != "windows":
        return "⚠️ [OS ERROR] Firewall feature only supports Windows."
    
    rule_name = f"NetOrchestra_Block_{ip_address.replace('.', '_')}"
    if action == "block":
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block remoteip={ip_address}'
    else:
        cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
        
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if action == "unblock" or "Ok." in result.stdout or result.returncode == 0:
            return f"✅ [SUCCESS] Firewall policy updated successfully for {ip_address}!"
        else:
            return "❌ [PERMISSION ERROR] Please run as ADMINISTRATOR."
    except Exception as e:
        return f"⚠️ [SYSTEM ERROR] Firewall command failed: {str(e)}"

# 2. एआई पार्सिंग एंडपॉइंट (The Bridge Endpoint)
@app.get("/api/execute")
def execute_command(command: str = Query(..., description="User English Command")):
    command_lower = command.lower()
    words = command_lower.split()
    target_ip = "127.0.0.1"
    
    for word in words:
        if word.count('.') == 3:
            target_ip = word
            break

    if "unblock" in command_lower or "allow" in command_lower or "clean" in command_lower:
        log = f"🔓 [FIREWALL] Executing cleanup to UNBLOCK IP: {target_ip}..."
        result = manage_firewall_rule(target_ip, "unblock")
        return {"log": log, "result": result}
        
    elif "block" in command_lower or "restrict" in command_lower:
        log = f"🛡️ [FIREWALL] Generating rule to BLOCK IP: {target_ip}..."
        result = manage_firewall_rule(target_ip, "block")
        return {"log": log, "result": result}
        
    elif "google" in command_lower or "internet" in command_lower:
        log = f"[AI Controller] Analyzing network path to Core Internet (8.8.8.8)..."
        result = test_network_node("8.8.8.8")
        return {"log": log, "result": result}
        
    else:
        log = f"[AI Controller] Analyzing network path to Target: {target_ip}..."
        result = test_network_node(target_ip)
        return {"log": log, "result": result}

if __name__ == "__main__":
    import uvicorn
    # सर्वर को पोर्ट 8000 पर लाइव करना
    uvicorn.run(app, host="127.0.0.1", port=8000)
