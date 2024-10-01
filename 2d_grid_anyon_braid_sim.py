import numpy as np
import random
from typing import List, Tuple, Dict

class AnyonSystem:
    def __init__(self, size: int, anyons: List[str], fusion_rules: Dict[Tuple[str, str], List[str]], R_matrix: Dict[Tuple[str, str], np.ndarray]):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.anyons = anyons
        self.fusion_rules = fusion_rules
        self.R_matrix = R_matrix
        self.anyon_positions = {}

    def create_anyon(self, anyon_type: str, x: int, y: int):
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.grid[y][x] is None:
                self.grid[y][x] = anyon_type
                self.anyon_positions[(x, y)] = anyon_type
                print(f"Created {anyon_type} at ({x}, {y})")
            else:
                print(f"Position ({x}, {y}) is already occupied")
        else:
            print("Invalid position")

    def move_anyon(self, x1: int, y1: int, x2: int, y2: int):
        if 0 <= x1 < self.size and 0 <= y1 < self.size and 0 <= x2 < self.size and 0 <= y2 < self.size:
            if self.grid[y1][x1] is not None:
                anyon = self.grid[y1][x1]
                self.grid[y1][x1] = None
                del self.anyon_positions[(x1, y1)]
                if self.grid[y2][x2] is None:
                    self.grid[y2][x2] = anyon
                    self.anyon_positions[(x2, y2)] = anyon
                    print(f"Moved {anyon} from ({x1}, {y1}) to ({x2}, {y2})")
                else:
                    result = self.fuse(anyon, self.grid[y2][x2])
                    if len(result) == 1:
                        self.grid[y2][x2] = result[0]
                        self.anyon_positions[(x2, y2)] = result[0]
                        print(f"Fused {anyon} and {self.grid[y2][x2]} at ({x2}, {y2}), result: {result[0]}")
                    else:
                        self.grid[y2][x2] = random.choice(result)
                        self.anyon_positions[(x2, y2)] = self.grid[y2][x2]
                        print(f"Fused {anyon} and {self.grid[y2][x2]} at ({x2}, {y2}), result: {self.grid[y2][x2]} (randomly chosen from {result})")
            else:
                print(f"No anyon at position ({x1}, {y1})")
        else:
            print("Invalid position")

    def fuse(self, a: str, b: str) -> List[str]:
        if (a, b) in self.fusion_rules:
            return self.fusion_rules[(a, b)]
        elif (b, a) in self.fusion_rules:
            return self.fusion_rules[(b, a)]
        else:
            raise ValueError(f"No fusion rule defined for {a} and {b}")

    def braid(self, pos1: Tuple[int, int], pos2: Tuple[int, int]):
        if pos1 in self.anyon_positions and pos2 in self.anyon_positions:
            a, b = self.anyon_positions[pos1], self.anyon_positions[pos2]
            if (a, b) in self.R_matrix:
                R = self.R_matrix[(a, b)]
                phase = np.angle(R[0, 0])
                print(f"Braided {a} at {pos1} with {b} at {pos2}")
                print(f"Braiding phase: {phase:.4f}")
                return phase
            else:
                print(f"No R-matrix defined for {a} and {b}")
        else:
            print("Invalid anyon positions for braiding")

    def print_grid(self):
        for row in self.grid:
            print(" ".join([a if a else "." for a in row]))
        print()

# Ising anyons
ising_anyons = ["1", "s", "p"]
ising_fusion_rules = {
    ("1", "1"): ["1"],
    ("1", "s"): ["s"],
    ("1", "p"): ["p"],
    ("s", "s"): ["1", "p"],
    ("s", "p"): ["s"],
    ("p", "p"): ["1"]
}

# R-matrices for Ising anyons
ising_R_matrix = {
    ("s", "s"): np.array([[np.exp(1j * np.pi / 8), 0], [0, np.exp(-1j * np.pi / 8)]]),
    ("s", "p"): np.array([[0, -1j], [1j, 0]]),
    ("p", "p"): np.array([[-1]])
}

# 创建一个5x5的系统
system = AnyonSystem(5, ising_anyons, ising_fusion_rules, ising_R_matrix)

# 模拟过程
system.create_anyon("s", 1, 1)
system.create_anyon("s", 3, 3)
system.print_grid()

system.move_anyon(1, 1, 2, 1)
system.print_grid()

# 编织操作
system.braid((2, 1), (3, 3))

system.move_anyon(2, 1, 3, 3)
system.print_grid()

system.create_anyon("p", 0, 0)
system.print_grid()

# 另一个编织操作
system.braid((0, 0), (3, 3))

system.move_anyon(0, 0, 1, 1)
system.print_grid()