import yaml

def fibonacci(n):
    a = 0
    b = 1
    res = []
    res.append(a)
    res.append(b)
    for i in range(2, n):
        res.append(a+b)
        a = b
        b = res[-1]
 
    return res
 
print("FIBONACI SERIES")
n = int(input("Please Enter Number of Element to Print: "))
res = fibonacci(n)
print("Fibonacci Series: ", *res)

'''PyInstaller

Spec File: is an executable python code that tells PyIstaller how to process our Python script. It needs no change except:
    To bundle our data files with the app.
    To include run-time libraries that are unknown to PyInstaller.
    To add Python run-time options to the executable.
    To create a multiprogram bundle with merged common modules.

Build Folder: stores metadata and is useful for debugging.
    pyinstaller --log-level=DEBUG program.py

Import Error
    pyinstaller --hidden-import program.py
    pyinstaller --additional-hooks-dir=. program.py
'''

### Quick Start
# pyinstaller --onefile --windowed pyinstaller-sample.py
# pyinstaller pyinstaller-sample.py
# pyinstaller program.py --name pythonproject
# pyi-makespec pyinstaller-sample.py -> Create Spec File


### Reference
# https://www.askpython.com/python/pyinstaller-executable-files