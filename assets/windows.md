Launchpad GDPR Obfuscator Service
# Automatized Set Up - WINDOWS VENV (virtual enviorments)

Run `./assets/setup_and_test.ps1` in the terminal.

* [color code in powershell terminal](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/write-host?view=powershell-7.5)

* [automatate in powershell](https://learn.microsoft.com/en-us/training/paths/powershell/)

* [scripting in powershell](https://learn.microsoft.com/en-us/training/modules/script-with-powershell/)

* [realpython](https://realpython.com/)

# Manual Set Up - WINDOWS VENV (virtual enviorments)

Before running commands, ensure to run this scripts in PowerShell. 
Open PowerShell as Administrator and run:<br>
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## Step-by-step instructions:

1. Create Venv:<br> 
`python -m venv venv`

2. Activate Venv:<br>
`.\venv\Scripts\Activate.ps1`

3. Upgrade:<br>
`python -m pip install --upgrade pip`

4. Install dependencies:<br> 
`pip install -r requirements.txt`

You can install dependencies induvisually too in one go:<br>
`pip install `

5. PYTHONPATH - here you tell for pc to run everything from your project root<br>
`$env:PYTHONPATH = "."`

If you want to be sure that your test run on the right path use *;* :<br>
`$env:PYTHONPATH="."; python -m pytest tests/test_obfuscator.py -vv -s --color=yes`

6. Run unit tests:<br>
Run every tests in test_***.py file  -vv =>   -s => <br>
`python -m pytest tests/test_obfuscator.py -vv -s --color=yes`

Run a particular unit test within a file:<br>
``

7. Other tests:

    1. **Security Test (Bandit):** Scans code for common security issues (like hardcoded passwords or insecure function calls), [bandit](https://bandit.readthedocs.io/en/latest/)<br>
    `python -m bandit -lll -r src/`<br>

    2. **Code Formatter (Black):** Automatically reformats your code to comply with the PEP 8 style guide, [black](https://black.readthedocs.io/en/stable/)<br>
    `python -m black src tests`

    3. **Linter (Flake8):** Checks for stylistic errors, unused imports, lenght of the code (best practice between 88 - 100 charackter per line) and complex code sections, [flacke8](https://flake8.pycqa.org/en/latest/)<br>
    `python -m flake8 --max-line-length=100 src tests`

    4. **Vulnerability Audit (pip-audit):** Checks if your installed dependencies in requirements.txt have known security vulnerabilities., [audit](https://pypi.org/project/pip-audit/)<br>
    `python -m pip_audit`

    5. **PEP8 Compliant - All tests together:** Run this single line to verify everything before a Git Push. It sets the path and runs all tools in sequence.<br>
    `$env:PYTHONPATH="."; python -m pytest tests -vv; python -m black src tests; python -m bandit -lll -r src/; python -m pip_audit; python -m flake8 --max-line-length=100 src tests`

8. **Coverage Tracking**:<br>
If you want to see exactly which lines of your Lambda are covered by your tests, [coverage](https://coverage.readthedocs.io/en/7.13.1/)
Run Coverage and Create a coverage.txt file: <br>
`python -m coverage run -m pytest tests; python -m coverage report -m > coverage.txt`

9. Deactivate venv: `deactivate`
