# sovereign_source/kolkata_spatial_sim.py
# Aligned Geographic Mapping Engine for KMA Using Sovereign-L

import numpy as np
import pandas as pd
import sovereign_accel as accel
import sovereign_climate as climate

# 1. Establish the actual real-world geographic boundaries of the KMA
LAT_MIN, LAT_MAX = 22.45, 22.65  # Genuine Kolkata latitude degrees
LON_MIN, LON_MAX = 88.25, 88.45  # Genuine Kolkata longitude degrees
GRID_RES = 32

lats = np.linspace(LAT_MIN, LAT_MAX, GRID_RES)
lons = np.linspace(LON_MIN, LON_MAX, GRID_RES)

physics_mesh = climate.DiscretePhysicsEngine(dimension=GRID_RES)
accelerator = accel.HardwareAcceleratorEngine()

# 2. Populate the lattice network layers by pairing indexes with real degrees
print("[GEOSPATIAL INIT] Mapping Coupled Layers over Kolkata Metropolitans...")
for i, lat in enumerate(lats):
    for j, lon in enumerate(lons):
        # Calculate distance to central Kolkata (Esplanade core approx 22.56, 88.35)
        dist_to_center = np.sqrt((lat - 22.56)**2 + (lon - 88.35)**2)
        
        base_weather = 120
        base_pollution = 10
        base_thermal = 28
        
        # Define Central Urban Heat Island Core (Dense concrete city center)
        if dist_to_center < 0.05:
            base_thermal = 38
            base_pollution = 80
        # Define Western Industrial Belt (Howrah industrial manufacturing zones)
        elif 22.60 <= lat <= 22.65 and 88.25 <= lon <= 88.30:
            base_thermal = 34
            base_pollution = 200
            
        physics_mesh.load_field_data(i, j, base_weather, base_pollution, base_thermal)

# Trigger industrial emission plume leak at core factory coordinate (16, 16)
factory_x, factory_y = 16, 16  
physics_mesh.pollution_grid[(factory_x, factory_y)] += 5000

# Process the transport loops sweeps
SIMULATION_STEPS = 12
for step in range(1, SIMULATION_STEPS + 1):
    drift_report = physics_mesh.execute_conservative_transport_sweep()

# 3. SPATIAL RE-ALIGNMENT PASS: Map raw keys to true geographic positions
# This explicitly matches every array index step with its real degree point
spatial_rows = []
for i in range(GRID_RES):
    for j in range(GRID_RES):
        spatial_rows.append({
            "latitude": float(lats[i]),    # Map index i back to true latitude degree
            "longitude": float(lons[j]),  # Map index j back to true longitude degree
            "weather_mass": physics_mesh.weather_grid[(i, j)],
            "pollution_tokens": physics_mesh.pollution_grid[(i, j)],
            "thermal_index": physics_mesh.thermal_grid[(i, j)]
        })

df_out = pd.DataFrame(spatial_rows)
df_out.to_csv("kolkata_sim_output.csv", index=False)
print("\n[SUCCESS] Spatial simulation complete. Output file written safely to: kolkata_sim_output.csv")
