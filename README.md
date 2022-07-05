# RozhlasDownloader
Smol typer tool to download Rozhlas audio (vltava.rozhlas works, other were not tried). It doesn't have fancy-ass name, so I call it smol tool or typer App. 

## Installation

This smol tool uses poetry to manaage dependencies. So, to get everything ready run:

> poetry install

## Usage

This typer App runs with single argument which is vltava.rozhlas.cz link. Then it downloads all episodes and gives them metadata.

Example call:
> python main.py https://vltava.rozhlas.cz/tom-stoppard-albertuv-most-v-cem-nachazi-smysl-zivota-absolventi-filozofie-5948710
