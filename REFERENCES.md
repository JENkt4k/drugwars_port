# References and Attribution

This project is an unofficial TI-Nspire CX II reimplementation inspired by historical versions of **Drug Wars**.

## Historical game references

### John E. Dell

John E. Dell is credited as the author of the original Drug Wars game.

This repository does not claim ownership of Dell's original source code, name, or other pre-existing material.

### Jonathan Maier / J.M.

The TI-82/83-era version used as the main behavioral reference for this port is commonly identified as **J.M.'s Drugwar Simulation 2.00**, by Jonathan Maier, circa 1994.

Archived TI-BASIC source reference:

- https://gist.github.com/mattmanning/1002653

The archived BASIC source was used to understand gameplay rules such as commodity pricing, random events, debt/bank behavior, inventory, police encounters, and scoring.

The Python implementation in this repository is a rewritten port rather than a line-for-line relicensing of that historical source.

## Known historical implementation issue

The archived TI-BASIC program appears to reuse variable `N` for more than one purpose, including heroin inventory and location-related state. The Python port intentionally separates those concepts into independent state variables instead of reproducing the collision.

## TI-Nspire / build tooling

### Luna

Luna converts Python source into TI-Nspire `.tns` documents.

- https://github.com/ndless-nspire/Luna

Luna is a third-party project and has its own licensing terms. Nothing in this repository changes or supersedes Luna's license.

### TI-Nspire CX II Connect

Used to transfer generated `.tns` documents to the calculator.

- https://education.ti.com/en/products/computer-software/ti-nspire-cx-ii-connect

### TI-Nspire Python documentation

- https://education.ti.com/en/activities/ti-codes/python/ti-nspire-cx-ii/python-modules

## Generated artwork

Project-specific artwork may be generated for the graphical edition, including skyline backgrounds and event illustrations. Artwork licensing should be documented alongside the corresponding files when assets are added to the repository.

## Trademark / affiliation notice

Texas Instruments and TI-Nspire are trademarks of their respective owner(s). This project is not affiliated with or endorsed by Texas Instruments, John E. Dell, Jonathan Maier, or maintainers of historical Drug Wars archives.
