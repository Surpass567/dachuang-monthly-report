from pathlib import Path
import json,csv,hashlib,re,ast
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

SRC=Path(__file__).resolve().parent
FIG=SRC.parents[1]
E=SRC/'evidence'
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'],'font.size':10,'axes.unicode_minus':False,'axes.spines.top':False,'axes.spines.right':False})
d=np.load(E/'pid_sim.npz')
t,T,U=d['t'],d['T'],d['U'];n=len(t)
metrics={'samples':n,'dt_s':float(t[1]-t[0]),'time_start_s':float(t[0]),'time_end_s':float(t[-1]),'Tmin_C':float(T.min()),'Tmax_C':float(T.max()),'full_peak_above_target_K':float(T.max()-68),'latter_half_peak_above_target_K':float(T[n//2:].max()-68),'mean_opening_pct':float(U.mean()),'upper_opening_samples_pct':float((U>=100-1e-10).mean()*100),'clamp_switch_max_T_difference_K':float(np.max(np.abs(T-d['T_nc']))),'clamp_switch_max_U_difference_pct':float(np.max(np.abs(U-d['U_nc']))),'Imax_clamped':float(d['I'].max()),'Imax_unclamped':float(d['I_nc'].max())}
# Execute only original definitions and inputs; skip top-level saving and plotting.
tree=ast.parse((E/'PID仿真.py').read_text(encoding='utf8'))
allowed={'TARGET','T_AMB','HEAT_BASE','HEAT_AMP','HEAT_T','A_HEAT','K_MIN','K_MAX','B_NAT','DT','T_END','KP','KI','KD','t','n','heat'}
nodes=[]
for node in tree.body:
    if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef)):nodes.append(node)
    elif isinstance(node,ast.Assign):
        names={n.id for target in node.targets for n in ast.walk(target) if isinstance(n,ast.Name)}
        if names and names<=allowed:nodes.append(node)
ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),'PID original definitions','exec'),ns)
check=ns['simulate'](8,.5,2,clamp=True)
assert np.array_equal(check[0],T) and np.array_equal(check[1],U)
metrics['upper_clip_events_pct']=check[4]/n*100
(SRC/'pid_verified_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf8')
fig,axes=plt.subplots(3,1,figsize=(9,7.5),sharex=True,layout='constrained')
axes[0].plot(t,d['heat'],color='#777777',ls='--',label='热源温度信号（模型输入）')
axes[0].plot(t,T,color='#b64d39',label='简化模型被控温度')
axes[0].axhline(68,color='#175d91',ls=':',label='设定值 68 °C')
axes[0].set_ylabel('温度 (°C)');axes[0].legend(ncol=2,fontsize=8)
axes[0].set_title('已有增量式 PID 数组的只读复核：0–89.95 s，采样间隔 0.05 s')
axes[1].plot(t,U,color='#175d91');axes[1].axhline(100,color='#b64d39',ls='--',lw=.8)
axes[1].set_ylabel('抽象执行量 (%)');axes[1].set_ylim(-5,110)
axes[1].text(.02,.83,f'上限采样占比 {metrics["upper_opening_samples_pct"]:.2f}%  |  超上限裁剪事件 {metrics["upper_clip_events_pct"]:.2f}%',transform=axes[1].transAxes,fontsize=9)
axes[2].plot(t,d['I'],color='#008477',label='限幅累计误差')
axes[2].plot(t,d['I_nc'],color='#d08b22',ls='--',label='不限幅累计误差')
axes[2].set_ylabel('累计误差（离散和）');axes[2].set_xlabel('保存的时间坐标 (s)');axes[2].legend(fontsize=8)
for ax in axes:ax.grid(alpha=.18);ax.set_xlim(0,90)
fig.savefig(FIG/'midterm_asset_pid_verified.png',dpi=240,facecolor='white');plt.close(fig)

def planar_polygons(path,zplane=.25):
    with h5py.File(path) as f:
        g=f['meshes/1/faces/zoneTopology']; names=b''.join(g['name'][:]).decode().split(';')
        zones=[(int(a),int(b)) for name,a,b in zip(names,g['minId'][:],g['maxId'][:]) if name.startswith('fluid') and name.endswith('-solid')]
        counts=f['meshes/1/faces/nodes/1/nnodes'][:];offs=np.r_[0,np.cumsum(counts,dtype=np.int64)]
        c=next(iter(f['meshes/1/nodes/coords'].values()));cmin=int(c.attrs['minId'][0])
        polys=[]
        for lo,hi in zones:
            ids=f['meshes/1/faces/nodes/1/nodes'][offs[lo-1]:offs[hi]].astype(np.int64)
            unique,inv=np.unique(ids,return_inverse=True);pts=c[unique-cmin][inv]*1000
            nn=counts[lo-1:hi];off=np.r_[0,np.cumsum(nn,dtype=np.int64)]
            mins=np.minimum.reduceat(pts[:,2],off[:-1]);maxs=np.maximum.reduceat(pts[:,2],off[:-1])
            mask=(np.abs(mins-zplane)<1e-6)&(np.abs(maxs-zplane)<1e-6)
            polys.extend([pts[off[i]:off[i+1],:2] for i in np.where(mask)[0]])
        assert polys
        return polys

raw=list(csv.DictReader((E/'raw_02s.csv').open(encoding='utf-8-sig')))
fig,axes=plt.subplots(2,3,figsize=(10,6.1),layout='constrained')
mesh_manifest=[]
for col,grid in enumerate([2943269,3235081,4610769]):
    row=next(r for r in raw if int(r['grid'])==grid)
    print('mesh',grid,flush=True);polys=planar_polygons(row['cas'])
    for rr in range(2):
        ax=axes[rr,col];pc=PolyCollection(polys,facecolor='#dfebf2',edgecolor='#3b6077',linewidths=.16,rasterized=True)
        ax.add_collection(pc);ax.autoscale_view();ax.set_aspect('equal');ax.set_xlabel('x (mm)');ax.set_ylabel('y (mm)')
        if rr==0:ax.set_title(f'{grid:,} 单元\nz=0.25 mm 流固界面')
        else:ax.set_xlim(1.4,2.5);ax.set_ylim(1.0,1.8);ax.set_title('同一局部区域放大')
    mesh_manifest.append({'grid':grid,'case':row['cas'],'plane_z_mm':.25,'face_count':len(polys)})
fig.savefig(FIG/'midterm_asset_naca_mesh_actual.png',dpi=280,facecolor='white');plt.close(fig)
(SRC/'mesh_figure_manifest.json').write_text(json.dumps(mesh_manifest,ensure_ascii=False,indent=2),encoding='utf8')

source_inventory=[]
for p in sorted((SRC/'monthly_sources').glob('*.tex')):
    s=p.read_text(encoding='utf8')
    source_inventory.append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tables':[{'label':re.search(r'\\label\{([^}]+)\}',b).group(1) if re.search(r'\\label\{([^}]+)\}',b) else None,'text':b} for b in re.findall(r'\\begin\{table\}.*?\\end\{table\}',s,re.S)],'images':re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',s)})
(SRC/'monthly_inventory.json').write_text(json.dumps(source_inventory,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(metrics,ensure_ascii=False),flush=True)
