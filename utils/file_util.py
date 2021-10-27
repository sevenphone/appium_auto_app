# -- coding: utf-8 --
import os
import yaml


def remove_not_start_with_file(file_dir: str, file_start_str: str):
    """删除文件夹内命名不是以XX开头的文件
    :param file_dir: 文件夹路径
    :param file_start_str:文件名开头格式
    :return:
    """
    all_file_in_dir = os.listdir(file_dir)
    for file_name in all_file_in_dir:
        if not file_name.startswith(file_start_str):
            full_file_name = os.path.join(file_dir, file_name)
            os.remove(full_file_name)


def create_folder_from_dir(father_dir: str, child_folder: str):
    """从父目录创建子文件夹
    :param father_dir: 父目录
    :param child_folder: 需要创建的子文件夹
    :return:
    """
    full_path = os.path.join(father_dir, child_folder)
    if not os.path.exists(full_path):
        os.makedirs(full_path)


def return_full_file(father_dir: str, child_folder: str, file_name: str, create_file: bool = False) -> str:
    """组合父目录,子文件夹和文件返回完整文件路径
    :param father_dir: 父目录,不包括 文件的上层文件夹
    :param child_folder: 子文件夹,即文件的上层文件夹
    :param file_name: 文件名
    :param create_file: 是否需要创建文件，默认不创建
    :return: 完整文件路径
    """
    create_folder_from_dir(father_dir, child_folder)
    full_file = os.path.join(father_dir, child_folder, file_name)
    if create_file and (not os.path.exists(full_file)):
        # os.system(f"touch {full_file}")   # touch能创建文件，但Windows下会报不是内部或外部命令
        os.system(f"echo=# -- coding: utf-8 -- >{full_file}")
    return full_file


def read_yaml(yaml_file: str):
    """读取yaml文件
    :param yaml_file: yaml文件所在路径
    :return: yaml文件读取出的list或dict
    """
    file = open(yaml_file, "r", encoding="UTF-8")
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data
