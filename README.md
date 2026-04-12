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
1. Enter the input file name when prompted (without path or extension). Press Enter to use the default `random_50` instance. Input files must be placed in the `input/` folder as `.csv` files with columns `id`, `x`, `y`.
2. Choose an algorithm by entering its number:
   - **1** Greedy (Nearest Neighbour)
   - **2** 2-opt
   - **3** K-opt (ILS)
   - **4** Simulated Annealing
   - **5** Genetic Algorithm
   - **6** Hill Climbing
3. The program will output the distance of each path and the final score.
