import os, sys
sys.path.append("C:\\Program Files\\Lumerical\\v242\\api\\python\\")
import lumapi
from y_class import YBranchOptimization

if __name__ == "__main__":
    # Extract parameters from the command line
    wavelength_start = float(sys.argv[1])
    wavelength_stop = float(sys.argv[2])
    opt_points = int(sys.argv[3])
    max_iter = int(sys.argv[4])
    x = float(sys.argv[5])
    y = float(sys.argv[6])
    material = sys.argv[7]
    concaveDepth = float(sys.argv[8])
    lowerBonds = float(sys.argv[9])
    upperBonds = float(sys.argv[10])
    wgWidth = float(sys.argv[11])
    thickness = float(sys.argv[12])
    # Correctly convert string to boolean
    cladding = sys.argv[13].lower() in ['true', '1', 'yes']
    gpu = sys.argv[14].lower() in ['true', '1', 'yes']

    # Initialize the YBranchOptimization object
    optimizer = YBranchOptimization(
        wavelength_start=wavelength_start,
        wavelength_stop=wavelength_stop,
        opt_points=opt_points,
        max_iter=max_iter,
        x=x,
        y=y,
        material=material,
        concaveDepth=concaveDepth,
        lowerBonds=lowerBonds,
        upperBonds=upperBonds,
        wgWidth=wgWidth,
        thickness=thickness,
        cladding=cladding,
        gpu=gpu
    )

    # Initialize the geometry/layout with y_branch_init_
    fdtd = lumapi.FDTD()  # Initialize the FDTD object
    optimizer.y_branch_init_(fdtd)
    fdtd.save("y_branch_3D_INIT")

    print("Geometry and layout initialization complete.")
