# The Agentic City

A city with a multi-agent simulation that aims to test, via emergent behaviour, optimality for taxation, transport systems, sustainable use of land, development, and more.

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