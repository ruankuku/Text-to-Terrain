import re
import os

def deep_clean_notes(input_dir="extracted_chapters", output_dir="deep_cleaned_chapters"):
    """
    深度清理注释，使用多种方法确保彻底清除
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    chapter_files = [
        "chapters_IV-VI.txt",
        "chapters_VI-X.txt", 
        "chapters_XIII-XIV.txt",
        "chapters_XIV-XVII.txt"
    ]
    
    for filename in chapter_files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f"deep_cleaned_{filename}")
        
        if not os.path.exists(input_path):
            print(f"警告: 找不到文件 {input_path}")
            continue
            
        print(f"\n正在深度清理: {filename}")
        
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 方法1: 使用多种正则表达式模式
        cleaned_content = content

        pattern1 = r'\n\s*\d+\s*\(return\)\s*\[[^\]]*\]\s*\n'
        pattern2 = r'\n\s*\d+\s*\(return\)\s*\[[\s\S]*?\]\s*\n'
        pattern3 = r'\d+\s*\(return\)\s*\[[^\]]*\]'
        pattern4 = r'\n\s*\d+\s*\(return\)\s*\[.*?\]\s*\n'
        
        patterns = [pattern1, pattern2, pattern3, pattern4]
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, cleaned_content, re.DOTALL)
            if matches:
                print(f"  使用模式{i+1}找到 {len(matches)} 个注释")
                cleaned_content = re.sub(pattern, '\n\n', cleaned_content, flags=re.DOTALL)
        

        cleaned_content = remove_notes_comprehensively(cleaned_content)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)
        
        print(f"  已保存: {output_path}")
        
        remaining_notes = check_remaining_notes(cleaned_content)
        if remaining_notes:
            print(f"  警告: 可能仍有 {len(remaining_notes)} 个注释未被完全删除")
            debug_path = os.path.join(output_dir, f"debug_{filename}")
            with open(debug_path, 'w', encoding='utf-8') as debug_file:
                for note in remaining_notes[:5]:  
                    debug_file.write(f"可能未删除的注释:\n{note}\n\n")
            print(f"  调试信息已保存: {debug_path}")
    
    print("\n深度清理完成！")

def remove_notes_comprehensively(content):
    """
    使用多种方法综合清理注释
    """
    lines = content.split('\n')
    cleaned_lines = []
    in_note = False
    note_start_pattern = r'^\s*\d+\s*\(return\)\s*\['

    for line in lines:
        if re.match(note_start_pattern, line):
            in_note = True
            if ']' in line:
                in_note = False
            continue
        
        if in_note and ']' in line:
            in_note = False
            continue
        
        if in_note:
            continue
        
        if re.search(r'\d+\s*\(return\)\s*\[', line) and ']' in line:
            line = re.sub(r'\d+\s*\(return\)\s*\[.*?\]', '', line)
        
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def check_remaining_notes(content):
    """
    检查是否还有注释残留
    """
    patterns = [
        r'\d+\s*\(return\)\s*\[',
        r'^\s*\d+\s*\(return\)\s*\[',
        r'\[\s*\]' 
    ]
    
    remaining = []
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        for pattern in patterns:
            if re.search(pattern, line):
                start = max(0, i-2)
                end = min(len(lines), i+3)
                context = '\n'.join(lines[start:end])
                remaining.append(context)
                break 
    
    return remaining

def analyze_note_patterns(input_dir="extracted_chapters"):
    """
    分析注释模式，帮助我们理解为什么有些注释没被删除
    """
    chapter_files = [
        "chapters_IV-VI.txt",
        "chapters_VI-X.txt", 
        "chapters_XIII-XIV.txt",
        "chapters_XIV-XVII.txt"
    ]
    
    for filename in chapter_files:
        input_path = os.path.join(input_dir, filename)
        
        if not os.path.exists(input_path):
            continue
            
        print(f"\n分析 {filename} 中的注释模式:")
        
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        note_patterns = [
            r'\n\s*(\d+)\s*\(return\)\s*\[[^\]]*\]\s*\n',
            r'\n\s*(\d+)\s*\(return\)\s*\[[\s\S]*?\]\s*\n',
            r'(\d+)\s*\(return\)\s*\[[^\]]*\]',
        ]
        
        for pattern in note_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                print(f"  模式 '{pattern[:30]}...' 找到 {len(matches)} 个匹配")
                if matches:
                    print(f"    示例: {matches[0] if isinstance(matches[0], str) else matches[0][0]}")
        
        unusual_patterns = [
            r'\(\s*return\s*\)', 
            r'\(\s*return\)',    
            r'\(return\s*\)',   
        ]
        
        for pattern in unusual_patterns:
            matches = re.findall(pattern, content)
            if matches:
                print(f"  异常格式 '{pattern}' 找到 {len(matches)} 个匹配")

if __name__ == "__main__":
    analyze_note_patterns()
    deep_clean_notes()