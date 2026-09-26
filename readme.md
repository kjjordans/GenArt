# Generative Pen-Plotter Art Toolbox


A modular Python project for learning and combining generative-art algorithms, image preprocessing, and plotter-oriented rendering. The primary workflow uses **vsketch** for interactive sketches and SVG generation, **vpype** for path processing, and a custom plotter that accepts **GRBL G-code**.


## Project goals


- Learn algorithms through small, finished plotter studies.

- Build reusable modules rather than isolated scripts.

- Keep geometry separate from composition and physical-machine settings.

- Support both purely generative and image-driven workflows.

- Make every result reproducible with explicit seeds and saved parameters.


## Proposed structure


generative-plotter/

├── README.md
├── pyproject.toml
├── src/plotter_art/
│   ├── geometry/
│   ├── transforms/
│   ├── fields/
│   ├── samplers/
│   ├── image/
│   ├── systems/
│   ├── renderers/
│   └── utils/
├── sketches/
├── assets/
├── outputs/
├── tests/
└── notes/