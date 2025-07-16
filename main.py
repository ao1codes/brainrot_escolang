#!/usr/bin/env python3
import sys
import os

VERSION = "1.0.0"

class BrainrotError(Exception):
    pass

def parse_lines(lines):
    """
    Yield meaningful tokens from the source:
     - ignore blank lines
     - ignore comments (# at line start)
     - strip inline comments
     - split into tokens by whitespace
    """
    for idx, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        # remove inline comments
        if '#' in line:
            line = line.split('#', 1)[0].strip()
        if not line:
            continue
        tokens = line.split()
        yield idx, tokens

class Interpreter:
    def __init__(self, debug=False):
        self.acc = 0
        self.pc = 0
        self.lines = []
        self.loop_stack = []
        self.stack = []
        self.vars = {}
        self.debug = debug

    def load(self, filepath):
        if not os.path.isfile(filepath):
            raise BrainrotError(f"File not found: {filepath}")
        with open(filepath) as f:
            raw = f.readlines()
        self.lines = list(parse_lines(raw))

    def run(self):
        while self.pc < len(self.lines):
            line_no, tokens = self.lines[self.pc]
            cmd = tokens[0]
            if self.debug:
                print(f"[DEBUG] Line {line_no}: {tokens} | ACC={self.acc} STACK={self.stack} VARS={self.vars}")
            old_pc = self.pc
            try:
                self.execute(cmd, tokens[1:])
            except BrainrotError as e:
                print(f"Error at line {line_no}: {e}", file=sys.stderr)
                sys.exit(1)
            if self.pc == old_pc:
                self.pc += 1

    def execute(self, cmd, args):
        # Basic arithmetic
        if cmd == 'rizz':
            self.acc += 1
        elif cmd == 'gyatt':
            self.acc -= 1
        elif cmd == 'drip':
            self.acc += 5
        elif cmd == 'npc':
            self.acc -= 5
        elif cmd == 'lit':
            self.acc += 10
        elif cmd == 'slaps':
            self.acc -= 10
        elif cmd == 'yeet':
            self.acc *= 2
        elif cmd == 'flex':
            # push acc squared to stack (do NOT modify acc)
            self.stack.append(self.acc * self.acc)
        elif cmd == 'cringe':
            if self.acc != 0:
                self.acc //= 2

        # Stack operations
        elif cmd == 'fam':            # push acc to stack
            self.stack.append(self.acc)
        elif cmd == 'peekback':      # read top of stack without popping
            if not self.stack:
                raise BrainrotError("Stack is empty")
            self.acc = self.stack[-1]
        elif cmd == 'clapback':      # pop from stack to acc
            if not self.stack:
                raise BrainrotError("Stack is empty")
            self.acc = self.stack.pop()

        # Variables
        elif cmd == 'set':
            if len(args) != 1:
                raise BrainrotError("Usage: set <varname>")
            self.vars[args[0]] = self.acc
        elif cmd == 'get':
            if len(args) != 1:
                raise BrainrotError("Usage: get <varname>")
            v = args[0]
            if v not in self.vars:
                raise BrainrotError(f"Unknown variable '{v}'")
            self.acc = self.vars[v]

        # I/O
        elif cmd == 'spill':
            val = input("spill> ")
            try:
                self.acc = int(val)
            except ValueError:
                raise BrainrotError("Invalid integer input")
        elif cmd == 'skibidi':
            print(self.acc)

        # Control flow
        elif cmd == 'no' and args == ['cap']:
            self.acc = 0
        elif cmd == 'sus':
            if self.acc == 0:
                self.pc += 2
        elif cmd == 'suspect':
            if self.acc > 0:
                self.pc += 2

        elif cmd == 'vibe':
            if self.acc > 0:
                self.loop_stack.append(self.pc)
            else:
                depth = 1
                while depth and self.pc < len(self.lines) - 1:
                    self.pc += 1
                    _, toks = self.lines[self.pc]
                    if toks[0] == 'vibe':
                        depth += 1
                    elif toks[0] == 'unvibe':
                        depth -= 1
                if depth:
                    raise BrainrotError("Unmatched 'vibe'")
        elif cmd == 'unvibe':
            if not self.loop_stack:
                raise BrainrotError("Unmatched 'unvibe'")
            start = self.loop_stack[-1]
            if self.acc > 0:
                self.pc = start + 1
            else:
                self.loop_stack.pop()

        # File include
        elif cmd == 'load':
            if len(args) != 1:
                raise BrainrotError("Usage: load <filename>")
            filename = args[0]
            prev_lines, prev_pc = self.lines, self.pc
            self.load(filename)
            self.lines, self.pc = prev_lines, prev_pc

        # Meta
        elif cmd == 'help':
            self.print_help()
        elif cmd == 'version':
            print(f"Brainrot version {VERSION}")

        # No-op / comments
        elif cmd == 'mid':
            pass

        else:
            raise BrainrotError(f"Unknown command '{cmd}'")

    def print_help(self):
        print("Brainrot commands:")
        print("- rizz       : +1")
        print("- gyatt      : -1")
        print("- drip       : +5")
        print("- npc        : -5")
        print("- lit        : +10")
        print("- slaps      : -10")
        print("- yeet       : *2")
        print("- cringe     : //2")
        print("- flex       : push acc² to stack")
        print("- fam        : push acc")
        print("- peekback   : read top of stack")
        print("- clapback   : pop to acc")
        print("- set <v>    : var=v")
        print("- get <v>    : load var")
        print("- spill      : input number")
        print("- skibidi    : print acc")
        print("- no cap     : acc=0")
        print("- sus        : skip if acc==0")
        print("- suspect    : skip if acc>0")
        print("- vibe ...   : loop while acc>0")
        print("- unvibe     : end loop")
        print("- load <f>   : include file")
        print("- help       : this list")
        print("- version    : show version")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Brainrot esolang interpreter')
    parser.add_argument('file', nargs='?', help='Path to .brainrot source')
    parser.add_argument('--debug', action='store_true', help='Trace execution')
    args = parser.parse_args()

    interp = Interpreter(debug=args.debug)

    # REPL if no file given
    if not args.file:
        print(f"Brainrot v{VERSION} REPL. Type 'help'. Ctrl-C to exit.")
        try:
            while True:
                line = input(">>> ")
                if not line.strip():
                    continue
                toks = line.split()
                interp.lines = [(0, toks)]
                interp.pc = 0
                interp.execute(toks[0], toks[1:])
        except KeyboardInterrupt:
            print("\nGoodbye.")
        sys.exit(0)

    # run file
    try:
        interp.load(args.file)
        interp.run()
    except BrainrotError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
