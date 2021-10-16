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

I haven't examined all of these, but I'm pointing them out for those
who are more interested in a more formal approach.

# Install #

pipenv was used to setup dependencies.  Feel free to use your Python
package-manager of choice.  A Pipfile is included for installing
dependencies.


$ pip install -U pipenv
$ pipenv install
$ pipenv shell

# Running #

$ python -m bitey.app

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

## Linting ##

This package uses black and flake8 for linting and style checking.
I'm not strict on some of the recommended lints, but you can run them
if you want.

$ pipenv run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
$ pipenv run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
$ pipenv run black --check --diff .

Focus is on making sure the tests run.

