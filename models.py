import os
import numpy as np
import heapq

from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

from functions import (
    strain, stress, q_factor
)

class CycleItem:
    def __init__(self, args):
        self.cycle = None
        # self.seq = int(float(args[0]))
        self.prop1 = float(args[1])
        # self.prop2 = float(args[2])
        self.prop3 = float(args[3])
        self.prop4 = float(args[4])
        self.prop5 = float(args[5])
        self.prop6 = float(args[6])
        self.prop7 = float(args[7])
        self.prop8 = float(args[8])
        # self.prop9 = float(args[9])
        # self.prop11 = float(args[10])
        # self.prop12 = float(args[11])


class Cycle:

    def __init__(self, lines):
        self.k = -1
        self.m = -1
        self.maxload_strain = -9999.0
        self.max_strain = -9999.0
        self.stress_begin = 0.0
        self.stress_relax = 0.0
        self.strain_range = 0.0
        self.q = None
        self.is_critial_cycle = False
        self.xx = None
        self.z = None

        for i, line in enumerate(lines):
            line = line.decode()
            if i == 0:
                self.no = int(line[line.find('=') + 1:].strip())
                self.items = []
            else:
                self.add_item(CycleItem(line.split()))

    def add_item(self, item):
        item.cycle = self
        self.items.append(item)
    
    def calculate(self, sample):

        if self.no in sample.critial_cycle_nos:
            self.is_critial_cycle = True
        
        start_time = self.items[0].prop1 + sample.loadingtime
        end_time = start_time + sample.holdingtime

        for i, item in enumerate(self.items):
            
            item.prop4 = strain(item.prop4, sample.offset)
            item.prop3 = stress(item.prop3, sample.OD, sample.ID)

            if abs(start_time - item.prop1) <= 0.001:
                start_time = item.prop1
                self.k = i + 1

            if abs(end_time - item.prop1) <= 0.001:
                end_time = item.prop1
                self.m = i

            if item.prop4 > self.max_strain:
                self.max_strain = item.prop4

        self.maxload_strain = self.items[self.k].prop4
        self.strain_range = self.max_strain - self.maxload_strain
        self.stress_begin = self.items[self.k].prop3
        self.stress_relax = self._calculate_stress_relax(sample.stress_relax_count)
        self.q = self._calculate_q(sample.noise_count, sample.holdtype, sample.E, sample.fitting_num, sample.fitting_windowsize, sample.fitting_polyorder)
    
    def get_fittings(self):
        if self.k == -1 or self.m == -1:
            raise Exception('k or m not calculated')
        return self.items[self.k: self.m + 1]
    
    def _calculate_stress_relax(self, count):
        stress_relax = 0.0
        for i in range(self.m - count, self.m):
            stress_relax = stress_relax + self.items[i].prop3
        return stress_relax / count

    def _calculate_q(self, noise_count, holdtype, E, fitting_num, fitting_windowsize, fitting_polyorder):
        fittings = self.get_fittings()

        if holdtype == Sample.COMPEESSION:
            top_n_small_items = heapq.nsmallest(noise_count, fittings, key=lambda item: item.prop4)
            n = len(top_n_small_items)

            fittings = list(filter(lambda item: item.prop4 > top_n_small_items[n - 1].prop4, fittings))
        else:
            top_n_large_items = heapq.nlargest(noise_count, fittings, key=lambda item: item.prop4)
            n = len(top_n_large_items)
            fittings = list(filter(lambda item: item.prop4 < top_n_large_items[n - 1].prop4, fittings))

        if len(fittings) <= 2:
            return 1.0

        xx = []
        yy = []

        min_stress_in_fittings = 9999.00
        max_stress_in_fittings = -9999.00

        for fitting in fittings:
            xx.append(fitting.prop4)
            yy.append(fitting.prop3)
            if fitting.prop3 > max_stress_in_fittings:
                max_stress_in_fittings = fitting.prop3
            
            if fitting.prop3 < min_stress_in_fittings:
                min_stress_in_fittings = fitting.prop3
        
        self.xx = np.array(xx)
        yy = np.array(yy)

        ysm = np.linspace(min_stress_in_fittings, max_stress_in_fittings, fitting_num)
        itp = interp1d(yy, xx, kind='linear')
        xsm = savgol_filter(itp(ysm), fitting_windowsize, fitting_polyorder)

        self.z = np.polyfit(xsm, ysm, 1)
        return q_factor(E, self.z[0])


class Sample:
    COMPEESSION = 0
    TENSION = 1

    def __init__(self, file, ID, OD, E, initiation, final, loadingtime, holdingtime, stress_relax_count, noise_count, holdtype, fitting_num, fitting_windowsize, fitting_polyorder, output_dir=None, fitting_cycle_nos_by_picture=None, output_file_format='csv'):
        self.ID = ID
        self.OD = OD
        self.E = E
        self.initiation = initiation
        self.final = final
        self.loadingtime = loadingtime
        self.holdingtime = holdingtime
        self.stress_relax_count = stress_relax_count
        self.noise_count = noise_count
        self.holdtype = holdtype
        self.fitting_num = fitting_num
        self.fitting_windowsize = fitting_windowsize
        self.fitting_polyorder = fitting_polyorder
        self.output_file_format = output_file_format
        self.fitting_cycle_nos_by_picture = fitting_cycle_nos_by_picture or self._get_default_fitting_cycle_nos_by_picture(final, initiation)

        self.file = os.path.realpath(file)
        self.name, _ = os.path.splitext(os.path.basename(self.file))

        if output_dir is None:
            output_dir = os.path.dirname(self.file)
        self.output_dir = output_dir

        self.critial_cycle_nos = self._get_critial_cycle_nos()

        # wait until first cycle parsed
        self.offset = None
    
    def _get_critial_cycle_nos(self):
        critial_cycle_nos = [1, 2, 3, 10, 50, round(self.final / 2)]
        critial_cycle_nos.extend([i for i in range(100, self.final + 1, 100)])
        critial_cycle_nos.extend([self.initiation, self.final])
        return critial_cycle_nos
    
    def _get_default_fitting_cycle_nos_by_picture(self, final , initiation):
        return [1, 2, 3, 10, 50, round(final / 2), initiation]