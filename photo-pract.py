import time
import multiprocessing
from pathlib import Path
from PIL import Image


def process(args):
    src, dst = args
    img = Image.open(src)
    img = img.rotate(-90, expand=True)
    img = img.resize((800, 600), Image.LANCZOS)
    img = img.convert("L")
    img.save(dst)


if __name__ == '__main__':
    # создаём тестовые фото
    Path("images").mkdir(exist_ok=True)
    for i in range(10):
        Image.new("RGB", (1200, 900), color=(i*25, 100, 200)).save(f"images/img_{i}.jpg")

    # список задач (откуда -> куда)
    Path("processed").mkdir(exist_ok=True)
    tasks = []
    for f in sorted(Path("images").glob("*.jpg")):
        src = str(f)
        dst = f"processed/out_{f.name}"
        tasks.append((src, dst))

    print(f"Файлов: {len(tasks)}")

    # последовательно
    t = time.perf_counter()
    for task in tasks:
        process(task)
    print(f"Последовательно: {time.perf_counter() - t:.3f} сек")

    # параллельно
    t = time.perf_counter()
    with multiprocessing.Pool() as pool:
        pool.map(process, tasks)
    print(f"Параллельно:     {time.perf_counter() - t:.3f} сек")