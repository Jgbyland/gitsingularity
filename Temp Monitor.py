import tkinter as tk
import psutil
import wmi
import os
import GPUtil
from tkinter import messagebox
from tkinter import ttk
import sv_ttk # For modern theme

def celsius_to_fahrenheit(celsius):
    if isinstance(celsius, float):
        return (celsius * 9/5) + 32
    return celsius

def show_sources():
    sources_text = """Sources:

1. Lawrence Berkeley National Laboratory - "Thermal Guidelines and Temperature Measurements"
https://datacenters.lbl.gov/sites/default/files/FINAL%20Thermal%20Guidelines%20and%20Temp%20Measurements%209-15-2020.pdf

2. HAL Science - "CPU Overheating Characterization in HPC Systems: A Case Study" 
https://hal.science/hal-01949708/file/CPU_Overheating_Characterization_in_HPC_Systems:A_Case_Study.pdf

3. MDPI Sustainability Journal - "Temperature Management Study"
https://www.mdpi.com/2071-1050/16/16/7222"""
    
    # Create info window
    info_window = tk.Toplevel()
    info_window.title("Sources")
    info_window.geometry("700x500")
    sv_ttk.set_theme("dark")  # Apply theme to new window
    
    # Add text widget with scrollbar
    text_frame = ttk.Frame(info_window)
    text_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(text_frame, wrap=tk.WORD, width=80, height=15, font=("Segoe UI", 12))
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget.insert(tk.END, sources_text)
    
    # Add copy button
    copy_button = ttk.Button(info_window, text="Copy to Clipboard", command=lambda: [info_window.clipboard_clear(), info_window.clipboard_append(sources_text), messagebox.showinfo("Success", "Text copied to clipboard!")])
    copy_button.pack(pady=10)

def show_cpu_info():
    info_text = """CPU Temperature Guidelines

Safe Operating Range:
• Normal Usage: 40°C - 65°C (104°F - 149°F)
• Heavy Load: 70°C - 85°C (158°F - 185°F)
• Maximum Safe Limit: 85°C - 100°C (185°F - 212°F)

Optimal Conditions:
• Idle Temperature: 30°C - 40°C (86°F - 104°F)
• Load Temperature: Below 80°C (176°F)
• Data Center Intake: 18°C - 27°C (65°F - 80°F)

Important Notes:
• Tjunction Max refers to the temperature at which CPU throttling occurs
• Extended operation above 80°C may reduce CPU lifespan
• Proper cooling is essential for optimal performance
• Regular monitoring helps prevent thermal damage

For detailed specifications, please check manufacturer guidelines."""
    
    # Create info window
    info_window = tk.Toplevel()
    info_window.title("CPU Temperature Information")
    info_window.geometry("700x500")
    sv_ttk.set_theme("dark")  # Apply theme to new window
    
    # Add text widget with scrollbar
    text_frame = ttk.Frame(info_window)
    text_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(text_frame, wrap=tk.WORD, width=80, height=15, font=("Segoe UI", 12))
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget.insert(tk.END, info_text)
    
    # Add sources button
    sources_button = ttk.Button(info_window, text="View Sources", command=show_sources)
    sources_button.pack(pady=10)

def show_gpu_sources():
    sources_text = """Sources:

1. Sysprobs - "GPU Temperature Management Guidelines"
https://www.sysprobs.com/

2. InfinitiveHost - "Best Practices for GPU Temperature Control"
https://www.infinitivehost.com/

3. ComputerMesh - "GPU Temperature Monitoring and Management"
https://computermesh.com/"""
    
    # Create info window
    info_window = tk.Toplevel()
    info_window.title("GPU Temperature Sources")
    info_window.geometry("700x500")
    sv_ttk.set_theme("dark")  # Apply theme to new window
    
    # Add text widget with scrollbar
    text_frame = ttk.Frame(info_window)
    text_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(text_frame, wrap=tk.WORD, width=80, height=15, font=("Segoe UI", 12))
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget.insert(tk.END, sources_text)
    
    # Add copy button
    copy_button = ttk.Button(info_window, text="Copy to Clipboard", command=lambda: [info_window.clipboard_clear(), info_window.clipboard_append(sources_text), messagebox.showinfo("Success", "Text copied to clipboard!")])
    copy_button.pack(pady=10)

def show_gpu_info():
    info_text = """GPU Temperature Guidelines

Safe Operating Range:
• Normal Usage: 30°C - 50°C (86°F - 122°F)
• Gaming/Heavy Load: 65°C - 85°C (149°F - 185°F)
• Maximum Safe Limit: 95°C - 100°C (203°F - 212°F)

Throttling Points:
• NVIDIA GPUs: ~95°C (203°F)
• AMD GPUs: ~100°C (212°F)

Best Practices:
• Keep temperatures below 85°C for longevity
• Monitor hot spots during intense workloads
• Maintain proper airflow and cooling
• Regular cleaning and maintenance recommended

Warning Signs:
• Consistent temperatures above 90°C
• Sudden performance drops
• Unusual fan behavior
• Graphical artifacts

For specific GPU models, consult manufacturer specifications."""
    
    # Create info window
    info_window = tk.Toplevel()
    info_window.title("GPU Temperature Information")
    info_window.geometry("700x500")
    sv_ttk.set_theme("dark")  # Apply theme to new window
    
    # Add text widget with scrollbar
    text_frame = ttk.Frame(info_window)
    text_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
    
    text_widget = tk.Text(text_frame, wrap=tk.WORD, width=80, height=15, font=("Segoe UI", 12))
    scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)
    
    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_widget.insert(tk.END, info_text)
    
    # Add sources button
    sources_button = ttk.Button(info_window, text="View Sources", command=show_gpu_sources)
    sources_button.pack(pady=10)

def get_temps():
    # Attempt to get CPU temperature using WMI
    w = wmi.WMI(namespace="root\wmi")
    temperature_info = w.MSAcpi_ThermalZoneTemperature()
    cpu_temp = 'N/A'
    
    if temperature_info:
        cpu_temp = temperature_info[0].CurrentTemperature / 10.0 - 273.15
    
    # Attempt to get GPU temperature using GPUtil
    gpus = GPUtil.getGPUs()
    gpu_temp = 'N/A'
    
    if gpus:
        gpu_temp = gpus[0].temperature
    
    return cpu_temp, gpu_temp

def update_temps():
    cpu_temp, gpu_temp = get_temps()
    if use_fahrenheit.get():
        cpu_temp = celsius_to_fahrenheit(cpu_temp)
        gpu_temp = celsius_to_fahrenheit(gpu_temp)
        unit = "°F"
        cpu_range = "(Safe range: 140-185°F)"
        gpu_range = "(Safe range: 150-185°F)"
    else:
        unit = "°C"
        cpu_range = "(Safe range: 60-85°C)"
        gpu_range = "(Safe range: 65-85°C)"
    
    cpu_label.config(text=f"CPU Temp: {cpu_temp:.1f}{unit} {cpu_range}" if isinstance(cpu_temp, float) else f"CPU Temp: {cpu_temp}")
    gpu_label.config(text=f"GPU Temp: {gpu_temp:.1f}{unit} {gpu_range}" if isinstance(gpu_temp, float) else f"GPU Temp: {gpu_temp}")
    root.after(1000, update_temps)

# Set up the main window
root = tk.Tk()
root.title("Temperature Monitor")
root.geometry("600x300")  # Set a fixed initial size

# Apply modern theme
sv_ttk.set_theme("dark")

# Create main container with padding
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# Temperature unit toggle
use_fahrenheit = tk.BooleanVar()
temp_toggle = ttk.Checkbutton(main_frame, text="Show temperatures in °F", variable=use_fahrenheit, command=update_temps)
temp_toggle.pack(pady=(0, 20))

# CPU temperature display with larger font and more spacing
cpu_frame = ttk.Frame(main_frame)
cpu_frame.pack(fill=tk.X, pady=15)
cpu_label = ttk.Label(cpu_frame, text="CPU Temp: ", font=("Segoe UI", 16))
cpu_label.pack(side=tk.LEFT, padx=10)
cpu_info_button = ttk.Button(cpu_frame, text="More Info", command=show_cpu_info, width=15)
cpu_info_button.pack(side=tk.RIGHT, padx=10)

# GPU temperature display with larger font and more spacing
gpu_frame = ttk.Frame(main_frame)
gpu_frame.pack(fill=tk.X, pady=15)
gpu_label = ttk.Label(gpu_frame, text="GPU Temp: ", font=("Segoe UI", 16))
gpu_label.pack(side=tk.LEFT, padx=10)
gpu_info_button = ttk.Button(gpu_frame, text="More Info", command=show_gpu_info, width=15)
gpu_info_button.pack(side=tk.RIGHT, padx=10)

update_temps()
root.mainloop()
