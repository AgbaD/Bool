#!/usr/bin/python
# Author:   @BlankGodd_

from app import create_app, db
from flask_migrate import Migrate
import os
from app.models import Cash_account, Coin_account, User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, app=app, User=User, Cash_account=Cash_account, Coin_account=Coin_account)

if __name__ == '__main__':
    app.run(debug=True)