import os
import numpy as np

import matplotlib.pyplot as plt

class Reporter(object):
    def __init__(self, sample):
        self.sample = sample

    def onStart(self):
        pass

    def onCycle(self, cycle, i):
        pass

    def onItem(self, item, i, j):
        pass

    def onFinish(self):
        pass

    def onError(self, error):
        pass

    def _get_output_path(self, filename):
        return os.path.join(self.sample.output_dir, filename)


class ReporterGroup(Reporter):
    def __init__(self, sample, children):
        super(ReporterGroup, self).__init__(sample)
        self.children = children
    
    def onStart(self):
        for child in self.children:
            child.onStart()

    def onCycle(self, cycle, i):
        for child in self.children:
            child.onCycle(cycle, i)

    def onItem(self, item, i, j):
        for child in self.children:
            child.onItem(item, i, j)
    
    def onError(self, error):
        for child in self.children:
            child.onError(error)

    def onFinish(self):
        for child in self.children:
            child.onFinish()


class FileReporter(Reporter):
    def __init__(self, sample, file_name_template, buffer_size=1000):
        super(FileReporter, self).__init__(sample)
        file_name = file_name_template.format(sample_name=sample.name, ext=sample.output_file_format)
        file_path = self._get_output_path(file_name)
        self.file = open(file_path, 'w')
        self.buffer_size = buffer_size
        self.buffer = []
    
    def add_line(self, line):
        self.buffer.append(line)
        if len(self.buffer) >= self.buffer_size:
            self.flush()
    
    def flush(self):
        if self.buffer:
            self.file.writelines(self.buffer)
            self.buffer.clear()
    
    def onError(self, err):
        self.add_line('not finished report, error when reporting')

    def onFinish(self):
        self.flush()
        if self.file:
            self.file.close()


class StressrelaxationDataReporter(FileReporter):
    def __init__(self, sample):
        super(StressrelaxationDataReporter, self).__init__(sample, "CF-Stressrelaxation-data-{sample_name}.{ext}")

    def onStart(self):
        self.add_line('HoldTime(s),Strain(%),Stress(MPa)\n')

    def onCycle(self, cycle, i):
        self.add_line('Cycle {}\n'.format(cycle.no))
    
    def onItem(self, item, i, j):
        if item.cycle.k <= j and j <= item.cycle.m:
            self.add_line('{},{},{}\n'.format(item.prop1, item.prop4, item.prop3))


class CycleStressrelaxationReporter(FileReporter):
    def __init__(self, sample):
        super(CycleStressrelaxationReporter, self).__init__(sample, "CF-Cycle-Stressrelaxation-{sample_name}.{ext}")

    def onStart(self):
        self.add_line('Cycle,StressBegin(MPa),StressRelax(MPa)\n')

    def onCycle(self, cycle, i):
        self.add_line('{},{},{}\n'.format(cycle.no, cycle.stress_begin, cycle.stress_relax))


class CritialCycleDataReporter(FileReporter):
    def __init__(self, sample):
        super(CritialCycleDataReporter, self).__init__(sample, "CF-CrticalCycle-data-{sample_name}.{ext}")

    def onStart(self):
        self.add_line('Cycle,Time(s),Strain(%),Stress(MPa),Sumexten(microstrain),T1(C),T2(C),T3(C)\n')

    def onItem(self, item, i, j):
        if item.cycle.is_critial_cycle:
            self.add_line('{},{},{},{},{},{},{},{}\n'.format(item.cycle.no, item.prop1, item.prop4, item.prop3, item.prop5, item.prop6, item.prop7, item.prop8))


class HalfLifeDataReporter(FileReporter):
    def __init__(self, sample):
        super(HalfLifeDataReporter, self).__init__(sample, "CF-HalfLife-data-{sample_name}.{ext}")

    def onStart(self):
        self.add_line('Cycle,Time(s),Strain(%),Stress(MPa),Sumexten(microstrain),T1(C),T2(C),T3(C)\n')
    
    def onItem(self, item, i, j):
        if item.cycle.is_critial_cycle and item.cycle.no == round(self.sample.final / 2):
            self.add_line('{},{},{},{},{},{},{},{}\n'.format(item.cycle.no, item.prop1, item.prop4, item.prop3, item.prop5, item.prop6, item.prop7, item.prop8))


class LoadStrainRangeQReporter(FileReporter):
    def __init__(self, sample):
        super(LoadStrainRangeQReporter, self).__init__(sample, 'CF-LoadStrainRange-Q-{sample_name}.{ext}')
    
    def onStart(self):
        self.add_line("Cycle,LoadStrainRange(%),Q\n")
    
    def onCycle(self, cycle, i):
        self.add_line('{},{},{}\n'.format(cycle.no, cycle.strain_range, cycle.q))


class QReporter(FileReporter):
    def __init__(self, sample):
        super(QReporter, self).__init__(sample, 'CF-Q-report-{sample_name}.{ext}')
        self.Q = []
    
    def onCycle(self, cycle, i):
        if i < self.sample.initiation:
            self.Q.append(cycle.q)
    
    def onFinish(self):
        QQ = np.array(self.Q)
        self.add_line('Cycle range 0 to Ni0\n')
        self.add_line('Average,STD\n')
        self.add_line('{},{}'.format(np.average(QQ), QQ.std()))

        self.Q.clear()
        super(QReporter, self).onFinish()


class ChartReporter(Reporter):
    def __init__(self, sample):
        super(ChartReporter, self).__init__(sample)
        self.strain_range = []
        self.figure = None
        self.axes = None
        self.cycle_count = 0
        self.critial_draw_data = dict()
    
    def onStart(self):
        self.figure, self.axes = plt.subplots()

    def onCycle(self, cycle, i):
        self.cycle_count+=1
        self.strain_range.append(cycle.strain_range)
        if cycle.is_critial_cycle:
            strain_cr, stress_cr = [], []
            for item in cycle.items:
                strain_cr.append(item.prop4)
                stress_cr.append(item.prop3)
            self.critial_draw_data[cycle.no] = (strain_cr, stress_cr)

        if cycle.no in self.sample.fitting_cycle_nos_by_picture and cycle.xx is not None and cycle.z is not None:
            self.axes.clear()
            self.axes.set_xlabel('Strain in relaxation (%)', fontsize='15')
            self.axes.set_ylabel('Stress in relaxation (MPa)', fontsize='15')
            self.axes.set_title('Cycle{}'.format(cycle.no), fontsize='15')
            self.axes.plot(cycle.xx, np.polyval(cycle.z, cycle.xx), 'b--')

            xx, yy = [], []
            for fitting in cycle.get_fittings():
                xx.append(fitting.prop4)
                yy.append(fitting.prop3)
            self.axes.scatter(xx, yy, s=10, facecolors='none', edgecolors='r')

            self.figure.savefig(self._get_output_path('CF-Cycle-{}.png'.format(cycle.no)))

    def onFinish(self):
        # picture 1
        self.axes.clear()
        self.axes.set_xlabel('Strain(%)', fontsize='15')
        self.axes.set_ylabel('Stress(MPa)', fontsize='15')
        self.axes.set_title('Cyclic loop', fontsize='15')

        for cycle_no, (strain_cr, stress_cr) in self.critial_draw_data.items():
            self.axes.plot(strain_cr, stress_cr, label='#{}'.format(cycle_no))

        self.figure.savefig(self._get_output_path('CF-Cyclic-Loop.png'))

        # picture 2
        self.axes.clear()
        self.axes.set_xlabel('Cycle', fontsize='15')
        self.axes.set_ylabel('Load strain range (%)', fontsize='15')
        self.axes.set_title('Cyclic load strain range', fontsize='15')
        n = np.linspace(1, self.cycle_count, self.cycle_count)
        self.axes.scatter(n, self.strain_range, s=10, facecolors='none', edgecolors='r', label='Experimental data')
        self.axes.axvline(x=self.sample.initiation, linewidth=0.5, color='b', label='Failure initiation')
        self.axes.axvline(x=self.sample.final, linewidth=0.5, color='r', label='Final failure')

        self.figure.savefig(self._get_output_path('CF-Cyclic-Load-Strain-Range.png'))


class ResultFileReporter(ReporterGroup):
    def __init__(self, sample):
        super(ResultFileReporter, self).__init__(sample, [
            StressrelaxationDataReporter(sample),
            CycleStressrelaxationReporter(sample),
            CritialCycleDataReporter(sample),
            HalfLifeDataReporter(sample),
            LoadStrainRangeQReporter(sample),
            QReporter(sample)
        ])


class CommonReporter(ReporterGroup):
    def __init__(self, sample):
        super(CommonReporter, self).__init__(None, [
            ResultFileReporter(sample),
            ChartReporter(sample)
        ])
