# C:\Program Files\Lumerical\v242\python\python.exe

import os, sys
sys.path.append("C:\\Program Files\\Lumerical\\v242\\api\\python\\")
import lumapi
import numpy as np
import scipy as sp
from scipy.constants import c
from lumopt.utilities.wavelengths import Wavelengths
from lumopt.geometries.polygon import FunctionDefinedPolygon
from lumopt.utilities.materials import Material
from lumopt.figures_of_merit.modematch import ModeMatch
from lumopt.optimizers.generic_optimizers import ScipyOptimizers
from lumopt.optimization import Optimization

class YBranchOptimization:
    def __init__(self, wavelength_start=1500, wavelength_stop=1600, opt_points=10, max_iter=70, x=2, y=0.1, 
                 material='Si (Silicon) - Palik', concaveDepth=0.2e-6, lowerBonds=0.2e-6, upperBonds=0.9e-6, 
                 wgWidth=0.5e-6, thickness=220e-9, cladding=True, gpu=True):
        self.wavelength_start = wavelength_start
        self.wavelength_stop = wavelength_stop
        self.opt_points = opt_points
        self.max_iter = max_iter
        self.x = x
        self.y = y
        self.material = material
        self.concaveDepth = concaveDepth
        self.lowerBonds = lowerBonds
        self.upperBonds = upperBonds
        self.wgWidth = wgWidth
        self.thickness = thickness
        self.cladding = cladding
        self.gpu = gpu

    def y_branch_init_(self, fdtd):
        '''
        here x is the length of the y-splitter in um
        y is w2 the width between the two output waveguides in um
        cladding --> Bool
        gpu --> Bool
        '''
        ## CLEAR SESSION
        # print(self.cladding)
        fdtd.switchtolayout()
        fdtd.selectall()
        fdtd.delete()
        
        ## SIM PARAMS
        size_x= self.x*1e-6 + 9e-6;
        size_y= self.y*1e-6 + 8e-6;
        size_z=1.2e-6;
        mesh_x=20e-9;
        mesh_y=20e-9;
        mesh_z=20e-9;
        finer_mesh_size=2.5e-6;
        mesh_accuracy=4;
        lam_c = 1.550e-6;
        
    
        ## GEOMETRY
        
        #INPUT WAVEGUIDE
        
        fdtd.addrect();
        fdtd.set('name','input wg');
        fdtd.set('x max',-(self.x/2)*1e-6);
        fdtd.set('x min',-(self.x/2)*1e-6-5e-6);
        fdtd.set('y span',self.wgWidth);
        fdtd.set('z min',0);
        fdtd.set('z max',self.thickness);
        fdtd.set('y',0);
        fdtd.set('material',self.material);
        
        #OUTPUT WAVEGUIDES
        
        fdtd.addwaveguide();
        fdtd.set('name','output wg top');
        fdtd.set("base width",self.wgWidth);
        fdtd.set("base height",self.thickness);
        fdtd.set("base angle",90);

        pole = np.array([[(self.x/2)*1e-6,((self.y/2)*1e-6+0.25e-6)],[(self.x/2)*1e-6+1e-6,((self.y/2)*1e-6+0.25e-6)],[(self.x/2)*1e-6+2e-6,1.35e-6],[(self.x/2)*1e-6+3e-6,1.35e-6],[(self.x/2)*1e-6+6e-6,1.35e-6]])
        fdtd.set("poles",pole);
        fdtd.set('z',self.thickness/2);
        fdtd.set('material',self.material);
        
        fdtd.addwaveguide();
        fdtd.set('name','output wg bottom');
        fdtd.set("base width",self.wgWidth);
        fdtd.set("base height",self.thickness);
        fdtd.set("base angle",90);

        pole = np.array([[(self.x/2)*1e-6,-((self.y/2)*1e-6+0.25e-6)],[(self.x/2)*1e-6+1e-6,-((self.y/2)*1e-6+0.25e-6)],[(self.x/2)*1e-6+2e-6,-1.35e-6],[(self.x/2)*1e-6+3e-6,-1.35e-6],[(self.x/2)*1e-6+6e-6,-1.35e-6]])
        fdtd.set("poles",pole);
        fdtd.set('z',self.thickness/2);
        fdtd.set('material',self.material);
        
        fdtd.addrect();
        fdtd.set('name','sub');
        fdtd.set('x span',12e-6+self.x*1e-6);
        fdtd.set('y span',10e-6+self.y*1e-6);
        if not self.cladding:
            fdtd.set('z max',0);
            fdtd.set('z min',-5e-6);
        else:
            fdtd.set('z span',10e-6);
            fdtd.set('z',0);
        fdtd.set('y',0);
        fdtd.set('x',2e-6);
        
        fdtd.set('material','SiO2 (Glass) - Palik');
        fdtd.set('override mesh order from material database',1);
        fdtd.set('mesh order',3);
        fdtd.set('alpha',0.8);

        fdtd.addrect();
        fdtd.set('name','out1 wg');
        fdtd.set('x min',(self.x/2)*1e-6+6e-6);
        fdtd.set('x max',(self.x/2)*1e-6+12e-6);
        fdtd.set('y span',self.wgWidth);
        fdtd.set('z max',self.thickness);
        fdtd.set('z min',0);
        fdtd.set('y',1.35e-6);
        fdtd.set('material',self.material);
        
        fdtd.addrect();
        fdtd.set('name','out2 wg');
        fdtd.set('x min',(self.x/2)*1e-6+6e-6);
        fdtd.set('x max',(self.x/2)*1e-6+12e-6);
        fdtd.set('y span',self.wgWidth);
        fdtd.set('z max',self.thickness);
        fdtd.set('z min',0);
        fdtd.set('y',-1.35e-6);
        fdtd.set('material',self.material);
            
        ## FDTD
        fdtd.addfdtd();
        fdtd.set('mesh accuracy',mesh_accuracy);
        fdtd.set('dimension','3D');
        fdtd.set('x',2e-6);
        fdtd.set('x span',size_x);
        fdtd.set('y min',-size_y/2);
        fdtd.set('y max',size_y/2);
        fdtd.set('z min',-size_z/2.0);
        fdtd.set('z max',size_z/2.0);
        fdtd.setnamed("FDTD", "express mode", self.gpu);
        fdtd.setresource("FDTD","GPU", self.gpu);
        
        
        ## SOURCE 1
        fdtd.addmode();
        fdtd.set('direction','Forward');
        fdtd.set('injection axis','x-axis');
        #fdtd.set('polarization angle',0);
        fdtd.set('y',0);
        fdtd.set("y span",1e-6);
        fdtd.set('x',-1e-6-(self.x/2)*1e-6);
        fdtd.set('center wavelength',lam_c);
        fdtd.set('wavelength span',0);
        fdtd.set('mode selection','fundamental TE mode');
        
        
        ## MESH IN OPTIMIZABLE REGION
        fdtd.addmesh();
        fdtd.set('x',0);
        fdtd.set('x span',finer_mesh_size);
        fdtd.set('y',0);
        fdtd.set('y span',finer_mesh_size);
        fdtd.set('z',0);
        fdtd.set('z span',finer_mesh_size);
        fdtd.set('dx',mesh_x);
        fdtd.set('dy',mesh_y);
        fdtd.set('dz',mesh_z);
        
        ## OPTIMIZATION FIELDS MONITOR IN OPTIMIZABLE REGION
        
        fdtd.addpower();
        fdtd.set('name','opt_fields');
        fdtd.set('monitor type','3D');
        fdtd.set('x',0);
        fdtd.set('x span',1e-6+self.x*1e-6);
        fdtd.set('y',0);
        fdtd.set('y span',2e-6+self.y*1e-6);
        fdtd.set('z',self.thickness/2);
        fdtd.set('z span',0.4e-6);
        ## FOM FIELDS
        
        fdtd.addpower();
        fdtd.set('name','fom1');
        fdtd.set('monitor type','2D X-Normal');
        fdtd.set('x',4.5e-6+(self.x/2)*1e-6);
        fdtd.set('y',1.35e-6);
        fdtd.set('y span',1e-6);
        fdtd.set('z',0);
        fdtd.set('z span',size_z)
        
    def run_optimization(self):
        """
        Runs the Y-branch optimization process.
        """
        # Define wavelength range
        example_directory = os.getcwd()
        wavelengths = Wavelengths(start=self.wavelength_start*1e-9, stop=self.wavelength_stop*1e-9, points=101)

        # Define initial points for optimization
        initial_points_x = np.linspace(-(self.x/2)*1e-6, (self.x/2)*1e-6, self.opt_points)
        initial_points_y = np.linspace(self.wgWidth/2, self.wgWidth+(self.y/2)*1e-6, initial_points_x.size)
        initial_x1_size = self.opt_points
        initial_points_x1 = np.linspace((self.x/2)*1e-6 - self.concaveDepth, (self.x/2)*1e-6, initial_x1_size)
        initial_points_y1 = np.linspace(0.0, (self.y/2)*1e-6, initial_points_x1.size)

        # Function to define the Y-splitter geometry
        def splitter(params):
            points_x = initial_points_x
            points_y = params[:initial_points_x.size]
            points_x1 = initial_points_x1
            points_y1 = params[initial_points_x.size:]
            n_interpolation_points = 100
            polygon_points_x = np.linspace(min(points_x), max(points_x), n_interpolation_points)
            polygon_points_x1 = np.linspace(min(points_x1), max(points_x1), initial_x1_size)
            interpolator = sp.interpolate.interp1d(points_x, points_y, kind='cubic')
            interpolator1 = sp.interpolate.interp1d(points_x1, points_y1, kind='cubic')
            polygon_points_y = interpolator(polygon_points_x)
            polygon_points_y1 = interpolator1(polygon_points_x1)
            polygon_points_up = [(x, y) for x, y in zip(polygon_points_x, polygon_points_y)]
            polygon_points_up1 = [(x, y) for x, y in zip(polygon_points_x1, polygon_points_y1)]
            polygon_points_down = [(x, -y) for x, y in zip(polygon_points_x, polygon_points_y)]
            polygon_points_down1 = [(x, -y) for x, y in zip(polygon_points_x1, polygon_points_y1)]
            return np.array(polygon_points_up1 + polygon_points_up[::-1] + polygon_points_down + polygon_points_down1[::-1])

        # Initial optimization parameters
        initial_params = np.concatenate((initial_points_y, initial_points_y1))
        bounds = [(self.lowerBonds, self.upperBonds)] * initial_points_y.size
        bounds1 = [(0., (self.y/2)*1e-6+0.01e-6)] * initial_points_y1.size

        # Define materials
        eps_in = Material(name=self.material, mesh_order=2)
        eps_out = Material(name='SiO2 (Glass) - Palik', mesh_order=3)
        depth = self.thickness

        # Load previous optimization results if available
        try:
            prev_results = np.loadtxt(f'3D_parameters_{self.opt_points}.txt') * 1.0e6
        except:
            print("Couldn't find 2D optimization parameters. Using default parameters.")
            prev_results = initial_params

        # wavelengths = Wavelengths(start=self.wavelength_start*1e-9, stop=self.wavelength_stop*1e-9, points=101)
        # eps_in = Material(name=self.material, mesh_order=2)
        # eps_out = Material(name='SiO2 (Glass) - Palik', mesh_order=3)
        
        # def splitter(params):
        #     points_x = np.linspace(-(self.x/2)*1e-6, (self.x/2)*1e-6, self.opt_points)
        #     points_y = params[:self.opt_points]
        #     polygon_points = np.array([(x, y) for x, y in zip(points_x, points_y)])
        #     return polygon_points
        
        # initial_params = np.linspace(self.wgWidth/2, self.wgWidth+(self.y/2)*1e-6, self.opt_points)
        # bounds = [(self.lowerBonds, self.upperBonds)] * self.opt_points
        
        polygon = FunctionDefinedPolygon(
            func=splitter,
            initial_params=prev_results,
            bounds=bounds + bounds1,
            z=self.thickness/2,
            depth=self.thickness,
            eps_out=eps_out,
            eps_in=eps_in,
            edge_precision=5,
            dx=1.0e-9
        )
        
        fom = ModeMatch(
            monitor_name='fom1',
            mode_number='fundamental TE mode',
            direction='Forward',
            target_T_fwd=lambda wl: np.ones(wl.size),
            norm_p=1
        )
        
        optimizer = ScipyOptimizers(
            max_iter=self.max_iter,
            method='L-BFGS-B',
            scaling_factor=1.0e6,
            pgtol=1.0e-5,
            ftol=1.0e-6,
            scale_initial_gradient_to=0.0
        )
        
        opt = Optimization(
            base_script=self.y_branch_init_,
            wavelengths=wavelengths,
            fom=fom,
            geometry=polygon,
            optimizer=optimizer,
            use_var_fdtd=False,
            hide_fdtd_cad=False,
            use_deps=True,
            plot_history=True,
            store_all_simulations=False
        )
        
        results = opt.run()
        
        np.savetxt(f'3D_parameters_{self.opt_points}.txt', results[1] / 1.0e6)
        with lumapi.FDTD(hide = False) as fdtd:
            fdtd.cd(example_directory)
            self.y_branch_init_(fdtd)     
            fdtd.addpoly(vertices = splitter(results[1] / 1e-6))
            fdtd.set('x', 0.0)
            fdtd.set('y', 0.0)
            fdtd.set('z', self.thickness/2)
            fdtd.set('z span', self.thickness)
            fdtd.set('material',self.material)
            fdtd.save("y_branch_3D_FINAL")
        return results

if __name__ == "__main__":
    optimizer = YBranchOptimization()
    results = optimizer.run_optimization()
