import random
import string


def random_num(num: int = 1) -> str:
    """生成随机数（str格式）
    :param num:需要生成的位数，默认是1位
    :return:随机数（str格式）
    """
    if num > 0:
        # result = ''.join(str(random.randint(0, 9)) for _ in range(num))
        result = ''.join(random.choice(string.digits) for _ in range(num))
    else:
        result = random_num()
    return result


def random_str(num: int = 1) -> str:
    """生成随机字符串
    :param num: 需要成功的字符串位数
    :return: 成成的随机字符串
    """
    # 字母：string.ascii_letters
    # 大写：string.ascii_uppercase
    # 小写：string.ascii_lowercase
    if num > 0:
        result = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num))
    else:
        result = random_str()
    return result


def random_phone() -> str:
    """随机生成中国手机号
    :return: 生成的随机手机号(str)
    """
    def random_phone_prefix():
        """随机号段"""
        operator = random.choice([1, 2, 3])
        if operator == 1:  # 电信
            number_segment = random.choice([133, 149, 153, 173, 174, 177, 180, 181, 189, 199])
        elif operator == 2:  # 联通
            number_segment = random.choice([130, 131, 132, 145, 146, 155, 156, 166, 171, 175, 176, 185, 186])
        else:  # 移动
            number_segment = random.choice([134, 135, 136, 137, 138, 139, 147, 148, 150, 151, 152,
                                            157, 158, 159, 172, 178, 182, 183, 184, 187, 188, 198])
        return str(number_segment)
    return random_phone_prefix() + random_num(8)


def get_keycode(original: str) -> int:
    """获取要输入的数字或字母的keycode
    :param original: 原始数字或字母
    :return: 对应的keycode；如果匹配不到则返回3(HOME)
    """
    key = {'0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12, '6': 13, '7': 14, '8': 15, '9': 16,
           'a': 29, 'b': 30, 'c': 31, 'd': 32, 'e': 33, 'f': 34, 'g': 35,
           'h': 36, 'i': 37, 'j': 38, 'k': 39, 'l': 40, 'm': 41, 'n': 42,
           'o': 43, 'p': 44, 'q': 45, 'r': 46, 's': 47, 't': 48,
           'u': 49, 'v': 50, 'w': 51, 'x': 52, 'y': 53, 'z': 54}
    for k, v in key.items():
        if k == str(original).strip().replace('\n', '').replace('\r', ''):
            return v
    return 3
