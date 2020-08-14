import sys, os
import math, heapq, numpy as np

import time

import matplotlib.pyplot as plt

from components import ProcessPoolExecutor, TxtCycleFileParser
from models import Cycle, CycleItem, Sample
from reporters import ReporterGroup, CommonReporter, ChartReporter, ResultFileReporter


class CycleAnalyst:

    def __init__(self):
        pass

    def analysis(self, sample, parser=TxtCycleFileParser(), reporter=None):
        reporter = reporter or CommonReporter(sample) # default reporter

        cycles = []

        with ProcessPoolExecutor() as executor:
            tasks = []
            for i, cycle_lines in enumerate(parser.parse_each_cycle(sample.file)):
                if i == 0:
                    sample.offset = float(cycle_lines[1].decode().split()[4].strip())
                task = executor.submit(self.parse_and_calculate, [cycle_lines, sample])

                tasks.append(task)

            for task in tasks:
                cycles.append(task.result())

        self.report(cycles, reporter)
    
    def parse_and_calculate(self, cycle_lines, sample):
        cycle = Cycle(cycle_lines)
        cycle.calculate(sample)
        return cycle

    def report(self, cycles, reporter):
        try:
            reporter.onStart()

            for i, cycle in enumerate(cycles):
                reporter.onCycle(cycle, i)

                for j, item in enumerate(cycle.items):
                    reporter.onItem(item, i, j)

        except Exception as err:
            reporter.onError(err)
            raise err
        finally:
            reporter.onFinish()


if __name__ == '__main__':

    ts = time.time()

    sample = Sample(
        file = 'D:\\Users\\wanghe\\Desktop\\haley_data\\SBS_G91_291-19.txt',
        ID = 0.0,
        OD = 0.250,
        E = 161000.00,
        initiation = 2511,
        final = 2719,
        loadingtime = 1.20,
        holdingtime = 600.00,
        stress_relax_count = 20,
        noise_count = 200,
        holdtype = Sample.COMPEESSION,
        fitting_num = 600,
        fitting_windowsize = 131,
        fitting_polyorder = 2
    )

    # CycleAnalyst().analysis(sample)

    # CycleAnalyst().analysis(sample, reporter = ChartReporter(sample)) # chart only

    CycleAnalyst().analysis(sample, reporter = ResultFileReporter(sample)) # file only

    print('finished in %s seconds' % round(time.time() - ts, 3))