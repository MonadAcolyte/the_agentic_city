from dataclasses import dataclass


@dataclass
class Metrics:
    step: int
    mean_land_value: float
    mean_accessibility: float
    household_moves: int
    firm_moves: int
    government_budget: float

    def __str__(self):
        return (
            f"step={self.step:>4}  "
            f"land_value={self.mean_land_value:>8.2f}  "
            f"accessibility={self.mean_accessibility:>6.4f}  "
            f"hh_moves={self.household_moves:>5}  "
            f"firm_moves={self.firm_moves:>4}  "
            f"budget={self.government_budget:>10.2f}"
        )


def snapshot(step: int, city_summary: dict) -> Metrics:
    return Metrics(
        step=step,
        mean_land_value=city_summary["mean_land_value"],
        mean_accessibility=city_summary["mean_accessibility"],
        household_moves=city_summary["household_moves"],
        firm_moves=city_summary["firm_moves"],
        government_budget=city_summary["government_budget"],
    )