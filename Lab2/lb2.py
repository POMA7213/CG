import cv2
import numpy as np

import tkinter as tk
from tkinter import filedialog
import os


def global_thresholding_by_otsu(image):
    # Вычисление гистограммы изображения
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # Вычисление общего числа пикселей в изображении
    total_pixels = image.shape[0] * image.shape[1]

    # Расчет накопленной суммы гистограммы
    cumulative_sum = np.cumsum(hist)

    # Нахождение порога на основе метода Отсу
    threshold = 0
    max_variance = 0

    for t in range(256):
        # Вычисление вероятностей классов
        w0 = cumulative_sum[t] / total_pixels
        w1 = (total_pixels - cumulative_sum[t]) / total_pixels

        # Вычисление средних значений классов
        mu0 = np.sum(np.multiply(hist[:t + 1], np.arange(t + 1))) / (cumulative_sum[t] + 1e-8)
        mu1 = np.sum(np.multiply(hist[t + 1:], np.arange(t + 1, 256))) / (
                cumulative_sum[255] - cumulative_sum[t] + 1e-8)

        # Вычисление межклассовой дисперсии
        variance = w0 * w1 * (mu0 - mu1) ** 2

        # Обновление порога, если дисперсия больше максимальной
        if variance > max_variance:
            max_variance = variance
            threshold = t

    # Применение порогового преобразования
    processed = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    return processed


def global_thresholding_by_hist(image):
    eps = 1e-3

    threshold = 128
    while True:
        fmask = image >= threshold
        fir = 255
        if np.sum(fmask) != 0:
            fir = np.mean(image[fmask])
        smask = image < threshold
        sec = 0
        if np.sum(smask) != 0:
            sec = np.mean(image[smask])
        pt = threshold
        threshold = (fir + sec) / 2
        if np.abs(threshold - pt) < eps:
            break

    # Применение порогового преобразования
    processed = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    return processed


def point(image):
    kernel = np.array(
        [[-1, -1, -1],
         [-1, 8, -1],
         [-1, -1, -1]], dtype=np.float32)

    tr = 200

    filtered_image = cv2.filter2D(image, -1, kernel)

    filtered_image = cv2.threshold(filtered_image, tr, 255, cv2.THRESH_BINARY)[1]

    return filtered_image


def ver_line(image):
    kernel1 = np.array(
        [[-1, 2, -1],
         [-1, 2, -1],
         [-1, 2, -1]], dtype=np.float32)

    tr = 200
    f1 = cv2.filter2D(image, -1, kernel1)
    filtered_image = cv2.threshold(f1, tr, 255, cv2.THRESH_BINARY)[1]

    return filtered_image


def line(image):
    kernel1 = np.array(
        [[-1, 2, -1],
         [-1, 2, -1],
         [-1, 2, -1]], dtype=np.float32)

    kernel2 = np.array(
        [[-1, -1, -1],
         [2, 2, 2],
         [-1, -1, -1]], dtype=np.float32)

    kernel3 = np.array(
        [[2, -1, -1],
         [-1, 2, -1],
         [-1, -1, 2]], dtype=np.float32)

    kernel4 = np.array(
        [[-1, -1, 2],
         [-1, 2, -1],
         [2, -1, -1]], dtype=np.float32)

    tr = 20

    f1 = cv2.filter2D(image, -1, kernel1)
    f2 = cv2.filter2D(image, -1, kernel2)
    f3 = cv2.filter2D(image, -1, kernel3)
    f4 = cv2.filter2D(image, -1, kernel4)

    filtered_image = cv2.threshold(np.maximum(np.maximum(f1, f2), np.maximum(f3, f4)), tr, 255, cv2.THRESH_BINARY)[1]

    return filtered_image


def border(image):
    kernel1 = np.array(
        [[1, 2, 1],
         [0, 0, 0],
         [-1, -2, -1]], dtype=np.float32)

    kernel2 = np.array(
        [[2, 1, 0],
         [1, 0, -1],
         [0, -1, -2]], dtype=np.float32)

    kernel3 = np.array(
        [[1, 0, -1],
         [2, 0, -2],
         [1, 0, -1]], dtype=np.float32)

    kernel4 = np.array(
        [[0, 1, 2],
         [-1, 0, 1],
         [-2, -1, 0]], dtype=np.float32)

    kernel5 = np.array(
        [[-1, 0, 1],
         [-2, 0, 2],
         [-1, 0, 1]], dtype=np.float32)

    kernel6 = np.array(
        [[-2, -1, 0],
         [-1, 0, 1],
         [-0, 1, 2]], dtype=np.float32)

    kernel7 = np.array(
        [[-1, -2, -1],
         [0, 0, 0],
         [1, 2, 1]], dtype=np.float32)

    kernel8 = np.array(
        [[0, -1, -2],
         [1, 0, -1],
         [2, 1, 0]], dtype=np.float32)

    tr = 200
    f1 = cv2.filter2D(image, -1, kernel1)
    f2 = cv2.filter2D(image, -1, kernel2)
    f3 = cv2.filter2D(image, -1, kernel3)
    f4 = cv2.filter2D(image, -1, kernel4)
    f5 = cv2.filter2D(image, -1, kernel5)
    f6 = cv2.filter2D(image, -1, kernel6)
    f7 = cv2.filter2D(image, -1, kernel7)
    f8 = cv2.filter2D(image, -1, kernel8)

    filtered_image = cv2.threshold(np.maximum(np.maximum(np.maximum(f1, f2), np.maximum(f3, f4)),
                                              np.maximum(np.maximum(f5, f6), np.maximum(f7, f8))), tr, 255,
                                   cv2.THRESH_BINARY)[1]

    return filtered_image


def select_input_directory():
    input_directory = filedialog.askdirectory(title="Select Input Directory")
    input_entry.delete(0, tk.END)
    input_entry.insert(0, input_directory)


def select_output_directory():
    output_directory = filedialog.askdirectory(title="Select Output Directory")
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_directory)


def process_images():
    input_directory = input_entry.get().replace('/', '\\')
    output_directory = output_entry.get().replace('/', '\\')

    methods = [
        global_thresholding_by_hist, global_thresholding_by_otsu, point, line, ver_line, border]

    for method in methods:
        method_output_directory = os.path.join(output_directory, method.__name__)
        os.makedirs(method_output_directory, exist_ok=True)

        image_files = os.listdir(input_directory)
        for image_file in image_files:
            print(image_file)
            if image_file.endswith('.png') or image_file.endswith('.jpg'):
                image_path = os.path.join(input_directory, image_file)
                print(image_path)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                # Процесс обработки изображения с использованием выбранного метода
                processed_image = method(image)

                output_image_path = os.path.join(method_output_directory, image_file)
                cv2.imwrite(output_image_path, processed_image)
        print(method.__name__, " Completed\n")

    print("Processing complete!")


# Создание графического интерфейса
root = tk.Tk()

# Кнопка 1 - выбор директории с исходными изображениями в формате PNG
button1 = tk.Button(root, text="Select Input Directory", command=select_input_directory)
button1.pack()

# Поле ввода для отображения выбранной директории
input_entry = tk.Entry(root)
input_entry.insert(0, "Input")
input_entry.pack()

# Кнопка 2 - выбор директории для сохранения обработанных изображений
button2 = tk.Button(root, text="Select Output Directory", command=select_output_directory)
button2.pack()

# Поле ввода для отображения выбранной директории
output_entry = tk.Entry(root)
output_entry.insert(0, "Output")
output_entry.pack()

# Кнопка 3 - обработка изображений
button3 = tk.Button(root, text="Process Images", command=process_images)
button3.pack()

root.mainloop()
