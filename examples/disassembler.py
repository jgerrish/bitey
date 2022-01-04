# A small example to show how to disassemble a file
# Execute it with the following
# PYTHONPATH=. pipenv run python examples/disassembler.py FILENAME
import click

from bitey.computer.computer import Computer
from bitey.memory.memory import Memory


@click.command()
@click.argument("filename")
@click.option("--count", "-c", is_flag=False, type=int, help="Disassemble count bytes")
@click.option("--skip", "-s", is_flag=False, type=int, help="Skip n bytes in input")
def cli(filename, count, skip):
    "Disassemble a file"
    data = None
    with open(filename, "rb") as f:
        data = f.read()

    subset = data
    computed_skip = 0
    if skip is not None:
        computed_skip = skip
    if count is not None:
        subset = data[computed_skip:computed_skip + count]
    else:
        subset = data[computed_skip:]

    with open("chip/6502.json") as f:
        s = f.read()
        computer = Computer.build_from_json(s)
        computer.memory = Memory(subset)
        print(computer.disassemble())


if __name__ == "__main__":
    cli()
