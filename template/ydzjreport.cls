%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ydzjreport.cls  ——  月度（阶段）总结报告 文档类
%  版本 v1.0
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
\ProvidesClass{ydzjreport}[2026/10/08 v1.0 月度阶段总结报告]

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
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{ulem}
\RequirePackage[hidelinks]{hyperref}

\geometry{left=2.2cm,right=2.2cm,top=2.4cm,bottom=2.2cm}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  2. 中文粗体
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ctex 已提供 \heiti / \songti / \kaishu，直接用黑体做粗体
\renewcommand{\textbf}[1]{{\heiti #1}}
\newcommand{\hei}{\heiti}
\newcommand{\song}{\songti}
\newcommand{\kai}{\kaishu}

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
  \begin{center}
    {\LARGE\heiti\color{ydzjblue} #1}\\[6pt]
    {\small\color{ydzjgrey}\ydzjperiod}
  \end{center}
  \vspace{2pt}
  \ydzjmetatable
  \vspace{6pt}
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
%       \makestageonehead 会产生输出（表格、颜色、字号），
%       必须在 \begin{document} 之后调用，否则报
%       "Missing \begin{document}"。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\stageonesetup}[6]{%
  \gdef\ydzjstage{#1}%
  \gdef\ydzjname{#2}%
  \gdef\ydzjfield{#3}%
  \gdef\ydzjperiod{#4}%
  \gdef\ydzjkeywords{#5}%
  \gdef\ydzjsummary{#6}%
  \setshorttitle{月度阅读总结 \(\cdot\) 阶段一}%
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
  \setshorttitle{月度总结 \(\cdot\) 阶段二}%
  \setauthor{\ydzjname}%
}
\newcommand{\makestagetwohead}{%
  \ydzjmakereporthead{月度总结 \(\cdot\) 阶段二（研究推进）}%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  8. 常用盒子
%     用法：
%       \note ... \noteend            注意事项（黄色边框）
%       \keypoint ... \keypointend    要点提示（蓝色边框）
%
%     实现说明（踩过的坑，别改回去）：
%       · 不要用 \colorbox{\begin{minipage}...\end{minipage}}：
%         \colorbox 的参数会在读到 minipage 开始后就被闭合，
%         导致 "Extra }, or forgotten \endgroup"。
%       · 不要给 \newenvironment 的第一个参数组里塞 math/figure 等，
%         否则报 "File ended while scanning use of \@newenv"。
%       · 环境名不要用 \note / \endnote（\endnote 已被占用）。
%       这里用「整行 minipage + 上下彩色横线」，最稳且不需要额外宏包。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newenvironment{ydzjnotebox}%
  {\par\medskip\noindent\begin{minipage}{\linewidth}%
   \color{ydzjwarnline}\hrule height 1.2pt\vspace{3pt}\par
   \small\color{black}}%
  {\vspace{3pt}\par\color{ydzjwarnline}\hrule height 1.2pt%
   \end{minipage}\par\medskip}

\newenvironment{ydzjkeybox}%
  {\par\medskip\noindent\begin{minipage}{\linewidth}%
   \color{ydzjblueii}\hrule height 1.2pt\vspace{3pt}\par
   \small\color{black}}%
  {\vspace{3pt}\par\color{ydzjblueii}\hrule height 1.2pt%
   \end{minipage}\par\medskip}

\newcommand{\note}{\begin{ydzjnotebox}}
\newcommand{\noteend}{\end{ydzjnotebox}}
\newcommand{\keypoint}{\begin{ydzjkeybox}}
\newcommand{\keypointend}{\end{ydzjkeybox}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  9. 表格便利命令
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 表头行：\tablehead{列1 & 列2 & 列3}
\newcommand{\tablehead}[1]{%
  \rowcolor{ydzjlight}\textbf{#1} \tabularnewline \midrule
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  10. 收尾
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\AtEndDocument{%
  \vfill
  \begin{center}\small\color{ydzjgrey}
  —— 本报告由 \ydzjname\ 撰写，格式遵循《月度总结规范 v1.0》——
  \end{center}
}

\endinput

