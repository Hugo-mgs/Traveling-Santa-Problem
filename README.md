# Travelling Santa Problem

## Installation
```bash
python -m venv my-env
source my-env/bin/activate  # macOS/Linux
my-env\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Running
```bash
python3 main.py
```

## Usage
1. Enter the input file name when prompted (without path or extension). Press Enter to use the default `santa_100` instance. Input files must be placed in the `input/` folder as `.csv` files with columns `id`, `x`, `y`.
2. Choose an algorithm by entering its number:
   - **1** Greedy (Nearest Neighbour) — no parameters required
   - **2** 2-opt — no parameters required
   - **3** K-opt (ILS) — parameters required:
     - `Number of iterations`: how many times the algorithm restarts from a perturbed solution (e.g. 50)
     - `K`: number of edges removed during each perturbation step (e.g. 3)
   - **4** Simulated Annealing — parameters required:
     - `Number of iterations`: how many neighbour moves are attempted in total (e.g. 1000)
     - `K`: number of edges involved in each random move (e.g. 2)
   - **5** Genetic Algorithm — parameters required:
     - `Population size`: number of solutions maintained each generation (e.g. 20)
     - `Max no-improve generations`: how many consecutive generations without improvement before stopping (e.g. 100)
   - **6** Hill Climbing — parameters required:
     - `Number of restarts`: how many times the algorithm restarts from a new starting point (e.g. 50)
3. The program will output the distance of each path, the final score, and the time elapsed.
4. The solution is saved to `solution.csv` in the current directory.
