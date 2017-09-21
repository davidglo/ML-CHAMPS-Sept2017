# Jupyter notebook

[Documentation](http://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/execute.html)

1. Launch from command line: 

    ```
    $ jupyter notebook
    ```
    
    ![alt text](http://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/images/dashboard_files_tab.png "JNB dash")

2. Click on existing notebook, or make new one: 

    ![alt text](http://nbviewer.jupyter.org/github/jupyter/notebook/blob/master/docs/source/examples/Notebook/images/dashboard_files_tab_new.png "JNB new") 

3. Enter code in cells and the hit `shift + enter` to run code:

    ```python
    In [1]: a, b = 1, 2
    In [2]: print(a+b)
    3
    ```
    3. `alt/option + enter` runs code and inserts new cell below. 

4. Many more options from menu bar:
    ![alt text](https://github.com/jupyter/notebook/blob/master/docs/source/examples/Notebook/images/menubar_toolbar.png "JNB toolbar")
    1. `Insert` allows you to insert cells
    2. `Cell` allows specific control on how to run cells
    3. `Kernel` controls the Python kernel used to run calculations.  Restart kernel from here if things get stuck!

5. Cells can be markdown or code - controlled from dropdown menu or from `cell` menu. 
