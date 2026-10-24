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

- `ls [-l] [path]` - содержимое папки, `-l` - с правами
- `cd [path]` - смена папки, без аргумента - в корень `~`
- `uptime` - время работы эмулятора
- `who` - текущий пользователь
- `tail [-n N] file` - последние N строк файла (по умолчанию 10)
- `mkdir dir ...` - создание папок
- `chmod MODE path ...` - смена прав, `MODE` восьмеричный (`755`)
- `vfs-load path` - загрузка другой VFS
- `exit [code]` - выход

Аргументы с пробелами пишутся в кавычках: `cd "my dir"`.

## Пример

```
> python main.py --vfs vfs\deep.csv
[debug] vfs = vfs\deep.csv, script = None
sniman@sniman:~$ cd "home/user/my docs"
sniman@sniman:~/home/user/my docs$ ls -l
-rw-r--r-- todo.txt
sniman@sniman:~/home/user/my docs$ cd nope
cd: nope: No such file or directory
sniman@sniman:~/home/user/my docs$ exit
```
