from cx_Freeze import setup, Executable

setup(
    name="Pyrogram Login",  # Имя вашего приложения
    version="1.0",  # Версия вашего приложения
    description="Pyrogram Login App",  # Описание вашего приложения
    executables=[Executable(script="s_construct.py", base="Win32GUI", icon="your_icon.ico")]
)

