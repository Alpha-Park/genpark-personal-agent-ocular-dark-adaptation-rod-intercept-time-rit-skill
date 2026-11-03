---
name: genpark-personal-agent-ocular-dark-adaptation-rod-intercept-time-rit-skill
description: Scotopic Dark Adaptation Rod Intercept Time (RIT) analyzer. Tracks retinal luminance sensitivity recovery curves following photo-bleaching, fitting biphasic exponential recovery to quantify early macular and photoreceptor health.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - ophthalmology
  - retina
  - dark-adaptation
  - scotopic
  - openclaw
  - genpark
  - mcp
---

# Ocular Dark Adaptation Rod Intercept Time (RIT) Skill

## Overview
This skill computes retinal dark adaptation kinetics following a bleaching exposure:
- **Kohlrausch Bend**: Detects the inflection point separating rapid cone recovery from slow, highly sensitive rod-mediated dark adaptation.
- **Rod Intercept Time (RIT)**: The time in minutes required for retinal sensitivity to reach a standard criterion threshold ($\approx 5.0 \times 10^{-3} \text{ cd}/m^2$).
- **Early Photoreceptor Biomarker**: RIT prolongation serves as one of the earliest objective indicators of impaired nutrient transport across Bruch's membrane and the retinal pigment epithelium (RPE).

## Mathematical Formulation
1. **Biphasic Dark Adaptation Model**:
   $$S(t) = \begin{cases} S_{\text{cone}}(t) & t < t_{\alpha} \\ S_{\text{rod}}(t) & t \ge t_{\alpha} \end{cases}$$
2. **Kohlrausch Break Point**:
   $$t_{\alpha} = \arg\max_t \left| \frac{d^2 S(t)}{dt^2} \right|$$
3. **Rod Intercept Time (RIT)**:
   $$\text{RIT} = t \quad \text{such that} \quad S(t) = S_{\text{criterion}}$$

## Usage
```python
from client import DarkAdaptationRITClient

client = DarkAdaptationRITClient()
res = client.analyze_dark_adaptation_curve(
    time_minutes=[1.0, 2.5, 4.0, 5.0, 6.0, 8.0],
    log_sensitivity_thresholds=[5.5, 4.2, 3.8, 3.4, 2.7, 1.8]
)
print(res["rod_intercept_time_rit_min"])
```
