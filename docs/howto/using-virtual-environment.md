# Using a virtual environment
When you have multiple python projects on your computer and these projects use different versions of the same packages, you may run into conflicts.
An easy way to deal with this is by making use of virtual environments. 
A virtual environment can be installed in a subdirectory of your project and contains its own python binary and its own version of the required packages.

Assuming you are using python 3.6, you can create a virtual environment as follows:

### Creating a virtual environment
From the root of your project, run 

- `python3 -m venv ./venv` (Linux / MacOS)
- `c:\Python35\python -m venv .\venv` (Windows)

You should now have a venv folder in your project.

### Activating the virtual environment
Now, to make sure that your project is using this virtual environment, you'll have to activate it. 
This will prepend the *venv/bin* directory to your PATH so that python and pip will run from this virtual environment and pip will install dependencies in the venv folder.

- `source <venv>/bin/activate` (Linux / MacOS - bash)
- `<venv>\Scripts\activate.bat` (Windows - cmd.exe)
- `<venv>\Scripts\Activate.ps1` (Windows - PowerShell)

You can test whether you are using the right python now by doing: 
- `which python` and `which pip` (Linux / MacOS - bash)
- `where python` and `where pip` (Windows - cmd.exe)
- `where.exe python` and `where.exe pip` (Windows - PowerShell)

You should be seeing the python and pip from within the venv folder

### Install dependencies into the virtual environment
From your project root run `pip install -r requirements.txt`.
The packages mentioned in the requirements.txt file will now be installed in the *venv/lib/python3.6/site-packages* folder.

### Deactivating your virtual environment
Just run `deactivate`, and your PATH is back to normal.
