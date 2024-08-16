import typer
from pm.handler import list_credentials, save_credentials, delete_credentials, configure_pg, update_credentials

app = typer.Typer(add_completion=False,
                  rich_markup_mode='markdown',
                  pretty_exceptions_enable=False,
                  pretty_exceptions_show_locals=False,
                  pretty_exceptions_short=False)


@app.callback()
def main():
    pass


@app.command(help="Configure", name="configure")
def configure():
    configure_pg()


@app.command(help="List Credentials", name="list")
def list_():
    list_credentials()


@app.command(help="Save Credentials", name="save")
def save(website: str = typer.Option(..., "--website", "-w", help="Website"),
         email: str = typer.Option(..., "--email", "-e", help="Email"),
         password: str = typer.Option(..., "--password", "-p", help="Password")):
    save_credentials(website, email, password)


@app.command(help="Update Credentials", name="update")
def update(id_: str = typer.Option(..., "--id", help="Website"),
           website: str = typer.Option(None, "--website", "-w", help="Website"),
           email: str = typer.Option(None, "--email", "-e", help="Email"),
           password: str = typer.Option(None, "--password", "-p", help="Password")):
    update_credentials(id_, website, email, password)


@app.command(help="Delete Credentials", name="delete")
def delete(id_: str = typer.Option(..., "--id", help="Website")):
    delete_credentials(id_)


if __name__ == "__main__":
    app()
