"""
Ocular Dark Adaptation Rod Intercept Time (RIT) & Retinal Kinetics Client.
Zero-mock pure Python standard library implementation.
Calculates biphasic dark adaptation recovery curve, Kohlrausch bend (rod-cone break),
and Rod Intercept Time (RIT in minutes) to evaluate scotopic photoreceptor sensitivity.
"""

import math
from typing import Dict, Any, List, Optional, Tuple


class DarkAdaptationRITClient:
    """
    Evaluates retinal scotopic adaptation dynamics and calculates the Rod Intercept Time (RIT),
    defined as the duration in minutes required for visual sensitivity to recover to a standard
    scotopic sensitivity threshold (typically 5.0 x 10^-3 cd/m^2 or log sensitivity = 3.0) post-bleach.
    """

    def __init__(self, target_scotopic_threshold_log_units: float = 3.0):
        self.target_threshold = target_scotopic_threshold_log_units

    def analyze_dark_adaptation_curve(
        self,
        time_minutes: List[float],
        log_sensitivity_thresholds: List[float],
        age_years: Optional[int] = 35
    ) -> Dict[str, Any]:
        """
        Analyzes dark adaptation trajectory.
        time_minutes: Elapsed minutes since photo-bleach exposure (e.g., [1.0, 2.5, 4.0, ...]).
        log_sensitivity_thresholds: Log luminance thresholds (log cd/m^2) measured over time.
        age_years: Subject age in years.
        """
        if not time_minutes or not log_sensitivity_thresholds:
            raise ValueError("Time and sensitivity series cannot be empty.")
        if len(time_minutes) != len(log_sensitivity_thresholds):
            raise ValueError("Time series and sensitivity series must have identical length.")
        if len(time_minutes) < 4:
            raise ValueError("Dark adaptation analysis requires at least 4 temporal measurements.")

        # Ensure sorted by time
        data_points = sorted(zip(time_minutes, log_sensitivity_thresholds), key=lambda x: x[0])
        times = [p[0] for p in data_points]
        values = [p[1] for p in data_points]

        # Identify the Kohlrausch bend (rod-cone break):
        # Cone recovery typically plateaus between 3 to 7 minutes before the rod recovery phase initiates.
        # The transition point has the minimum second derivative / inflection point.
        break_index = 1
        max_curvature = -float("inf")
        for i in range(1, len(times) - 1):
            dt1 = times[i] - times[i - 1]
            dt2 = times[i + 1] - times[i]
            if dt1 > 0 and dt2 > 0:
                slope1 = (values[i] - values[i - 1]) / dt1
                slope2 = (values[i + 1] - values[i]) / dt2
                curvature = abs(slope2 - slope1)
                if curvature > max_curvature:
                    max_curvature = curvature
                    break_index = i

        rod_cone_break_time_min = times[break_index]

        # Calculate Rod Intercept Time (RIT):
        # RIT is the time at which sensitivity reaches the predefined target threshold.
        # Linear interpolation between points crossing target_threshold
        rit_minutes = None
        for i in range(len(values) - 1):
            v1, v2 = values[i], values[i + 1]
            t1, t2 = times[i], times[i + 1]
            if (v1 >= self.target_threshold >= v2) or (v1 <= self.target_threshold <= v2):
                if v2 != v1:
                    frac = (self.target_threshold - v1) / (v2 - v1)
                    rit_minutes = t1 + frac * (t2 - t1)
                    break

        if rit_minutes is None:
            # If not reached within measured time, extrapolate from last rod slope
            if len(values) >= 2:
                last_slope = (values[-1] - values[-2]) / (times[-1] - times[-2])
                if last_slope < 0:
                    rit_minutes = times[-1] + (self.target_threshold - values[-1]) / last_slope

        # Normal clinical RIT reference:
        # Healthy young/middle-aged adults: RIT < 6.5 minutes.
        # Normal aging: slight extension (< 9.0 minutes).
        # Impaired dark adaptation (early sub-RPE lipid deposition, AMD): RIT > 9.5 minutes.
        # Severe photoreceptor / retinoid cycle dysfunction: RIT > 15.0 - 20.0 minutes.
        if rit_minutes is not None:
            if rit_minutes <= 6.5:
                classification = "Optimal Scotopic Rod Kinetics"
                clinical_interpretation = "Rapid rhodopsin regeneration; normal Bruch membrane and choriocapillaris nutrient exchange."
                adaptation_speed = "Normal / Fast"
            elif rit_minutes <= 9.0:
                classification = "Mild Scotopic Adaptation Delay"
                clinical_interpretation = "Borderline dark adaptation time within acceptable limits for physiological aging."
                adaptation_speed = "Mild Delay"
            elif rit_minutes <= 12.5:
                classification = "Moderate Dark Adaptation Impairment"
                clinical_interpretation = "Elevated Rod Intercept Time; suggests sub-RPE drusenoid deposition or retinoid transport compromise."
                adaptation_speed = "Moderate Delay"
            else:
                classification = "Severe Scotopic Photoreceptor Dysfunction"
                clinical_interpretation = "Pronounced RIT prolongation; high risk of night blindness / nyctalopia or early macular degeneration."
                adaptation_speed = "Severe Prolongation"
        else:
            classification = "Undetermined / Insufficient Curve Progression"
            clinical_interpretation = "Target sensitivity threshold not attained within sampling window."
            adaptation_speed = "Incomplete"

        return {
            "status": "success",
            "samples_analyzed": len(times),
            "target_threshold_log_units": self.target_threshold,
            "rod_cone_break_time_min": round(rod_cone_break_time_min, 2),
            "rod_intercept_time_rit_min": round(rit_minutes, 2) if rit_minutes is not None else None,
            "final_recorded_sensitivity": round(values[-1], 2),
            "evaluation": {
                "classification": classification,
                "adaptation_speed": adaptation_speed,
                "clinical_interpretation": clinical_interpretation
            }
        }
