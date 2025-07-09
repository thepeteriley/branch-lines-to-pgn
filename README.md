# Branch Lines to PGN and DOT

This script converts a plain-text list of chess opening lines into a PGN file with proper branching variations, and creates a DOT file (plus optional PNG) to visualize the move tree using Graphviz.

## Features

- Accepts input lines like: `1.d4 d5 2.Nf3 Nf6 3.e3 e6 4.Bd3 c5`
- Builds a PGN with a branching tree of variations
- Outputs a DOT file for visualization (can also generate a PNG image)

## Input Format

Create a `.txt` file where each line is a variation. Example:

1.d4 d5 2.Nf3 Nf6 3.e3 e6 4.Bd3 c5  
1.d4 d5 2.Nf3 Nf6 3.e3 e6 4.Bd3 Nc6  
1.d4 d5 2.Nf3 Nf6 3.e3 e6 4.Bd3 Be7

## Output

If the input file is `hammer_e6.txt`, the script produces:

- `hammer_e6-merged.pgn`: PGN file with variations  
- `hammere6-merged.dot`: DOT file for Graphviz  
- `hammere6-merged.png`: Image of the move tree (if Graphviz is installed)

![image](https://github.com/user-attachments/assets/c2b33305-82dd-4173-a0a9-2b3731d14dee)


## Installation

Python 3.8+ is required. Install dependencies with:

    pip install -r requirements.txt

You must also have Graphviz installed and the `dot` command available in your system PATH.

## Usage

1. Edit the `base_name` variable in the `main()` function to match your `.txt` file name (without the `.txt` extension).
2. Run the script:

    python branch_lines_to_pgn_and_dot.py

3. The PGN, DOT, and PNG files will be created in the same folder.

## File Overview

- `branch_lines_to_pgn_and_dot.py`: Main script  
- `requirements.txt`: Python dependencies  
- `README.md`: This file  
- `*.txt`: Input file with one line per variation  

## License

This project is licensed under the MIT License.

