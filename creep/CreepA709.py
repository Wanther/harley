from typing import List
import numpy as np

def creepfracture(stress, C, a0, a1, a2, T):
    'Calculate creep fracture time'
    return (3600.00 * (10**(((a0 + a1 * np.log10(stress) + a2 * np.log10(stress) * np.log10(stress)) / T) - C)))**(-1)

def yfit(x, poly):
    return np.exp(poly(np.log(x)))

class CreepA709:

    class Data:
        def __init__(self, times: List[float], stresses: List[float], base_time: float):
            self.times = times
            self.stresses = stresses
            self.base_time = base_time
            self.relative_times = list(map(lambda t: t - base_time + 0.02, times))

    class Result:
        def __init__(self, base_time: float, time_fits: List[float], stress_fits: List[float]):
            self.base_time = base_time
            self.time_fits = time_fits
            self.stress_fits = stress_fits
    
    def __init__(self, Temperature: int = 816, N: int = 8000, C: float = 14.9249760029308, a0: float = 26139.4634995320, a1: float = -2341.98112181595, a2: float = -739.1914468118):
        # parameters
        self.Temperature = Temperature
        self.N = N
        self.C = C  # 15.691918338
        self.a0 = a0  # 27068.250719
        self.a1 = a1  # -2045.2573528
        self.a2 = a2  # -906.37927664
        self.T = self.Temperature + 273.15

    def load_data(self, csvFile: str) -> Data:
        times = []
        stresses = []

        # file is auto closed in `with` statement
        with open(csvFile, 'r') as file:
            content = file.readlines()
            for cont in content[1:]:
                (time, stress) = cont.split(',')
                times.append(float(time))
                stresses.append(float(stress))

        return CreepA709.Data(times, stresses, times[0])

    def calculate(self, data: Data) -> Result:
        xx = np.array(data.relative_times)
        yy = np.array(data.stresses)
        logxx = np.log(xx)
        logyy = np.log(yy)
        sigma = np.ones(len(xx))
        sigma[0] = 10
        coeffs = np.polyfit(logxx, logyy, deg=3, w=sigma)
        time_fits = np.linspace(0.02, 120 + 0.02, num=121)
        poly = np.poly1d(coeffs)
        stress_fits = yfit(time_fits, poly)

        return CreepA709.Result(data.base_time, time_fits, stress_fits)
    
    def export_csv(self, result: Result, csvFile: str):
        with open(csvFile, 'w') as f:
            lines = ['Time,Stress\n']
            for i in range(len(result.time_fits)):
                line = '{},{}\n'.format(result.time_fits[i] + result.base_time, result.stress_fits[i])
                lines.append(line)
            f.writelines(lines)

    def draw_in_axes(self, title: str, data: Data, result: Result, axes):
        axes.set_title(title, fontdict={'fontsize': 15})
        axes.set_ylabel('Stress in relaxation (MPa)', fontdict={'fontsize': 15})
        axes.set_xlabel('Hold time (s)', fontdict={'fontsize': 15})

        axes.scatter(data.times, data.stresses, s=30, facecolors='none', edgecolors='k', label='Experimental data')
        axes.plot(result.time_fits + result.base_time, result.stress_fits, 'r-', linewidth=2)


if __name__ == '__main__':
    sample_name = '204D-D4-37'
    # Create a Analyzer
    analyzer = CreepA709(
        Temperature = 816,
        N = 8000,
        C = 14.9249760029308,  # 15.691918338
        a0 = 26139.4634995320,  # 27068.250719
        a1 = -2341.98112181595,  # -2045.2573528
        a2 = -739.1914468118,  # -906.37927664
    )
    # Load data
    data = analyzer.load_data('creep\\{}.csv'.format(sample_name))
    # Calculate result
    result = analyzer.calculate(data)
    # Export to CSV or Show Chart
    # analyzer.export_csv(result, 'creep\\{}_FittingCurve.csv'.format(sample_name))
    from matplotlib import pyplot as plt
    analyzer.draw_in_axes(sample_name, data, result, plt.figure().add_subplot())
    plt.show()