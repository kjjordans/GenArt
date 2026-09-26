**GENERATIVE PEN-PLOTTER ART**

Learning plan and modular project guide

Python • vsketch • vpype • GRBL G-code

| Purpose Build a reusable geometry-first toolbox while learning a broad range of generative, image-driven and plotter-specific algorithms through small finished studies. |
| --- |

Prepared for Joe Jordans  |  Version 0.1  |  25 September 2026

## 1. Project intent

This project is a practical learning programme and an evolving codebase. Each study should teach one main algorithm, produce a plot-ready SVG, and contribute at least one reusable module, test, example or documented pattern.

### Working principles

- Geometry first: algorithms return paths and shapes; sketches decide composition and style.
- Leverage vsketch and vpype rather than rebuilding reliable plotting operations.
- Keep every output reproducible using an explicit seed and saved parameter set.
- Start with compact studies, then combine methods into hybrid works.
- Design for physical plotting: bounded complexity, sensible line spacing and test plots before long runs.
- Treat image preprocessing as a source of fields, masks, contours and sampling density, not merely photo tracing.
### Definition of done for each study

- A clear visual question or target.
- A parameterised sketch with a fixed default seed.
- An SVG preview and a small physical test plot.
- Short notes on what worked, failed and should become reusable.
- At least one extraction into the toolbox when the code has reuse value.
## 2. Toolbox architecture

The architecture separates reusable geometry and algorithms from artwork-specific decisions. Begin lightly. Add abstractions only after two or more sketches need them.

generative-plotter/
├── README.md
├── pyproject.toml
├── src/plotter_art/
│   ├── geometry/       # curves, polylines, bounds, intersections
│   ├── transforms/     # rotate, scale, warp, repeat
│   ├── fields/         # scalar/vector fields, attractors, noise
│   ├── samplers/       # grids, jitter, Poisson-disc, weighted samples
│   ├── image/          # greyscale, masks, edges, contours, density maps
│   ├── systems/        # walkers, particles, growth, automata
│   ├── renderers/      # hatching, stippling, streamlines, contours
│   └── utils/          # seeds, parameters, logging, file naming
├── sketches/           # vsketch artworks and experiments
├── assets/             # source images with licence/source notes
├── outputs/            # generated SVG/PNG/G-code, normally ignored
├── tests/
└── notes/              # study logs and algorithm notes

### Module contracts

| Module | Input | Output | Responsibility |
| --- | --- | --- | --- |
| geometry | Numbers or geometry | Geometry | Represent and manipulate paths without styling. |
| fields | Position | Scalar or vector | Describe direction, density, distance or influence. |
| samplers | Region + field | Points | Choose where an algorithm starts or places marks. |
| image | Raster image | Mask, field, contours | Extract useful structure from source imagery. |
| systems | State + rules | Trajectories or geometry | Evolve behaviour over steps. |
| renderers | Geometry or field | Plotter paths | Translate information into marks. |
| sketches | Modules + parameters | Finished composition | Own the artistic decisions and vsketch interface. |

## 3. Learning roadmap

The roadmap is organised as capability stages rather than fixed calendar weeks. Move on when the outputs are understandable and reusable, not when a date is reached.

| Stage | Core topics | Toolbox additions | Suggested studies |
| --- | --- | --- | --- |
| 0. Foundation | Project structure, seed control, coordinate systems, vsketch workflow | utils, templates | Calibration sheet; seeded line study |
| 1. Curves & repetition | Parametric curves, polar coordinates, interpolation, transforms | geometry, transforms | Rosettes; Lissajous; harmonograph |
| 2. Space & subdivision | Grids, jitter, recursion, quadtree/BSP subdivision | samplers, subdivision | Molnár-style disturbed grid; recursive panels |
| 3. Fields & trajectories | Noise, scalar/vector fields, attractors, numerical integration | fields, streamlines | Flow-field ribbons; contour field |
| 4. Image foundations | Crop, resize, greyscale, contrast, blur, threshold, masks | image pipeline | Threshold portrait; multi-level contour poster |
| 5. Image to geometry | Edges, marching squares, contour tracing, skeletons | contours, vectorisation | Edge drawing; topographic portrait |
| 6. Tonal rendering | Hatching, cross-hatching, stippling, weighted sampling | renderers | Hatched photograph; stippled gradient |
| 7. Computational geometry | Hull, Voronoi, Delaunay, packing, clipping | geometry algorithms | Voronoi portrait; circle-packing study |
| 8. Emergent systems | Walkers, particles, boids, differential growth | systems | Swarm trails; branching network |
| 9. Rule-based growth | L-systems, space colonisation, cellular automata | growth systems | Botanical forms; urban growth map |
| 10. Hybrid compositions | Combine image fields, geometry and simulations | composition patterns | Photo-driven flow lines; contour + hatch + particles |

## 4. Image preprocessing track

Image preprocessing should be learned alongside generative geometry. The aim is to turn pixels into stable intermediate representations that other modules can consume.

| Step | Operation | Why it matters for plotting |
| --- | --- | --- |
| 1 | Crop, resize and orient | Defines composition and controls later computational cost. |
| 2 | Greyscale / channel selection | Creates a tonal field; individual colour channels may reveal different structure. |
| 3 | Levels, gamma and local contrast | Redistributes useful detail before reduction to lines. |
| 4 | Denoise / blur | Suppresses pixel-scale detail that becomes unwanted pen chatter. |
| 5 | Threshold / posterise | Creates masks or a small set of tonal bands. |
| 6 | Edges and gradients | Detects structural boundaries and local direction. |
| 7 | Morphology | Cleans masks, joins gaps and controls feature thickness. |
| 8 | Contours / skeletons | Converts regions into paths or centrelines. |
| 9 | Density map | Drives spacing, sampling probability, hatch density or stroke amplitude. |
| 10 | Vector cleanup | Simplifies, clips and filters paths before vsketch/vpype processing. |

### Recommended order of image studies

- Greyscale to parallel hatching.
- Threshold bands to nested contours.
- Canny/Sobel edges to simplified linework.
- Marching squares over tonal levels.
- Brightness-weighted stippling using rejection sampling, then Poisson-disc or centroidal Voronoi refinement.
- Gradient direction to locally oriented hatching.
- Image-conditioned flow fields and particles.
## 5. First twelve studies

| # | Study | Primary lesson | Reusable output |
| --- | --- | --- | --- |
| 01 | Plotter calibration and margins | Physical coordinate system and safe bounds | Page/plot presets |
| 02 | Parameterised rosette | Polar curves and repetition | Curve sampling helpers |
| 03 | Lissajous and harmonograph family | Parametric sampling and phase | Polyline sampler |
| 04 | Disturbed grid | Structured randomness | Grid + seeded jitter |
| 05 | Recursive subdivision | Recursion and spatial hierarchy | BSP/quadtree module |
| 06 | Noise contour map | Scalar fields and marching squares | Scalar field + contours |
| 07 | Streamline field | Vector fields and integration | Integrator + streamline renderer |
| 08 | Image threshold contours | Raster pipeline and masks | Image processing pipeline |
| 09 | Edge drawing | Gradients, edge detection and simplification | Edge-to-path workflow |
| 10 | Hatched image | Tone to line density | Hatch renderer |
| 11 | Stippled image | Weighted sampling | Density sampler |
| 12 | Voronoi portrait | Computational geometry + image density | Voronoi renderer |

## 6. Standard workflow for every sketch

1. Define one visual question and one main algorithm.

2. Create a minimal vsketch class with a small parameter set.

3. Generate explicit geometry in page units, separate from drawing commands where practical.

4. Preview several fixed seeds at low complexity.

5. Check bounds, minimum spacing, path count and likely plot duration.

6. Export SVG and run the normal vpype cleanup/optimisation pipeline.

7. Inspect travel paths and test a reduced A5 or corner crop.

8. Plot physically; record pen, paper, speed and issues.

9. Extract reusable code only after the study works.

10. Commit code, selected output and a short learning note.

### Suggested experiment record

seed | date | sketch version | paper | pen | page size | parameters | SVG path count | vpype pipeline | G-code settings | observations

## 7. Technical conventions

- Use millimetres as the project-level physical unit and convert only at clear boundaries.
- All randomness must be generated from a supplied seed. Avoid hidden module-level random state.
- Prefer functions that return paths or arrays over functions that draw immediately.
- Keep source images immutable; save preprocessing parameters rather than overwriting assets.
- Name outputs with sketch, seed and parameter-set identifier.
- Keep machine-specific GRBL settings and sender configuration outside reusable algorithms.
- Use vpype as the final geometry sanitation stage, while retaining an unoptimised SVG for debugging.
- Add smoke tests for deterministic output, finite coordinates and page-bound compliance.
### Dependencies to introduce only when needed

| Purpose | Likely package |
| --- | --- |
| Sketching and SVG generation | vsketch |
| Path processing and optimisation | vpype |
| Arrays and numerical work | NumPy |
| Raster image processing | Pillow; OpenCV or scikit-image when required |
| Geometry operations | Shapely |
| Voronoi, Delaunay, interpolation | SciPy |
| Testing | pytest |

## 8. Milestones and review gates

| Milestone | Evidence | Review question |
| --- | --- | --- |
| M1: Reliable skeleton | Studies 01–03 complete; repeatable export | Can a new sketch be created without copying ad hoc setup code? |
| M2: Composable geometry | Studies 04–07 complete | Can fields, samplers and renderers be recombined? |
| M3: Image pipeline | Studies 08–11 complete | Can one source image produce multiple distinct plotter interpretations? |
| M4: Geometry systems | Study 12 plus packing/growth experiment | Are computational geometry modules independent of composition? |
| M5: First hybrid series | Three related finished works | Does the toolbox support a coherent series rather than isolated demos? |

## 9. Immediate start

Begin with Study 01 and Study 02. Do not build the complete folder tree on day one. Create only the modules needed for calibration, page bounds, seeded randomness and sampled curves; let the architecture emerge through use.

### Study 01 acceptance criteria

- A page border and safe plotting rectangle.
- A spacing ladder, line-width/pen test and curves at several speeds.
- One known-good SVG and corresponding GRBL G-code.
- Documented machine origin, page placement and sender settings.
### Study 02 acceptance criteria

- A rosette generated from an explicit parametric function.
- Parameters for radial frequency, amplitude, phase, samples, layers and rotation.
- A fixed seed when jitter/noise is enabled.
- No geometry outside the safe plotting bounds.
- A small physical test and a short note describing aliasing, overdraw and useful parameter ranges.
## 10. Backlog of later topics

Keep this as a discovery list rather than a commitment: Fourier epicycles, differential line growth, reaction–diffusion, wave-function collapse, Truchet tiles, Penrose and aperiodic tilings, graph drawing, TSP stippling, maze generation, signed-distance fields, ray marching in 2D, moiré systems, weaving patterns, procedural maps, typography, data-driven drawing, hidden-line removal, multi-pen registration and plot interruption recovery.
