# harley
cycle analysis

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