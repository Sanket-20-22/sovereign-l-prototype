# sovereign_source/plot_kolkata_vectors.py
# Aligned Background Map Vector Field Plotter for Sovereign-L Framework
# Reference Priority: doi.org/10.5281/zenodo.21916505

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sovereign_climate as climate

def generate_kolkata_vector_fields():
    print("=================================================================")
    print("       SOVEREIGN-L: KOLKATA GRADIENT VECTOR FIELD PLOTTER        ")
    print("=================================================================")
    
    GRID_RES = 32
    physics_engine = climate.DiscretePhysicsEngine(dimension=GRID_RES)
    
    # Target folder path destination configuration
    target_dir = r"C:\Users\sanke\OneDrive\Documents\project_genesis\Genesis_Public_Launch\sovereign-l-prototype\sovereign_source"
    raster_path = os.path.join(target_dir, "kolkata_base_raster.png")
    
    # Check if the base raster image file exists on disk cleanly
    if not os.path.exists(raster_path):
        print(f"[ERROR] Could not find base map image file at: {raster_path}")
        print("Please ensure your 'kolkata_base_raster.png' is placed in your sovereign_source folder.")
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
    # Adjust gradient sign alignment to map flows naturally outward from source boundaries
    UHI_v, UHI_u = np.gradient(-thermal_matrix)
    Pollution_v, Pollution_u = np.gradient(-pollution_matrix)
    
    # =====================================================================
    # RENDER PASS 1: UHI THERMAL INDEX FLUX OVER REAL MAP (SLIDE 5)
    # =====================================================================
    fig1 = plt.figure(num=1, figsize=(11, 9))
    ax1 = fig1.add_subplot(111)
    
    # SYSTEM CRITICAL STEP: Project the real Kolkata base map image as the absolute bottom layer
    ax1.imshow(bg_img, extent=[0, GRID_RES-1, 0, GRID_RES-1], origin='upper', alpha=0.9)
    
    # Overlay the semi-transparent thermodynamic intensity contours
    contour1 = ax1.contourf(X, Y, thermal_matrix, cmap='magma', alpha=0.55, levels=15)
    cbar1 = fig1.colorbar(contour1, ax=ax1)
    cbar1.set_label('Thermal Energy Intensity Index (°C Equiv)', labelpad=15)
    
    # Mount high-contrast direction arrows over the geography features
    ax1.quiver(X[::2, ::2], Y[::2, ::2], UHI_u[::2, ::2], UHI_v[::2, ::2], 
              color='#FF3333', scale=25, width=0.005, headwidth=4, headlength=5, zorder=5)
    
    ax1.set_title("SLIDE 5: KOLKATA METROPOLITAN URBAN HEAT ISLAND FLUX VECTOR FIELD", fontsize=11, fontweight='bold', pad=20)
    ax1.set_xlabel("Lattice Coordinate X-Axis (KMC Spatial Grid Steps)", labelpad=10)
    ax1.set_ylabel("Lattice Coordinate Y-Axis (KMC Spatial Grid Steps)", labelpad=10)
    plt.tight_layout()
    plt.savefig("slide5_uhi_vectors.png", dpi=300)
    print("[EXPORT SUCCESS] Map-Aligned high-resolution thermal vector chart saved -> slide5_uhi_vectors.png")

    # =====================================================================
    # RENDER PASS 2: POLLUTANT ADVECTION DISPERSION OVER REAL MAP (SLIDE 6)
    # =====================================================================
    fig2 = plt.figure(num=2, figsize=(11, 9))
    ax2 = fig2.add_subplot(111)
    
    # Project the identical real Kolkata image map behind your pollutant vectors layer
    ax2.imshow(bg_img, extent=[0, GRID_RES-1, 0, GRID_RES-1], origin='upper', alpha=0.9)
    
    # Overlay the semi-transparent air mass pollution tokens density contours
    contour2 = ax2.contourf(X, Y, pollution_matrix, cmap='viridis', alpha=0.55, levels=15)
    cbar2 = fig2.colorbar(contour2, ax=ax2)
    cbar2.set_label('Atmospheric Pollutant Token Density (PM2.5 Equiv)', labelpad=15)
    
    # Mount high-contrast direction arrows tracking emission plume drift vectors over city streets
    ax2.quiver(X[::2, ::2], Y[::2, ::2], Pollution_u[::2, ::2], Pollution_v[::2, ::2], 
              color='#00CC00', scale=150, width=0.005, headwidth=4, headlength=5, zorder=5)
    
    ax2.set_title("SLIDE 6: KOLKATA METROPOLITAN POLLUTANT DISPERSION FLUX VECTOR FIELD", fontsize=11, fontweight='bold', pad=20)
    ax2.set_xlabel("Lattice Coordinate X-Axis (KMC Spatial Grid Steps)", labelpad=10)
    ax2.set_ylabel("Lattice Coordinate Y-Axis (KMC Spatial Grid Steps)", labelpad=10)
    plt.tight_layout()
    plt.savefig("slide6_pollution_vectors.png", dpi=300)
    print("[EXPORT SUCCESS] Map-Aligned high-resolution pollution vector chart saved -> slide6_pollution_vectors.png")
    
    print("\n[DISPLAY] Deploying synchronized multi-field map graphics plots...")
    plt.show()

if __name__ == "__main__":
    generate_kolkata_vector_fields()
