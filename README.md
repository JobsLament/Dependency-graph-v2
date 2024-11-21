# Визуализатор графа зависимостей
Зависимости пакетов из архива 
`Packages.gz` генерируются PNG-изображение графа зависимостей.
[](https://github.com/JobsLament/Dependency-graph-v2/blob/main/examle/image_2024-11-21_09-36-53.png)

## Описание
Этот скрипт обрабатывает `.gz` архив, содержащий информацию о пакетах 
(например, файл `Packages.gz`, который обычно встречается в системах на 
базе Debian) и визуализирует зависимости между пакетами с помощью 
направленного графа. Для построения графа используется библиотека 
`networkx`, а для рендеринга в PNG — Graphviz.

## Требования
Перед запуском скрипта убедитесь, что у вас установлены следующие зависимости:
 **Необходимые библиотеки Python**:
   - `networkx`: Для построения и манипуляции графами.
   - `subprocess`: Для выполнения внешних команд (например, Graphviz).
   - `gzip`: Для работы с архивами `.gz`.
 
 **Graphviz**:
