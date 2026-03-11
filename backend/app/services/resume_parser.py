import json

from app.core.logging import get_logger
from app.services.llm_client import LLMClient
from app.schemas.resume import ResumeData

logger = get_logger(__name__)

# 系统提示词：指导LLM如何解析简历
SYSTEM_PROMPT = """你是一个专业的简历解析助手。请将用户提供的简历文本解析为结构化的JSON格式。

## 输出要求
1.只输出纯JSON，不要有任何额外的解释或markdown标记
2.严格按照以下结构输出：

{
    "basic_info": {
        "name": "姓名",
        "gender": "性别，如：男/女",
        "age": "年龄或出生日期",
        "phone": "手机号码",
        "email": "电子邮箱",
        "location": "籍贯或现居地",
        "work_years": "工作年限，如：3年、应届",
        "education_level": "最高学历，如：本科、硕士",
        "job_intent": "求职意向/期望职位"
    },
    "education": [
        {
            "school": "学校名称",
            "major": "专业",
            "degree": "学历，如：专科/本科/硕士/博士",
            "period": "起止时间，如：2020.09-2024.06"
        }
    ],
    "work_experience": [
        {
            "company": "公司名称",
            "position": "职位",
            "period": "起止时间",
            "description": "工作内容描述"
        }
    ],
    "projects": [
        {
            "name": "项目名称",
            "role": "担任角色",
            "period": "起止时间",
            "description": "项目描述和个人职责"
        }
    ],
    "skills": ["技能1", "技能2", "技能3"],
     "awards": [
          {
              "name": "奖项名称，如：国家奖学金、优秀毕业生",
              "time": "获奖时间"
          }
      ],
      "certificates": [
          {
              "name": "证书名称，如：CPA、英语六级、PMP",
              "time": "获得时间"
          }
      ],
      "campus_experience": ["校园经历1，如：学生会主席", "社团活动2"],
      "self_evaluation": "自我评价/个人总结的完整内容"
}

 ## 解析规则
  1.如果某个字段在简历中找不到，设为null
  2.如果某个列表（如education）没有内容，设为空数组[]
  3.尽可能提取所有相关信息，不要遗漏
  4.保持原文信息的准确性，不要编造内容
  5.校园职务（如学生会主席、社团负责人、班长）放入campus_experience，不要放入work_experience
  6.奖学金、竞赛获奖、荣誉称号（如优秀毕业生、三好学生）放入awards
  7.资格证书、等级证书（如CPA、英语六级、驾照、PMP）放入certificates
  8.如果简历没有直接写工作年限，根据最早工作经历的起始时间到现在推算，填入work_years
  9.education_level取教育经历中最高的学历
  
 ## 示例
  输入简历片段：
  "张三，男，25岁，手机：13800138000，邮箱：zhangsan@email.com
  本科 | 北京大学 | 计算机科学 | 2018.09-2022.06
  校学生会主席（2020-2021）
  获国家奖学金（2021）、优秀毕业生（2022）
  持有英语六级证书（2020）、PMP认证（2023）
  2022.07至今 XX科技有限公司 Java开发工程师"

  期望输出：
  {
      "basic_info": {
          "name": "张三",
          "gender": "男",
          "age": "25岁",
          "phone": "13800138000",
          "email": "zhangsan@email.com",
          "location": null,
          "work_years": "3年",
          "education_level": "本科",
          "job_intent": null
      },
      "education": [{"school": "北京大学", "major": "计算机科学", "degree": "本科", "period": "2018.09-2022.06"}],
      "work_experience": [{"company": "XX科技有限公司", "position": "Java开发工程师", "period": "2022.07-至今",
  "description": null}],
      "projects": [],
      "skills": [],
      "awards": [{"name": "国家奖学金", "time": "2021"}, {"name": "优秀毕业生", "time": "2022"}],
      "certificates": [{"name": "英语六级", "time": "2020"}, {"name": "PMP认证", "time": "2023"}],
      "campus_experience": ["校学生会主席（2020-2021）"],
      "self_evaluation": null
  }"""

async def parse_resume(resume_text: str) -> ResumeData:
    """使用大模型解析简历文本，返回结构化数据

    Args:
        resume_text: 简历原始文本

    Returns:
        ResumeData: 结构化的简历数据

    Raises:
        ValueError: JSON解析失败
        RuntimeError: LLM调用失败
    """
    logger.info("开始解析简历，文本长度：%d", len(resume_text))

    # 1.创建LLM客户端
    client = LLMClient()

    try:
        # 2.调用大模型
        response = await client.chat(
            prompt=f"请解析以下简历：\n\n{resume_text}",
            system_prompt=SYSTEM_PROMPT
        )
        logger.info("LLM返回内容长度：%d", len(response))

        #3. 清理响应，去除可能得markdown代码块标记
        cleaned_response = response.strip()
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()

        # 4. 解析JSON
        try:
            data = json.loads(cleaned_response)
        except json.JSONDecodeError as exc:
            logger.error("JSON解析失败：%s", exc)
            logger.error("原始响应：%s",response[:500])
            raise ValueError(f"LLM返回的不是有效的JSON：{exc}")

        # 5. 转换为Pydantic模型（自动校验）
        resume_data = ResumeData(**data)
        logger.info("简历解析成功，姓名：%s",resume_data.basic_info.name)

        return resume_data

    finally:
        # 6.关闭客户端
        await client.close()
