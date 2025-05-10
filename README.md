# mini Python 编译器

## [English](#mini-python-compiler)

### 简介

这是一个小型 Python 编译器 / 解释器，支持生成 PYC 文件。

### 特性

  * 可直接执行脚本（python compiler.py script.py）
  * 支持编译为 PYC 文件（-c 标志）
  * 优化的代码结构
  * 内存高效操作
  * 增强的错误处理

### 安装指南

无需额外安装，直接运行代码即可。

### 使用方法

  * 执行脚本：python compiler.py script.py [args...]
  * 编译为 PYC：python compiler.py -c script.py

### FAQ

  * **如何编译一个 Python 脚本为 PYC 文件？**

答：使用命令 “python compiler.py -c script.py” 即可将 Python 脚本编译为 PYC 文件。

  * **编译器支持哪些优化？**

答：目前支持常量折叠优化，后续会添加更多优化功能。

  * **生成的 PYC 文件在哪里？**

答：默认在源文件所在目录下的 “__pycache__” 文件夹中，文件名为 “[源文件名].[Python 标签].pyc”。

  * **如何查看编译器版本信息？**

答：运行 “python compiler.py -v” 即可查看版本信息。

### 许可证

Apache-2.0 许可证。

### 致谢

感谢你的使用与支持，如有问题可通过 tomma_2022@outlook.com 联系作者 Dinnerb0ne。

# Mini Python Compiler

## Introduction

This is a mini Python compiler / interpreter with PYC generation support.

## Features

  * Execute scripts directly (python compiler.py script.py)
  * Compile to PYC files (-c flag)
  * Optimized code structure
  * Memory efficient operation
  * Enhanced error handling

## Installation

No extra installation is required; just run the code directly.

## Usage

  * Execute a script: python compiler.py script.py [args...]
  * Compile to PYC: python compiler.py -c script.py

## FAQ

  * **How to compile a Python script to a PYC file?**

**A:** Use the command “python compiler.py -c script.py” to compile a Python script to a PYC file.

  * **What optimizations does the compiler support?**

**A:** Currently, constant folding optimization is supported, and more optimizations will be added in the future.

  * **Where is the generated PYC file located?**

**A:** By default, it is in the “__pycache__” folder under the source file directory, with the file name “[source filename].[Python tag].pyc”.

  * **How to view the compiler version information?**

**A:** Run “python compiler.py -v” to view the version information.

## License

Apache-2.0 License.

## Acknowledgments

Thank you for your usage and support. If you have any questions, please contact the author Dinnerb0ne at tomma_2022@outlook.com.
