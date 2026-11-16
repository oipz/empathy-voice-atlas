from pathlib import Path
import json, csv, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT if Path(__file__).resolve().parent.name=='tools' else ROOT/'outputs/empathy-voice-atlas'
DIST=OUT/'dist'; DIST.mkdir(parents=True,exist_ok=True)
DATA=OUT/'docs' if Path(__file__).resolve().parent.name=='tools' else ROOT/'outputs/共情语音测试集设计'; DATA.mkdir(parents=True,exist_ok=True)
records=[]
def add(name,lang,group,scale,material,evaluation,fit,limit,url,example,access='官方提供入口；使用前核对具体数据许可',priority=False):
    records.append(dict(name=name,language=lang,group=group,scale=scale,material=material,evaluation=evaluation,fit=fit,limitation=limit,source=url,example=example,access=access,priority=priority))

add('HumDial-EIBench','中文 / 英文','共情语音','1,077题；中文528题，其中生成任务144题','真人录制的多轮音频、转写、情感和任务标注；通常3–5轮','Task 3 分开评文本共情、声音共情与一致性、音质和自然度','最值得先看中文Task 3；评分拆分非常贴合你的目标','其他任务偏声音理解；现成题不一定语义充分，需逐题筛选。144是中文生成题数，不是全部中文音频数','https://huggingface.co/datasets/ASLP-lab/HumDial-EIBench','用户连续几轮解释失落原因，系统生成一段理解其处境的语音回复。','HF公开；按官方文件与代码使用，未在本次批量下载',True)
add('EChat-200K / EChat-eval','中文 / 英文','共情语音','约20万训练对话；评测另设，论文报告各任务280例','输入语音、文字、情感等副语言标签，以及回复文本和语音；真实与合成输入混合','理解副语言信息并生成适当的共情语音回复','可参考端到端输入输出格式、合成流程和评分','20万是训练规模，不能当测试题数；年龄、性别适配不应代替共情，也不宜鼓励刻板印象','https://huggingface.co/datasets/ASLP-lab/EChat-200K','先标注用户难过，再生成安慰回复文本及其语音。','HF公开入口；论文描述DeepSeek生成文本、CosyVoice2合成，样本级完整合成日志需核查',True)
add('CPED','中文','中文语义与情感','约1.2万对话、13.3万话语；40部电视剧','对话文本、13类情感、19类对话行为、角色个性和人口属性','情感识别、个性识别、个性化情感回复生成','适合中文日常处境和多轮关系语境','电视剧人物回复不一定共情；文本标注可用不代表原剧音视频可自由再分发','https://github.com/scutcyr/CPED','同一事件下，不同角色由于关系和个性而作出不同回应。',priority=True)
add('CAPE（认知评价情绪语料）','中文','中文语义与情感','两阶段自动构建；规模与版本以论文为准','人物属性、事件、认知评价、情绪和后续话语','情绪预测及下一句话生成','借鉴“为什么产生这种感受”的题目设计','是情绪生成语料，不等于所有回复都温暖支持；不要与同名人格评测CAPE混淆','https://aclanthology.org/2025.findings-naacl.353/','同样没被邀请，重视归属感的人与偏爱独处的人，感受可能不同。')
add('PsyQA','中文','中文语义与情感','论文约2.2万问题、5.6万回答；仓库仅少量样例','心理支持问题、长回答、部分援助策略标注','长咨询回答生成及策略分析','适合研究确认感受、解释、建议等内容策略','单轮长文本和咨询场景偏多；不能直接评价口语自然度','https://github.com/thu-coai/PsyQA','用户担心工作受挫，回复先回应压力，再提供可选择的行动。','完整数据需签署协议并发给作者审核；本次未申请、未发送邮件',True)
add('SmileChat / SMILE','中文','中文语义与情感','约5.5万合成多轮对话','从单轮心理问答扩展的多轮咨询文本','多轮心理支持模型训练与评估','可以借鉴多轮追问和支持策略','多轮是模型扩写，不是真实用户对话；无回复音频','https://github.com/qiuhuachuan/smile','将一个求助问题展开成倾听、澄清、协商下一步的对话。')
add('SoulChatCorpus','中文','中文语义与情感','公开精简版258,354段对话、1,517,344轮；不同于论文230万样本口径','中文心理咨询问答扩展的多轮文本','共情对话训练及人工/自动评估','中文内容和多轮支持素材量大','合成扩展占重要部分；语音自然度和情感控制没有现成金标准','https://github.com/scutcyr/SoulChat','当用户说“我只想有人听听”，回复先倾听而不是连续开建议清单。','仓库和ModelScope提供公开入口；数据、代码与模型许可分别核对',True)
add('SoulChat-R1','中文','中文语义与情感','结构化多轮心理咨询语料；具体版本以官方为准','按目标、工作、结束阶段组织的对话及规划','结构化咨询流程和推理式支持生成','可参考对话目标与阶段保持','专业咨询流程不应成为所有日常共情的模板；内部推理不宜要求系统口头朗读','https://github.com/scutcyr/SoulChat-R1','先了解目标，再协商一个小步骤，最后确认用户是否愿意继续。')
add('CPsDD','中文','中文语义与情感','68,136段对话（官方报告）','问题、原因、支持关注点与策略路径驱动的合成心理支持对话','心理问题与支持策略分析、对话生成','适合借鉴分层场景和策略覆盖','策略符合不等于用户感到被理解；合成对话需要人工筛选','https://github.com/FakerBoom/CPsDD','同样是家庭分歧，先区分用户需要倾听、决策帮助还是边界支持。','研究用途；下载与许可按仓库说明核对')
add('M3ED','中文','中文语义与情感','990段对话、24,449条话语；56部电视剧','文本、音频、视频、说话人及7类情绪','多模态对话情绪识别','能观察情绪随多轮关系语境变化','识别任务；愤怒角色的话不等于理想助手回复，原始剧集涉及版权','https://github.com/AIM3-RUC/RUCM3ED','对话里一方责问，另一方解释，标注每轮各自情绪。')
add('EmotionTalk','中文','中文语义与情感','19名演员；23.6小时、19,250条话语','双人交互的音视频文本；7类情绪、5级情感极性、4个方面的语音描述','情绪识别、情感分析、说话风格描述','细粒度中文声音标签可用于情感表达分析','演员交互数据；没有“助手是否有共情”的标准答案','https://github.com/flageval-baai/EmotionTalk','对同一段话分别标情绪、极性和说话风格；这几种标签不是同一概念。','官方仓库提供数据说明；学术使用范围需核对')
add('EmotionDialogCN','中文','中文语义与情感','论文报告21,880段会话、119名专业演员、400多小时','20类日常情境、18类情绪的多模态互动','普通话对话情绪研究','比孤立朗读更贴近日常情绪交互','专业演员场景录制不等于自然用户求助；此处确认论文，未确认可直接下载的完整发布包','https://arxiv.org/abs/2608.20905','在预设生活情境中互动，再标注各轮情绪。','已确认论文；数据开放状态需另行核实')
add('ESD','中文 / 英文','语音表达与自然度','20人×350文本×5情绪＝35,000条；中英文各10人','同一文本由同一说话人录制中性、快乐、愤怒、悲伤、惊讶语音','情感语音转换、情感合成、相同文字下的表达对比','很适合你关心的情感类别准确度；平行文本减少语义干扰','朗读语料，不测回复是否理解用户；不能把悲伤用户机械映射为悲伤回复','https://github.com/HLTSingapore/Emotional-Speech-Data','把同一句中性内容分别说成开心与悲伤，听者只根据声音判断。','数据需要按作者要求签署许可；仓库代码许可不等于数据许可',True)
add('CSEMOTIONS','中文','语音表达与自然度','4,160条，约10.24小时','audio、text、emotion、speaker；7类情感，包含俏皮和害怕','多情感中文语音合成及表达控制','直接查看中文情感标签与音频的对应关系','不少文本本身带强情绪词；不宜直接当“只靠声音分类”的平行测试。说话人数在资料中有口径差异，本页不强定','https://huggingface.co/datasets/ATH-MaaS/CSEMOTIONS','文字本身表达愤怒，emotion也标angry；分类正确可能来自文字也可能来自声音。','HF公开，数据卡标Apache-2.0',True)
add('CEAEval-D','中文','语音表达与自然度','人工子集7,136片段、91故事；另有约150万弱标注片段','中文有声书、长文本上下文；15个维度涵盖表达适切性、韵律、情绪、角色和环境','有上下文的表达适切性评分；人工部分为核心','很贴合“这个地方这样说合不合适”，补足只看情绪类别的不足','叙事和角色表演不是语音聊天；弱标注不能当人评金标准','https://huggingface.co/datasets/TianRW/CEAEval-Data','同一句“你终于来了”，在迎接朋友和严肃追问中，适合的说法不同。','HF公开；CC-BY-NC-4.0；网页预览失败不等于文件不能下载',True)
add('Audio Turing Test / ATT-Corpus','中文相关','语音表达与自然度','整体1,000条；公开白盒文本500条，另500条黑盒','难读表达、情绪/副语言、混合语言等语音合成挑战文本','真人/机器辨别，以及自动辅助评分','“像真人说话吗”的自然度补充','公开文本不等于1,000条配套真人音频全公开；像真人、音色好听和共情是三个判断','https://huggingface.co/datasets/meituan-longcat/Audio-Turing-Test-Corpus','让模型自然说出带停顿、语气和口语变化的短句，再听辨是否像真人。','公开部分标CC-BY-NC-4.0；保留白盒/黑盒区分',True)
add('DRAMA-Eval','中文 / 英文','语音表达与自然度','双语、多轮、多说话人；按发布版本读取','结构化剧本上下文和角色语音生成条件','音质、句级执行、互动自然度、全局连贯与场景沉浸','适合研究回复跨轮声音风格与角色稳定性','剧本表演强于日常共情；情境对齐可以借鉴，但不直接替代用户体验评分','https://github.com/ASLP-lab/DRAMA-Eval','前一轮还在严肃讨论，后一轮不应突然变成播音腔或夸张欢笑。','官方HF数据入口可用；本页未批量下载')
add('SpeechParaling-Bench','中文 / 英文','语音表达与自然度','1,000多条中英平行查询，覆盖100多种特征','细粒度声音指令、句内变化和上下文适配任务','声学语言模型辅助的成对比较','借鉴情感强弱、语速、停顿和局部变化控制','自动模型偏好不是人工真值；与端到端内容共情仍需分开报告','https://speechparaling-bench.github.io/','同一句话开头平静，最后轻微惊喜，而不是全句都大喊。')
add('NVBench（2026语音非语言发声）','中文 / 英文','语音表达与自然度','论文初版45类非语言发声；以论文版本为准','笑、叹息等非语言发声的控制与语境','类型、位置、显著度与整体语音质量','检查笑声或叹息是否自然、是否出现在适当位置','非语言发声更多不等于更共情；勿与同名可视化数据集或其他NV-Bench混淆','https://arxiv.org/abs/2604.16211','安慰失落的人时，随意插入轻笑会降低合适度，即使笑声很逼真。','已确认论文；具体数据入口与新版本名称需沿论文核对')
add('SEED-TTS-EVAL','中文 / 英文','语音表达与自然度','2,000中文、1,000英文测试项','参考声音、目标文字及零样本合成评测材料','CER/WER和说话人相似度等','补充检查说错字、漏字、声音身份漂移','识别错误率低不等于自然、好听或情感合适','https://github.com/BytedanceSpeech/seed-tts-eval','合成一句话，检查内容是否完整且声音身份是否稳定。')
add('AISHELL-3','中文','语音表达与自然度','约85小时、218位说话人','多说话人普通话朗读语音与转写','多说话人语音合成和声音建模','普通话清晰度和说话人覆盖素材','训练语料；没有逐条共情或情感表达金标准','https://www.openslr.org/93/','同一类朗读任务由不同说话人完成，用于声音建模。')
add('Emilia','含中文的多语','语音表达与自然度','初版约10.2万小时、6种语言','从真实网络音频提取的语音与转写','语音生成训练和多语言自然语音研究','可以观察自然口语分布','大训练语料不等于可直接使用的共情测试集；无逐条共情评分','https://emilia-dataset.github.io/Emilia-Demo-Page/','收集真实语音片段并配转写，训练更接近自然表达的生成系统。')
add('DailyTalk','英文','英文参考','2,541段对话','由DailyDialog选取改写并录制的对话语音','对话式语音合成和上下文建模','借鉴真实轮次和口语化回复长度','不是中文；对话自然不意味着每轮都在共情','https://github.com/keonlee9420/DailyTalk','问答轮次之间用符合语境的语调衔接。')
add('EmpatheticDialogues','英文','英文参考','约2.5万对话，32类情绪情境','描述个人经历的文字及倾听者对话','基于语义处境的共情回复生成','直接说明：共情任务可以完全没有输入音频','英语文化语境需重新编写中文样例；情境情绪标签不是助手必须输出的情绪','https://github.com/facebookresearch/EmpatheticDialogues','用户用文字说自己落选了，助手理解失落、回应付出，不需要先听到哭腔。',priority=True)
add('ESConv','英文','英文参考','约1,300段情感支持对话；早期版本规模不同','求助者—支持者多轮文本和8类支持策略','策略识别、策略驱动支持回复生成','借鉴情感确认、提问、建议的时机','支持策略出现次数不是共情质量；没有输出语音','https://github.com/thu-coai/Emotional-Support-Conversation','先探索用户需要倾听还是建议，再决定是否提供下一步。')
add('ExTES','英文','英文参考','11,177段扩展支持对话','LLM生成的多场景情绪支持文本','扩展情绪支持任务覆盖','扩展日常问题类型和支持方式','合成素材；应人工重写复核，不能直接当真人偏好真值','https://github.com/pandazzh2020/ExTES','同一生活烦恼分别采用倾听、澄清和可行建议的支持路径。')
add('EPITOME','英文','英文参考','研究约10,143对；公开可用部分与完整来源不同','心理支持帖子—回复、情绪回应/理解解释/探索三个维度的标注与依据','文本共情强度识别','非常适合借鉴内容评分，不要求双方情感相同','公开Reddit子集不等于包含全部TalkLife数据；心理支持语域偏重','https://github.com/behavioral-data/Empathy-Mental-Health','“听起来你在担心被误解”比“好吧”表现出更具体的处境理解。')
add('EchoMind','英文为主','理解与通用基准','本地1,628情境、13,401选择题；真人与合成两部分','音频、文本、情绪、多个声音条件及选择题','共情理解与推理的选择题准确率','可做声音线索影响的独立诊断','任务设计特意突出副语言线索；不能代表共情任务的全部定义，也非主要输出自然度评测','https://huggingface.co/datasets/hlt-cuhksz/EchoMind','相同文字配不同语气，看理解和选择的回应是否随之改变。','完整快照已在此前下载；本站提供旧浏览站入口')
add('URO-Bench Basic（中文）','中文','理解与通用基准','已下载1,691例、10个子集，约5.09小时','语音输入、转写、部分任务有参考答案','复述、摘要、问答、推理、开放回复；质量指标另计','可当语义正确性与任务执行的基础对照','Basic不直接测共情；不要用CER或问答分数替代语音情感体验','https://github.com/Ruiqi-Yan/URO-Bench','用户口头提出数学题，检查系统是否正确回答。','完整中文Basic已下载；本站提供此前浏览站入口')
general=[
('VoxDialogue','多属性语音对话；4,500段多轮脚本','12类语音/背景属性','带年龄、口音、情绪等属性的脚本与合成语音','https://voxdialogue.github.io/'),
('SD-Eval','7,303条评测语音、8.76小时','情绪、口音、年龄、背景音适配','已有语料和合成/混合声音，生成情境适配回复','https://github.com/AmphionTeam/SD-Eval'),
('MTalk-Bench','多轮语音交互','语义、副语言和环境线索','多轮问题与情境评分要求','https://github.com/FreedomIntelligence/MTalk-Bench'),
('VoiceBench','真实与合成语音指令','语音指令遵循及扰动鲁棒性','语音指令、文本和任务判据','https://github.com/MatthewCYM/VoiceBench'),
('S2SArena','原始论文154例、4领域21类任务','语音到语音指令与副语言执行','语音输入和输出控制要求；后续版本需另核','https://arxiv.org/abs/2503.05085'),
('AudioBench','多任务集合，随版本扩展','通用音频理解','语音、环境声与多类问答/识别任务','https://github.com/AudioLLMs/AudioBench'),
('Dynamic-SUPERB Phase-2','约180项任务','自然语言指令式音频理解','多数据源的指令、音频与答案','https://dynamic-superb.github.io/'),
('AIR-Bench','基础约1.9万例，开放问答约2千例','音频理解和开放问答','音频、问题、参考答案','https://github.com/OFA-Sys/AIR-Bench'),
('AudioEntailment','按发布子集计','判断声音是否支持文字陈述','音频和候选陈述/蕴含标签','https://github.com/microsoft/AudioEntailment'),
('SAKURA','约4,000道选择题','多属性、多跳语音理解','音频、问题、选择项及答案','https://github.com/ckyang1124/SAKURA'),
('MMAU','约1万音频问题、27种能力','语音/音乐/环境声推理','音频、选择题和正确选项','https://arxiv.org/abs/2410.19168'),
('MMAR','1,000条真实世界音频问题','混合音频复杂推理','音频及推理问题、参考答案','https://github.com/ddlBoJack/MMAR'),
('MMSU','约5,000测试项、47类任务','细粒度语言理解','语音、问题、目标回答的对齐样本','https://arxiv.org/abs/2506.04779'),
('MSU-Bench','2025初版与2026扩展口径不同','多说话人语音理解','多人对话的归属、语义和推理问题','https://github.com/ASLP-lab/MSU-Bench'),
('SpeechR','按论文任务版本计','事实检索、程序推理与规范判断','语音及不同回答方式的推理题','https://arxiv.org/abs/2508.02018'),
('AudioCaps','约4.6万训练音频描述','环境声音描述','音频片段和人工文字描述','https://audiocaps.github.io/')]
for n,s,e,m,u in general:
    add(n,'按子集核对','理解与通用基准',s,m,e,'作为理解能力或声音适配的辅助对照','不能直接回答“中文助手回复是否共情、自然、好听”；需核对中文子集和生成输出要求',u,'示意任务：听一段音频，根据任务要求回答问题或生成适配回复。')

rows=[
('失落','求职','准备了很久的面试还是没过，我现在不想听大道理，只想缓一下。','只倾听，不急于建议','温暖、克制、留停顿','准备和落选；明确不想听建议','别用“一定有更好的”保证未来','准备那么久却没等到想要的结果，确实会很失落。先不用急着振作，我愿意听你说。'),
('失落','兴趣','我画了一个月的画发出去，几乎没人看，有点怀疑自己。','理解付出与不被看见','温暖、认真','付出未被看见；不要把点赞当能力','别直接评价画作好坏','花了一个月心血，却像没被看见一样，难免会受打击。你愿意说说这幅画里最想表达的是什么吗？'),
('失落','人际','朋友搬走了，平时下班一起吃饭的人突然不在了。','陪伴与生活变化','柔和、自然','日常陪伴缺失','别轻描淡写说再交一个','少了那个下班能一起吃饭的人，日常里会空出很大一块。你最想念你们一起做的哪件小事？'),
('失落','学习','考完知道自己没发挥好，我已经复盘过了，先别帮我分析错题。','尊重已复盘和暂停需求','平稳、接纳','已经复盘；暂不分析','别继续出学习计划','你已经认真复盘过了，现在还是难受也很正常。我们可以先把考试放一放，陪你聊点别的。'),
('焦虑','工作','明天第一次给整个部门汇报，我担心讲到一半脑子空白。','理解担心并给一个小办法','稳定、鼓励','首次公开汇报；怕卡住','别承诺绝不会卡住','第一次面对整个部门，紧张很能理解。要不要只准备一句卡住时的过渡话，让自己有个可以停靠的地方？'),
('焦虑','生活','快搬家了，事情全堆一起，我不知道先做什么。','降低负荷，协商第一步','平静、简短','事情多而混乱','别一次列二十条','事情挤在一起确实容易乱。我们先只挑一件：今天有没有必须处理、错过就来不及的事？'),
('焦虑','社交','周末聚会我谁都不熟，怕一直尴尬地坐着。','理解不确定，不强迫外向','轻松、温和','陌生聚会和尴尬担忧','别要求必须主动表演','到一个谁都不熟的场合，担心冷场很自然。你不必一下子融入所有人，先和一个人聊几句也可以。'),
('焦虑','决策','我在两个工作机会之间来回纠结，不希望你直接替我选。','帮助澄清价值而非代选','认真、平稳','明确不要代选','别直接指定公司','两个机会都重要，来回权衡会很累。我不替你决定；我们可以先看看，你最不愿意牺牲的是哪一点。'),
('生气','工作','我做的方案被同事拿去署了自己的名，真的很气。','确认不公平，支持边界','认真、稳住节奏','成果被冒领','别鼓动报复；不要替用户暴怒','自己的劳动被这样拿走，生气很能理解。你愿意的话，我们可以一起想一个能清楚说明贡献、又保留证据的沟通方式。'),
('生气','生活','室友又半夜外放，我提醒过很多次了，我只想把边界说清楚。','协助表达具体边界','坚定、克制','反复发生；需要边界措辞','别说忍一忍','反复提醒还被打扰，确实会烦。可以直接说：晚上十一点后请戴耳机，外放会影响我休息。'),
('生气','服务','快递把礼物摔坏了，还说我小题大做。','回应损失及被轻视','严肃、尊重','礼物损坏和被否定','别替客服辩解','礼物坏了已经让人难受，还被说小题大做，会更生气。你现在想先说说这件礼物，还是一起整理投诉时要说明的情况？'),
('生气','人际','家人总拿我跟别人比，我不想吵架，但真的受够了。','尊重关系与自主性','温和、坚定','不想吵但想停止比较','别劝断绝关系或服从','一直被比较会让人觉得自己的努力没被看见。你可以不吵架，也把“这样比较让我难受，希望你停下来”说清楚。'),
('自责','工作','我把文件发错群了，虽然已经撤回，还是觉得自己特别蠢。','区分失误与自我价值','温暖、不过分轻快','已撤回仍自我贬低','别嘲笑或夸大后果','发错群会让人一下子很慌，但一次失误并不说明你很蠢。你已经及时撤回了，我们也可以看看是否还有需要补上的说明。'),
('自责','学习','讨论时答错一个常识问题，大家笑了一下，我现在还在回想。','理解尴尬，不猜别人心意','接纳、柔和','反复回想社交尴尬','别断言大家早忘了','那一刻被笑到，确实可能让人一直回想。答错一个问题不等于你整个人都被否定了；你愿意说说当时最刺痛你的是什么吗？'),
('自责','家庭','我刚才对妈妈语气很冲，现在后悔，但不知道怎么开口。','承认行为责任并支持修复','真诚、平稳','后悔和想道歉','别用共情替行为开脱','你在意刚才的语气，也想修复关系。可以从一句具体的道歉开始：刚才我说话很冲，对不起，我想重新好好说。'),
('自责','兴趣','健身计划又没坚持住，感觉自己没有自制力。','减少羞辱，探索阻碍','温暖、不训话','计划中断和自我归因','别贴懒惰标签','计划没坚持下来会让人挫败，但不必立刻把它归成“我没有自制力”。最近最难做到的是时间、体力，还是这个计划本身太满？'),
('喜悦','学习','我终于通过驾照考试了，之前挂了两次！','分享喜悦并看见坚持','开心、适度有活力','终于通过；经历两次失败','别淡化或突然讲交通风险','太好了！前面两次受挫后你还坚持下来，这次终于过了，真的值得好好开心一下。'),
('喜悦','工作','我第一次独立做的项目上线了，虽然不大，但我特别开心。','认可具体成就','欣喜、自然','第一次独立完成；不要贬低规模','别说这没什么','第一次独立把项目做上线，这种从头跟到落地的成就感很特别。规模不大也完全值得庆祝！'),
('喜悦','家庭','今天孩子第一次主动给我做早餐，有点被暖到了。','回应被关心的感动','温暖、轻快','主动照顾带来的温暖','别虚构孩子动机','被孩子这样惦记着，确实很暖。那顿早餐里，你最舍不得忘掉的是哪个小细节？'),
('喜悦','兴趣','练了很久的曲子终于完整弹下来了，我想先炫耀一下。','允许庆祝，不急着改进','开心、鼓励','明确想分享成就','别立即指出进步空间','那就好好炫耀一下！练了那么久，终于能完整弹下来，这一刻很值得享受。'),
('复杂','工作','我升职了很开心，但想到要带团队又有点怕。','同时接纳喜悦和担心','温暖、稳健','两种感受都要回应','别只庆祝或只谈压力','升职的开心和带团队的忐忑，可以同时存在。先为你走到这一步高兴；等你愿意，我们再挑一个最担心的问题慢慢聊。'),
('复杂','人际','我替朋友结婚开心，也有一点说不出的失落。','允许复杂感受','柔和、接纳','祝福和失落并存','别指责嫉妒或逼问感情','替朋友开心，同时又觉得有些东西变了，这两种感受并不矛盾。你不需要因为那一点失落就责怪自己。'),
('复杂','生活','一个人住很自由，但周末回家太安静时也会孤单。','理解自由与孤独并存','温暖、自然','不把独居当错误','别直接要求找伴侣','自由和孤单有时会一起出现，并不说明你选错了生活。你更想有人陪你聊一会儿，还是一起想想让周末舒服一点的小安排？'),
('复杂','边界','我想拒绝朋友借钱，又怕显得不够义气。','支持边界，不代替做主','坚定、体贴','经济边界和关系担忧','别断言朋友别有用心','想顾及朋友，也想保护自己的安排，这份纠结很真实。拒绝借钱不必等于否定友情；我们可以一起把话说得清楚又体面。')]
cases=[]
for i,(state,domain,user,goal,style,anchor,avoid,ref) in enumerate(rows,1):
    hist=[]
    if i%2==0:
        hist=[{'role':'user','text':'我想聊聊最近的一件事。'},{'role':'assistant','text':'可以，你希望我先听你说，还是一起想办法？'}]
    cases.append({'id':f'ZH-EV-{i:03d}','version':'0.1-draft','status':'authored_not_recorded_not_validated','track':'main_semantic_sufficient','semantic_family_id':f'family-{i:03d}','domain':domain,'user_affect':state,'history':hist,'input_text':user,'input_audio':None,'input_audio_condition':'planned_human_conversational_reading','acoustic_cue_required':False,'support_goal':goal,'acceptable_output_styles':style.split('、'),'content_anchors':anchor.split('；'),'failure_examples':avoid.split('；'),'reference_response_text':ref,'reference_is_unique_answer':False,'reference_response_audio':None,'speaker_id':None,'recording_provenance':None,'gold_validation':None})

def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
dump(DATA/'catalog.json',records)
(DATA/'pilot_24.jsonl').write_text('\n'.join(json.dumps(c,ensure_ascii=False) for c in cases)+'\n',encoding='utf-8')
dump(DATA/'example_complete.json',cases[0])
with (DATA/'ratings_template.csv').open('w',encoding='utf-8-sig',newline='') as f:
    csv.writer(f).writerow(['case_id','system_id','run_id','judge_id','panel','understanding_1_5','validation_1_5','helpfulness_1_5','boundary_1_5','naturalness_1_5','pleasantness_1_5','context_voice_fit_1_5','perceived_emotion','emotion_intensity_1_5','intelligibility_1_5','severe_failure','evidence','output_audio','output_transcript','first_audio_latency_ms','total_latency_ms'])
dump(DATA/'output_template.json',{'case_id':'ZH-EV-001','system_id':'填写实际系统版本','run_id':None,'input_audio':None,'output_audio':None,'output_transcript':None,'transcript_source':None,'system_prompt':None,'inference_parameters':{},'started_at':None,'first_audio_latency_ms':None,'total_latency_ms':None,'error':None})
schema={'$schema':'https://json-schema.org/draft/2020-12/schema','title':'中文共情语音主测试草案','type':'object','required':['id','status','track','semantic_family_id','input_text','input_audio','acoustic_cue_required','support_goal','content_anchors','reference_is_unique_answer'],'properties':{'id':{'type':'string'},'status':{'enum':['authored_not_recorded_not_validated','recorded_pending_validation','validated']},'track':{'const':'main_semantic_sufficient'},'semantic_family_id':{'type':'string'},'input_text':{'type':'string'},'input_audio':{'type':['string','null']},'acoustic_cue_required':{'const':False},'support_goal':{'type':'string'},'content_anchors':{'type':'array','items':{'type':'string'}},'reference_is_unique_answer':{'const':False}}}
dump(DATA/'schema.json',schema)
bundle={'updated':'2026-11-16','datasets':records,'cases':cases}
(DIST/'data.js').write_text('window.ATLAS='+json.dumps(bundle,ensure_ascii=False)+';',encoding='utf-8')
print(f'{len(records)} datasets; {len(cases)} draft cases')
