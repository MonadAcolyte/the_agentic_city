import math
import random
from typing import Dict, List, Optional

from city.plot import Plot, LAND_USE_RESIDENTIAL, LAND_USE_COMMERCIAL, LAND_USE_MIXED, LAND_USE_EMPTY
from city.household import Household
from city.firm import Firm, ALL_SECTORS
from city.government import Government


GRID_SIZE      = 40
CELL_SIZE      = 4            # each plot is a 4x4 cell
NUM_HOUSEHOLDS = 200
NUM_FIRMS      = 30

RELOCATION_SAMPLE_SIZE = 5    # plots an agent considers when deciding to move
MOVE_THRESHOLD         = 0.05 # minimum utility gain required to move
EXPLORATION_NOISE      = 0.02 # small random perturbation so agents keep exploring
MAX_HH_PER_PLOT        = 4    # density cap per residential plot


def _cells(grid_size: int, cell_size: int) -> List[tuple]:
    cells_per_side = grid_size // cell_size
    return [
        (cx * cell_size, cy * cell_size)
        for cx in range(cells_per_side)
        for cy in range(cells_per_side)
    ]


class City:
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

        self.grid_size  = GRID_SIZE
        self.cell_size  = CELL_SIZE
        self.plots:      Dict[int, Plot]      = {}
        self.households: Dict[int, Household] = {}
        self.firms:      Dict[int, Firm]      = {}
        self.government: Government           = Government()

        self.household_moves = 0
        self.firm_moves      = 0

        self.generate_grid()
        self.generate_plots()
        self.generate_households()
        self.generate_firms()
        self.update_accessibility()
        self.update_plot_values()

    def generate_grid(self):
        assert self.grid_size % self.cell_size == 0, "Grid size must be divisible by cell size"

    def generate_plots(self):
        """One plot per grid cell — 100 plots on a 40x40 / 4x4 grid."""
        for pid, (x, y) in enumerate(_cells(self.grid_size, self.cell_size)):
            self.plots[pid] = Plot(id=pid, x=x, y=y)

    def generate_households(self):
        """
        Distribute households across residential plots.
        Each plot can hold up to MAX_HH_PER_PLOT households.
        """
        all_plots = list(self.plots.values())
        for hid in range(NUM_HOUSEHOLDS):
            income = random.gauss(50_000, 15_000)
            income = max(income, 10_000)
            hh = Household(id=hid, income=income)

            available = [p for p in all_plots if p.resident_count() < MAX_HH_PER_PLOT]
            if available:
                plot = random.choice(available)
                hh.home_plot = plot.id
                plot.household_ids.append(hid)
                plot.land_use = LAND_USE_RESIDENTIAL if not plot.firm_ids else LAND_USE_MIXED

            self.households[hid] = hh

    def generate_firms(self):
        """Each firm occupies one plot (firms are singular tenants per plot)."""
        unoccupied_by_firms = [p for p in self.plots.values() if not p.firm_ids]
        for fid in range(NUM_FIRMS):
            sector            = random.choice(ALL_SECTORS)
            employees_needed  = random.randint(2, 20)
            firm = Firm(id=fid, sector=sector, plot_id=None, employees_needed=employees_needed)

            if unoccupied_by_firms:
                plot = random.choice(unoccupied_by_firms)
                firm.plot_id = plot.id
                plot.firm_ids.append(fid)
                plot.land_use = LAND_USE_COMMERCIAL if not plot.household_ids else LAND_USE_MIXED
                unoccupied_by_firms.remove(plot)

            self.firms[fid] = firm

    def _euclidean(self, p1: Plot, p2: Plot) -> float:
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    def update_accessibility(self):
        """
        Gravity-model accessibility: each plot scores 1/(d+1) for every firm,
        summed across all firm locations.
        """
        firm_plots = [
            self.plots[f.plot_id]
            for f in self.firms.values()
            if f.plot_id is not None
        ]
        for plot in self.plots.values():
            plot.accessibility = sum(
                1.0 / (self._euclidean(plot, fp) + 1.0)
                for fp in firm_plots
            )

    def update_plot_values(self):
        """
        Land value = base + accessibility premium + centrality premium.
        """
        cx = cy   = self.grid_size / 2
        max_dist  = math.sqrt(2) * self.grid_size / 2
        for plot in self.plots.values():
            dist_to_centre = math.sqrt((plot.x - cx) ** 2 + (plot.y - cy) ** 2)
            centrality     = 1.0 - (dist_to_centre / max_dist)
            plot.value     = 50.0 + (plot.accessibility * 200.0) + (centrality * 100.0)

    def _update_plot_land_use(self, plot: Plot):
        if plot.household_ids and plot.firm_ids:
            plot.land_use = LAND_USE_MIXED
        elif plot.household_ids:
            plot.land_use = LAND_USE_RESIDENTIAL
        elif plot.firm_ids:
            plot.land_use = LAND_USE_COMMERCIAL
        else:
            plot.land_use = LAND_USE_EMPTY

    def move_households(self):
        """
        Each household looks at RELOCATION_SAMPLE_SIZE plots with spare capacity.
        Moves if utility gain exceeds MOVE_THRESHOLD.
        """
        for hh in self.households.values():
            candidates = [
                p for p in self.plots.values()
                if p.resident_count() < MAX_HH_PER_PLOT
                and p.id != hh.home_plot
            ]
            if not candidates:
                continue

            sample = random.sample(candidates, min(RELOCATION_SAMPLE_SIZE, len(candidates)))

            current_util = 0.0
            if hh.home_plot is not None:
                cp = self.plots[hh.home_plot]
                current_util = hh.utility(cp.value, cp.accessibility)

            best_plot = None
            best_util = current_util

            for candidate in sample:
                u = hh.utility(candidate.value, candidate.accessibility)
                u += random.gauss(0, EXPLORATION_NOISE)
                if u > best_util + MOVE_THRESHOLD:
                    best_util = u
                    best_plot = candidate

            if best_plot is not None:
                if hh.home_plot is not None:
                    old_plot = self.plots[hh.home_plot]
                    old_plot.household_ids.remove(hh.id)
                    self._update_plot_land_use(old_plot)

                best_plot.household_ids.append(hh.id)
                self._update_plot_land_use(best_plot)
                hh.home_plot = best_plot.id
                self.household_moves += 1

    def move_firms(self):
        """
        Each firm looks at RELOCATION_SAMPLE_SIZE plots with no existing firm.
        Moves if desirability gain exceeds MOVE_THRESHOLD.
        """
        for firm in self.firms.values():
            candidates = [
                p for p in self.plots.values()
                if not p.firm_ids
                and p.id != firm.plot_id
            ]
            if not candidates:
                continue

            sample = random.sample(candidates, min(RELOCATION_SAMPLE_SIZE, len(candidates)))

            current_des = 0.0
            if firm.plot_id is not None:
                cp = self.plots[firm.plot_id]
                current_des = firm.desirability(cp.accessibility, cp.value)

            best_plot = None
            best_des  = current_des

            for candidate in sample:
                d = firm.desirability(candidate.accessibility, candidate.value)
                d += random.gauss(0, EXPLORATION_NOISE)
                if d > best_des + MOVE_THRESHOLD:
                    best_des  = d
                    best_plot = candidate

            if best_plot is not None:
                if firm.plot_id is not None:
                    old_plot = self.plots[firm.plot_id]
                    old_plot.firm_ids.remove(firm.id)
                    self._update_plot_land_use(old_plot)

                best_plot.firm_ids.append(firm.id)
                self._update_plot_land_use(best_plot)
                firm.plot_id = best_plot.id
                self.firm_moves += 1

    def collect_taxes(self):
        """Property tax on every occupied plot."""
        for plot in self.plots.values():
            if plot.is_occupied():
                self.government.collect_tax(plot.value)

    def update(self):
        """One full simulation tick."""
        self.update_accessibility()
        self.update_plot_values()
        self.move_households()
        self.move_firms()
        self.collect_taxes()

    def summary(self) -> dict:
        values          = [p.value         for p in self.plots.values()]
        accessibilities = [p.accessibility  for p in self.plots.values()]
        return {
            "mean_land_value":    sum(values) / len(values),
            "mean_accessibility": sum(accessibilities) / len(accessibilities),
            "household_moves":    self.household_moves,
            "firm_moves":         self.firm_moves,
            "government_budget":  self.government.budget,
        }