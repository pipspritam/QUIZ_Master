import platform
import subprocess

# Get the current operating system
current_os = platform.system()

# Set the terminal command based on the operating system
if current_os == "Darwin":  # macOS
    terminal_command = "open -a Terminal"
elif current_os == "Windows":  # Windows
    terminal_command = "start cmd"
else:
    raise NotImplementedError("Operating system not supported.")

# Command to run the Python script in the new terminal session
python_command = "python3 main.py"  # Replace with the name of your Python script

# Combine the commands and execute in a new terminal session
subprocess.run(f"{terminal_command} -e '{python_command}'", shell=True)
