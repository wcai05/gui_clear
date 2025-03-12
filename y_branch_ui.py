import subprocess
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QCheckBox
from PyQt6.QtCore import Qt
from y_class import YBranchOptimization  # Assuming your class is saved in YBranchOptimization.py

class OptimizationGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Y-Branch Optimization")
        self.setGeometry(100, 100, 400, 450)

        # Create the layout and form elements
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Parameter Inputs
        self.wavelength_start_input = QLineEdit(self)
        self.wavelength_start_input.setText("1500")
        form_layout.addRow("Wavelength Start (nm):", self.wavelength_start_input)

        self.wavelength_stop_input = QLineEdit(self)
        self.wavelength_stop_input.setText("1600")
        form_layout.addRow("Wavelength Stop (nm):", self.wavelength_stop_input)

        self.opt_points_input = QLineEdit(self)
        self.opt_points_input.setText("10")
        form_layout.addRow("Optimization Points:", self.opt_points_input)

        self.max_iter_input = QLineEdit(self)
        self.max_iter_input.setText("70")
        form_layout.addRow("Max Iterations:", self.max_iter_input)

        self.x_input = QLineEdit(self)
        self.x_input.setText("2")
        form_layout.addRow("X (Length of Y-branch in µm):", self.x_input)

        self.y_input = QLineEdit(self)
        self.y_input.setText("0.1")
        form_layout.addRow("Y (Width between output wg in µm):", self.y_input)

        self.material_input = QLineEdit(self)
        self.material_input.setText("Si (Silicon) - Palik")
        form_layout.addRow("Material:", self.material_input)

        self.concaveDepth_input = QLineEdit(self)
        self.concaveDepth_input.setText("0.2e-6")
        form_layout.addRow("Concave Depth (m):", self.concaveDepth_input)

        self.lowerBonds_input = QLineEdit(self)
        self.lowerBonds_input.setText("0.2e-6")
        form_layout.addRow("Lower Bonds (m):", self.lowerBonds_input)

        self.upperBonds_input = QLineEdit(self)
        self.upperBonds_input.setText("0.9e-6")
        form_layout.addRow("Upper Bonds (m):", self.upperBonds_input)

        self.wgWidth_input = QLineEdit(self)
        self.wgWidth_input.setText("0.5e-6")
        form_layout.addRow("Waveguide Width (m):", self.wgWidth_input)

        self.thickness_input = QLineEdit(self)
        self.thickness_input.setText("220e-9")
        form_layout.addRow("Thickness (m):", self.thickness_input)

        self.cladding_checkbox = QCheckBox(self)
        self.cladding_checkbox.setChecked(True)
        form_layout.addRow("Cladding:", self.cladding_checkbox)

        self.gpu_checkbox = QCheckBox(self)
        self.gpu_checkbox.setChecked(True)
        form_layout.addRow("Use GPU:", self.gpu_checkbox)

        # Add the form layout to the main layout
        layout.addLayout(form_layout)

        # Run Initialization Button
        self.init_button = QPushButton("Run Initialization", self)
        self.init_button.clicked.connect(self.run_y_branch_init)
        layout.addWidget(self.init_button)

        # Run Button
        self.run_button = QPushButton("Run Optimization", self)
        self.run_button.clicked.connect(self.run_optimization)
        layout.addWidget(self.run_button)

        # # Add checkbox to run y_branch_init_ function
        # self.init_button_checkbox = QCheckBox("Run y_branch_init_ function", self)
        # layout.addWidget(self.init_button_checkbox)



        # Results Output
        self.results_label = QLabel("Results will appear here...", self)
        layout.addWidget(self.results_label)

        self.setLayout(layout)

    def run_optimization(self):
        # Get inputs from the form
        wavelength_start = float(self.wavelength_start_input.text())
        wavelength_stop = float(self.wavelength_stop_input.text())
        opt_points = int(self.opt_points_input.text())
        max_iter = int(self.max_iter_input.text())
        x = float(self.x_input.text())
        y = float(self.y_input.text())
        material = self.material_input.text()
        concaveDepth = float(self.concaveDepth_input.text())
        lowerBonds = float(self.lowerBonds_input.text())
        upperBonds = float(self.upperBonds_input.text())
        wgWidth = float(self.wgWidth_input.text())
        thickness = float(self.thickness_input.text())
        cladding = self.cladding_checkbox.isChecked()
        gpu = self.gpu_checkbox.isChecked()

        # Prepare the command to run the script in Lumerical's Python environment
        python_executable = r"C:/Program Files/Lumerical/v242/python/python.exe"
        script_path = r"y_branch_run_opt.py"  # The path to your script file

        # Build the arguments for the subprocess call
        command = [
            python_executable,
            script_path,
            str(wavelength_start),
            str(wavelength_stop),
            str(opt_points),
            str(max_iter),
            str(x),
            str(y),
            material,
            str(concaveDepth),
            str(lowerBonds),
            str(upperBonds),
            str(wgWidth),
            str(thickness),
            str(cladding),
            str(gpu)
        ]

        # Run the subprocess to execute the optimization in the Lumerical environment
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.results_label.setText(f"Optimization Results:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            self.results_label.setText(f"Error during optimization:\n{e.stderr}")

    def run_y_branch_init(self):
        """
        Runs the `y_branch_init_` function to initialize the geometry/layout in the FDTD simulation.
        This is executed in the Lumerical Python environment using subprocess.
        """
        wavelength_start = float(self.wavelength_start_input.text())
        wavelength_stop = float(self.wavelength_stop_input.text())
        opt_points = int(self.opt_points_input.text())
        max_iter = int(self.max_iter_input.text())
        x = float(self.x_input.text())
        y = float(self.y_input.text())
        material = self.material_input.text()
        concaveDepth = float(self.concaveDepth_input.text())
        lowerBonds = float(self.lowerBonds_input.text())
        upperBonds = float(self.upperBonds_input.text())
        wgWidth = float(self.wgWidth_input.text())
        thickness = float(self.thickness_input.text())
        cladding = self.cladding_checkbox.isChecked()
        gpu = self.gpu_checkbox.isChecked()

        # Prepare the command to run the initialization function in Lumerical's Python environment
        python_executable = r"C:/Program Files/Lumerical/v242/python/python.exe"
        script_path = r"y_branch_init_script.py"  # Path to a separate Python script containing the initialization function

        # Build the arguments for the subprocess call
        command = [
            python_executable,
            script_path,
            str(wavelength_start),
            str(wavelength_stop),
            str(opt_points),
            str(max_iter),
            str(x),
            str(y),
            material,
            str(concaveDepth),
            str(lowerBonds),
            str(upperBonds),
            str(wgWidth),
            str(thickness),
            str(cladding),
            str(gpu)
        ]

        # Run the subprocess to execute the y_branch_init_ function in the Lumerical environment
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.results_label.setText(f"Initialization Successful:\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            self.results_label.setText(f"Error during initialization:\n{e.stderr}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OptimizationGUI()
    window.show()
    sys.exit(app.exec())
