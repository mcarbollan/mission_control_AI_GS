"""Gera um banner ASCII para o Mission Control AI."""
import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", default="ansi_shadow")
    parser.add_argument("--text", default="Mission Control AI")
    parser.add_argument("--fonts", action="store_true")
    args = parser.parse_args()
    if args.fonts:
        console.print("\n".join(pyfiglet.FigletFont.getFonts()))
        return
    banner = pyfiglet.figlet_format(args.text, font=args.font)
    console.print(Align.center(Text(banner, style="bold #06B6D4")))
    console.print(Align.center(Text("FIAP · Global Solution 2026.1", style="italic")))

if __name__ == "__main__":
    main()
