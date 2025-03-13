---

## **Y-Branch Optimization GUI**
A **PyQt6 GUI** for running **Y-Branch Optimization** using **Lumerical FDTD**. This application allows users to modify optimization parameters, initialize the FDTD simulation, and run the optimization process.

### **Features**
✅ Auto-detects **Lumerical Python environment**  
✅ Allows modification of all optimization parameters via GUI  
✅ Supports **FDTD initialization** and **optimization execution**  
✅ Runs on any Windows machine with **Lumerical installed**  

---

## **Installation Instructions**
### **1. Clone the Repository**
Open a terminal or command prompt and run:

```bash
git clone https://github.com/yourusername/YBranchOptimizationGUI.git
cd YBranchOptimizationGUI
```

### **2. Install Python Dependencies**
Make sure you have **Python 3.8+** installed.  
Then, install required packages using:

```bash
pip install -r requirements.txt
```

### **3. Ensure Lumerical is Installed**
This tool requires **Lumerical FDTD** with Python API support.  
Make sure **Lumerical is installed** before running the GUI.

### **4. Run the GUI**
Execute the following command:

```bash
python y_branch_ui.py
```

The **GUI window should appear**, allowing you to configure parameters and run the optimization.

---

## **Usage Instructions**
### **1. Modify Optimization Parameters**
- You can modify parameters like **wavelength range, number of optimization points, max iterations, waveguide width, thickness, and material.**
- Use **checkboxes** to enable/disable **cladding** and **GPU acceleration**.

### **2. Run Initialization**
- Click **"Run Initialization"** to set up the **Y-branch geometry** in Lumerical FDTD.
- This ensures the correct **geometry and layout** before optimization.

### **3. Run Optimization**
- Click **"Run Optimization"** to start the optimization process in the **Lumerical Python environment**.
- The **results will be displayed** in the GUI after completion.

---

## **Troubleshooting**
### **1. "Lumerical Python environment not found"**
- This means **Lumerical is not installed** or the Python path is incorrect.
- Ensure **Lumerical FDTD is installed** and modify the `find_lumerical_python()` function in `main.py`:
```python
def find_lumerical_python():
    possible_paths = [
        r"C:\Program Files\Lumerical\v242\python\python.exe",
        r"C:\Program Files\Lumerical\v241\python\python.exe",
        r"C:\Program Files\Lumerical\Ansys\python\python.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError("Lumerical Python environment not found. Please check the installation path.")
```

### **2. "ModuleNotFoundError: No module named 'PyQt6'"**
- Run the following command to install PyQt6:
  ```bash
  pip install PyQt6
  ```

### **3. "Permission denied" or "Command not found" (Mac/Linux Users)**
- This project is designed for **Windows with Lumerical installed**.
- If using Mac/Linux, ensure you have a **Windows-compatible Lumerical installation**.

---

## **File Structure**
```
YBranchOptimizationGUI/
│── y_branch_ui.py                     # PyQt6 GUI script
│── y_branch_run_opt.py          # Runs optimization
│── y_branch_init_script.py      # Initializes FDTD setup
│── y_class.py                   # YBranchOptimization class definition
│── requirements.txt             # Python dependencies
│── README.md                    # Project instructions
```

---

## **Future Improvements**
- 🔹 Add **support for Linux/Mac** versions of Lumerical.
- 🔹 Package the application as an **executable (.exe)** for easier distribution.
- 🔹 Improve **real-time logging** of optimization results.

---

## **Contributing**
Feel free to **fork the repository**, open an **issue**, or submit a **pull request** to improve the project.

---

## **License**
📝 This project is **open-source** under the **MIT License**.  

---

## **Contact**
📧 For any questions, feel free to reach out:  
💬 **GitHub Issues**: [Open an issue](https://github.com/yourusername/YBranchOptimizationGUI/issues)

---
