#!/usr/bin/env python
from app import create_app

app = create_app()
app.run(debug=True)
