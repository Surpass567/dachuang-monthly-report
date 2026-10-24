"""Rebuild report month-three figure 2 as native, editable draw.io cells."""
from pathlib import Path
import shutil
import json
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / '逻辑月3_图2_UDF接口与实现流程.drawio'
NAVY = '#19364D'
BLUE = '#2869AB'
PALE = '#EDF4F8'
GREY = '#718393'

doc = ET.Element('mxfile', host='app.diagrams.net', agent='Codex', version='26.0.0', type='device')
diagram = ET.SubElement(doc, 'diagram', id='month3-figure2', name='UDF 接口与实现流程')
model = ET.SubElement(diagram, 'mxGraphModel', dx='1600', dy='900', grid='1', gridSize='10',
    guides='1', tooltips='1', connect='1', arrows='1', fold='1', page='1', pageScale='1',
    pageWidth='1600', pageHeight='900', math='0', shadow='0', background='#FFFFFF')
cells = ET.SubElement(model, 'root')
ET.SubElement(cells, 'mxCell', id='0')
ET.SubElement(cells, 'mxCell', id='1', parent='0')
layers = {}
for key, label in [('title','标题与说明'), ('A','A 常用接口'), ('B','B 密度代码'), ('C','C 编译挂接流程'), ('D','D 三种实现方式')]:
    layers[key] = 'layer-' + key
    ET.SubElement(cells, 'mxCell', id=layers[key], value=label, parent='0')

def node(id, value, x, y, w, h, *, layer='A', size=22, bold=False, color=NAVY,
         fill='none', stroke='none', align='left', font='Microsoft YaHei', spacing=0,
         rounded=False):
    style = (f'rounded={int(rounded)};whiteSpace=wrap;html=0;fillColor={fill};strokeColor={stroke};'
             f'fontColor={color};fontSize={size};fontFamily={font};fontStyle={int(bold)};'
             f'align={align};verticalAlign=middle;spacing={spacing};shadow=0;')
    cell = ET.SubElement(cells, 'mxCell', id=id, value=value, style=style, vertex='1', parent=layers[layer])
    ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})
    return id

def edge(id, source, target, points=()):
    cell = ET.SubElement(cells, 'mxCell', id=id, source=source, target=target, edge='1', parent=layers['C'],
        style=f'edgeStyle=orthogonalEdgeStyle;rounded=0;html=0;strokeColor={BLUE};strokeWidth=2;endArrow=block;endFill=1;')
    geo = ET.SubElement(cell, 'mxGeometry', relative='1', **{'as':'geometry'})
    if points:
        arr = ET.SubElement(geo, 'Array', **{'as':'points'})
        for x,y in points:
            ET.SubElement(arr, 'mxPoint', x=str(x), y=str(y))

def table(prefix, x, y, widths, rows, layer):
    for r, row in enumerate(rows):
        xx = x
        for c, (value, width) in enumerate(zip(row,widths)):
            node(f'{prefix}-{r}-{c}', value, xx, y+r*56, width, 56, layer=layer,
                size=21 if c == 0 else 22, bold=r==0, color='#FFFFFF' if r==0 else NAVY,
                fill=NAVY if r==0 else (PALE if r%2 else '#FFFFFF'),
                stroke='#FFFFFF', spacing=16)
            xx += width

node('title','UDF 初步学习 | 接口与实现流程',70,25,1460,65,layer='title',size=42,bold=True)
node('heading-A','A  常用接口及作用',70,115,650,45,size=28,bold=True)
table('interfaces',70,165,[370,280],[
    ['接口','用途'],
    ['DEFINE_PROPERTY','密度、黏度、导热系数'],
    ['DEFINE_SPECIFIC_HEAT','返回 Cp，并设置显热 *h'],
    ['DEFINE_ON_DEMAND','独立数值自检'],
], 'A')
node('heading-B','B  密度接口示例',930,115,610,45,layer='B',size=28,bold=True)
code = [
    'DEFINE_PROPERTY(water_rp_density,c,t)',
    '{',
    '  real T = C_T(c,t);',
    '  water_check_temperature(T);',
    '  return water_poly(T,a_rho);',
    '}',
]
for i, line in enumerate(code):
    node(f'code-{i}',line,930,174+29*i,620,31,layer='B',size=21,font='Consolas')
node('heading-C','C  编译与挂接流程',70,465,700,45,layer='C',size=28,bold=True)
flow = dict(layer='C', size=23, bold=True, color=BLUE, fill=PALE, stroke='#C4D6E5', align='center', rounded=True, spacing=5)
node('source','编写源码',70,540,170,60,**flow)
node('build','Build / Load',290,540,210,60,**flow)
node('material','材料挂接',550,540,170,60,**flow)
node('check','按需自检',70,650,170,60,**flow)
node('solve','重新求解与守恒检查',290,650,430,60,**flow)
edge('source-build','source','build')
edge('build-material','build','material')
edge('material-check','material','check',[(635,625),(155,625)])
edge('check-solve','check','solve')
node('checks','关键检查：Kelvin 温标、SI 单位、dh/dT = Cp',70,730,760,42,layer='C',size=22,color=GREY)
node('heading-D','D  三种水物性实现方式',930,465,650,45,layer='D',size=28,bold=True)
table('implementations',930,520,[155,495],[
    ['形式','求解期间的计算'],
    ['查表版','分段插值，无需 REFPROP DLL'],
    ['拟合版','多项式运算，无需 REFPROP DLL'],
    ['实时版','调用 REFPROP DLL'],
], 'D')
node('takeaway','学习要点：理解接口、物性单位和编译挂接流程，保持 Cp 与积分一致。',70,810,1480,42,
     layer='title',size=24,bold=True,color='#008C83')
node('scope','依据：已有水物性 UDF 源码与使用说明；本例范围为液态纯水 280–360 K、101325 Pa。',70,858,1480,30,
     layer='title',size=19,color=GREY)

ET.indent(doc, space='  ')
ET.ElementTree(doc).write(OUT, encoding='utf-8', xml_declaration=True)
shutil.copy2(ROOT/'reports/figs/udf_learning_interfaces.png', HERE/'原图2_udf_learning_interfaces.png')
vertices = cells.findall("mxCell[@vertex='1']")
edges = cells.findall("mxCell[@edge='1']")
assert len(vertices) >= 30 and len(edges) == 4
assert not any('image=' in c.get('style','') or 'image;' in c.get('style','') for c in vertices)
ids = [c.get('id') for c in cells]
assert len(ids) == len(set(ids))
for c in edges:
    assert c.get('source') in ids and c.get('target') in ids
validation = {'native_vertices':len(vertices),'native_connectors':len(edges),'embedded_raster_images':0,
              'unique_ids':True,'all_connectors_have_valid_endpoints':True,'source_figure':'reports/figs/udf_learning_interfaces.png'}
(HERE/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(OUT)
print(json.dumps(validation,ensure_ascii=False))
