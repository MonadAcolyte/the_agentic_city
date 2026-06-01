from dataclasses import dataclass
from typing import Optional


SECTOR_RETAIL      = "retail"
SECTOR_OFFICE      = "office"
SECTOR_INDUSTRIAL  = "industrial"

ALL_SECTORS = [SECTOR_RETAIL, SECTOR_OFFICE, SECTOR_INDUSTRIAL]


@dataclass
class Firm:
    id: int
    sector: str
    plot_id: Optional[int]
    employees_needed: int

    def desirability(self, plot_accessibility: float, plot_value: float) -> float:
        """
        Firms prefer accessible plots but are sensitive to land cost.
        """
        return plot_accessibility - (plot_value * 0.001)

    def __repr__(self):
        return f"Firm(id={self.id}, sector={self.sector}, plot={self.plot_id}, employees={self.employees_needed})"