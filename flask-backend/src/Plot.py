from src.FunctionManager import FunctionManager
import matplotlib
from math import *
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from src.Function import Function
from src.Error_Stack import ErrorStack
import os
import io
import base64

class Plot(ErrorStack):
    """
    Class responsible for plotting functions in Function Manager
    """
    def __init__(self, functionManager, N = 10000):
        super().__init__()
        self.functionManager = functionManager
        self.num_points = N
    def convert_plot_to_base64(self,figure):
        buf = io.BytesIO()

        figure.savefig(buf, format = "png")
        base64_string = base64.b64encode(buf.getvalue())
        return str(base64_string)[2:-1]

    def run(self):
        y_grid, x_grid = self.preprocess()
        plt.close("all")
        figure_list = []
        start_time = os.times()[0]
        fig = plt.figure()
        gs = 0
        # gs = fig.add_gridspec(y_grid, x_grid)
        i = 1
        for f in self.functionManager.Functions_container:
            fig = plt.figure(i)
            if f.in_dimension == 1 and f.out_dimension == 1:
                self.plot2d(f, fig,gs, i, 0)
            elif f.in_dimension == 1 and f.out_dimension == 2:
                self.plot3d_one_two(f,fig,gs,i,0)
            elif f.in_dimension == 2 and f.out_dimension == 1:
                self.plot3d_two_one(f,fig,gs,i,0)
            elif f.out_dimension ==2 and f.out_dimension ==2:
                self.plot3d_two_to_two(f,fig,gs,i,0)
            figure_list.append(self.convert_plot_to_base64(fig))
            i += 1
            plt.close("all")
        end_time = os.times()[0]
        print("Plotting took: {} seconds".format(end_time - start_time))
        plt.close("all")
        return figure_list, self.get_errors()


    def preprocess(self):
        y_grid = 1
        x_grid = 1
        for f in self.functionManager.Functions_container:
            y_grid += 1

        return y_grid, x_grid

    def plot2d(self,function, figure, grid, y_grid_number = 0, x_grid_number = 0):

        xs = np.linspace(-5, 5, self.num_points)
        ys = []

        for x in xs:
            ys.append(function.evaluate(x))
        ys = np.array(ys)

        ax = figure.add_subplot()#grid[y_grid_number:,:])
        ax.clear()
        ax.set_xlabel("{}".format(function.str_vars[0]), fontsize="8")
        ax.set_ylabel("{}({})".format(function.name, function.str_vars[0]), fontsize="8", rotation = "horizontal")
        try:
          ax.set_title(function.get_latex())
        except:
            ax.set_title(function.info_string)
        ax.plot(xs, ys)


    def plot3d_two_one(self, function, figure,grid, y_grid = 0, x_grid = 0):
        xs = np.linspace(-5, 5, 200)
        ys = np.linspace(-5, 5, 200)

        zs = []
        for i in range(len(xs)):
            zs_row = []
            for j in range(len(ys)):
                value = function.evaluate(xs[i], ys[j])
                # print("the value is {}".format(value))
                if value != [None]:
                    zs_row += value
                else:
                    # print("Adding 0")
                    self.push_error("Function {} undefined at plot value, plotting 0 instead".format(function.info_string))
                    zs_row += [0]

            zs.append(zs_row)
        zs = np.array(zs)
        zs = np.nan_to_num(zs)
        xs, ys = np.meshgrid(xs, ys)
        ax = figure.add_subplot(projection = "3d")#grid[y_grid:, :], projection="3d")
        ax.clear()
        # strs = function.get_latex()
        # if "\\bmod" in strs:
        ax.set_title(function.info_string)
        # else:
        #     ax.set_title(function.get_latex())

        ax.plot_surface(xs, ys, zs, cmap=cm.get_cmap("Spectral"), antialiased=True)


    def plot3d_one_two(self, function, figure, grid, y_grid =0, x_grid = 0):
        xs = np.linspace(-5,5,4000)
        ys = []
        zs = []
        for i in range(xs.size):
            new_y, new_z = function.evaluate(xs[i])
            if new_y != None:
                ys.append(new_y)
            else:
                ys.append(0)
                self.push_error("Function {} undefined at plot value, plotting 0 instead".format(function.info_string))
            if new_z != None:
                zs.append(new_z)
            else:
                self.push_error("Function {} undefined at plot value, plotting 0 instead".format(function.info_string))
                zs.append(0)

        ys = np.array(ys)
        zs = np.array(zs)
        copy_xs = xs
        xs, ys = np.meshgrid(xs, ys)
        copy_xs, zs = np.meshgrid(copy_xs, zs)


        ax = figure.add_subplot(projection = "3d")#grid[y_grid,x_grid], projection="3d")
        ax.clear()
        # try:
        #     ax.set_title(function.get_latex())
        # except:
        ax.set_title(function.info_string)
        ax.plot_surface(xs,ys,zs, cmap = cm.get_cmap("Spectral"), antialiased = True)

    def plot3d_two_to_two(self, function, figure,grid,y_grid =0, x_grid= 0):
        #Countor norm =1
        number_of_contours = 10

        total_xs = np.array([])
        total_ys = np.array([])
        total_contours = np.array([])
        for r in range(1,number_of_contours):
            num = 10
            angles = np.linspace(0,2*np.pi,num)
            # euclidean_norm = []
            xs = []
            ys = []
            for theta in angles:
                x_val = np.cos(theta)
                y_val = np.sin(theta)
                # euclidean_norm.append(np.sqrt( r*x_val**2 + r*y_val**2))
                x_val *= np.sqrt(r)
                y_val *= np.sqrt(r)
                xs.append(x_val)
                ys.append(y_val)
            new_xs = []
            new_ys = []
            for x in xs:
                for y in ys:
                    new_x, new_y = function.evaluate(x,y)
                    if new_x != None:
                        new_xs.append(new_x)
                    else:
                        self.push_error(
                            "Function {} undefined at plot value, plotting 0 instead".format(function.info_string))
                        new_xs.append(0)
                    if new_y != None:
                        new_ys.append(new_y)
                    else:
                        self.push_error(
                            "Function {} undefined at plot value, plotting 0 instead".format(function.info_string))
                        new_ys.append(0)

            new_xs = np.array(new_xs)

            new_ys = np.array(new_ys)

            contour_map_values = np.linspace(r,r,num*num)#*2500)
            # contour_map_values = contour_map_values.reshape(2500,2500)

            # print(contour_map_values)
            # ax = figure.add_subplot(projection="3d")
            # ax.clear()
            # ax.set_title("{}".format(function.info_string), font="Times")
            # ax.plot_wireframe(new_xs, new_ys, contour_map_values)
            # must be a better way than this #TODO Runtime here is very very bad
            total_xs = np.append(total_xs, new_xs)
            total_ys = np.append(total_ys,new_ys)
            total_contours = np.append(total_contours, contour_map_values)

        ax = figure.add_subplot(projection = "3d")
        ax.clear()
        # try:
        #     ax.set_title(function.get_latex())
        # except(ValueError):
        #     ax.set_title(function.info_string)
        ax.plot(total_xs, total_ys, total_contours)


        # ax = figure.add_subplot(projection="3d")  # grid[y_grid,x_grid], projection="3d" )
        # ax.plot_surface(new_xs, new_ys,euclidean_norm, cmap=cm.get_cmap("Spectral"), antialiased=True)


if __name__ == "__main__":
    # fm = FunctionManager("f(x,y) = (x**2 + 1/y) g(y) = (y**2, y**3) f(k) = (log(k))")
    fm = FunctionManager("f(x,y) = (tan(x+y))")
    p = Plot(fm)
    p.run()
