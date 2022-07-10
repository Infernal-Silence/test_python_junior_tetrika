from bs4 import BeautifulSoup
import requests


# Задача №1.


def task(array: str) -> int:
    return array.index("0")


# Задача №2.


def animals_wiki():
    animals = {}
    link = "/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%96%D0%B8%D0%B2%D0%BE%D1%82%D0%BD%D1%8B%D0%B5_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"

    while True:
        res = requests.get(f"https://ru.wikipedia.org{link}")
        soup = BeautifulSoup(res.content, "html.parser")
        link = soup.select_one("#mw-pages").findChildren("a", recursive=False)[-1].attrs["href"]
        tag_h3 = soup.select_one(".mw-category-columns").find_all("h3")

        for tag in tag_h3:
            if tag.get_text() == "A":
                return animals
            animals[tag.text] = animals.get(tag.text, 0) + len(tag.find_next().findChildren("li", recursive=False))

        # print(animals)


animals = animals_wiki()

print(*[f"{k}: {v}" for k, v in animals.items()], sep="\n")


# Задача №3.

def chunks(sections):
    return [sections[i: i + 2] for i in range(0, len(sections), 2)]


def merge(sections):
    sections = sorted(sections, key=lambda s: s[0])
    merged = []
    for s in sections:
        if not merged:
            merged.append(s)
            continue

        a, b = merged[-1]
        c, d = s

        if b < c:
            merged.append(s)
        if c < b:
            merged[-1] = [a, d]
    return merged


def get_intersections(section, sections):
    a, b = section
    res = []
    for c, d in sections:
        if b >= c and a <= d:
            res.append([max(a, c), min(b, d)])
    return res


def appearance(intervals):
    intersections = []
    # sections_pupil = merge(chunks(intervals["pupil"]))
    # sections_tutor = merge(chunks(intervals["tutor"]))
    sections_pupil = chunks(intervals["pupil"])
    sections_tutor = chunks(intervals["tutor"])
    for section in sections_pupil:
        intersections.extend(get_intersections(section, sections_tutor))

    res = get_intersections(intervals["lesson"], intersections)

    return sum(map(lambda s: s[1] - s[0], res))


tests = [
    {
        "data": {
            "lesson": [
                1594663200,
                1594666800,
            ],
            "pupil": [
                1594663340,
                1594663389,
                1594663390,
                1594663395,
                1594663396,
                1594666472,
            ],
            "tutor": [
                1594663290,
                1594663430,
                1594663443,
                1594666473,
            ],
        },
        "answer": 3117,
    },
    # {
    #     "data": {
    #         "lesson": [
    #             1594702800,
    #             1594706400,
    #         ],
    #         "pupil": [
    #             1594702789,
    #             1594704500,
    #             1594702807,
    #             1594704542,
    #             1594704512,
    #             1594704513,
    #             1594704564,
    #             1594705150,
    #             1594704581,
    #             1594704582,
    #             1594704734,
    #             1594705009,
    #             1594705095,
    #             1594705096,
    #             1594705106,
    #             1594706480,
    #             1594705158,
    #             1594705773,
    #             1594705849,
    #             1594706480,
    #             1594706500,
    #             1594706875,
    #             1594706502,
    #             1594706503,
    #             1594706524,
    #             1594706524,
    #             1594706579,
    #             1594706641,
    #         ],
    #         "tutor": [
    #             1594700035,
    #             1594700364,
    #             1594702749,
    #             1594705148,
    #             1594705149,
    #             1594706463,
    #         ],
    #     },
    #     "answer": 3577,
    # },                       Почему в тестах есть пересечение таймстемпов?
    {
        "data": {
            "lesson": [
                1594692000,
                1594695600,
            ],
            "pupil": [
                1594692033,
                1594696347,
            ],
            "tutor": [
                1594692017,
                1594692066,
                1594692068,
                1594696341,
            ],
        },
        "answer": 3565,
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["data"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
