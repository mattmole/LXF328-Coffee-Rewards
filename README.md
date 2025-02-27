# LXF328-Coffee-Rewards
Python and Django Coffee Shop Reward System - created for Linux Format 328

To utilise:

* Clone the repo to a directory on your filesystem
* uv init .
* uv add django rich
* uv run manage.py makemigrations Rewards
* uv run manage.py migrate
* uv run manage.py createsuperuser
* Using the admin interface (http://localhost:8000) add some entries to the account code builder model
* Visit http://localhost:8000/rewards/points
