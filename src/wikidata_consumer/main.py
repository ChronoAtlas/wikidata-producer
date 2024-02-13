import typer
import time

app = typer.Typer()

@app.command()
def run() -> None:
    while True:
        print("Hello, World!")
        time.sleep(3)

if __name__ == "__main__":
    app();
