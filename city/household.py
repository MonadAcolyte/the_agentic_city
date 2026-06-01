from dataclasses import dataclass
from typing import Optional


@dataclass
class Household:
    id: int
    income: float
    home_plot: Optional[int] = None

    def utility(self, plot_value: float, plot_accessibility: float) -> float:
        """
        Simple utility score for a plot.
        Higher accessibility and lower cost relative to income is preferred.
        """
        affordability = 1.0 - (plot_value / (self.income + 1e-9))
        return plot_accessibility + max(affordability, 0.0)

    def __repr__(self):
        return f"Household(id={self.id}, income={self.income:.0f}, home={self.home_plot})"