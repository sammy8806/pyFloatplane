# pyFloatplane

pyFloatplane is a Python3 REST-Client for [Floatplane.com](https://floatplane.com) and is considered **UNOFFICIAL**.

Some use-cases for the library are:

* Video downloads
* Image grabbing
* Comment interaction
* Pull-based Video notifications

The example `download.py` can list your subscriptions and show the last _n_ videos with their respective comments.

## Guidance steps

### Config

The `lmg-forums` element in the config is considered **deprecated** and isn't needed anymore.
It was used for the forum-based VideoUrl-Endpoint.

### PipEnv

You can use **pipenv**
Example commands:

```bash
pipenv --three install
pipenv run python download.py
```
