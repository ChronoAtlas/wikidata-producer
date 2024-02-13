import time

import typer

app = typer.Typer()


@app.command()
def run() -> None:
    while True:  # noqa: WPS457
        print("Hello, World!")
        time.sleep(3)


if __name__ == "__main__":
    app()
