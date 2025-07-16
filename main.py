#!/usr/bin/env python3
import sys

def parse_lines(lines):
    for idx, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if '#' in line:
            line = line.split('#', 1)[0].strip()
        if not line:
            continue
        yield idx, line

class BrainrotError(Exception):
    pass

class Interpreter:
    def __init__(self, debug=False):
        self.acc = 0
        self.pc = 0
        self.lines = []
        self.loop_stack = []
        self.debug = debug

    def load(self, filepath):
        try:
            with open(filepath) as f:
                raw = f.readlines()
        except OSError as e:
            raise BrainrotError(f"Could not open file: {e}")
        self.lines = list(parse_lines(raw))

    def run(self):
        while self.pc < len(self.lines):
            idx, cmd = self.lines[self.pc]
            if self.debug:
                print(f"[DEBUG] Line {idx}: '{cmd}' | ACC={self.acc}")
            old_pc = self.pc
            self.execute(cmd)
            if self.pc == old_pc:
                self.pc += 1

    def execute(self, cmd):
        if cmd == 'rizz':
            self.acc += 1
        elif cmd == 'gyatt':
            self.acc -= 1
        elif cmd == 'drip':
            self.acc += 5
        elif cmd == 'npc':
            self.acc -= 5
        elif cmd == 'yeet':
            self.acc *= 2
        elif cmd == 'cringe':
            if self.acc != 0:
                self.acc //= 2
        elif cmd == 'skibidi':
            print(self.acc)
        elif cmd == 'no cap':
            self.acc = 0
        elif cmd == 'sus':
            if self.acc == 0:
                # skip next command entirely
                self.pc += 2
        elif cmd == 'vibe':
            if self.acc > 0:
                self.loop_stack.append(self.pc)
            else:
                depth = 1
                while depth and self.pc < len(self.lines) - 1:
                    self.pc += 1
                    _, c = self.lines[self.pc]
                    if c == 'vibe':
                        depth += 1
                    elif c == 'unvibe':
                        depth -= 1
                if depth:
                    raise BrainrotError(f"Unmatched 'vibe' at line {self.pc}")
        elif cmd == 'unvibe':
            if not self.loop_stack:
                raise BrainrotError(f"Unmatched 'unvibe' at line {self.pc}")
            start = self.loop_stack[-1]
            if self.acc > 0:
                # jump to first command inside the loop body
                self.pc = start + 1
            else:
                self.loop_stack.pop()
        elif cmd == 'mid':
            pass
        else:
            raise BrainrotError(f"Unknown command '{cmd}'")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Brainrot esolang interpreter')
    parser.add_argument('file', help='Path to .brainrot source')
    parser.add_argument('--debug', action='store_true', help='Trace execution')
    args = parser.parse_args()

    interp = Interpreter(debug=args.debug)
    try:
        interp.load(args.file)
        interp.run()
    except BrainrotError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
