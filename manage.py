import subprocess
import sys

from sqlalchemy_utils import database_exists, create_database

from exchange_operations import create_app

app = create_app()


@app.cli.command(with_appcontext=True)
def test():
    sys.exit(subprocess.call(['py.test',
                              './']))


@app.cli.command(with_appcontext=True)
def recreate_db():
    from exchange_operations import db_sql_alchemy as db
    db.drop_all()
    db.create_all()
    db.session.commit()


@app.cli.command(with_appcontext=True)
def create_db():
    from exchange_operations import db_sql_alchemy as db
    if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()
        db.session.commit()
