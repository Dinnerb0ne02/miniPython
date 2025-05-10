# developed with python-3.13.3-embed-amd64
# -*- coding: utf-8 -*-
# mini Python Compiler v0.1.1
# License: Apache-2.0
# Copyright (c) 2025 Dinnerb0ne<tomma_2022@outlook.com>

"""
Enhanced Python Compiler/Interpreter with PYC support
Features:
+ Execute .py scripts directly
+ Compile to .pyc files (-c flag)
+ Run .pyc files directly (-r flag)
+ Optimized code structure
+ Memory efficient operation
"""

import ast
import sys
import os
import marshal
import types
import importlib.util
from typing import Dict, Optional, Tuple

class PythonCompiler:
    # Core compiler implementation with PYC support
    
    # Magic number for Python 3.13 (example)
    PYTHON_MAGIC = importlib.util.MAGIC_NUMBER
    
    def __init__(self):
        self.optimizations = {
            'constant_folding': True,
            'peephole': True
        }
        self._code_cache: Dict[Tuple[str, int], types.CodeType] = {}

    def compile_source(self, source: str, filename: str = "<string>") -> types.CodeType:
        # Compile Python source to bytecode
        cache_key = (filename, hash(source))
        if cache_key in self._code_cache:
            return self._code_cache[cache_key]
        
        try:
            tree = ast.parse(source, filename, 'exec')
            
            if self.optimizations['constant_folding']:
                tree = self._optimize_ast(tree)
            
            code = compile(tree, filename, 'exec')
            
            if self.optimizations['peephole']:
                code = self._peephole_optimize(code)
            
            self._code_cache[cache_key] = code
            return code
            
        except Exception as e:
            raise CompilerError(f"Compilation failed: {str(e)}")

    def _optimize_ast(self, node: ast.AST) -> ast.AST:
        # Apply AST-level optimizations
        class Optimizer(ast.NodeTransformer):
            def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
                if (isinstance(node.left, ast.Constant)) and isinstance(node.right, ast.Constant):
                    try:
                        if isinstance(node.op, ast.Add):
                            return ast.Constant(node.left.value + node.right.value)
                        elif isinstance(node.op, ast.Sub):
                            return ast.Constant(node.left.value - node.right.value)
                        elif isinstance(node.op, ast.Mult):
                            return ast.Constant(node.left.value * node.right.value)
                        elif isinstance(node.op, ast.Div):
                            return ast.Constant(node.left.value / node.right.value)
                    except:
                        pass
                return node
        return Optimizer().visit(node)

    def _peephole_optimize(self, code: types.CodeType) -> types.CodeType:
        # Basic bytecode optimization
        return code

    def load_pyc(self, pyc_path: str) -> types.CodeType:
        # Load compiled code from .pyc file
        try:
            with open(pyc_path, 'rb') as f:
                # Read and validate header
                magic = f.read(4)
                if magic != self.PYTHON_MAGIC:
                    raise CompilerError("Invalid magic number in .pyc file")
                
                # Skip timestamp and size (8 bytes)
                f.read(8)
                
                # Load marshaled code
                return marshal.load(f)
        except Exception as e:
            raise CompilerError(f"Failed to load .pyc file: {str(e)}")

    def generate_pyc(self, code: types.CodeType, source_path: str) -> str:

        #Generate standard .pyc file
        
        cache_dir = os.path.join(os.path.dirname(source_path), "__pycache__")
        os.makedirs(cache_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(source_path))[0]
        pyc_name = f"{base_name}.{self._get_python_tag()}.pyc"
        pyc_path = os.path.join(cache_dir, pyc_name)
        
        with open(pyc_path, 'wb') as f:
            # Write header
            f.write(self.PYTHON_MAGIC)
            f.write(int(os.path.getmtime(source_path)).to_bytes(4, 'little'))
            f.write(os.path.getsize(source_path).to_bytes(4, 'little'))
            f.write(b'\x00' * 4)  # Padding
            
            # Write marshaled code
            marshal.dump(code, f)
        
        return pyc_path

    def _get_python_tag(self) -> str:
        # Get Python implementation/version tag
        return f"mini-{sys.version_info[0]}{sys.version_info[1]:02d}"

    def execute(self, code: types.CodeType, globals: Optional[Dict] = None) -> None:
        # Execute compiled code
        if globals is None:
            globals = {
                '__name__': '__main__',
                '__file__': '<string>',
                '__builtins__': __builtins__,
                'PythonCompiler': PythonCompiler,  # For self-compilation
                'CompilerError': CompilerError
            }
        exec(code, globals)

class CompilerError(Exception):
    # Custom compilation error (todo)
    pass

def main():

    mode = 'execute'
    target = sys.argv[1]
    
    match target:
        case '-c':
            if len(sys.argv) < 3:
                print("[Error] Missing input file")
                sys.exit(1)
            mode = 'compile'
            target = sys.argv[2]
        case '-r':
            if len(sys.argv) < 3:
                print("[Error] Missing .pyc file")
                sys.exit(1)
            mode = 'run_pyc'
            target = sys.argv[2]
        case '-h':
            print("[info] Usage:")
            print("     |Execute script: python c.py script.py [args...]")
            print("     |Compile to PYC: python c.py -c script.py")
            print("     |Run PYC file:   python c.py -r script.pyc")
            sys.exit(1)

        case '-v':
            print("mini Python Compiler v0.1.1")
            print("Copyright (c) 2025 Dinnerb0ne<tomma_2022@outlook.com>")
            sys.exit(0)

    
    if not os.path.exists(target):
        print(f"[Error] File '{target}' not found")
        sys.exit(1)
    
    compiler = PythonCompiler()
    
    try:
        if mode == 'compile':
            # Compile to .pyc
            with open(target, 'r', encoding='utf-8') as f:
                code = compiler.compile_source(f.read(), target)
            pyc_path = compiler.generate_pyc(code, target)
            print(f"[info] Successfully compiled to {pyc_path}")
        
        elif mode == 'run_pyc':
            # Run .pyc directly
            code = compiler.load_pyc(target)
            sys.argv = sys.argv[2:]  # Remove -r and pyc path
            compiler.execute(code)
        
        else:
            # Normal execution
            with open(target, 'r', encoding='utf-8') as f:
                code = compiler.compile_source(f.read(), target)
            sys.argv = sys.argv[1:]  # Remove script path
            compiler.execute(code)
            
    except CompilerError as e:
        print(f"[Error] Compiler: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[Error] Runtime: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except MemoryError:
        print("[Error] Out of memory", file=sys.stderr)
        sys.exit(1)
