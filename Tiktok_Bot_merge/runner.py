import subprocess
import threading
import os
import signal
import sys
import datetime
import psutil
import time

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.abspath(os.path.join(base_path, relative_path))

process = None
chrome_pid = None
cmd_pid = None

def start(shop_name=None, log_callback=None):
    global process
    if process is not None and process.poll() is None:
        if log_callback:
            log_callback("Bot already running.")
        return

    print("Starting the Bot.....")
    print(f"Python executable: {sys.executable}")

    script_path = resource_path("Tiktok_Bot_merge/TikTok.py")
    # Use the bundled Python interpreter from the Python311 subfolder
    python_interpreter = resource_path("Python311/python.exe")
    # python_interpreter=resource_path("myenv/Scripts/python.exe")
    
    script_path = os.path.abspath(script_path)
    if not os.path.exists(script_path):
        print("TikTok.py does not exist at runtime!")
        if log_callback:
            log_callback("TikTok.py not found!")
        return
    def run_subprocess():
        global process
        try:
            process = subprocess.Popen(
                #[sys.executable, script_path, shop_name],
                [python_interpreter, script_path, shop_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                encoding="utf-8",
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
            )

            for line in process.stdout:
                print(f"[Subprocess Output] {line.strip()}")
                if log_callback:
                    log_callback(f"[Bot Log] {line.strip()}")

            return_code = process.wait()
            print(f"Subprocess exited with code {return_code}")

            if return_code != 0:
                print("Subprocess returned a non-zero exit code.")
                if log_callback:
                    log_callback(f"Bot process failed: {return_code}")
        except Exception as e:
            if log_callback:
                log_callback(f"Failed to start bot: {e}")
            return
        def read_output():
            if not process.stdout:
                if log_callback:
                    log_callback("Could not capture output from TikTok.py")
                return
            try:
                for line in local_process.stdout:
                    line = line.strip()
                    print(line)
                    if log_callback:
                        log_callback(line)
            except Exception as e:
                print(f"Error reading bot output: {e}")
                if log_callback:
                    log_callback(f"Error reading output: {e}")
            finally:
                try:
                    local_process.stdout.close()
                except Exception:
                    pass
        threading.Thread(target=read_output, daemon=True).start()
    # Start the subprocess in a new thread
    threading.Thread(target=run_subprocess, daemon=True).start()
    local_process = process
    if log_callback:
        log_callback("Bot started successfully.")

def stop():
    global process
    if process is not None and process.poll() is None:
        print("Stopping the bot...")

        try:
            # Get the PID of the main bot process
            parent_pid = process.pid
            parent_process = psutil.Process(parent_pid)

            # Kill all child processes (including the CMD window and Chrome browser)
            for child in parent_process.children(recursive=True):
                print(f"Killing child process with PID: {child.pid}")
                child.kill()

            # Kill the main process itself
            print(f"Killing main process with PID: {parent_pid}")
            process.kill()

            process.wait()  # Ensure the process has been fully terminated
            print("Bot and all related processes have been terminated.")
            process = None  # Clear the process object

            # Fallback: Kill all Chrome and ChromeDriver processes (Windows only)
            if os.name == "nt":
                #os.system("taskkill /F /IM chrome.exe /T")
                os.system("taskkill /F /IM chromedriver.exe /T")
                print("Fallback: Killed all chrome.exe and chromedriver.exe processes.")

        except Exception as e:
            print(f"Error stopping bot: {e}")
    else:
        print("No bot is currently running.")
        
# def stop():
#     global process
#     if process is not None and process.poll() is None:
#         print("Bot is stopped.....")
#         if os.name == "nt":
#             process.send_signal(signal.CTRL_BREAK_EVENT)
#         else:
#             process.terminate()
#         process = None
#     else:
#         print("No bot is currently running.")