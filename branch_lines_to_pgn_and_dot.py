import chess.pgn
import chess
import uuid
import re
import subprocess

def parse_line_to_moves(line):
    # Removes tokens like 1.d4 or 4...e5, leaving just SAN moves
    tokens = line.strip().split()
    san_moves = []

    for token in tokens:
        # Strip leading move numbers (e.g. 1., 4..., 10...Nc6 → Nc6)
        cleaned = re.sub(r'^\d+\.{1,3}', '', token)
        if cleaned:
            san_moves.append(cleaned)

    return san_moves

def build_game_from_lines(lines):
    root = chess.pgn.Game()
    root.headers["Event"] = "Branching Repertoire"

    for line in lines:
        moves = parse_line_to_moves(line)
        node = root
        board = node.board()

        for move_san in moves:
            try:
                move = board.parse_san(move_san)
            except ValueError:
                print(f"Invalid move: {move_san}")
                break

            # Check if the move already exists as a variation
            found = False
            for var in node.variations:
                if var.move == move:
                    node = var
                    board.push(move)
                    found = True
                    break

            if not found:
                node = node.add_variation(move)
                board.push(move)

    return root

def write_pgn(game, filename):
    with open(filename, "w", encoding="utf-8") as f:
        print(game, file=f)

def escape_label(text):
    return text.replace("\\", "\\\\").replace('"', r'\"')

def node_id():
    return f"n{uuid.uuid4().hex[:8]}"

def add_nodes(node, graph_lines, parent_id=None, ply=-1):
    if node.move:
        current_id = node_id()
        try:
            board_before = node.parent.board()
            move_san = board_before.san(node.move)
        except Exception:
            move_san = str(node.move)

        fillcolor = "lightgray" if ply % 2 == 1 else "white"
        label = escape_label(move_san)
        graph_lines.append(
            f'"{current_id}" [label="{label}", style=filled, fillcolor={fillcolor}];'
        )

        if parent_id:
            graph_lines.append(f'"{parent_id}" -> "{current_id}";')

        my_parent_id = current_id
    else:
        my_parent_id = parent_id

    for var in node.variations:
        add_nodes(var, graph_lines, my_parent_id, ply + 1)

def export_pgn_to_dot(pgn_path, dot_path):
    with open(pgn_path, "r", encoding="utf-8") as f:
        game = chess.pgn.read_game(f)

    graph_lines = ['digraph Opening {', 'node [shape=box fontname="Arial"];']
    add_nodes(game, graph_lines, ply=-1)
    graph_lines.append("}")

    with open(dot_path, "w", encoding="utf-8") as f:
        f.write("\n".join(graph_lines))

    print(f"DOT file written to: {dot_path}")

def main():
    base_name = "hammer_e6"  # without .txt
    # base_name = "toth_e4"  # without .txt
    input_file = f"{base_name}.txt"
    output_pgn = f"{base_name.replace('-lines', '')}-merged.pgn"
    output_dot = f"{base_name.replace('-lines', '').replace('-', '')}-merged.dot"
    output_png = output_dot.replace(".dot", ".png")

    with open(input_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    game = build_game_from_lines(lines)
    write_pgn(game, output_pgn)
    export_pgn_to_dot(output_pgn, output_dot)

    # Generate PNG using Graphviz's dot command
    subprocess.run(["dot", "-Tpng", output_dot, "-o", output_png], check=True)
    print(f"PNG image written to: {output_png}")

if __name__ == "__main__":
    main()

