import subprocess
import platform
import re
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NetOrchestra AI Production Engine", version="3.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IP_REGEX = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

def check_rule_exists(rule_name: str) -> bool:
    cmd = f'netsh advfirewall firewall show rule name="{rule_name}"'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return "No rules match" not in result.stdout

def test_network_node(ip_address: str) -> str:
    if not re.match(IP_REGEX, ip_address):
        return "⚠️ [VALIDATION ERROR] Invalid IP Address format."
    is_windows = platform.system().lower() == "windows"
    flag = "-n" if is_windows else "-c"
    command = ["ping", flag, "2", ip_address]
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        if result.returncode == 0:
            if "time=" in result.stdout:
                latency = result.stdout.split("time=")[1].split("ms")[0].strip()
                return f"✅ [ONLINE] Node {ip_address} is operational. Latency: {latency} ms"
            return f"✅ [ONLINE] Node {ip_address} is operational."
        return f"🚨 [OFFLINE] Target {ip_address} is unreachable."
    except Exception as e:
        return f"⚠️ [ERROR] Diagnostics failed: {str(e)}"

def manage_firewall_rule(ip_address: str, action: str) -> str:
    if platform.system().lower() != "windows":
        return "⚠️ [OS ERROR] Windows Advanced Firewall required."
    if not re.match(IP_REGEX, ip_address):
        return "⚠️ [SECURITY ALERT] Malicious IP payload blocked."

    rule_name = f"NetOrchestra_Block_{ip_address.replace('.', '_')}"
    
    if action == "block":
        if check_rule_exists(rule_name):
            return f"ℹ️ [INFO] Policy already enforced. IP {ip_address} is already blocked."
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=out action=block remoteip={ip_address}'
    else:
        if not check_rule_exists(rule_name):
            return f"ℹ️ [INFO] Cleanup skipped. No active block rule found for {ip_address}."
        cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
        
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if action == "unblock" or "Ok." in result.stdout or result.returncode == 0:
            return f"✅ [SUCCESS] Network policy sync complete for {ip_address}."
        return "❌ [PRIVILEGE ERROR] Access Denied. Run as ADMINISTRATOR."
    except Exception as e:
        return f"⚠️ [CRITICAL ERROR] Kernel mapping failed: {str(e)}"

# 🔥 नया फीचर: विंडोज फायरवॉल से लाइव ब्लॉक लिस्ट निकालना
@app.get("/api/blocked-ips")
def get_blocked_ips():
    if platform.system().lower() != "windows":
        return {"blocked_ips": []}
    
    # netsh से हमारे बनाए सारे रूल्स की लिस्ट मंगवाना
    cmd = 'netsh advfirewall firewall show rule name=all'
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True, errors='ignore')
        lines = result.stdout.split('\n')
        
        blocked_ips = set()
        current_rule_is_ours = False
        
        for line in lines:
            if "Rule Name:" in line and "NetOrchestra_Block_" in line:
                current_rule_is_ours = True
            elif "RemoteIP:" in line and current_rule_is_ours:
                # IP एड्रेस निकालना
                ip_match = re.search(IP_REGEX, line)
                if ip_match:
                    blocked_ips.add(ip_match.group(0))
                current_rule_is_ours = False
            elif "Rule Name:" in line:
                current_rule_is_ours = False
                
        return {"blocked_ips": list(blocked_ips)}
    except Exception as e:
        return {"blocked_ips": [], "error": str(e)}

@app.get("/api/execute")
def execute_command(command: str = Query(..., description="Natural Language Command")):
    clean_command = re.sub(r'[;&|`$]', '', command).strip()
    command_lower = clean_command.lower()
    ip_match = re.search(IP_REGEX, command_lower)
    target_ip = ip_match.group(0) if ip_match else "127.0.0.1"

    if any(word in command_lower for word in ["unblock", "allow", "clean", "remove"]):
        log = f"🔓 [AI INTENT] Detected: POLICY CLEANUP for Node {target_ip}"
        result = manage_firewall_rule(target_ip, "unblock")
        return {"log": log, "result": result}
    elif any(word in command_lower for word in ["block", "restrict", "isolate", "stop"]):
        log = f"🛡️ [AI INTENT] Detected: TRAFFIC ISOLATION for Node {target_ip}"
        result = manage_firewall_rule(target_ip, "block")
        return {"log": log, "result": result}
    elif "google" in command_lower or "internet" in command_lower:
        log = f"🌐 [AI INTENT] Detected: WAN LINK DIAGNOSTICS (8.8.8.8)"
        result = test_network_node("8.8.8.8")
        return {"log": log, "result": result}
    else:
        log = f"🖥️ [AI INTENT] Detected: INFRASTRUCTURE AUDIT for Node {target_ip}"
        result = test_network_node(target_ip)
        return {"log": log, "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
