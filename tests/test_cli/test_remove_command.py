from passpie.cli import cli
from passpie.database import CredentialFactory

from tinydb import Query


def test_cli_remove_all_credentials(irunner):
    irunner.db.insert_multiple([CredentialFactory(), CredentialFactory()])
    result = irunner.run(cli, "remove --all")

    assert result.exit_code == 0, result.output
    assert len(irunner.db) == 0


def test_cli_remove_one_credential_by_fullname(irunner, mocker):
    mocker.patch("passpie.cli.click.confirm", return_value=True)
    credentials = [
        CredentialFactory(fullname="foo@bar"),
        CredentialFactory(fullname="spam@egg"),
    ]
    irunner.db.insert_multiple(credentials)
    result = irunner.run(cli, "remove foo@bar")

    assert len(irunner.db) == 1, result.output
    assert irunner.db.search(irunner.db.query("spam@egg"))
    assert not irunner.db.search(irunner.db.query("foo@bar"))
