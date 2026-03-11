import asyncio
import json
import os
from pathlib import Path
from datetime import datetime

# 把backend目录加入模块搜索路径，保证能import app包
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.chdir(Path(__file__).resolve().parent.parent)

from app.services.file_parser import parse_file
from app.services.resume_parser import parse_resume

# 配置
RESUME_DIR = r"D:\hr-ai-assistant\简历数据"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "test_results"

def scan_resumes(directory: str) -> list[Path]:
    """扫描目录下所有PDF和Word文件，返回文件路径列表"""
    supported = {".pdf",".docx",".doc"}
    resume_dir = Path(directory)

    if not resume_dir.exists():
        print(f"错误：目录不存在 -> {directory}")
        return []

    files = [f for f in resume_dir.iterdir() if f.suffix.lower() in supported]
    print(f"找到{len(files)}份简历文件")
    return sorted(files)

def analyze_coverage(data: dict) -> dict:
    """分析简历解析结果的文段覆盖率，遍历所有字段，统计哪些有值，哪些为空，计算覆盖率百分比"""
    filled = []
    empty = []

    # 检查basic_info中的每个字段
    basic = data.get("basic_info", {})
    for key, value in basic.items():
        field_name = f"basic_info.{key}"
        if value:
            filled.append(field_name)
        else:
            empty.append(field_name)

    # 检查列表类型的字段
    list_fields = [
        "education", "work_experience", "projects",
        "skills", "awards", "certificates", "campus_experience"
    ]
    for field in list_fields:
        items = data.get(field, [])
        if items:
            filled.append(f"{field}({len(items)}条)")
        else:
            empty.append(field)

    # 检查self_evaluation
    if data.get("self_evaluation"):
        filled.append("self_evaluation")
    else:
        empty.append("self_evaluation")

    total = len(filled) + len(empty)
    rate = round(len(filled) / total * 100, 1) if total > 0 else 0

    return {
        "coverage_rate": f"{rate}%",
        "filled_count": len(filled),
        "empty_count": len(empty),
        "filled_fields": filled,
        "empty_fields": empty,
        }

async def process_one(file_path: Path) -> dict:
    """处理单份简历，返回包含文件名、解析状态、覆盖率、原始数据的字典"""
    filename = file_path.name
    print(f"\n{'='*50}")
    print(f"正在处理：{filename}")

    result = {
        "filename": filename,
        "success": False,
        "error": None,
        "coverage": None,
        "data": None,
    }

    try:
        # 第一步：提取文字
        suffix = file_path.suffix.lower().lstrip(".")
        extract = parse_file(str(file_path), suffix)
        text = extract["text"]

        if len(text.strip()) < 50:
            result["error"] = "提取文本过短，可能是扫描件或空文件"
            print(f"跳过：{result['error']}")
            return result

        # 第2步：AI解析
        resume_data = await parse_resume(text)
        data_dict = resume_data.model_dump()

        # 第3步：统计覆盖率
        coverage = analyze_coverage(data_dict)

        result["success"] = True
        result["coverage"] = coverage
        result["data"] = data_dict
        print(f"解析成功！覆盖率：{coverage['coverage_rate']}")
        print(f"已填充：{coverage['filled_fields']}")
        print(f"为空的：{coverage['empty_fields']}")

    except Exception as e:
        result["error"] = str(e)
        print(f"解析失败：{e}")

    return result

async def main():
    """主函数：扫描简历-逐个解析-汇总统计-保存结果"""
    print("=" * 50)
    print("简历批量解析测试")
    print("=" * 50)

    # 1.扫描简历文件
    files = scan_resumes(RESUME_DIR)
    if not files:
        print("没有找到简历文件，退出")
        return

    # 2.准备输出文件
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"batch_result_{timestamp}.json"

    # 3.逐个处理
    results = []
    for i, f in enumerate(files, 1):
        print(f"\n[{i}/{len(files)}]", end="")
        result = await process_one(f)
        results.append(result)

        # 每完成一份就保存，覆盖同一个文件
        with open(output_file, "w", encoding="utf-8") as out:
            json.dump(results, out, ensure_ascii=False, indent=2)

    # 4.汇总统计
    total = len(results)
    success = sum(1 for r in results if r["success"])
    failed = total - success

    print(f"\n{'='*50}")
    print(f"批量测试完成！")
    print(f"总计：{total}份")
    print(f"成功：{success}份")
    print(f"失败：{failed}份")
    print(f"成功率：{round(success / total * 100, 1)}%")
    print(f"\n结果已保存到：{output_file}")

if __name__ == "__main__":
    asyncio.run(main())