# Strnad et al. (2026) – Dunkelflaute Risk Assessment

**Title:** Assessing the risk of future Dunkelflaute events for Germany using generative deep learning
**Authors:** Felix Strnad, Jonathan Schmidt, Fabian Mockert, Philipp Hennig, Nicole Ludwig
**Institutions:** University of Tübingen + KIT Karlsruhe
**Publication:** Environmental Data Science, Cambridge, May 2026 (Open Access)
**Method:** Score-based Diffusion Models + CMIP6 + ERA5

## Definition
Dunkelflaute = 48h average CF (wind + solar) < 0.06

## Key Findings
- Frequency and duration: stable even under SSP2-4.5 and SSP5-8.5
- CF threshold 0.06 is scientifically validated

## Use in Project
**Implementation in `app/dunkelflaute.py`:**
```python
CF = (wind_power + solar_power) / total_capacity
is_dunkelflaute = CF_48h < 0.06