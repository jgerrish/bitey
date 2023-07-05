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

from bitey.logger import setup_logger
from bitey.computer.computer import Computer
from bitey.debug.debugger import DebuggerStateChange
from bitey.debug.cli_debugger import CLIDebugger
from bitey.debug.config_decoder import ConfigDecoder
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
@click.option(
    "--reset", "-r", is_flag=False, type=int, help="Reset address (PC initial value)"
)
@click.option("--config", "-c", is_flag=False, type=str, help="CPU config file")
@click.option("--debug", "-d", is_flag=True, type=bool, help="Enable debugger")
@click.option(
    "--eval-enabled",
    is_flag=True,
    type=bool,
    help="Enable eval in debugger.  WARNING: Security risk",
)
def cli(filename, pc, reset, config, debug, eval_enabled):  # noqa: C901
    "Load a program into memory and run it"

    setup_logger()
    data = None
    with open(filename, "rb") as f:
        data = f.read()

    debug_config = None
    if config is not None:
        with open(config, "r") as f:
            debug_config_decoder = ConfigDecoder()
            debug_config = debug_config_decoder.decode(f.read())

    if data is not None:
        computer = get_computer()
        computer.load(data)

        print("reset: {}".format(reset))
        if reset is not None:
            computer.memory.write(0xFFFC, (reset & 0xFF))
            computer.memory.write(0xFFFD, ((reset >> 8) & 0xFF))

        if pc is not None:
            print("Setting PC to 0x{}".format(pc))
            computer.cpu.registers["PC"].set(pc)

        computer.cpu.reset(computer.memory, False, False)

        print("Computer PC: {}".format(computer.cpu.registers["PC"].get()))
        print(
            "reset vector: {} {}".format(
                computer.memory.read(0xFFFC), computer.memory.read(0xFFFD)
            )
        )

        debugger = None
        # The previous behavior of the 6502 emulator was to load the
        # first instruction but not execute it.
        # This run script doesn't load the first instruction, so the program
        # starts with PC at the start of your routine and nothing loaded.
        #
        # In addition, no CPU "housekeeping" is done, so no instructions count toward
        # the loaded or executed limit.
        #
        # This behavior may change as additional features are added to
        # the emulator or additional systems are implemented.
        instructions_loaded_limit = (
            min(len(data), 100000) + computer.cpu.num_instructions_loaded
        )
        instructions_executed_limit = (
            min(len(data), 100000) + computer.cpu.num_instructions_executed
        )

        if (debug is not None) and debug:
            debugger = CLIDebugger(computer, DebuggerState.STEPPING, eval_enabled)
            if debug_config is not None:
                print("applying debugger configuration data:\n{}".format(debug_config))
                debug_config.apply(debugger)
            try:
                debugger.run(instructions_loaded_limit, instructions_executed_limit)
            except DebuggerStateChange as dsc:
                print(dsc)
                return
        else:
            computer.run(True, instructions_loaded_limit, instructions_executed_limit)
            print(computer.cpu.registers)
            print(
                "Number of instructions executed: {}".format(
                    computer.cpu.num_instructions_executed
                )
            )


if __name__ == "__main__":
    # cProfile.run("cli()")
    cli()
