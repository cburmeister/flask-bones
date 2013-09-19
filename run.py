#!/usr/bin/env python
from app import create_app
from app.config import base_config

app = create_app(base_config)
app.run(debug=True)
