# sovereign_climate.py
# Corrected Input/Output Library for Coupled Discrete Statistical Mechanics Simulations

class DiscretePhysicsEngine:
    def __init__(self, dimension=256):
        """Initializes an empty multiscale matrix grid coordinate space."""
        self.dim = int(dimension)
        self.weather_grid = {}
        self.pollution_grid = {}
        self.thermal_grid = {}
        self.clear_all_layers()

    def clear_all_layers(self):
        for x in range(self.dim):
            for y in range(self.dim):
                self.weather_grid[(x, y)] = 0
                self.pollution_grid[(x, y)] = 0
                self.thermal_grid[(x, y)] = 0

    def load_field_data(self, x, y, weather_mass, pollution_tokens, thermal_index):
        """Direct Input Channel: Populates a target coordinate space frame."""
        if (0 <= x < self.dim) and (0 <= y < self.dim):
            self.weather_grid[(x, y)] = int(weather_mass)
            self.pollution_grid[(x, y)] = int(pollution_tokens)
            self.thermal_grid[(x, y)] = int(thermal_index)

    def execute_conservative_transport_sweep(self):
        """
        Executes a coupled fluid advection pass using the Conservative Mass-Sharing Protocol.
        Output: Dictionary tracking absolute mathematical numerical drift profiles
        """
        # Record baseline initialization field mass balances
        init_w = sum(self.weather_grid.values())
        init_p = sum(self.pollution_grid.values())
        init_t = sum(self.thermal_grid.values())

        next_w = { (x,y): 0 for x in range(self.dim) for y in range(self.dim) }
        next_p = { (x,y): 0 for x in range(self.dim) for y in range(self.dim) }
        next_t = { (x,y): 0 for x in range(self.dim) for y in range(self.dim) }

        # Discrete cellular automata state transition sweep
        for x in range(self.dim):
            for y in range(self.dim):
                w_val = self.weather_grid[(x, y)]
                p_val = self.pollution_grid[(x, y)]
                t_val = self.thermal_grid[(x, y)]

                # Pure Base-8 Conservative splitting rules applied to each layer independently
                w_share = w_val // 8
                p_share = p_val // 8
                t_share = t_val // 8

                next_w[(x, y)] += w_val % 8
                next_p[(x, y)] += p_val % 8
                next_t[(x, y)] += t_val % 8

                # 8 Orthogonal axial neighborhood distribution routing tracks
                neighbors = [
                    ((x+1)%self.dim, y), ((x-1)%self.dim, y),
                    (x, (y+1)%self.dim), (x, (y-1)%self.dim),
                    ((x+1)%self.dim, (y+1)%self.dim), ((x-1)%self.dim, (y-1)%self.dim),
                    ((x+1)%self.dim, (y-1)%self.dim), ((x-1)%self.dim, (y+1)%self.dim)
                ]
                for nx, ny in neighbors:
                    next_w[(nx, ny)] += w_share
                    next_p[(nx, ny)] += p_share
                    next_t[(nx, ny)] += t_share

        # SCIENTIFIC COUPLING STEP: 
        # Apply the Urban Heat Island thermal feedback from the pollution layer 
        # using a balanced, zero-net-flux transformation to ensure perfect conservation.
        for x in range(self.dim):
            for y in range(self.dim):
                # Calculate trapped heat overhead from current node pollution density
                current_p_density = next_p[(x, y)]
                heat_induced_overhead = current_p_density // 32
                
                # Symmetrically shift heat overhead from a neighbor to the local node.
                # This simulates real-world heat stagnation without creating energy out of thin air.
                neighbors = [
                    ((x+1)%self.dim, y), ((x-1)%self.dim, y),
                    (x, (y+1)%self.dim), (x, (y-1)%self.dim)
                ]
                target_neighbor = neighbors[(x + y) % 4]
                
                # Transfer the thermal units: local gains, neighbor loses exactly the same amount
                next_t[(x, y)] += heat_induced_overhead
                next_t[target_neighbor] -= heat_induced_overhead

        self.weather_grid = next_w
        self.pollution_grid = next_p
        self.thermal_grid = next_t

        return {
            "weather_field_drift": float(sum(self.weather_grid.values()) - init_w),
            "pollution_field_drift": float(sum(self.pollution_grid.values()) - init_p),
            "thermal_field_drift": float(sum(self.thermal_grid.values()) - init_t)
        }
