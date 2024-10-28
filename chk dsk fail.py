import tkinter as tk
import subprocess
import sys
import ctypes
import traceback
from tkinter import ttk, messagebox

class ChkdskGUI:
    def __init__(self):
        # Initialize root first so log_output has access to output_text
        self.root = tk.Tk()
        self.root.title("System File Check & CHKDSK GUI")
        self.root.geometry("800x600")

        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create shared output text area first so log_output can use it
        ttk.Label(main_frame, text="Output:").grid(row=1, column=0, sticky=tk.W, pady=(10,0))
        self.output_text = tk.Text(main_frame, height=15, width=80)
        self.output_text.grid(row=2, column=0, pady=5)
        self.output_text.tag_configure("error", foreground="red")
        self.output_text.tag_configure("info", foreground="blue")

        # Check if running with admin privileges
        if not self.is_admin():
            try:
                self.restart_with_admin()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restart with admin privileges: {str(e)}\n\n{traceback.format_exc()}")
            sys.exit()

        # Create tool selection notebook
        tool_notebook = ttk.Notebook(main_frame)
        tool_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # CHKDSK Tab
        chkdsk_frame = ttk.Frame(tool_notebook, padding="5")
        tool_notebook.add(chkdsk_frame, text="CHKDSK")

        # Drive selection
        ttk.Label(chkdsk_frame, text="Drive:").grid(row=0, column=0, sticky=tk.W)
        self.drive_var = tk.StringVar()
        try:
            self.log_output("Scanning for available drives...")
            drives = [f"{chr(x)}:" for x in range(65, 91) if self.drive_exists(chr(x))]
            if not drives:
                messagebox.showwarning("Warning", "No drives were found")
                self.log_output("No drives were found", error=True)
            else:
                self.log_output(f"Found drives: {', '.join(drives)}")
        except Exception as e:
            drives = []
            error_msg = f"Failed to enumerate drives: {str(e)}\n\n{traceback.format_exc()}"
            messagebox.showwarning("Warning", error_msg)
            self.log_output(error_msg, error=True)
            
        self.drive_combo = ttk.Combobox(chkdsk_frame, textvariable=self.drive_var, values=drives)
        self.drive_combo.grid(row=0, column=1, sticky=tk.W)
        if drives:
            self.drive_combo.set(drives[0])  # Set default selection
        
        # CHKDSK Options Frame
        options_frame = ttk.LabelFrame(chkdsk_frame, text="CHKDSK Options", padding="5")
        options_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # CHKDSK Options
        self.fix_errors = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Fix errors (/F)", variable=self.fix_errors).grid(row=0, column=0, sticky=tk.W)
        
        self.force_dismount = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Force dismount (/X)", variable=self.force_dismount).grid(row=1, column=0, sticky=tk.W)
        
        self.verbose = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Verbose output (/V)", variable=self.verbose).grid(row=2, column=0, sticky=tk.W)
        
        self.recover_bad_sectors = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Locate bad sectors and recover data (/R)", variable=self.recover_bad_sectors).grid(row=3, column=0, sticky=tk.W)
        
        self.skip_folder_cycle = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Skip folder cycle checking (/C)", variable=self.skip_folder_cycle).grid(row=4, column=0, sticky=tk.W)

        # Run CHKDSK Button
        ttk.Button(chkdsk_frame, text="Run CHKDSK", command=self.run_chkdsk).grid(row=2, column=0, columnspan=2, pady=10)

        # SFC Tab
        sfc_frame = ttk.Frame(tool_notebook, padding="5")
        tool_notebook.add(sfc_frame, text="System File Checker")

        # SFC Options Frame
        sfc_options_frame = ttk.LabelFrame(sfc_frame, text="SFC Options", padding="5")
        sfc_options_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # SFC Options
        self.sfc_scannow = tk.BooleanVar(value=True)
        ttk.Checkbutton(sfc_options_frame, text="Scan Now - Scan and repair system files", variable=self.sfc_scannow).grid(row=0, column=0, sticky=tk.W)
        
        self.sfc_verifyonly = tk.BooleanVar()
        ttk.Checkbutton(sfc_options_frame, text="Verify Only - Scan without repairing", variable=self.sfc_verifyonly).grid(row=1, column=0, sticky=tk.W)
        
        self.sfc_scanonce = tk.BooleanVar()
        ttk.Checkbutton(sfc_options_frame, text="Scan Once - Scan and repair at next boot", variable=self.sfc_scanonce).grid(row=2, column=0, sticky=tk.W)

        # Run SFC Button
        ttk.Button(sfc_frame, text="Run SFC", command=self.run_sfc).grid(row=1, column=0, columnspan=2, pady=10)

        self.log_output("Program started successfully", tag="info")

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def log_output(self, message, error=False, tag=None):
        """Add a message to the output text area"""
        self.output_text.insert(tk.END, f"{message}\n", tag if tag else "error" if error else None)
        self.output_text.see(tk.END)
        self.root.update()

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            error_msg = f"Failed to check admin status: {str(e)}\n\n{traceback.format_exc()}"
            messagebox.showerror("Error", error_msg)
            return False

    def restart_with_admin(self):
        try:
            script_path = sys.argv[0]
            args = ' '.join(sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}" {args}', None, 1)
        except Exception as e:
            error_msg = f"Failed to restart with admin privileges: {str(e)}\n\n{traceback.format_exc()}"
            raise Exception(error_msg)

    def drive_exists(self, drive_letter):
        try:
            result = subprocess.run(f"dir {drive_letter}:", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
        except Exception as e:
            error_msg = f"Error checking drive {drive_letter}: {str(e)}\n\n{traceback.format_exc()}"
            self.log_output(error_msg, error=True)
            raise Exception(error_msg)

    def run_sfc(self):
        command = ["sfc"]
        
        if self.sfc_scannow.get():
            command.append("/scannow")
        elif self.sfc_verifyonly.get():
            command.append("/verifyonly")
        elif self.sfc_scanonce.get():
            command.append("/scanonce")
        else:
            self.log_output("Error: No SFC option selected", error=True)
            messagebox.showerror("Error", "Please select an SFC option")
            return

        try:
            self.log_output(f"Running SFC command: {' '.join(command)}", tag="info")
            # Use cmd.exe to run sfc command to capture all output
            full_command = ["cmd", "/c", "sfc", "/scannow"]
            process = subprocess.Popen(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.output_text.delete(1.0, tk.END)
            self.log_output("Starting System File Checker scan...\n", tag="info")
            
            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()
                
                if output == '' and error == '' and process.poll() is not None:
                    break
                    
                if output:
                    # Clean and format the output
                    output = output.strip()
                    if output:
                        if "Windows Resource Protection" in output:
                            self.log_output(output, tag="info")
                        elif "Verification" in output:
                            self.log_output(output)
                        elif "found corrupt files" in output.lower():
                            self.log_output(output, error=True)
                        elif "successfully repaired" in output.lower():
                            self.log_output(output, tag="info")
                        else:
                            self.log_output(output)
                            
                if error:
                    self.log_output(f"Error: {error.strip()}", error=True)
            
            return_code = process.poll()
            if return_code != 0:
                self.log_output(f"\nSFC scan failed with error code {return_code}", error=True)
                messagebox.showerror("Error", f"SFC scan failed with error code {return_code}")
            else:
                self.log_output("\nSystem File Checker scan completed", tag="info")
                
        except Exception as e:
            error_msg = f"Failed to run SFC: {str(e)}\n\n{traceback.format_exc()}\nMake sure to run this program as administrator."
            self.log_output(error_msg, error=True)
            messagebox.showerror("Error", error_msg)

    def run_chkdsk(self):
        if not self.drive_var.get():
            self.log_output("Error: No drive selected", error=True)
            messagebox.showerror("Error", "Please select a drive")
            return

        command = ["chkdsk", self.drive_var.get()]
        
        if self.fix_errors.get():
            command.append("/F")
        if self.force_dismount.get():
            command.append("/X")
        if self.verbose.get():
            command.append("/V")
        if self.recover_bad_sectors.get():
            command.append("/R")
        if self.skip_folder_cycle.get():
            command.append("/C")

        try:
            self.log_output(f"Running CHKDSK command: {' '.join(command)}", tag="info")
            self.run_process(command)
        except Exception as e:
            error_msg = f"Failed to run CHKDSK: {str(e)}\n\n{traceback.format_exc()}\nMake sure to run this program as administrator."
            self.log_output(error_msg, error=True)
            messagebox.showerror("Error", error_msg)

    def run_process(self, command):
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            self.output_text.delete(1.0, tk.END)
            self.log_output(f"Started process: {' '.join(command)}", tag="info")
            
            # Create a separate thread for reading process output
            def read_output():
                while True:
                    output = process.stdout.readline()
                    error = process.stderr.readline()
                    
                    if output == '' and error == '' and process.poll() is not None:
                        break
                        
                    if output:
                        self.root.after(0, lambda: self.log_output(output.strip()))
                    if error:
                        self.root.after(0, lambda: self.log_output(f"Error: {error.strip()}", error=True))
                
                return_code = process.poll()
                if return_code != 0:
                    error_msg = f"Process exited with code {return_code}"
                    self.root.after(0, lambda: self.log_output(error_msg, error=True))
                    self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                else:
                    self.root.after(0, lambda: self.log_output("Process completed successfully", tag="info"))
            
            # Start output reading thread
            import threading
            output_thread = threading.Thread(target=read_output, daemon=True)
            output_thread.start()
                    
        except Exception as e:
            error_msg = f"Failed to run process: {str(e)}\n\n{traceback.format_exc()}"
            self.log_output(error_msg, error=True)
            raise Exception(error_msg)

def main():
    try:
        app = ChkdskGUI()
        app.root.mainloop()
    except Exception as e:
        error_msg = f"Application failed to start: {str(e)}\n\n{traceback.format_exc()}"
        messagebox.showerror("Fatal Error", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()
