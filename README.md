# shell-emulator

Эмулятор командной строки UNIX на Python.

Запуск: `run.bat` или `python main.py [--vfs PATH] [--script PATH]`.

- `--vfs` - путь к VFS
- `--script` - стартовый скрипт: команды по строкам, комментарии через `#`

Тесты: `python -m unittest discover tests`.
Проверка параметров: `scripts\params.bat`, `scripts\errors.bat`.

## Команды

- `ls`, `cd` - пока заглушки, выводят имя и аргументы
- `exit [code]` - выход

Аргументы с пробелами пишутся в кавычках: `cd "my dir"`.
