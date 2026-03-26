"""修复报告文件中的 Unicode 转义序列，将其转换为可读的中文字符"""
import re
import os


def decode_unicode_escapes(text):
    """解码文本中的 Unicode 转义序列"""
    
    def replace_escape(match):
        """处理 Unicode 转义"""
        try:
            code = int(match.group(1), 16)
            # 跳过代理字符（surrogate characters）
            if 0xD800 <= code <= 0xDFFF:
                return match.group(0)
            return chr(code)
        except:
            return match.group(0)
    
    # 先处理双反斜杠转义
    result = re.sub(r'\\\\u([0-9a-fA-F]{4})', replace_escape, text)
    # 再处理单反斜杠转义
    result = re.sub(r'\\u([0-9a-fA-F]{4})', replace_escape, result)
    
    return result


def remove_surrogates(text):
    """移除代理字符（surrogate characters）"""
    result = []
    for char in text:
        code = ord(char)
        # 跳过代理字符区域 (0xD800-0xDFFF)
        if 0xD800 <= code <= 0xDFFF:
            continue
        result.append(char)
    return ''.join(result)


def fix_report_file(input_file, output_file=None):
    """修复报告文件编码"""
    if output_file is None:
        output_file = input_file
    
    # 读取原始文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content:
        print(f"[ERROR] 输入文件为空: {input_file}")
        return None
    
    # 统计原始转义序列数量
    escape_count = len(re.findall(r'\\u[0-9a-fA-F]{4}', content))
    print(f"发现 {escape_count} 个 Unicode 转义序列")
    
    if escape_count == 0:
        print(f"[INFO] 没有需要修复的转义序列")
        return input_file
    
    # 解码 Unicode 转义序列
    fixed_content = decode_unicode_escapes(content)
    
    # 移除代理字符
    fixed_content = remove_surrogates(fixed_content)
    
    # 验证修复
    remaining_count = len(re.findall(r'\\u[0-9a-fA-F]{4}', fixed_content))
    print(f"修复后剩余 {remaining_count} 个转义序列")
    
    # 确保内容不为空
    if not fixed_content:
        print(f"[ERROR] 修复后内容为空，放弃写入")
        return None
    
    # 如果输入输出相同，先写入临时文件
    if input_file == output_file:
        temp_file = input_file + '.tmp'
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        # 替换原文件
        os.replace(temp_file, output_file)
    else:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
    
    print(f"[OK] 报告已修复并保存到: {output_file}")
    return output_file


if __name__ == "__main__":
    fix_report_file("report.html")
