# README.md

## Описание

Этот скрипт на языке Python выполняет различные методы обработки изображений для коллекции изображений. Он предоставляет функции для применения глобальной бинаризации, обнаружения точек, обнаружения линий, обнаружения вертикальных линий и обнаружения границ с использованием различных фильтрующих ядер.

## Требования

- Python 3
- OpenCV (`cv2`)
- NumPy
- Tkinter (для графического интерфейса)
- pyinstaller

## Установка

1. Убедитесь, что у вас установлен Python 3.
2. Установите необходимые пакеты, выполнив следующую команду:
```
pip install opencv-python numpy
```
Скрипт предоставляет следующие методы обработки изображений:

1. Глобальная бинаризация по гистограмме (global_thresholding_by_hist)
Этот метод выполняет глобальную бинаризацию на входном изображении с использованием подхода на основе гистограммы.

2. Глобальная бинаризация по методу Оцу (global_thresholding_by_otsu)
Этот метод применяет глобальную бинаризацию на входном изображении с использованием метода Оцу, который автоматически определяет пороговое значение на основе гистограммы изображения.

3. Обнаружение точек (point)
Этот метод обнаруживает точки на входном изображении с помощью специального фильтрующего ядра.

4. Обнаружение линий (line)
Этот метод обнаруживает линии на входном изображении, применяя несколько фильтрующих ядер и объединяя результаты.

5. Обнаружение вертикальных линий (ver_line)
Этот метод специально обнаруживает вертикальные линии на входном изображении с помощью фильтрующего ядра.

6. Обнаружение границ (border)
Этот метод обнаруживает границы на входном изображении, применяя различные фильтрующие ядра и объединяя результаты.

Обратите внимание, что обработанные изображения будут сохранены в отдельных директекториях, названных соответственно используемому методу обработки.

Вы можете свободно изменять скрипт и экспериментировать с различными методами обработки изображений в соответствии с вашими потребностями.
