from city.city import City
from simulation.metrics import snapshot

STEPS = 100
PRINT_EVERY = 10


def main():
    print("initialising city...")
    city = City(seed=42)
    print(f"  {len(city.plots)} plots  |  {len(city.households)} households  |  {len(city.firms)} firms\n")

    history = []

    for step in range(STEPS):
        city.update()
        m = snapshot(step + 1, city.summary())
        history.append(m)
        if (step + 1) % PRINT_EVERY == 0:
            print(m)

    print("\ndone.")
    print(f"final budget:  {city.government.budget:.2f}")
    print(f"total hh moves:   {city.household_moves}")
    print(f"total firm moves: {city.firm_moves}")


if __name__ == "__main__":
    main()