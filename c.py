# developed with python-3.13.3-embed-amd64
# -*- coding: utf-8 -*-
# mini Python Compiler v0.1.0
# License: Apache-2.0
# Copyright (c) 2025 Dinnerb0ne<tomma_2022@outlook.com>

"""
mini Python Compiler/Interpreter with PYC generation
Features:
+ Execute scripts directly (python compiler.py script.py)
+ Compile to PYC files (-c flag)
+ Optimized code structure
+ Memory efficient operation
+ Enhanced error handling
"""

import ast
import sys
import os
import marshal
import types
from typing import Dict, Optional, Tuple

class PythonCompiler:
    """Core compiler implementation with PYC generation support"""

    PYTHON_MAGIC = b'\x03\xf3\r\n'  # Magic number for Python 3.13.3
    def __init__(self):
        self.optimizations = {
            'constant_folding': True,
            'peephole': True
        }
        self._code_cache: Dict[Tuple[str, int], types.CodeType] = {}

    def compile_source(self, source: str, filename: str = "<string>") -> types.CodeType:
        """Compile Python source to bytecode with optimizations"""
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
        """Apply AST-level optimizations"""
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
        """Basic bytecode optimizations"""
        return code  # Actual implementation would modify code.co_code
    
    def _get_python_tag(self) -> str:
        """Get Python implementation and version tag (e.g., cpython-313)"""
        impl = sys.implementation.name  # e.g., 'cpython'
        ver = "mini python 0.1.0"  # e.g., (3, 13, ...)
        return f"{impl}-{ver}"

    def generate_pyc(self, code: types.CodeType, source_path: str, output_dir: str = None) -> str:
        """
        Generate standard .pyc file with original filename
        Args:
            code: Compiled code object
            source_path: Path to source file
            output_dir: Optional output directory (defaults to __pycache__)
        Returns:
            Path to generated .pyc file
        """
        # Get source file info
        source_name = os.path.basename(source_path)
        base_name = os.path.splitext(source_name)[0]  # Remove .py extension
        source_mtime = int(os.path.getmtime(source_path))
        source_size = os.path.getsize(source_path) & 0xFFFFFFFF
        
        # Determine output directory
        if output_dir is None:
            base_dir = os.path.dirname(source_path)
            output_dir = os.path.join(base_dir, "__pycache__")
            os.makedirs(output_dir, exist_ok=True)
        
        # Generate standard PYC filename (e.g., script.cpython-313.pyc)
        pyc_name = f"{base_name}.{self._get_python_tag()}.pyc"
        output_path = os.path.join(output_dir, pyc_name)
        
        # Write PYC file
        with open(output_path, 'wb') as f:
            # Header (16 bytes)
            f.write(self.PYTHON_MAGIC)  # Magic number
            f.write(source_mtime.to_bytes(4, 'little'))  # Timestamp
            f.write(source_size.to_bytes(4, 'little'))  # Source size
            f.write(b'\x00' * 4)  # Padding
            
            # Marshaled code object
            marshal.dump(code, f)
        
        return output_path

    def execute(self, code: types.CodeType, globals: Optional[Dict] = None) -> None:
        """Execute compiled code with proper context"""
        if globals is None:
            globals = {
                '__name__': '__main__',
                '__file__': '<string>',
                '__builtins__': __builtins__
            }
        exec(code, globals)

class CompilerError(Exception):
    """Custom compilation error exception"""
    pass

def main():
    if len(sys.argv) < 2:
        print("[info] Usage:")
        print("[info] |  Execute script: python compiler.py script.py [args...]")
        print("[info] |  Compile to PYC: python compiler.py -c script.py")
        sys.exit(1)
    
    compile_only = False
    script_path = sys.argv[1]
    
    if script_path == '-c':
        if len(sys.argv) < 3:
            print("Error: No input file specified for compilation")
            sys.exit(1)
        compile_only = True
        script_path = sys.argv[2]

    if script_path == '-v':
        print("mini Python Compiler v0.1.0")
        print("Copyright (c) 2025 Dinnerb0ne<tomma_2022@outlook.com>")
        sys.exit(0)
    
    if not os.path.exists(script_path):
        print(f"[error] Error: File '{script_path}' not found")
        sys.exit(1)
    
    # Read source code
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except IOError as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Set up arguments
    if compile_only:
        sys.argv = [sys.argv[0]] + sys.argv[3:]
    else:
        sys.argv = sys.argv[1:]
    
    # Compile
    compiler = PythonCompiler()
    try:
        code = compiler.compile_source(source, script_path)
        
        if compile_only:
            pyc_path = compiler.generate_pyc(code, script_path)
            print(f"Successfully compiled to {pyc_path}")
        else:
            compiler.execute(code)
            
    except CompilerError as e:
        print(f"[error] Compilation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[error] Runtime error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except MemoryError:
        print("[error] Memory error: Operation requires too much memory", file=sys.stderr)
        sys.exit(1)