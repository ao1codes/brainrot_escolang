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
        # single main accumulator
        self.acc = 0
        # program counter
        self.pc = 0
        # loaded program: list of (line_no, tokens)
        self.lines = []
        # loop stack (pc indexes)
        self.loop_stack = []
        # generic stack
        self.stack = []
        # variables
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
            # only auto-advance if execute() didn't move pc
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
            self.acc = self.acc * self.acc
        elif cmd == 'cringe':
            if self.acc != 0:
                self.acc //= 2

        # Stack operations
        elif cmd == 'fam':            # push acc to stack
            self.stack.append(self.acc)
        elif cmd == 'clapback':      # pop from stack to acc
            if not self.stack:
                raise BrainrotError("Stack is empty")
            self.acc = self.stack.pop()

        # Variables
        elif cmd == 'set':           # set var to acc
            if len(args) != 1:
                raise BrainrotError("Usage: set <varname>")
            self.vars[args[0]] = self.acc
        elif cmd == 'get':           # load var into acc
            if len(args) != 1:
                raise BrainrotError("Usage: get <varname>")
            v = args[0]
            if v not in self.vars:
                raise BrainrotError(f"Unknown variable '{v}'")
            self.acc = self.vars[v]

        # I/O
        elif cmd == 'spill':         # prompt user for integer
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
            # skip next if acc == 0
            if self.acc == 0:
                self.pc += 2
        elif cmd == 'suspect':
            # skip next if acc > 0
            if self.acc > 0:
                self.pc += 2

        elif cmd == 'vibe':
            # start loop if acc > 0
            if self.acc > 0:
                self.loop_stack.append(self.pc)
            else:
                # skip to matching unvibe
                depth = 1
                while depth and self.pc < len(self.lines) - 1:
                    self.pc += 1
                    _, tokens = self.lines[self.pc]
                    if tokens[0] == 'vibe':
                        depth += 1
                    elif tokens[0] == 'unvibe':
                        depth -= 1
                if depth:
                    raise BrainrotError("Unmatched 'vibe'")
        elif cmd == 'unvibe':
            if not self.loop_stack:
                raise BrainrotError("Unmatched 'unvibe'")
            start = self.loop_stack[-1]
            if self.acc > 0:
                # jump to first command inside loop
                self.pc = start + 1
            else:
                self.loop_stack.pop()

        # File include
        elif cmd == 'load':
            if len(args) != 1:
                raise BrainrotError("Usage: load <filename>")
            filename = args[0]
            prev_lines = self.lines
            prev_pc = self.pc
            self.load(filename)
            # after include, resume original
            self.lines = prev_lines
            self.pc = prev_pc

        # Meta
        elif cmd == 'help':
            self.print_help()
        elif cmd == 'version':
            print(f"Brainrot version {VERSION}")

        # No-op / comments
        elif cmd == 'mid':
            pass

        # Unknown
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
        print("- flex       : square")
        print("- fam        : push acc")
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
    parser = argparse.ArgumentParser(
        description='Brainrot esolang interpreter (Gen Z slang edition)'
    )
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
                interp.lines = [(0, line.split())]
                interp.pc = 0
                interp.execute(interp.lines[0][1][0], interp.lines[0][1][1:])
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
