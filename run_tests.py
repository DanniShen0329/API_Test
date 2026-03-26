"""直接运行测试并生成报告的脚本"""
import subprocess
import sys
import os


def run_tests():
    """运行测试并生成报告"""
    print("=" * 60)
    print("开始执行价格组API测试")
    print("=" * 60)
    
    # 确保在项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # 设置Python路径
    env = os.environ.copy()
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"{project_root};{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = project_root
    
    # 执行测试并生成报告
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/api/test_price_group_api.py",
        "-v",
        "--html=report.html",
        "--self-contained-html",
        "--tb=short"
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    print("-" * 60)
    
    result = subprocess.run(
        cmd,
        env=env,
        capture_output=False,
        text=True
    )
    
    print("-" * 60)
    
    # 修复报告编码
    if os.path.exists("report.html"):
        print("正在修复报告编码...")
        try:
            subprocess.run(
                [sys.executable, "fix_report_encoding.py"],
                check=True,
                capture_output=True
            )
            print("报告编码修复完成")
        except Exception as e:
            print(f"报告编码修复失败: {e}")
    
    print("=" * 60)
    if result.returncode == 0:
        print("✅ 测试执行成功！")
    else:
        print(f"⚠️ 测试执行完成，返回码: {result.returncode}")
    print(f"报告位置: {os.path.join(project_root, 'report.html')}")
    print("=" * 60)
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())
