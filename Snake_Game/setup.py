import cx_Freeze

executables = [cx_Freeze.Executable("snake.py")]

cx_Freeze.setup(
    name = "Poison Overloaded",
    options = {"build_exe":{"packages":["pygame","random","time"],"include_files":["apple.png","snakehead.png","comicsansms.ttf"]}}, 
    description = "Snake Game",
    executables = executables)