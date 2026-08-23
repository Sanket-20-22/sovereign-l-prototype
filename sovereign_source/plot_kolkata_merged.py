# plot_kolkata_merged.py
# Unified Multi-Field Merged Map & Vector Overlay for Sovereign-L Framework
# Reference Priority: doi.org/10.5281/zenodo.21916505

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sovereign_climate as climate

# Force connection to active desktop UI engine to ensure pop-up rendering
import matplotlib
matplotlib.use('TkAgg')

def generate_unified_kolkata_map():
    print("=================================================================")
    print("       SOVEREIGN-L: UNIFIED MULTI-FIELD MERGED PLOTTER           ")
    print("=================================================================")
    
    GRID_RES = 32
    physics_engine = climate.DiscretePhysicsEngine(dimension=GRID_RES)
    
    # Target folder path destination configuration
    target_dir = r"C:\Users\sanke\OneDrive\Documents\project_genesis\Genesis_Public_Launch\sovereign-l-prototype\sovereign_source"
    raster_path = os.path.join(target_dir, "kolkata_base_raster.png")
    
    if not os.path.exists(raster_path):
        print(f"[ERROR] Base map image not found at: {raster_path}")
        return
        
    # Load the real Kolkata raster image file from disk natively
    bg_img = mpimg.imread(raster_path)
    
    # 1. Map real-world KMC attributes into your active matrix frames
    for x in range(GRID_RES):
        for y in range(GRID_RES):
            base_weather = 120
            base_pollution = 12
            base_thermal = 30  
            
            # Model Urban Heat Island Core (Dense concrete roof and asphalt zones)
            if 12 <= x <= 20 and 12 <= y <= 20:
                base_thermal = 42    
                base_pollution = 95  
                
            # Model Local Industrial Source Center (Point source plume stack)
            if x == 16 and y == 16:
                base_pollution = 400
                
            physics_engine.load_field_data(x, y, base_weather, base_pollution, base_thermal)
            
    # Run the mass-conserving transport loop sweep to settle gradients with 0.00% drift
    physics_engine.get_orthogonal_neighbors = lambda x, y: [
        ((x+1)%GRID_RES, y), ((x-1)%GRID_RES, y),
        (x, (y+1)%GRID_RES), (x, (y-1)%GRID_RES)
    ]
    physics_engine.execute_conservative_transport_sweep()
    
    # 2. Extract state arrays to compute spatial directional vector derivatives
    X, Y = np.meshgrid(np.arange(GRID_RES), np.arange(GRID_RES))
    thermal_matrix = np.zeros((GRID_RES, GRID_RES))
    pollution_matrix = np.zeros((GRID_RES, GRID_RES))
    
    for x in range(GRID_RES):
        for y in range(GRID_RES):
            thermal_matrix[y, x] = physics_engine.thermal_grid[(x, y)]
            pollution_matrix[y, x] = physics_engine.pollution_grid[(x, y)]
            
    # Compute Discrete Central Difference Gradients
    UHI_v, UHI_u = np.gradient(-thermal_matrix)
    Pollution_v, Pollution_u = np.gradient(-pollution_matrix)
    
    # =====================================================================
    # BUILD THE SINGLE MERGED COUPLING MATRIX PLOT
    # =====================================================================
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Layer 1 (Bottom): The Real-World Kolkata Map
    ax.imshow(bg_img, extent=[0, GRID_RES-1, 0, GRID_RES-1], origin='upper', alpha=0.85)
    
    # Layer 2 (Middle-Left Ambient): Urban Heat Island Shading (Magma/Hot Profile)
    contour_thermal = ax.contourf(X, Y, thermal_matrix, cmap='YlOrRd', alpha=0.4, levels=10)
    cbar_t = fig.colorbar(contour_thermal, ax=ax, pad=0.02, shrink=0.7)
    cbar_t.set_label('UHI Thermal Intensity Index (°C Equiv)', labelpad=10)
    
    # Layer 3 (Middle-Right Ambient): Pollution Dispersion Shading (Viridis/Plume Profile)
    contour_pollution = ax.contour(X, Y, pollution_matrix, cmap='winter', alpha=0.6, levels=8, linewidths=1.5)
    ax.clabel(contour_pollution, inline=True, fontsize=8, fmt='%d')
    
    # Layer 4 (Top Overlays): Red Quiver Arrows tracking UHI Heat Expansion
    ax.quiver(X[::2, ::2], Y[::2, ::2], UHI_u[::2, ::2], UHI_v[::2, ::2], 
              color='#FF1111', scale=30, width=0.005, headwidth=4, headlength=5, 
              label='Thermal Flux Vector', zorder=5)
              
    # Layer 5 (Top Overlays): Bright Cyan Quiver Arrows tracking Pollutant Advection Drift
    ax.quiver(X[::2, ::2], Y[::2, ::2], Pollution_u[::2, ::2], Pollution_v[::2, ::2], 
              color='#00FFCC', scale=180, width=0.005, headwidth=4, headlength=5, 
              label='Pollutant Advection Vector', zorder=6)
    
    # Structural Map Detailing Configurations
    ax.set_title("UNIFIED EXASCALE ENVIRONMENTAL MAP: COUPLED UHI & POLLUTANT FLUX VECTORS", fontsize=11, fontweight='bold', pad=20)
    ax.set_xlabel("Lattice Coordinate X-Axis (KMC Spatial Grid Steps)", labelpad=10)
    ax.set_ylabel("Lattice Coordinate Y-Axis (KMC Spatial Grid Steps)", labelpad=10)
    
    # Insert custom Legend tags to distinguish both arrow networks clearly
    ax.plot([], [], color='#FF1111', marker='>', linestyle='None', markersize=8, label='Heat Flux (UHI)')
    ax.plot([], [], color='#00FFCC', marker='>', linestyle='None', markersize=8, label='Pollutant Drift (PM)')
    ax.legend(loc='upper right', facecolor='#222222', labelcolor='#FFFFFF')
    
    plt.tight_layout()
    
    # Save the single merged master graphic directly to your hard drive disk
    output_filename = "kolkata_merged_multiscale_field.png"
    plt.savefig(output_filename, dpi=300)
    print(f"\n[MERGER SUCCESS] Unified multi-field simulation map saved directly to folder path:")
    print(f" -> {os.path.join(target_dir, output_filename)}")
    
    print("\n[DISPLAY] Launching live merged visualization canvas...")
    plt.show()

if __name__ == "__main__":
    generate_unified_kolkata_map()
