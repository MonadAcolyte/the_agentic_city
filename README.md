# The Agentic City

A city with a multi-agent simulation that aims to test, via emergent behaviour, optimality for taxation, transport systems, sustainable use of land, development, and more.

# Design principles

1. The simulation engine is independent of visualization.

2. Agents make local decisions using incomplete information.

3. Complex city-wide behaviour should emerge from simple rules.

4. Policies should affect incentives rather than directly control outcomes.

5. The model should remain computationally lightweight.

# Simulation Time Loop

Simulation Tick

1. Calculate accessibility
2. Update plot values
3. Households evaluate relocation
4. Firms evaluate relocation
5. Collect taxes
6. Update metrics
7. Advance timestep

# V 0.0

Working proof of concept initial files.

```
main.py

city/
    city.py
    plot.py
    household.py
    firm.py
    government.py

simulation/
    engine.py
    accessibility.py
    relocation.py
    metrics.py

visualization/
    plots.py
```
The program should be able to do:

```
city = City()

city.generate_grid()

city.generate_plots()

city.generate_households()

city.generate_firms()
```

...with a setpup that includes something like:
- 40x40 world
- 100 plots
- 200 households
- 30 firms

# V 1.0 goals:

These are all the features that I'd like to implement for a first version.

```
urban-sim/

├── main.py

├── city/
│   ├── city.py
│   ├── plot.py
│   ├── household.py
│   ├── firm.py
│   └── government.py

├── simulation/
│   ├── engine.py
│   ├── accessibility.py
│   ├── valuation.py
│   └── relocation.py

├── visualization/
│   ├── plots.py
│   └── pygame_view.py

├── scenarios/
│   └── baseline.yaml

├── results/
│   └── (generated)

└── tests/
```

___