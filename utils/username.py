import random


def get_random_name():
    name = random.choice(
        [
            "철수",
            "영희",
            "니꼬",
            "린",
            "톰 크루즈",
            "해리 포터",
            "수지",
            "다람쥐",
            "스칼렛 요한슨",
            "곽철용",
            "카피추",
            "빌 게이츠",
        ]
    )
    deco = random.choice(
        [
            "배고픈",
            "행복한",
            "두근두근한",
            "멋진",
            "힘찬",
            "갓갓",
            "놀란",
            "한 끗으로 5억을 태운",
            "욕심이 전혀 없는",
            "격렬하게 쉬고 싶은",
        ]
    )
    nickname = f"{deco} {name}"
    return nickname
