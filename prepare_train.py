def split_txt_by_category(input_txt, output_folder):
    """
    将一个文本文件根据每行末尾的数字进行分类，并保存为多个 .box 文件。

    参数：
    - input_txt: 输入的txt文件路径，每一行的末尾是分类数字
    - output_folder: 输出的文件夹路径，用于保存分类后的 .box 文件
    """

    # 创建一个字典，用来存储不同分类的行
    categories = {}

    # 读取输入文件
    with open(input_txt, 'r') as file:
        for line in file:
            # 去掉行尾的换行符，并提取末尾的分类数字
            line = line.strip()
            *text, category = line.split()  # 将文本和分类分开
            category = int(category)  # 分类数字转换为整数

            # 将这一行加入对应分类的列表中
            if category not in categories:
                categories[category] = []
            categories[category].append(" ".join(text))

    # 保存每个分类的内容到单独的 .box 文件
    for category, lines in categories.items():
        if category < 10:
            output_file = f"{output_folder}/num-00{category+1}.box"
        else:
            output_file = f"{output_folder}/num-0{category+1}.box"
        with open(output_file, 'w') as out_file:
            for line in lines:
                out_file.write(line + '\n')

    print(f"文件已根据分类保存到 {output_folder} 文件夹中。")

# 使用示例：
input_txt = 'train_ocr/sum/num.box'  # 输入的txt文件路径
output_folder = 'train_ocr/sum/'  # 输出的文件夹路径
split_txt_by_category(input_txt, output_folder)
