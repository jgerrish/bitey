# bitey #

![python tests](https://github.com/jgerrish/bitey/actions/workflows/python-package.yml/badge.svg)

Bitey is a 6502 CPU emulator.  It is currently not feature-complete,
cycle-accurate or any of those things.  It's meant to be a simple
clean emulator for a classic chipset.  It may possibly be expanded to
include emulation of 8-bit systems in the future.

It uses a simple JSON format for describing the CPU architecture.


Why not VHDL or Verilog or insert-hardware-description-language?

I'm not an electrical engineer.  I don't have access to the common
simulation environments or experience working with the intricacies of
those languages.  JSON provides a middle-ground between most existing
classic 8-bit emulators and full-blown hardware definition in a
language.

The target audience of this application is those who want a simple
understanding of emulation and a clean-ish base to work from.

There are some existing projects that are more focused on those design
patterns.

Apple2fpga by Stephen A. Edwards at Columbia Univeristy
http://www.cs.columbia.edu/~sedwards/apple2fpga/

AppleLogic includes links to other projects.
http://www.applelogic.org/

AppleIIe for MiSTer
https://github.com/MiSTer-devel/Apple-II_MiSTer

FPGA-64
https://www.syntiac.com/fpga64.html


Some software transistor and gate-level simulators include:

Visual6502 by Ijor, Segher Boessenkool, Ed Spittles, Brian Silverman,
Barry Silverman and others
https://github.com/trebonian/visual6502.git

Breaknes by the emu-russia team
https://github.com/emu-russia/breaknes.git


I haven't examined all of these, but I'm pointing them out for those
who are more interested in a more formal approach.

The instruction database was completed with the help of the following set by kirbyUK:
https://gist.github.com/kirbyUK/1a0797e19f54c1e35e67ce7b385b323e


# Install #

pipenv was used to setup dependencies.  Feel free to use your Python
package-manager of choice.  A Pipfile is included for installing
dependencies.


$ pip install -U pipenv
$ pipenv install
$ pipenv shell

# Running #

The examples directory includes examples of using the library.

For example, to disassemble code:

$ PYTHONPATH=. pipenv run python examples/disassembler.py BINFILE


# Development #

## Design ##

There are some design decisions that were implemented that may seem inconsistent.

First, ordering of parameters in the Register, Flag and Instruction
classes differs.  For Register and Flag, short_name and name are
first, followed by size or bit_field_pos.  For the Instruction class,
name and opcode are first, followed by description.

It's called the description field instead of short_name and name
because the name of the instruction is for example LDA.  This
inconsistency may be changed later.

The opcode field comes before the description field because name and
opcode are the two primary elements used when manipulating
instructions.

A single Instruction is represented by the Instruction class.  A set
of instructions is represented by the Instructions class.  An
Instruction matches a single opcode, and can be thought of as an
"instantiation" of that opcode, not to be confused with the OOP
meaning of the word.

Instructions belong to an InstructionClass, which can have different
opcodes for different addressing modes.  A set of InstructionClasses
belong to an InstructionSet.  These InstructionSets combined with
Register and Flag definitions define chipsets, which are described in
JSON documents in the chip directory.

Different chipsets may have slightly different versions of
instructions.  For example, the NMOS and CMOS versions of the 6502
have some different features, bugs and quirks.  These differences are
often described with different words in the literature, as a "bug",
"quirk", "characteristic", "feature" or "idiom".  All these terms
describe a rich spectrum of advertant or inadvertant design choices
that bring life or difficulty to hardware designs.

John West and Marko MŠkelŠ have a document describing decimal / BCD
mode in NMOS 6500 series in depth and other processor features.  It
includes commented versions of decimal addition and subtraction code.
The name of the document is "Documentation for the NMOS 65xx/85xx
Instruction Set."  It also includes more detailed information on
processor differences.

Related to differences in behavior, some instructions are undocumented
and may behave differently on different chipsets.


### Bus Design ###

Most of the components, like instructions, flags and registers had
simple designs.  The CPU buses provided different design challenges:

  * The model should be simple and not introduce synchronization /
    concurrency issues.
  * The API should be easy to understand.

The requirements are that the CPU should be able to request items
(instructions or data) from memory and get those items back.  And it
should be able to write data to memory locations.  Research needs to
be done on the synchronization requirements and how the true hardware
deals with this (clocks, etc).

## Tests ##

To run tests:

$ pipenv run python -m pytest

Or if you have pytest-3 and the other requirements installed using system packages:

$ pytest

or

$ pytest-3


### Running external functional tests ###

There are several collections of full functional tests for 6502
processors.  One example is Running Adam Barnes' cc65 port of Klaus
Dormann's 6502 functional tests:

[Adam Barnes' cc65 port of Klaus Dormann's 6502 65C02 functional tests](https://github.com/amb5l/6502_65C02_functional_tests.git)

Running the tests:

PYTHONPATH=. python3 examples/run.py --debug --pc 1024 6502_functional_test.bin

Then press "c" to continue.



## Linting ##

This package uses black and flake8 for linting and style checking.
I'm not strict on some of the recommended lints, but you can run them
if you want.

$ pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
$ pipenv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
$ pipenv run black --check --diff .

Focus is on making sure the tests run.


## Debugging ##

A debugger and debugging modules are now included with the emulator.

Here's an example debugging a simple 6502 object file with with four instructions:

0000  ea        NOP
0001  e8        INX
0002  e8        INX
0003  e8        INX


$ PYTHONPATH=. pipenv run python examples/run.py -c data/nop-inx-inx-inx-sample-breakpoints.json --debug data/nop-inx-inx-inx.bin

reset: None
Computer PC: 0
reset vector: 0 0
applying debugger configuration data:
  Breakpoints:
    description: second NOP code
    address: 0x0002

> c
Breakpoint
0x0002 INX
> r
A: 0x00, P: 0x00, PC: 0x02, S: 0xFF, X: 0x01, Y: 0x00
> s
0x0003 INX
> c
> q
DebuggerState.EXIT
