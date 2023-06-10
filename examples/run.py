"""
A small example to show how to run a binary file, executing the
data as a 6502 program.

Execute it with the following

PYTHONPATH=. pipenv run python examples/run.py data/nop.bin

Here are some other examples of how to run it with the debugger:

PYTHONPATH=. pipenv run python examples/run.py -c data/nop-sample-breakpoints.json --debug data/nop.bin

When the prompt comes up, type c to continue the program and watch it
stop on the first breakpoint.
"""

import click
import json

from bitey.logger import setup_logger
from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU
from bitey.debug.debugger import DebuggerStateChange
from bitey.debug.cli_debugger import CLIDebugger
from bitey.debug.debugger import DebuggerState


def get_computer():
    with open("chip/6502.json") as f:
        s = f.read()
        computer = Computer.build_from_json(s)
        # computer.memory = Memory(subset)

        return computer
    return None


@click.command()
@click.argument("filename")
@click.option("--pc", "-p", is_flag=False, type=int, help="PC initial value")
@click.option("--sp", "-s", is_flag=False, type=int, help="Stack Pointer address")
@click.option(
    "--reset", "-r", is_flag=False, type=int, help="Reset address (PC initial value)"
)
@click.option("--config", "-c", is_flag=False, type=str, help="CPU config file")
@click.option("--debug", "-d", is_flag=True, type=bool, help="Enable debugger")
def cli(filename, pc, sp, reset, config, debug):  # noqa: C901
    "Load a program into memory and run it"

    setup_logger()
    data = None
    with open(filename, "rb") as f:
        data = f.read()

    config_data = None
    if config is not None:
        with open(config, "r") as f:
            json_data = f.read()
            config_data = json.loads(json_data)

    if data is not None:
        computer = get_computer()

        print("PC: {}".format(pc))
        if pc is not None:
            computer.memory.write(0xFFFC, (pc & 0xFF))
            computer.memory.write(0xFFFD, ((pc >> 8) & 0xFF))
        # print("reset: {}".format(reset))
        # if reset is not None:
        #     computer.memory.write(0xFFFC, (reset & 0xFF))
        #     computer.memory.write(0xFFFD, ((reset >> 8) & 0xFF))

        if reset is not None:
            print("Loading at specific offset")
            computer.load(data, offset=reset)
        else:
            computer.load(data)

        if sp is not None:
            print("Setting stack start")
            CPU.stack_start = sp

        computer.cpu.reset(computer.memory)
        if pc is not None:
            print("Setting PC to 0x{}".format(pc))
            computer.cpu.registers["PC"].set(pc)

        print("Computer PC: {}".format(computer.cpu.registers["PC"].get()))
        print("Computer SP: {}".format(computer.cpu.registers["S"].get()))
        print(
            "reset vector: {} {}".format(
                computer.memory.read(0xFFFC), computer.memory.read(0xFFFD)
            )
        )

        debugger = None
        # The cpu reset routine loads but DOESN'T run the first instruction in memory,
        # so this should be computer.cpu.num_instructions_loaded - 1
        instructions_loaded_limit = (
            min(len(data), 2000) + computer.cpu.num_instructions_loaded - 1
        )
        # The cpu reset routine loads but DOESN'T run the first instruction in memory,
        # so this should be computer.cpu.num_instructions_loaded
        instructions_executed_limit = (
            min(len(data), 2000) + computer.cpu.num_instructions_executed
        )

        if config_data is not None:
            print("Found config_data")
            if "breakpoints" in config_data:
                for breakpoint in config_data["breakpoints"]:
                    print("Breakpoint: {}".format(breakpoint))
                    if "address" in breakpoint:
                        computer.cpu.set_breakpoint(breakpoint["address"])
            if "watchpoints" in config_data:
                for watchpoint in config_data["watchpoints"]:
                    print("Watchpoint: {}".format(watchpoint))
                    if "address" in watchpoint:
                        computer.cpu.set_watchpoint(
                            watchpoint["address"], computer.memory
                        )

        if (debug is not None) and debug:
            debugger = CLIDebugger(computer, DebuggerState.STEPPING)
            try:
                debugger.run(instructions_loaded_limit, instructions_executed_limit)
            except DebuggerStateChange as dsc:
                print(dsc)
                return
        else:
            computer.run(True, instructions_loaded_limit, instructions_executed_limit)
            print(computer.cpu.registers)


if __name__ == "__main__":
    # cProfile.run("cli()")
    cli()
