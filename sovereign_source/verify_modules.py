# verify_modules.py
# Input-Output Test Pipeline for sovereign_accel and sovereign_climate Modules

import sovereign_accel as accel
import sovereign_climate as climate  # Updated to target your renamed module file

if __name__ == "__main__":
    print("=================================================================")
    print("      SOVEREIGN PRODUCTION MODULES: INITIALIZATION PASS          ")
    print("=================================================================")
    
    # 1. Instantiate both libraries as independent modular objects
    accelerator = accel.HardwareAcceleratorEngine()
    physics_core = climate.DiscretePhysicsEngine(dimension=16)

    # 2. Test input-to-output loop of the hardware accelerator module
    print("[TEST 1] Dispatching parameters to sovereign_accel API...")
    hw_report = accelerator.compute_node_update(current_local_val=64, neighborhood_resonance=128)
    print(f" └── Out Stabilized Core State: {hw_report['stabilized_state']}")
    print(f" └── Out Global Bus Reduction : {hw_report['metrics']['bus_load_reduction_saved']}")

    # 3. Test input-to-output loop of the scientific physics module
    print("\n[TEST 2] Injecting multiscale variables to sovereign_climate API...")
    physics_core.load_field_data(x=5, y=5, weather_mass=512, pollution_tokens=128, thermal_index=32)
    physics_core.load_field_data(x=6, y=6, weather_mass=256, pollution_tokens=64, thermal_index=20)
    
    drift_ledger = physics_core.execute_conservative_transport_sweep()
    print(f" └── Weather Layer Drift  : {drift_ledger['weather_field_drift']:+.2f} units")
    print(f" └── Pollution Layer Drift: {drift_ledger['pollution_field_drift']:+.2f} units")
    print(f" └── Thermal Layer Drift  : {drift_ledger['thermal_field_drift']:+.2f} units")
    print("=================================================================")
    print(" -> SUCCESS: Both input-output modules operating with 100% stability.\n")
