%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  midterm.cls  ——  中期检查报告正式版式
%
%  设计依据：国内高校大学生创新创业训练计划「中期检查报告」的通行格式，
%            以及学位论文/研究报告的常规排版惯例：
%              · 封面（项目名称、组员、负责人、指导教师、日期）
%              · 目录
%              · 一级标题「一、」黑体三号居中；二级「1.1」黑体四号；
%                三级「1.1.1」黑体小四；均为黑色，不使用彩色
%              · 正文宋体小四，1.5 倍行距，首行缩进 2 字符
%              · 图题在下、表题在上，宋体五号居中，编号「图 1-1」
%              · 三线表，表头浅灰底
%              · 页脚居中页码
%
%  与 ydzjreport.cls 的接口兼容：保留 \TBD / \pending / \planned /
%  \placeholderbox / \placeholderfigure / \placeholderpair / \reportfigure /
%  \ydzjname / \ydzjclosingnote / \ydzjlight 等名称，正文无需改动。
%
%  用法：
%    导言区：\midtermsetup{标题}{组员}{项目名}{期间}{关键词}{摘要}
%    正文首：\makecover   然后 \tableofcontents
%
%  编译：xelatex 跑两遍
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{midterm}[2026/10/24 v1.0 中期检查报告正式版式]

% 忽略外部传入的其它选项（如 stage2 / fontset=...），避免报未知选项
\DeclareOption*{}
\ProcessOptions\relax

\LoadClass[UTF8,a4paper,zihao=-4]{ctexart}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  1. 页面
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage[
  a4paper,
  top=2.54cm, bottom=2.54cm,
  left=3.17cm, right=3.17cm,
  headheight=15pt, headsep=0.7cm, footskip=1.1cm
]{geometry}

\linespread{1.5}          % 1.5 倍行距
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}
\raggedbottom

% 中文断行（XeLaTeX 必需，否则中文长段落会超框）
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt minus 0.1pt
\tolerance=3000
\emergencystretch=3em

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  2. 宏包
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\RequirePackage{graphicx}
\RequirePackage[table]{xcolor}
\RequirePackage{booktabs}
\RequirePackage{tabularx}
\RequirePackage{longtable}
\RequirePackage{multirow}
\RequirePackage{ragged2e}
\RequirePackage{enumitem}
\RequirePackage{float}
\RequirePackage{placeins}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{bm}
\RequirePackage{fancyhdr}
\RequirePackage{etoolbox}
\RequirePackage{needspace}
\RequirePackage[unicode,bookmarksnumbered=true]{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=black, citecolor=black, urlcolor=black,
  bookmarksopen=true
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  3. 颜色（正式版式只用黑、灰，保留模板同名颜色以兼容正文）
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\definecolor{ydzjlight}{gray}{0.93}   % 表头浅灰底（原为浅蓝，改为灰）
\definecolor{ydzjgrey}{gray}{0.35}
\definecolor{ydzjrule}{gray}{0.65}
\definecolor{ydzjblue}{gray}{0.15}
\definecolor{ydzjblueii}{gray}{0.25}
\definecolor{ydzjblueiii}{gray}{0.35}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  4. 表格列类型与间距（正文使用 Y / C 列）
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcolumntype{Y}{>{\RaggedRight\arraybackslash}X}
\newcolumntype{C}{>{\Centering\arraybackslash}X}
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.22}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  5. 标题格式（黑色黑体，中文数字一级标题）
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}

\ctexset{
  section = {
    name   = {,、},
    number = \chinese{section},
    format = \centering\heiti\zihao{3},
    aftername = {},
    beforeskip = 2.2ex plus .3ex minus .2ex,
    afterskip  = 1.8ex plus .2ex,
  },
  subsection = {
    number = \arabic{section}.\arabic{subsection},
    format = \heiti\zihao{4}\raggedright,
    beforeskip = 1.6ex plus .2ex minus .2ex,
    afterskip  = 1.2ex plus .2ex,
  },
  subsubsection = {
    number = \arabic{section}.\arabic{subsection}.\arabic{subsubsection},
    format = \heiti\zihao{-4}\raggedright,
    beforeskip = 1.3ex plus .2ex minus .2ex,
    afterskip  = 1.0ex plus .2ex,
  },
  paragraph = {
    format = \heiti\zihao{-4}\raggedright,
  },
}

% 目录标题
\renewcommand{\contentsname}{目\hspace{1em}录}
\ctexset{
  contentsname = {目\hspace{1em}录},
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  5. 图题、表题
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\captionsetup{
  font = {small},        % 五号
  labelsep = quad,
  skip = 6pt,
}
\captionsetup[table]{position=top}
\captionsetup[figure]{position=bottom}

% 编号：图 1-1、表 1-1（按一级标题分组）
\renewcommand{\thefigure}{\thesection-\arabic{figure}}
\renewcommand{\thetable}{\thesection-\arabic{table}}
\@addtoreset{figure}{section}
\@addtoreset{table}{section}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  6. 页眉页脚
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\songti\ydzjshorttitle}
\fancyhead[R]{\small\songti 中期检查报告}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% 封面页不要页眉页脚
\newcommand{\ydzjplainstyle}{\thispagestyle{empty}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  7. 元信息与封面
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\ydzjshorttitle}{}
\newcommand{\setshorttitle}[1]{\gdef\ydzjshorttitle{#1}}

\newcommand{\midtermsetup}[6]{%
  \gdef\ydzjstage{#1}%
  \gdef\ydzjname{#2}%
  \gdef\ydzjfield{#3}%
  \gdef\ydzjperiod{#4}%
  \gdef\ydzjkeywords{#5}%
  \gdef\ydzjsummary{#6}%
  \setshorttitle{#1}%
}

% 兼容旧接口
\newcommand{\stagetwosetup}[6]{\midtermsetup{#1}{#2}{#3}{#4}{#5}{#6}}
\newcommand{\makestagetwohead}{\makecover}

% 封面上的可填写项（未知信息留横线，不编造）
\newcommand{\ydzjprojno}{}
\newcommand{\ydzjmajor}{}
\newcommand{\ydzjadviser}{}
\newcommand{\ydzjleader}{}
\newcommand{\setprojno}[1]{\gdef\ydzjprojno{#1}}
\newcommand{\setleader}[1]{\gdef\ydzjleader{#1}}
\newcommand{\setadviser}[1]{\gdef\ydzjadviser{#1}}
\newcommand{\setmajor}[1]{\gdef\ydzjmajor{#1}}

\newcommand{\coverrule}[2]{%
  \noindent
  \makebox[5.4em][s]{\heiti\zihao{4}#1}%
  \underline{\makebox[0.60\textwidth][c]{\zihao{-4}#2}}\par\vspace{0.95em}}

\newcommand{\makecover}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \centering
    \vspace*{1.2cm}

    {\heiti\zihao{2} 大学生创新创业训练计划\par}
    \vspace{0.8cm}
    {\heiti\zihao{1} 中期检查报告\par}

    \vspace{2.2cm}

    {\heiti\zihao{3}\ydzjfield\par}

    \vspace{2.8cm}

    \zihao{4}
    \begin{center}
      \coverrule{项目类别}{（创新创业训练）}
      \coverrule{项目编号}{\ydzjprojno}
      \coverrule{项目负责人}{\ydzjleader}
      \coverrule{项目组成员}{\ydzjname}
      \coverrule{指导教师}{\ydzjadviser}
      \coverrule{所在学院}{\ydzjmajor}
    \end{center}

    \vfill
    {\heiti\zihao{4}\ydzjperiod\par}
    \vspace{1.2cm}
  \end{titlepage}
  \clearpage
  \pagenumbering{roman}
  \tableofcontents
  \clearpage
  \pagenumbering{arabic}
  \setcounter{page}{1}
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  8. 常用标记（与 ydzjreport 兼容）
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\DeclareRobustCommand{\TBD}[1]{{\color{ydzjgrey}\textbf{【待补充：#1】}}}
\newcommand{\pending}[1]{\par\noindent\textbf{证据补充与适用边界：}#1\par}
\newcommand{\planned}[1]{\par\noindent\textbf{后续拟开展：}#1\par}
\newcommand{\ydzjclosingnote}{}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  9. 图片占位框（图片暂缺时用框占位）
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\placeholderbox}[2]{%
  \begingroup\setlength{\fboxsep}{8pt}%
  \fbox{\begin{minipage}[c][#2][c]{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}%
  \centering\small\songti\textbf{【此处为图位】}\par\medskip #1\par
  \end{minipage}}\endgroup}

\newcommand{\reportfigure}[4]{%
  \begin{figure}[!htbp]\centering
  \includegraphics[width=#4]{#3}\caption{#2}\label{#1}\end{figure}}

\newcommand{\placeholderfigure}[4]{%
  \begin{figure}[!htbp]\centering
  \placeholderbox{#3}{#4}\caption{#2}\label{#1}\end{figure}}

\newcommand{\placeholderpair}[7]{%
  \begin{figure}[!htbp]\centering
  \begin{subfigure}[t]{0.48\linewidth}\centering
    \placeholderbox{#4}{#7}\caption{#3}\label{#1:a}
  \end{subfigure}\hfill
  \begin{subfigure}[t]{0.48\linewidth}\centering
    \placeholderbox{#6}{#7}\caption{#5}\label{#1:b}
  \end{subfigure}
  \caption{#2}\label{#1}\end{figure}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  10. 列表与其它微调
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\setlist[itemize]{leftmargin=2.2em, itemsep=2pt, topsep=4pt}
\setlist[enumerate]{leftmargin=2.4em, itemsep=2pt, topsep=4pt}

% 浮动体参数
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.8}
\renewcommand{\textfraction}{0.08}
\renewcommand{\floatpagefraction}{0.75}

\endinput
