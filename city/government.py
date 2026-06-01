from dataclasses import dataclass


@dataclass
class Government:
    property_tax_rate: float = 0.01
    budget: float = 0.0

    def collect_tax(self, land_value: float) -> float:
        tax = land_value * self.property_tax_rate
        self.budget += tax
        return tax

    def __repr__(self):
        return f"Government(tax_rate={self.property_tax_rate:.2%}, budget={self.budget:.2f})"