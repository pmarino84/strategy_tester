# Strategy tester

Built with [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
Documented with [pdoc](https://pdoc.dev/)

A tool to simplify backtesing and/or optimization of your trading strategy.

## ByBit

perpetual commission:
  
  1. maker: 0.0200%
  2. taker: 0.0550%

## Development

Follow the official [instructions](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

How to use virtual environment:

- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- deactivate

For commits use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) standar.

To create the documentations run the command:

```bash
cd src && pdoc strategy_tester -o ../docs --no-show-source
```
