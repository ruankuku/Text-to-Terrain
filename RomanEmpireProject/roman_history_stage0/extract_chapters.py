import re
import os

def extract_chapter_ranges(input_file_path, output_dir="extracted_chapters"):
    """
    提取指定章节范围的所有内容
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(input_file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    chapter_ranges = [
        ('IV-VI', 'CHAPTER IV', 'CHAPTER VII'),  
        ('VI-X', 'CHAPTER VI', 'CHAPTER XI'),    
        ('XIII-XIV', 'CHAPTER XIII', 'CHAPTER XV'), 
        ('XIV-XVII', 'CHAPTER XIV', 'CHAPTER XVIII') 
    ]
    
    for range_name, start_chapter, end_chapter in chapter_ranges:
        print(f"正在提取 {range_name} 章节...")
        
        # 构建正则表达式模式
        pattern = f"{re.escape(start_chapter)}.*?{re.escape(end_chapter)}"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            extracted_content = match.group(0)
            
            # 保存到文件
            output_filename = f"{output_dir}/chapters_{range_name}.txt"
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(extracted_content)
            
            print(f"成功保存: {output_filename}")
            print(f"提取内容长度: {len(extracted_content)} 字符")
        else:
            print(f"警告: 未找到 {range_name} 章节")
    
    print("\n所有章节提取完成！")

def find_all_chapter_titles(input_file_path):
    """
    查找并打印所有章节标题，用于调试
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(input_file_path, 'r', encoding='latin-1') as file:
            content = file.read()
    
    # 查找所有章节标题
    chapter_pattern = r'CHAPTER\s+[IVXLCDM]+'
    chapters = re.findall(chapter_pattern, content, re.IGNORECASE)
    
    print(f"在文件中找到 {len(chapters)} 个章节标题:")
    for i, chapter in enumerate(chapters):
        print(f"  {i+1}. {chapter}")

# 使用方法
if __name__ == "__main__":
    input_file = "decline_fall_full.txt"  # 您的文件路径
    
    if os.path.exists(input_file):
        print("文件找到，开始提取章节...")
        
        # 可选：先查看所有章节标题，确认格式
        # find_all_chapter_titles(input_file)
        
        # 提取章节范围
        extract_chapter_ranges(input_file)
        
    else:
        print(f"错误: 找不到文件 {input_file}")
        print("请确保文件路径正确")