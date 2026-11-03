"""
Example usage of Ocular Dark Adaptation Rod Intercept Time (RIT) Skill.
Demonstrates normal rapid scotopic recovery vs prolonged rod intercept time.
"""

import json
from client import DarkAdaptationRITClient


def main():
    print("=== Testing Ocular Dark Adaptation Rod Intercept Time (RIT) Skill ===")
    client = DarkAdaptationRITClient(target_scotopic_threshold_log_units=3.0)

    # 1. Healthy normal rod adaptation: Cone plateau around 3-5 min, crosses 3.0 threshold by ~5.5 min
    t_normal = [1.0, 2.5, 4.0, 5.0, 6.0, 8.0, 10.0, 15.0]
    s_normal = [5.5, 4.2, 3.8, 3.4, 2.7, 1.8, 1.2, 0.8]  # Crosses 3.0 between 5.0 and 6.0 min (~5.57 min)
    res_normal = client.analyze_dark_adaptation_curve(t_normal, s_normal, age_years=32)
    print("\n[Case 1: Normal Rapid Scotopic Kinetics]")
    print(json.dumps(res_normal, indent=2))

    # 2. Impaired dark adaptation / delayed rhodopsin regeneration (Crosses 3.0 threshold at ~11.5 min)
    t_impaired = [1.0, 3.0, 6.0, 9.0, 11.0, 13.0, 16.0, 20.0]
    s_impaired = [5.8, 4.8, 4.3, 3.7, 3.2, 2.5, 1.9, 1.4]  # Crosses 3.0 between 11.0 and 13.0 min (~11.57 min)
    res_impaired = client.analyze_dark_adaptation_curve(t_impaired, s_impaired, age_years=68)
    print("\n[Case 2: Prolonged Rod Intercept Time / Impaired Scotopic Vision]")
    print(json.dumps(res_impaired, indent=2))

    # Assertions
    assert res_normal["rod_intercept_time_rit_min"] < 6.5
    assert res_impaired["rod_intercept_time_rit_min"] > 9.5
    assert res_normal["rod_cone_break_time_min"] < res_impaired["rod_cone_break_time_min"]
    print("\n[SUCCESS] Dark Adaptation Rod Intercept Time tests passed!")


if __name__ == "__main__":
    main()
