%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ydzjreport.cls  ——  月度（阶段）总结报告 文档类
%  版本 v1.4：正文直接从第一节开始，不输出开篇标题及信息框。
%
%  设计目标
%    1. 同一份 .tex 在 Overleaf 与本地 TeX Live / MiKTeX 都能编译
%       —— 字体交给 ctex 自动检测（这正是 ctex 的强项）
%    2. 三人写出的报告排版完全一致
%    3. 两种阶段（初步阅读 / 研究推进）共用同一套版式
%
%  引擎要求
%    XeLaTeX 或 LuaLaTeX（不要用 pdfLaTeX）
%    Overleaf：Menu -> Compiler -> XeLaTeX
%    本地：    xelatex 文件名.tex     （跑两遍）
%
%  字体说明
%    ctex 会按平台自动选字体：
%      Windows -> SimSun / SimHei
%      Overleaf/Linux -> Fandol 或 Noto CJK
%      macOS -> Songti SC / Heiti SC
%    想强制指定，可在 \documentclass 加选项，例如：
%      \documentclass[stage1,fontset=fandol]{ydzjreport}
%    三人若要「字形完全一致」，统一用 fontset=fandol。
%
%  ⚠️ 维护注意
%    不要在类文件顶层调用 \IfFontExistsTF —— 它基于 \ifcsname，
%    在类文件顶层使用会破坏 TeX 条件平衡，引发
%    "Missing \begin{document}" 与一连串错乱报错。
%    需要判断字体时，改用 ctex 的 fontset 机制。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ydzjreport}[2026/10/23 v1.4 月度阶段总结报告]

\newif\if@stageone
\@stageonetrue
\DeclareOption{stage1}{\@stageonetrue}
\DeclareOption{stage2}{\@stageonefalse}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexart}}
\ProcessOptions\relax

\LoadClass[11pt,a4paper]{ctexart}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  1. 基础宏包
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{geometry}
\RequirePackage[table]{xcolor}   % table 选项提供 \rowcolor
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{array}
\RequirePackage{ragged2e}
\RequirePackage{multirow}
\RequirePackage{enumitem}
\RequirePackage{titlesec}
\RequirePackage{fancyhdr}
\RequirePackage{graphicx}
\RequirePackage{float}
\RequirePackage{caption}
\RequirePackage{etoolbox}
% 浮动体管理与防孤行（needspace 可选，没有就退化）
\RequirePackage{placeins}        % 提供 \FloatBarrier
\makeatletter
\IfFileExists{needspace.sty}{%
  \RequirePackage{needspace}%
  \newcommand{\ydzj@needspace}{\needspace{6\baselineskip}}%
}{%
  \newcommand{\ydzj@needspace}{}%
}
\makeatother
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{ulem}
\RequirePackage[hidelinks]{hyperref}

\geometry{left=2.2cm,right=2.2cm,top=2.4cm,bottom=2.2cm}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  2. 中文粗体与缺字回退
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ctex 已提供 \heiti / \songti / \kaishu，直接用黑体做粗体
\renewcommand{\textbf}[1]{{\heiti #1}}
\newcommand{\hei}{\heiti}
\newcommand{\song}{\songti}
\newcommand{\kai}{\kaishu}

% ----------------------------------------------------------------------
%  缺字防护
%
%  实测缺口（用 fontTools 查字形表 + xelatex 的 Missing character 警告）：
%
%    · ⁴ ⁵ ⁶ ⁻ ₁ ₂ ₀  —— Unicode 上下标字符。
%                        丢的原因是**西文主字体里没有**，报
%                        "There is no ⁶ (U+2076) in font lmroman10-regular"
%    · μ (U+03BC)     —— 直接写希腊字母 μ 也会丢（要写成 $\mu$）
%    · ṁ (U+1E41)     —— 质量流量符号，中文字体全都没有（要写 $\dot{m}$）
%    · − (U+2212)     —— 数学减号（要写成数学模式的 $-$ 或 ASCII 的 -）
%    · ★ ⚠ ✅ ❌     —— emoji 类符号（要写成文字或 $^\ast$）
%
%  说明：`²` 和 `³` 在 SimSun 里有字形，加粗时 xeCJK 会路由到 SimSun，
%        所以 `W/cm²` 加粗其实能正常显示，**不算缺字**。
%
%  处理：
%    ① 中文字体挂 FreeSerif 回退（中文侧字符，零风险）；
%    ② 提供 \spx{} / \sbx{} 安全上下标命令；
%    ③ 其余靠写作规范规避——见 CONTRIBUTING.md「单位与符号」一节。
%
%  ⚠️ 试过给西文字体挂 FallbackFont 来根治，但在本机 TeX Live 下
%     \setmainfont 用字体名重新声明会解析成 nullfont，报
%     "Cannot use \XeTeXOTcountfeatures with nullfont"（100 个错误）。
%     所以**不要**在类文件里动西文字体。改用写作规范 + \spx 命令。
% ----------------------------------------------------------------------
\makeatletter
\IfFontExistsTF{FreeSerif}{%
  \setCJKfallbackfamilyfont{\CJKrmdefault}{FreeSerif}%
  \setCJKfallbackfamilyfont{\CJKsfdefault}{FreeSerif}%
  \setCJKfallbackfamilyfont{\CJKttdefault}{FreeSerif}%
}{}
\makeatother

% 安全上标/下标：写 \spx{2} 而不是 ²，\spx{6} 而不是 ⁶
\newcommand{\spx}[1]{$^{#1}$}
\newcommand{\sbx}[1]{$_{#1}$}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  3. 颜色与版式参数
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\definecolor{ydzjblue}{HTML}{0B4C8C}
\definecolor{ydzjblueii}{HTML}{1868A8}
\definecolor{ydzjblueiii}{HTML}{2E7DB8}
\definecolor{ydzjgrey}{HTML}{666666}
\definecolor{ydzjlight}{HTML}{F2F7FB}
\definecolor{ydzjrule}{HTML}{BBBBBB}
\definecolor{ydzjwarnbg}{HTML}{FFF8E1}
\definecolor{ydzjwarnline}{HTML}{E6A23C}

\linespread{1.28}
\setlength{\parindent}{2em}
\setlength{\parskip}{2pt}

% ----------------------------------------------------------------------
%  浮动体管理
%  不加这些参数时，图/表会被推到很后面，出现「某页只有一张图」的空页，
%  甚至把参考文献拆到两页。这里的设置让浮动体尽量留在原文附近。
% ----------------------------------------------------------------------
\renewcommand{\topfraction}{0.90}      % 页顶浮动最多占 90% 版心高
\renewcommand{\bottomfraction}{0.75}   % 页底浮动最多占 75%
\renewcommand{\textfraction}{0.07}     % 每页至少 7% 是正文
\renewcommand{\floatpagefraction}{0.75}% 浮动页至少 75% 满才单独成页
\setcounter{topnumber}{3}
\setcounter{bottomnumber}{2}
\setcounter{totalnumber}{4}
\setlength{\floatsep}{8pt plus 2pt minus 2pt}
\setlength{\textfloatsep}{10pt plus 3pt minus 3pt}
\setlength{\intextsep}{8pt plus 2pt minus 2pt}

% 防孤行寡行
\widowpenalty=10000
\clubpenalty=10000
\displaywidowpenalty=10000
\predisplaypenalty=10000

% 段落之间、章节之间不允许分页得太碎
\raggedbottom

% 中英混排换行优化：允许在英文/数字间断行，避免长 token 把行撑开
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt minus 0.1pt
\tolerance=3000
\emergencystretch=3em
\hyphenpenalty=50
\exhyphenpenalty=50

% 表格列型：Y = 自适应页宽 + 左对齐（杜绝超框）
\newcolumntype{Y}{>{\RaggedRight\arraybackslash}X}
\newcolumntype{C}{>{\Centering\arraybackslash}X}
\renewcommand{\arraystretch}{1.22}
% 全部报告共享表格样式；列宽和数字精度由数据含义决定。
\newcommand{\ydzjtablestyle}{%
  \small\linespread{1.08}\selectfont
  \renewcommand{\arraystretch}{1.15}%
  \setlength{\tabcolsep}{4pt}%
}
\AtBeginEnvironment{tabularx}{\ydzjtablestyle}
\AtBeginEnvironment{tabular}{\ydzjtablestyle}
\AtBeginEnvironment{tabular*}{\ydzjtablestyle}
\AtBeginEnvironment{longtable}{\ydzjtablestyle}

% 章节样式
\titleformat{\section}
  {\normalsize\heiti\color{ydzjblue}}{\thesection}{0.6em}{}
\titlespacing{\section}{0pt}{10pt}{5pt}
\titleformat{\subsection}
  {\normalsize\heiti\color{ydzjblueii}}{\thesubsection}{0.6em}{}
\titlespacing{\subsection}{0pt}{8pt}{4pt}
\titleformat{\subsubsection}
  {\normalsize\heiti\color{ydzjblueiii}}{\thesubsubsection}{0.6em}{}
\titlespacing{\subsubsection}{0pt}{6pt}{3pt}
% 四级标题按独立行排版；同一层级对应同一类内容，禁止手写编号。
\setcounter{secnumdepth}{4}
\titleformat{\paragraph}[block]
  {\normalsize\heiti\color{ydzjblueiii}}{\theparagraph}{0.6em}{}
\titlespacing{\paragraph}{0pt}{5pt}{2pt}
% 标题至少与少量正文同页，避免仅标题落在页尾。
\pretocmd{\section}{\Needspace{6\baselineskip}}{}{}
\pretocmd{\subsection}{\Needspace{4\baselineskip}}{}{}
\pretocmd{\subsubsection}{\Needspace{3\baselineskip}}{}{}
\pretocmd{\paragraph}{\Needspace{3\baselineskip}}{}{}

% 图题、表题
\captionsetup{font={small,sf},labelfont={bf,color=ydzjblue},labelsep=quad}
\captionsetup[table]{skip=4pt}
\captionsetup[figure]{skip=4pt}

% 列表间距
\setlist[itemize]{leftmargin=2em,itemsep=2pt,topsep=3pt,parsep=0pt}
\setlist[enumerate]{leftmargin=2.4em,itemsep=2pt,topsep=3pt,parsep=0pt}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  4. 页眉页脚
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\ydzjshorttitle}{}
\newcommand{\ydzjauthor}{}
\newcommand{\setshorttitle}[1]{\gdef\ydzjshorttitle{#1}}
\newcommand{\setauthor}[1]{\gdef\ydzjauthor{#1}}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{ydzjgrey}\ydzjshorttitle}
\fancyhead[R]{\small\color{ydzjgrey}\ydzjauthor}
\fancyfoot[C]{\small\color{ydzjgrey}第 \thepage\ 页}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  5. 元信息与报告头
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\ydzjstage}{}
\newcommand{\ydzjname}{}
\newcommand{\ydzjfield}{}
\newcommand{\ydzjperiod}{}
\newcommand{\ydzjkeywords}{}
\newcommand{\ydzjsummary}{}

\newcommand{\ydzjmetatable}{%
  \begin{center}
  \begin{tabularx}{\textwidth}{@{}>{\heiti}p{2.4cm}Y@{}}
  \toprule
  \rowcolor{ydzjlight} 报告阶段 & \ydzjstage \tabularnewline
  \midrule
  姓名 & \ydzjname \tabularnewline
  方向 & \ydzjfield \tabularnewline
  报告周期 & \ydzjperiod \tabularnewline
  关键词 & \ydzjkeywords \tabularnewline
  一句话摘要 & \ydzjsummary \tabularnewline
  \bottomrule
  \end{tabularx}
  \end{center}
}

\newcommand{\ydzjmakereporthead}[1]{%
  % 保留旧调用接口，只初始化编号；正文直接从第一节开始。
  \setcounter{section}{0}%
  \setcounter{subsection}{0}%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  6. 阶段一：初步阅读
%     用法（两步，缺一不可）：
%       导言区：\stageonesetup{阶段}{姓名}{方向}{周期}{关键词}{摘要}
%       正文首：\makestageonehead
%     为什么分两步：
%       \stageonesetup 只做 \gdef 赋值，可以在导言区调用；
%       \makestageonehead 仅初始化编号，不输出标题和元信息框。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\stageonesetup}[6]{%
  \gdef\ydzjstage{#1}%
  \gdef\ydzjname{#2}%
  \gdef\ydzjfield{#3}%
  \gdef\ydzjperiod{#4}%
  \gdef\ydzjkeywords{#5}%
  \gdef\ydzjsummary{#6}%
  \setshorttitle{#1}%
  \setauthor{\ydzjname}%
}
\newcommand{\makestageonehead}{%
  \ydzjmakereporthead{月度阅读总结 \(\cdot\) 阶段一（初步阅读）}%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  7. 阶段二：研究推进
%     用法：
%       导言区：\stagetwosetup{阶段}{姓名}{方向}{周期}{关键词}{摘要}
%       正文首：\makestagetwohead
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\stagetwosetup}[6]{%
  \gdef\ydzjstage{#1}%
  \gdef\ydzjname{#2}%
  \gdef\ydzjfield{#3}%
  \gdef\ydzjperiod{#4}%
  \gdef\ydzjkeywords{#5}%
  \gdef\ydzjsummary{#6}%
  \setshorttitle{#1}%
  \setauthor{\ydzjname}%
}
\newcommand{\makestagetwohead}{%
  \ydzjmakereporthead{月度总结 \(\cdot\) 阶段二（研究推进）}%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  8. 常用盒子
%     用法（标准环境语法）：
%       \begin{notebox} ... \end{notebox}        注意事项（橙色上下横线）
%       \begin{keybox}  ... \end{keybox}         要点提示（蓝色上下横线）
%
%     实现说明（踩过的坑，别改回去）：
%       · 不要用 \colorbox{\begin{minipage}...\end{minipage}}：
%         \colorbox 的参数会在读到 minipage 开始后就被闭合，
%         导致 "Extra }, or forgotten \endgroup"。
%       · 不要用 minipage 包内容：不能跨页，且报
%         "begin{minipage} ... ended by \end{...}"。
%       · 不要把 \begin{notebox} 包装成 \newcommand{\note} 再用
%         \noteend 收尾：LaTeX 会做环境名匹配检查，
%         \end{note} 会被判成 "\begin{list} ended by \end{note}"。
%         必须用 \begin{notebox} / \end{notebox} 原样写。
%       · 环境名不要叫 \note / \notebox（\note 已被 LaTeX 占用）。
%
%       这里用「list + 彩色横线」：可跨页、可嵌套、无需额外宏包，最稳。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{notebox}%
  {\par\addvspace{3pt plus 2pt}%
   \begin{list}{}{\leftmargin=1.2em \rightmargin=0pt
                  \topsep=3pt \partopsep=0pt \parsep=2pt \itemsep=2pt}%
   \item\relax
   {\color{ydzjwarnline}\hrule height 1.2pt}\par\vspace{3pt}%
   \small}%
  {\par\vspace{3pt}{\color{ydzjwarnline}\hrule height 1.2pt}%
   \end{list}\par\addvspace{3pt plus 2pt}}

\newenvironment{keybox}%
  {\par\addvspace{3pt plus 2pt}%
   \begin{list}{}{\leftmargin=1.2em \rightmargin=0pt
                  \topsep=3pt \partopsep=0pt \parsep=2pt \itemsep=2pt}%
   \item\relax
   {\color{ydzjblueii}\hrule height 1.2pt}\par\vspace{3pt}%
   \small}%
  {\par\vspace{3pt}{\color{ydzjblueii}\hrule height 1.2pt}%
   \end{list}\par\addvspace{3pt plus 2pt}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  9. 表格便利命令
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 表头行：\tablehead{列1 & 列2 & 列3}
\newcommand{\tablehead}[1]{%
  \rowcolor{ydzjlight}\textbf{#1} \tabularnewline \midrule
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  9b. 参考文献不跨页拆分
%
%  背景：不加处理时，参考文献会被图/表挤开，出现
%        「第 1 条在第 6 页，第 2、3 条跑到第 8 页」的现象。
%
%  处理：在参考文献前 \FloatBarrier 把浮动体排空，
%        并要求至少 6 行空间，不够就另起一页。
%
%  ⚠️ 不要在每个 \section 前加 \FloatBarrier——
%     实测会把正文挤成只剩几行的空白页（8 页 vs 7 页，
%     且出现一页只有 109 字符）。只在参考文献前用。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\makeatletter
\let\ydzj@thebib\thebibliography
\let\ydzj@endthebib\endthebibliography
\renewenvironment{thebibliography}[1]{%
  \FloatBarrier
  \ydzj@needspace
  \ydzj@thebib{#1}%
}{%
  \ydzj@endthebib
}
\makeatother

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  10. 收尾
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\AtEndDocument{%
  \FloatBarrier
  \vfill
  \begin{center}\small\color{ydzjgrey}
  —— 本报告由 \ydzjname\ 撰写，格式遵循《月度总结规范 v1.0》——
  \end{center}
}

\endinput

