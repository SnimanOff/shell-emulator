# shell-emulator

Эмулятор командной строки UNIX на Python.

Запуск: `run.bat` или `python main.py [--vfs PATH] [--script PATH]`.

- `--vfs` - VFS из CSV `path,type,data`: полный путь, `dir` или `file`,
  содержимое файла в base64; все изменения только в памяти
- `--script` - стартовый скрипт: команды по строкам, комментарии через `#`

Тесты: `python -m unittest discover tests`.
Скрипты для проверки: `scripts\params.bat`, `scripts\vfs.bat`,
`scripts\errors.bat`.

## Команды

- `ls [path]` - содержимое папки
- `cd [path]` - смена папки, без аргумента - в корень `~`
- `uptime` - время работы эмулятора
- `who` - текущий пользователь
- `tail [-n N] file` - последние N строк файла (по умолчанию 10)
- `exit [code]` - выход

Аргументы с пробелами пишутся в кавычках: `cd "my dir"`.
