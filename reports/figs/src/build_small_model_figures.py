from pathlib import Path
import json, csv, gc, sys
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

SIM = Path(__file__).resolve().parents[4]
WORK = SIM/'UDFwrite'
OUT = Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.sans-serif':['Microsoft YaHei','DejaVu Sans'], 'axes.unicode_minus':False,'font.size':9})
rows = list(csv.DictReader((Path(__file__).resolve().parent/'small_model_results.csv').open(encoding='utf-8-sig')))

def topology(f):
    g=f['meshes/1/faces/zoneTopology']
    names=b''.join(g['name'][:]).decode().split(';')
    return [dict(name=n,lo=int(a),hi=int(b)) for n,a,b in zip(names,g['minId'][:],g['maxId'][:])]

def surface(cas,dat,heat=False,normal=2,zone_name=None):
    with h5py.File(cas) as f,h5py.File(dat) as d:
        zs=topology(f)
        candidates=[z for z in zs if z['name'].startswith('heat')] if heat else [z for z in zs if z['name'].startswith('fluid') and z['name'].endswith('-solid')]
        if not heat and len(candidates)>1 and zone_name is None:
            all_polys=[];counts_total=0
            for zz in candidates:
                p,_,level,count=surface(cas,dat,heat,normal,zz['name']);all_polys.extend(p);counts_total+=count
            return all_polys,None,level,counts_total
        z=next(z for z in zs if z['name']==zone_name) if zone_name else candidates[0]
        counts=f['meshes/1/faces/nodes/1/nnodes'][:]
        offsets=np.r_[0,np.cumsum(counts,dtype=np.int64)]
        ids=f['meshes/1/faces/nodes/1/nodes'][offsets[z['lo']-1]:offsets[z['hi']]].astype(np.int64)
        unique,inv=np.unique(ids,return_inverse=True)
        coords=next(iter(f['meshes/1/nodes/coords'].values()))
        pts=coords[unique-int(coords.attrs['minId'][0])][inv]*1000
        cs=counts[z['lo']-1:z['hi']]; offs=np.r_[0,np.cumsum(cs,dtype=np.int64)]
        # Select planar horizontal faces. No interpolation or reconstructed geometry.
        lo=np.minimum.reduceat(pts[:,normal],offs[:-1]); hi=np.maximum.reduceat(pts[:,normal],offs[:-1])
        horizontal=np.abs(hi-lo)<1e-7
        levels,n=np.unique(np.round(lo[horizontal],6),return_counts=True)
        level=float(levels[np.argmax(n)])
        mask=horizontal & (np.abs(lo-level)<1e-6)
        indices=np.where(mask)[0]
        plane=[i for i in range(3) if i!=normal]
        polygons=[pts[offs[i]:offs[i+1]][:,plane] for i in indices]
        vals=None
        if heat:
            a=np.full(z['hi']-z['lo']+1,np.nan)
            for ds in d['results/1/phase-1/faces/SV_T'].values():
                l=int(ds.attrs['minId'][0]);h=int(ds.attrs['maxId'][0]);ll=max(l,z['lo']);hh=min(h,z['hi'])
                if ll<=hh:a[ll-z['lo']:hh-z['lo']+1]=ds[ll-l:hh-l+1]
            vals=a[indices]-273.15
            assert np.isfinite(vals).all()
        return polygons,vals,level,len(indices)

def paths(row):
    if row['编号'] in ['M14','M15','M16','M17']:
        name={'M14':'NACA0016_v2','M15':'NACA1416_v2','M16':'NACA3416_v2','M17':'A_leaf'}[row['编号']]
        return WORK/f'small_model_extract_work/{name}.cas.h5', WORK/f'small_model_extract_work/{name}.dat.h5'
    return SIM/row['Case源文件'],SIM/row['Data源文件']

manifest=[]
def group(identifiers,labels,filename):
    fig,axes=plt.subplots(2,3,figsize=(10.5,6.4),layout='constrained')
    for col,(ident,label) in enumerate(zip(identifiers,labels)):
        row=next(r for r in rows if r['编号']==ident);cas,dat=paths(row)
        print('Extract',ident,flush=True)
        item={'id':ident,'case':str(cas),'data':str(dat),'panels':[]}
        for rr in range(2):
            normal=1 if ident=='M02' else 2
            polys,vals,level,count=surface(cas,dat,rr==1,normal)
            ax=axes[rr,col]
            if rr==0:
                pc=PolyCollection(polys,facecolor='#cbdce8',edgecolor='#4c6a80',linewidths=.10,rasterized=True)
                title=f'{label}\n流固界面网格  {"xyz"[normal]}={level:g} mm'
            else:
                pc=PolyCollection(polys,array=vals,cmap='inferno',edgecolor='face',linewidths=0,rasterized=True)
                title=f'加热面温度  '+('稳态' if ident=='M17' else f't={float(row["保存时刻 (s)"]):g} s')
                cb=fig.colorbar(pc,ax=ax,shrink=.72,pad=.02);cb.set_label('温度 (°C)',fontsize=8)
            ax.add_collection(pc);ax.autoscale_view();ax.set_aspect('equal');ax.set_title(title,fontsize=9)
            ax.set_xlabel('x (mm)');ax.set_ylabel('z (mm)' if normal==1 else 'y (mm)');ax.tick_params(labelsize=7)
            item['panels'].append({'surface':'heat' if rr else 'fluid-solid','z_mm':level,'face_count':count,'range_C':[float(vals.min()),float(vals.max())] if vals is not None else None})
            del polys;gc.collect()
        manifest.append(item)
    fig.savefig(OUT/filename,dpi=260,facecolor='white');plt.close(fig)

group(['M02','M09','M17'],['六边形 v4.2','gao2.1','叶脉 A_leaf'],'month2_other_models.png')
group(['M14','M15','M16'],['NACA0016 v2','NACA1416 v2','NACA3416 v2'],'month2_naca_models.png')
(OUT/'src/figure_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
