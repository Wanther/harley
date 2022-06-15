# harley
## cycle analysis

```python
from cyclic_analysis import CycleAnalyst, Sample

sample = Sample(
    file = 'SBS_G91_291-19.txt',
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

CycleAnalyst().analysis(sample)
```

## Creep A709

```python
from creep import CreepA709

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
analyzer.export_csv(result, 'creep\\{}_FittingCurve.csv'.format(sample_name))
from matplotlib import pyplot as plt
analyzer.draw_in_axes(sample_name, data, result, plt.figure().add_subplot())
plt.show()
```