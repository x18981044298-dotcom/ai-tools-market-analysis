# -*- coding: utf-8 -*-
"""
数据处理模块 - AI工具市场多维度分析
"""

import pandas as pd
import numpy as np

class AIToolsDataProcessor:
    """AI工具数据处理器"""
    
    def __init__(self):
        self.df = self._load_data()
        self._add_analysis_dimensions()
    
    def _load_data(self):
        """加载原始数据"""
        # 第1页精确数据 (排名 1-100)
        page1_data = [
            (1, "Creativity", 8787, "创意"),
            (2, "Business", 6508, "商业"),
            (3, "Personal", 5418, "个人"),
            (4, "Images", 2726, "图像"),
            (5, "Marketing", 2169, "营销"),
            (6, "Text", 1934, "文本"),
            (7, "Software", 1634, "软件"),
            (8, "Relationship", 1259, "关系/情感"),
            (9, "Productivity", 1190, "生产力"),
            (10, "Writing", 1151, "写作"),
            (11, "Education", 1024, "教育"),
            (12, "Health", 919, "健康"),
            (13, "Coding", 885, "编程"),
            (14, "Social media", 878, "社交媒体"),
            (15, "Video", 840, "视频"),
            (16, "Chatting", 774, "聊天"),
            (17, "Sales", 702, "销售"),
            (18, "Learning", 673, "学习"),
            (19, "Career", 643, "职业"),
            (20, "AI", 514, "人工智能"),
            (21, "Stories", 503, "故事"),
            (22, "Content", 496, "内容"),
            (23, "Job search", 495, "求职"),
            (24, "Art", 484, "艺术"),
            (25, "Music", 423, "音乐"),
            (26, "School", 400, "学校"),
            (27, "Nutrition", 381, "营养"),
            (28, "Finance", 372, "金融"),
            (29, "SEO", 372, "搜索引擎优化"),
            (30, "Language learning", 349, "语言学习"),
            (31, "Spirituality", 335, "心灵/精神"),
            (32, "Fashion", 303, "时尚"),
            (33, "Website", 292, "网站"),
            (34, "Customer experience", 291, "客户体验"),
            (35, "Startup", 290, "创业"),
            (36, "Mental health", 286, "心理健康"),
            (37, "Customer support", 284, "客户支持"),
            (38, "Image editing", 278, "图像编辑"),
            (39, "School subject", 273, "学科"),
            (40, "Management", 270, "管理"),
            (41, "Games", 258, "游戏"),
            (42, "Design", 245, "设计"),
            (43, "Travel", 233, "旅行"),
            (44, "Prompts", 231, "提示词"),
            (45, "Data analysis", 230, "数据分析"),
            (46, "HR", 226, "人力资源"),
            (47, "Branding", 224, "品牌"),
            (48, "Summaries", 221, "摘要"),
            (49, "Avatars", 219, "头像"),
            (50, "Legal", 217, "法律"),
            (51, "Virtual companion", 214, "虚拟伴侣"),
            (52, "Teaching", 202, "教学"),
            (53, "Wealth", 201, "财富"),
            (54, "Brainstorming", 199, "头脑风暴"),
            (55, "Knowledge", 196, "知识"),
            (56, "SEO content", 195, "SEO内容"),
            (57, "Illustration", 195, "插画"),
            (58, "Research", 194, "研究"),
            (59, "Studying", 194, "学习/备考"),
            (60, "Business strategy", 188, "商业战略"),
            (61, "Transcription", 187, "转录"),
            (62, "Recruiting", 181, "招聘"),
            (63, "Resume", 181, "简历"),
            (64, "Job interview", 175, "工作面试"),
            (65, "Books", 175, "书籍"),
            (66, "Chatbot", 172, "聊天机器人"),
            (67, "Logo", 170, "标志"),
            (68, "Academic research", 166, "学术研究"),
            (69, "Documents", 166, "文档"),
            (70, "Shopping", 159, "购物"),
            (71, "Translation", 159, "翻译"),
            (72, "Market research", 153, "市场研究"),
            (73, "Divination", 153, "占卜"),
            (74, "Recipes", 152, "食谱"),
            (75, "Email", 151, "邮件"),
            (76, "Interior design", 149, "室内设计"),
            (77, "Fitness", 146, "健身"),
            (78, "ChatGPT", 146, "ChatGPT相关"),
            (79, "Apps", 146, "应用"),
            (80, "E-commerce", 141, "电商"),
            (81, "Anime", 138, "动漫"),
            (82, "Financial advice", 137, "财务建议"),
            (83, "Ads", 137, "广告"),
            (84, "Wallpaper", 133, "壁纸"),
            (85, "Dating", 131, "约会"),
            (86, "Anime image", 129, "动漫图像"),
            (87, "Interview preparation", 127, "面试准备"),
            (88, "Movies", 124, "电影"),
            (89, "Stocks", 123, "股票"),
            (90, "Information retrieval", 120, "信息检索"),
            (91, "Meetings", 119, "会议"),
            (92, "Short stories", 119, "短篇故事"),
            (93, "Cartoon image", 119, "卡通图像"),
            (94, "Startup advice", 115, "创业建议"),
            (95, "Legal advice", 114, "法律建议"),
            (96, "Product management", 114, "产品管理"),
            (97, "Names", 110, "名字/命名"),
            (98, "LinkedIn", 109, "LinkedIn相关"),
            (99, "Personal development", 109, "个人发展"),
            (100, "Portraits", 106, "肖像"),
        ]
        
        # 第2页数据 (排名 101-150)
        page2_data = [
            (101, "Emotional support", 104, "情感支持"),
            (102, "Document chat", 101, "文档聊天"),
            (103, "Coloring pages", 101, "着色页"),
            (104, "Presentations", 101, "演示文稿"),
            (105, "Social media assistant", 100, "社交媒体助手"),
            (106, "YouTube", 98, "YouTube相关"),
            (107, "Twitter", 95, "Twitter相关"),
            (108, "Audio", 94, "音频"),
            (109, "Voice", 93, "语音"),
            (110, "Note taking", 92, "笔记"),
            (111, "Landing pages", 90, "落地页"),
            (112, "Product descriptions", 89, "产品描述"),
            (113, "Spreadsheets", 88, "电子表格"),
            (114, "Copywriting", 87, "文案写作"),
            (115, "Podcast", 86, "播客"),
            (116, "Photo editing", 85, "照片编辑"),
            (117, "Customer service", 84, "客户服务"),
            (118, "Video editing", 83, "视频编辑"),
            (119, "Automation", 82, "自动化"),
            (120, "Crypto", 81, "加密货币"),
            (121, "Real estate", 80, "房地产"),
            (122, "NFT", 79, "NFT"),
            (123, "3D", 78, "3D建模"),
            (124, "eBooks", 77, "电子书"),
            (125, "Browser extension", 76, "浏览器扩展"),
            (126, "Search", 75, "搜索"),
            (127, "Paraphrasing", 74, "改写"),
            (128, "SQL", 73, "SQL数据库"),
            (129, "Speech", 72, "语音合成"),
            (130, "Meditation", 71, "冥想"),
            (131, "Therapy", 70, "治疗"),
            (132, "Memory", 69, "记忆"),
            (133, "Religion", 68, "宗教"),
            (134, "Dream", 67, "梦境"),
            (135, "Horoscope", 66, "星座"),
            (136, "Tarot", 65, "塔罗牌"),
            (137, "Skincare", 64, "护肤"),
            (138, "Makeup", 63, "化妆"),
            (139, "Hairstyle", 62, "发型"),
            (140, "Outfit", 61, "穿搭"),
            (141, "Gift", 60, "礼物"),
            (142, "Birthday", 59, "生日"),
            (143, "Wedding", 58, "婚礼"),
            (144, "Baby names", 57, "宝宝起名"),
            (145, "Pet", 56, "宠物"),
            (146, "Cooking", 55, "烹饪"),
            (147, "Meal planning", 54, "餐食计划"),
            (148, "Wine", 53, "葡萄酒"),
            (149, "Coffee", 52, "咖啡"),
            (150, "Cocktails", 51, "鸡尾酒"),
        ]
        
        all_data = page1_data + page2_data
        df = pd.DataFrame(all_data, columns=['rank', 'category', 'tools_count', 'chinese_name'])
        return df
    
    def _add_analysis_dimensions(self):
        """添加多维度分析标签"""
        
        # 1. 用户场景分类（生活/工作/学习/娱乐）
        user_scenario_mapping = {
            # 工作场景
            'Business': '工作', 'Marketing': '工作', 'Sales': '工作', 'Coding': '工作',
            'Software': '工作', 'Data analysis': '工作', 'HR': '工作', 'Management': '工作',
            'Recruiting': '工作', 'Product management': '工作', 'Customer support': '工作',
            'Customer experience': '工作', 'Customer service': '工作', 'Legal': '工作',
            'Legal advice': '工作', 'Finance': '工作', 'Financial advice': '工作',
            'Accounting': '工作', 'Market research': '工作', 'Business strategy': '工作',
            'Startup': '工作', 'Startup advice': '工作', 'E-commerce': '工作',
            'SEO': '工作', 'SEO content': '工作', 'Ads': '工作', 'Branding': '工作',
            'Email': '工作', 'Meetings': '工作', 'Presentations': '工作',
            'Documents': '工作', 'Spreadsheets': '工作', 'Automation': '工作',
            'Landing pages': '工作', 'Product descriptions': '工作', 'Copywriting': '工作',
            'Real estate': '工作', 'SQL': '工作', 'Website': '工作', 'Apps': '工作',
            
            # 学习场景
            'Education': '学习', 'Learning': '学习', 'School': '学习', 'School subject': '学习',
            'Language learning': '学习', 'Studying': '学习', 'Teaching': '学习',
            'Academic research': '学习', 'Research': '学习', 'Knowledge': '学习',
            'Books': '学习', 'eBooks': '学习',
            
            # 生活场景
            'Personal': '生活', 'Health': '生活', 'Mental health': '生活', 'Nutrition': '生活',
            'Fitness': '生活', 'Recipes': '生活', 'Cooking': '生活', 'Meal planning': '生活',
            'Fashion': '生活', 'Skincare': '生活', 'Makeup': '生活', 'Hairstyle': '生活',
            'Outfit': '生活', 'Shopping': '生活', 'Travel': '生活', 'Interior design': '生活',
            'Gift': '生活', 'Birthday': '生活', 'Wedding': '生活', 'Baby names': '生活',
            'Pet': '生活', 'Wine': '生活', 'Coffee': '生活', 'Cocktails': '生活',
            'Meditation': '生活', 'Therapy': '生活',
            
            # 职业发展
            'Career': '职业发展', 'Job search': '职业发展', 'Resume': '职业发展',
            'Job interview': '职业发展', 'Interview preparation': '职业发展',
            'LinkedIn': '职业发展', 'Personal development': '职业发展',
            
            # 创作场景
            'Creativity': '创作', 'Writing': '创作', 'Text': '创作', 'Content': '创作',
            'Stories': '创作', 'Short stories': '创作', 'Art': '创作', 'Music': '创作',
            'Images': '创作', 'Image editing': '创作', 'Design': '创作', 'Logo': '创作',
            'Illustration': '创作', 'Video': '创作', 'Video editing': '创作',
            'Audio': '创作', 'Voice': '创作', 'Podcast': '创作', 'Photo editing': '创作',
            'Avatars': '创作', 'Anime': '创作', 'Anime image': '创作', 'Cartoon image': '创作',
            'Portraits': '创作', 'Wallpaper': '创作', '3D': '创作', 'Coloring pages': '创作',
            
            # 社交/关系
            'Relationship': '社交关系', 'Dating': '社交关系', 'Emotional support': '社交关系',
            'Virtual companion': '社交关系', 'Social media': '社交关系',
            'Social media assistant': '社交关系', 'YouTube': '社交关系', 'Twitter': '社交关系',
            'Chatting': '社交关系', 'Chatbot': '社交关系',
            
            # 娱乐场景
            'Games': '娱乐', 'Movies': '娱乐', 'Divination': '娱乐', 'Horoscope': '娱乐',
            'Tarot': '娱乐', 'Dream': '娱乐', 'Spirituality': '娱乐', 'Religion': '娱乐',
            
            # 工具/效率
            'Productivity': '效率工具', 'Summaries': '效率工具', 'Transcription': '效率工具',
            'Translation': '效率工具', 'Note taking': '效率工具', 'Search': '效率工具',
            'Information retrieval': '效率工具', 'Document chat': '效率工具',
            'Paraphrasing': '效率工具', 'Brainstorming': '效率工具', 'Prompts': '效率工具',
            'Memory': '效率工具', 'Browser extension': '效率工具', 'Speech': '效率工具',
            
            # AI/技术
            'AI': '技术', 'ChatGPT': '技术', 'NFT': '技术', 'Crypto': '技术',
            'Wealth': '金融投资', 'Stocks': '金融投资', 'Names': '其他',
        }
        self.df['user_scenario'] = self.df['category'].map(user_scenario_mapping).fillna('其他')
        
        # 2. 用户意图分类
        intent_mapping = {
            # 内容生产型
            'Creativity': '内容生产', 'Writing': '内容生产', 'Text': '内容生产',
            'Images': '内容生产', 'Video': '内容生产', 'Audio': '内容生产',
            'Music': '内容生产', 'Art': '内容生产', 'Design': '内容生产',
            'Content': '内容生产', 'Stories': '内容生产', 'Illustration': '内容生产',
            'Logo': '内容生产', 'Avatars': '内容生产', 'Anime': '内容生产',
            'Copywriting': '内容生产', 'SEO content': '内容生产', '3D': '内容生产',
            'Podcast': '内容生产', 'Presentations': '内容生产',
            
            # 决策支持型
            'Finance': '决策支持', 'Legal': '决策支持', 'Legal advice': '决策支持',
            'Financial advice': '决策支持', 'Market research': '决策支持',
            'Business strategy': '决策支持', 'Data analysis': '决策支持',
            'Startup advice': '决策支持', 'Stocks': '决策支持', 'Research': '决策支持',
            'Academic research': '决策支持', 'Product management': '决策支持',
            
            # 效率提升型
            'Productivity': '效率提升', 'Automation': '效率提升', 'Summaries': '效率提升',
            'Transcription': '效率提升', 'Translation': '效率提升', 'Email': '效率提升',
            'Documents': '效率提升', 'Spreadsheets': '效率提升', 'Note taking': '效率提升',
            'Search': '效率提升', 'Paraphrasing': '效率提升', 'Document chat': '效率提升',
            
            # 关系陪伴型
            'Relationship': '关系陪伴', 'Emotional support': '关系陪伴',
            'Virtual companion': '关系陪伴', 'Dating': '关系陪伴', 'Chatting': '关系陪伴',
            'Chatbot': '关系陪伴', 'Therapy': '关系陪伴', 'Mental health': '关系陪伴',
            
            # 技能学习型
            'Education': '技能学习', 'Learning': '技能学习', 'Language learning': '技能学习',
            'Studying': '技能学习', 'School': '技能学习', 'Teaching': '技能学习',
            'Knowledge': '技能学习', 'Interview preparation': '技能学习',
            
            # 工具开发型
            'Coding': '工具开发', 'Software': '工具开发', 'Website': '工具开发',
            'Apps': '工具开发', 'SQL': '工具开发', 'AI': '工具开发',
            'ChatGPT': '工具开发', 'Browser extension': '工具开发',
            
            # 营销获客型
            'Marketing': '营销获客', 'SEO': '营销获客', 'Ads': '营销获客',
            'Sales': '营销获客', 'E-commerce': '营销获客', 'Branding': '营销获客',
            'Landing pages': '营销获客', 'Social media': '营销获客',
            
            # 生活服务型
            'Health': '生活服务', 'Nutrition': '生活服务', 'Fitness': '生活服务',
            'Recipes': '生活服务', 'Fashion': '生活服务', 'Travel': '生活服务',
            'Shopping': '生活服务', 'Interior design': '生活服务',
        }
        self.df['user_intent'] = self.df['category'].map(intent_mapping).fillna('其他')
        
        # 3. 商业化模式
        biz_model_mapping = {
            # B2B SaaS（高付费意愿）
            'Data analysis': 'B2B SaaS', 'Legal': 'B2B SaaS', 'Legal advice': 'B2B SaaS',
            'HR': 'B2B SaaS', 'Recruiting': 'B2B SaaS', 'Product management': 'B2B SaaS',
            'Customer support': 'B2B SaaS', 'Customer service': 'B2B SaaS',
            'Market research': 'B2B SaaS', 'Sales': 'B2B SaaS', 'CRM': 'B2B SaaS',
            'Automation': 'B2B SaaS', 'Spreadsheets': 'B2B SaaS', 'Documents': 'B2B SaaS',
            'Finance': 'B2B SaaS', 'E-commerce': 'B2B SaaS',
            
            # B2B 订阅
            'SEO': 'B2B 订阅', 'Marketing': 'B2B 订阅', 'Ads': 'B2B 订阅',
            'Content': 'B2B 订阅', 'SEO content': 'B2B 订阅', 'Copywriting': 'B2B 订阅',
            'Email': 'B2B 订阅', 'Social media': 'B2B 订阅', 'Branding': 'B2B 订阅',
            
            # B2C 订阅
            'Productivity': 'B2C 订阅', 'Writing': 'B2C 订阅', 'Summaries': 'B2C 订阅',
            'Translation': 'B2C 订阅', 'Learning': 'B2C 订阅', 'Education': 'B2C 订阅',
            'Language learning': 'B2C 订阅', 'Studying': 'B2C 订阅',
            
            # 一次性付费/模板
            'Design': '一次性/模板', 'Logo': '一次性/模板', 'Avatars': '一次性/模板',
            'Wallpaper': '一次性/模板', 'Interior design': '一次性/模板',
            'Resume': '一次性/模板', 'Presentations': '一次性/模板',
            
            # 免费/流量型
            'Creativity': '免费/流量', 'Images': '免费/流量', 'Anime': '免费/流量',
            'Horoscope': '免费/流量', 'Dream': '免费/流量', 'Tarot': '免费/流量',
            'Coloring pages': '免费/流量', 'Games': '免费/流量', 'Memes': '免费/流量',
            'Divination': '免费/流量',
            
            # 陪伴/订阅
            'Virtual companion': '陪伴订阅', 'Relationship': '陪伴订阅',
            'Emotional support': '陪伴订阅', 'Chatbot': '陪伴订阅',
            'Dating': '陪伴订阅', 'Therapy': '陪伴订阅',
        }
        self.df['biz_model'] = self.df['category'].map(biz_model_mapping).fillna('混合模式')
        
        # 4. 目标用户类型 (基于分类特征客观判断)
        target_user_mapping = {
            'Legal': 'B2B企业', 'Legal advice': 'B2B企业', 'Finance': 'B2B企业', 
            'Financial advice': 'B2B/B2C', 'Data analysis': 'B2B企业', 
            'Market research': 'B2B企业', 'HR': 'B2B企业', 'Recruiting': 'B2B企业',
            'Product management': 'B2B企业', 'Business strategy': 'B2B企业', 
            'Sales': 'B2B企业', 'Customer support': 'B2B企业', 'Customer service': 'B2B企业',
            'Automation': 'B2B企业', 'E-commerce': 'B2B/B2C', 'Real estate': 'B2B/B2C',
            'SEO': 'B2B/B2C', 'Marketing': 'B2B/B2C', 'Ads': 'B2B/B2C',
            'Education': 'B2C个人', 'Learning': 'B2C个人', 'Language learning': 'B2C个人',
            'Productivity': 'B2B/B2C', 'Writing': 'B2C个人', 'Coding': 'B2B/B2C',
            'Design': 'B2C个人', 'Video': 'B2C个人', 'Audio': 'B2C个人', 'Music': 'B2C个人',
            'Personal': 'B2C个人', 'Health': 'B2C个人', 'Fitness': 'B2C个人',
            'Creativity': 'B2C个人', 'Images': 'B2C个人', 'Games': 'B2C个人',
            'Relationship': 'B2C个人', 'Dating': 'B2C个人',
        }
        self.df['target_user'] = self.df['category'].map(target_user_mapping).fillna('B2C个人')
        
        # 5. 竞争强度 (基于工具数量的客观指标)
        # 使用百分位数排名，0-100，数值越高竞争越激烈
        self.df['competition_rank'] = self.df['tools_count'].rank(pct=True) * 100
        
        # 6. 赛道饱和度
        max_tools = self.df['tools_count'].max()
        self.df['saturation_index'] = self.df['tools_count'] / max_tools * 100
        
        # 7. 市场层级
        def get_tier(count):
            if count >= 1000: return 'Tier 1 头部'
            elif count >= 500: return 'Tier 2 腰部上'
            elif count >= 200: return 'Tier 3 腰部'
            elif count >= 100: return 'Tier 4 腰部下'
            else: return 'Tier 5 尾部'
        self.df['market_tier'] = self.df['tools_count'].apply(get_tier)
        
        # 8. 颗粒度分类
        granularity_mapping = {
            'Creativity': '超宽泛', 'Business': '超宽泛', 'Personal': '超宽泛',
            'Marketing': '宽泛', 'Software': '宽泛', 'Education': '宽泛',
            'Health': '宽泛', 'Finance': '宽泛',
            'SEO': '中等', 'Coding': '中等', 'Design': '中等', 'Sales': '中等',
            'Data analysis': '精准', 'Legal': '精准', 'HR': '精准',
            'Market research': '精准', 'Product management': '精准',
            'Wine': '极精准', 'Coffee': '极精准', 'Cocktails': '极精准',
            'Tarot': '极精准', 'Wedding': '极精准', 'Birthday': '极精准',
            'Baby names': '极精准', 'Horoscope': '极精准',
        }
        self.df['granularity'] = self.df['category'].map(granularity_mapping).fillna('中等')
        
        # 9. 大模型推动标签
        llm_driven = ['Document chat', 'Chatbot', 'ChatGPT', 'Virtual companion',
                      'Presentations', 'Spreadsheets', 'Research', 'Academic research',
                      'Summaries', 'Paraphrasing', 'Translation', 'Coding', 'SQL']
        self.df['llm_driven'] = self.df['category'].isin(llm_driven)
        
        # 10. 现实痛点驱动标签
        pain_driven = ['Job interview', 'Interview preparation', 'Mental health',
                       'Emotional support', 'Productivity', 'Therapy', 'Job search',
                       'Resume', 'Health', 'Fitness']
        self.df['pain_driven'] = self.df['category'].isin(pain_driven)
        
        # 11. 市场份额
        self.df['market_share'] = self.df['tools_count'] / self.df['tools_count'].sum() * 100
        self.df['cumulative_share'] = self.df['market_share'].cumsum()
        
        # 12. 用户角色
        persona_mapping = {
            # 工作角色
            'Product management': '产品经理', 'HR': '人力资源', 'Recruiting': '招聘专员',
            'Data analysis': '数据分析师', 'Coding': '开发者', 'Software': '开发者',
            'Management': '管理者', 'Sales': '销售', 'Marketing': '营销人员',
            'Design': '设计师', 'Legal': '法务', 'Finance': '财务',
            'Teaching': '教师', 'Research': '研究员', 'Customer service': '客服',
            
            # 兴趣角色
            'Fashion': '时尚爱好者', 'Cooking': '美食爱好者', 'Wine': '品酒师',
            'Pet': '宠物主人', 'Travel': '旅行者', 'Games': '游戏玩家',
            'Music': '音乐爱好者', 'Art': '艺术爱好者', 'Fitness': '健身达人',
            
            # 情绪角色
            'Relationship': '情感需求者', 'Emotional support': '情感需求者',
            'Therapy': '心理咨询', 'Mental health': '心理健康关注者',
            'Spirituality': '精神追求者', 'Meditation': '冥想者',
            
            # 学习角色
            'Learning': '学习者', 'Education': '学生', 'Language learning': '语言学习者',
            'Studying': '备考生', 'Job search': '求职者', 'Career': '职场人',
        }
        self.df['persona'] = self.df['category'].map(persona_mapping).fillna('通用用户')
        
        # 13. 超级领域合并
        super_domain_mapping = {
            # 文本超级领域
            'Writing': '文本超级领域', 'Text': '文本超级领域', 'Summaries': '文本超级领域',
            'SEO content': '文本超级领域', 'Paraphrasing': '文本超级领域',
            'Copywriting': '文本超级领域', 'Content': '文本超级领域',
            'Stories': '文本超级领域', 'Short stories': '文本超级领域',
            
            # 图像超级领域
            'Images': '图像超级领域', 'Image editing': '图像超级领域',
            'Anime image': '图像超级领域', 'Cartoon image': '图像超级领域',
            'Photo editing': '图像超级领域', 'Portraits': '图像超级领域',
            'Avatars': '图像超级领域', 'Wallpaper': '图像超级领域',
            'Art': '图像超级领域', 'Design': '图像超级领域',
            'Illustration': '图像超级领域', 'Logo': '图像超级领域',
            
            # 音视频超级领域
            'Video': '音视频超级领域', 'Video editing': '音视频超级领域',
            'Audio': '音视频超级领域', 'Voice': '音视频超级领域',
            'Music': '音视频超级领域', 'Podcast': '音视频超级领域',
            'Speech': '音视频超级领域', 'Transcription': '音视频超级领域',
            
            # 教育超级领域
            'Education': '教育超级领域', 'Learning': '教育超级领域',
            'School': '教育超级领域', 'School subject': '教育超级领域',
            'Language learning': '教育超级领域', 'Studying': '教育超级领域',
            'Teaching': '教育超级领域', 'Academic research': '教育超级领域',
            
            # 商业超级领域
            'Business': '商业超级领域', 'Marketing': '商业超级领域',
            'Sales': '商业超级领域', 'SEO': '商业超级领域', 'Ads': '商业超级领域',
            'E-commerce': '商业超级领域', 'Branding': '商业超级领域',
            'Business strategy': '商业超级领域', 'Startup': '商业超级领域',
            
            # 健康超级领域
            'Health': '健康超级领域', 'Mental health': '健康超级领域',
            'Nutrition': '健康超级领域', 'Fitness': '健康超级领域',
            'Therapy': '健康超级领域', 'Meditation': '健康超级领域',
        }
        self.df['super_domain'] = self.df['category'].map(super_domain_mapping).fillna('独立领域')
        
        # 14. 竞争格局象限（基于工具数量的客观分类）
        def get_competition_quadrant(row):
            # 基于工具数量划分竞争程度
            if row['tools_count'] >= 500:
                return '红海赛道 (工具数≥500)'
            elif row['tools_count'] >= 200:
                return '竞争赛道 (200≤工具数<500)'
            elif row['tools_count'] >= 100:
                return '机会赛道 (100≤工具数<200)'
            else:
                return '蓝海赛道 (工具数<100)'
        self.df['competition_quadrant'] = self.df.apply(get_competition_quadrant, axis=1)
    
    def get_data(self):
        """获取处理后的数据"""
        return self.df
    
    def get_market_structure_stats(self):
        """获取市场结构统计"""
        df = self.df
        total_tools = df['tools_count'].sum()
        
        # 头部占比
        top10_share = df.head(10)['tools_count'].sum() / total_tools * 100
        top20_share = df.head(20)['tools_count'].sum() / total_tools * 100
        
        # 层级分布
        tier_dist = df.groupby('market_tier')['tools_count'].agg(['count', 'sum'])
        
        return {
            'total_tools': total_tools,
            'total_categories': len(df),
            'top10_share': top10_share,
            'top20_share': top20_share,
            'tier_distribution': tier_dist,
            'max_tools': df['tools_count'].max(),
            'min_tools': df['tools_count'].min(),
            'median_tools': df['tools_count'].median(),
        }
    
    def get_blue_ocean_opportunities(self, top_n=20):
        """获取蓝海机会赛道 (工具数量最少的分类)"""
        df = self.df.copy()
        df_sorted = df.sort_values('tools_count', ascending=True)
        return df_sorted.head(top_n)
    
    def get_red_ocean_warnings(self, top_n=20):
        """获取红海警示赛道 (工具数量最多的分类)"""
        df = self.df.copy()
        df_sorted = df.sort_values('tools_count', ascending=False)
        return df_sorted.head(top_n)

