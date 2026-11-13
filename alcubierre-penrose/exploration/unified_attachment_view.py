"""A single attachment picture using one injective global coordinate map.

Uses the checked convex coordinate map, followed by a smooth invertible
display stretch. Height is not temporal. Only the front/future geometry
is shown; no separate cap/scri panels or independently placed surfaces.
"""
import json
from pathlib import Path
import numpy as np
from scipy.special import expit
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.lines import Line2D
import global_convex_conformal as globalmap
import useful_2p1_view as view

OUT=view.OUT
GREEN='#21836b';ORANGE=view.SEND;RIM='#a74054'


def display(z):
    z=np.asarray(z);x=z[...,1]
    xx=x+.24*np.logaddexp(0,(x-1.1)/.08)
    yy=z[...,2]+.4*expit((x-1.15)/.06)*np.tanh(z[...,2]/.04)
    return np.stack([z[...,0]+2*x,xx,yy],axis=-1)


def grid(name,z,color,alpha):
    n,m=z.shape[:2]
    return dict(name=name,vertices=display(z).reshape(-1,3).tolist(),
                faces=globalmap.grid_faces(n,m).tolist(),color=color,opacity=alpha)


def make_scene():
    h=view.cap.build_horizon();um=-h.C/2
    meshes=[];lines=[];points=[]
    def line(name,z,color,width=2):
        lines.append(dict(name=name,points=display(z).tolist(),color=color,width=width))
    def point(name,z,color):points.append(dict(name=name,point=display(z).tolist(),color=color))
    # Whole ordinary future scri, cut off only at very large |u|.
    hv=np.linspace(-.995,.995,42);us=2*hv/(1-hv*hv)
    uu,theta=np.meshgrid(us,np.linspace(-np.pi,np.pi,110),indexing='ij')
    meshes.append(grid('Future null infinity',globalmap.scri_map(uu,theta),GREEN,.13))
    for u in [-10.,0.,10.]:
        line('Null-infinity cuts',globalmap.scri_map(u,np.linspace(-np.pi,np.pi,180)),GREEN,.7)
    for angle in [0.,np.pi]:
        line('Axial directions on null infinity',globalmap.scri_map(us,angle),GREEN,1.5)
    # Cap is a boundary value of THE SAME map. Lambda finite is regular.
    k,y=np.meshgrid(np.linspace(-.995,.995,65),np.linspace(-.6,.6,33),indexing='ij')
    lam=k/np.sqrt(1-k*k)
    meshes.append(grid('Open cap strip',globalmap.cap_map(0.,lam,y),ORANGE,.65))
    ls=np.linspace(-.999,.999,220);ls=ls/np.sqrt(1-ls*ls)
    for yrim in [-.6,.6]:line('Excluded cap rims',globalmap.cap_map(0.,ls,yrim),RIM,2.5)
    line('C+ curve',globalmap.cap_map(0.,0.,np.linspace(-.6,.6,100)),ORANGE,4)
    # Physical sheet: matched continuous surface across planar patch and wings.
    ys=np.r_[np.linspace(-5,-.65,95),np.linspace(-.65,.65,100),np.linspace(.65,5,95)]
    ts=np.r_[np.linspace(0,2,150),np.linspace(2.03,6,100)]
    yy,tt=np.meshgrid(ys,ts)
    meshes.append(grid('Sending horizon sheet',globalmap.coordinates(tt,h.h(yy),yy),ORANGE,.08))
    yc,tc=np.meshgrid(np.linspace(-.6,.6,35),np.r_[np.linspace(0,2,200),np.linspace(2.05,24,140)])
    meshes.append(grid('Planar patch to the cap',globalmap.coordinates(tc,np.ones_like(tc),yc),ORANGE,.18))
    for t in [0.,2.,5.]:
        line('Horizon time sections',globalmap.coordinates(t,h.h(ys),ys),ORANGE,.7)
    # Extra exterior chart samples, still passed through the same global map,
    # resolve the two wings all the way to their exact scri boundary values.
    defects=np.linspace(.002,4,55);rs=np.r_[0,np.geomspace(1e-6,.65,65)]
    rr,dd=np.meshgrid(rs,defects)
    for sign in [-1,1]:
        for branch in [-1,1]:
            angle=sign*(np.pi/3+branch*np.arccos(np.clip(1-rr*dd,-1,1)))
            R=1/np.maximum(rr,1e-6);u=um-dd;t=R+u
            y=R*np.sin(angle);x=R*np.cos(angle)-2*t
            valid=(rr*dd<2)&(sign*y>view.cap.Y_EXTERIOR+.025)&(t>=0)
            # Exclude invalid cells rather than bridging clipped-away regions.
            z=globalmap.coordinates(t,x,y);z[:,0]=globalmap.scri_map(u[:,0],sign*np.pi/3)
            n,m=rr.shape;faces=globalmap.grid_faces(n,m)
            keep=np.all(valid.reshape(-1)[faces],axis=1)
            meshes.append(dict(name='Exterior wings to null infinity',vertices=display(z).reshape(-1,3).tolist(),faces=faces[keep].tolist(),color=ORANGE,opacity=.09))
        line('Wing contact on null infinity',globalmap.scri_map(np.r_[-500.,np.linspace(-35,um,160)],sign*np.pi/3),ORANGE,3)
        point('Q+' if sign>0 else 'Q−',globalmap.scri_map(um,sign*np.pi/3),ORANGE)
    # Actual null generators from the near bubble wing through the flat tail.
    def rhs(t,z):
        y=z[0];v=float(view.cap.shift(float(h.h(y)),y))
        return [np.sqrt(max(v*v-1,0))/(-v)]
    back=solve_ivp(rhs,[0,-12],[.85],rtol=2e-11,atol=1e-12,dense_output=True,max_step=.05)
    ahead=solve_ivp(rhs,[0,800],[.85],rtol=2e-11,atol=1e-12,dense_output=True,max_step=.5)
    ts=np.r_[0.,np.geomspace(.001,800,900)]
    ys=np.where(ts<0,back.sol(np.minimum(ts,0))[0],ahead.sol(np.maximum(ts,0))[0])
    generator_errors=[]
    for sign in [-1,1]:
        z=globalmap.coordinates(ts,h.h(ys),sign*ys)
        target=globalmap.scri_map(um,sign*np.pi/3)
        generator_errors.append(float(np.linalg.norm(z[-1]-target)))
        line('Wing null generators',np.vstack([z,target]),ORANGE,3)
    # Planar generator approaches its C+ point, never a scri point.
    ts=np.linspace(0,24,900)
    for y in [-.3,.3]:
        z=globalmap.coordinates(ts,np.ones_like(ts),np.full_like(ts,y))
        line('Planar null generators',np.vstack([z,globalmap.cap_map(0.,0.,y)]),ORANGE,2.3)
    # Same massive traveler as the preceding figures; continue only in the cap.
    collar=view.FrontCollar('cap');sol,cross=collar.geodesic()
    tau=np.linspace(0,sol.t[-1],600);p,q=sol.sol(tau)[:2]
    x=np.array([collar.x_from_product(v) for v in p*q]);Q=collar.pq_factors(x)[1]
    qb=q/Q;ll=(x-1)/qb;z=np.empty((len(tau),3));mask=qb>0
    z[mask]=globalmap.coordinates(-np.log(qb[mask]),x[mask],.3)
    z[~mask]=globalmap.cap_map(qb[~mask],ll[~mask],.3)
    line('Traveler',z,view.TRAVELER,3)
    lc=-2*sol.sol(cross)[0]/collar.scale
    point('E: crossing',globalmap.cap_map(0.,lc,.3),view.TRAVELER)
    ts=np.linspace(0,24,500)
    line('Rider',globalmap.coordinates(ts,0*ts,0*ts),'#27323a',2)
    point('Rider end',globalmap.stationary_end(0.,0.),'#27323a')
    # No boundary shell or artificial cap-to-scri bridge is added.
    scene=dict(meshes=meshes,lines=lines,points=points)
    return scene,dict(generator_coordinate_endpoint_errors=generator_errors,
        display_map='(Zt+2Zx, Zx+0.24 softplus((Zx-1.1)/0.08), Zy+0.4 sigmoid((Zx-1.15)/0.06) tanh(Zy/0.04))',
        display_injectivity='dX/dZx=1+3 sigmoid>0; dY/dZy=1+10 sigmoid sech^2>0; Zt recovered by subtraction',
        height_is_physical_time=False,
        scope='Single coordinate attachment picture of front/future surfaces; no smooth rim bridge or maximal-extension claim')


def draw(scene):
    fig=plt.figure(figsize=(13,10),facecolor='white');ax=fig.add_axes([.03,.13,.94,.74],projection='3d')
    for mesh in scene['meshes']:
        v=np.array(mesh['vertices']);f=np.array(mesh['faces'])
        ax.add_collection3d(Poly3DCollection(v[f][:,:,[1,2,0]],facecolors=mesh['color'],edgecolors='none',alpha=mesh['opacity']))
    for l in scene['lines']:
        v=np.array(l['points']);ax.plot(v[:,1],v[:,2],v[:,0],color=l['color'],lw=l['width']*.75)
    for p in scene['points']:
        v=np.array(p['point']);ax.scatter(v[1],v[2],v[0],color=p['color'],s=30,zorder=10)
        if p['name'].startswith('Q'):ax.text(v[1]+.025,v[2],v[0]+.045,p['name'],fontsize=10,color=p['color'])
    capcenter=display(globalmap.cap_map(0.,0.,0.))
    ax.set(xlim=(-1.1,3.2),ylim=(-1.3,1.3),zlim=(-1.4,3.25))
    ax.set_box_aspect([4.3,2.6,4.65],zoom=1.35);ax.view_init(elev=32,azim=-35)
    ax.set_axis_off()
    from mpl_toolkits.mplot3d import proj3d
    def label(text,z,xy,color):
        v=display(z);px,py,_=proj3d.proj_transform(v[1],v[2],v[0],ax.get_proj())
        ax.annotate(text,xy=(px,py),xycoords='data',xytext=xy,textcoords='axes fraction',color=color,fontsize=11,
                    arrowprops=dict(arrowstyle='-',color=color,lw=1),ha='left')
    label('Open cap strip\n(red edges: excluded rims)',globalmap.cap_map(0.,1.,.2),(.77,.87),ORANGE)
    label('Ordinary future\nnull infinity',globalmap.scri_map(0.,-np.pi/2),(.08,.30),GREEN)
    label('Traveler crosses here',globalmap.cap_map(0.,-.62,.3),(.73,.68),view.TRAVELER)
    label('C⁺ curve: planar\ngenerator endpoints',globalmap.cap_map(0.,0.,-.3),(.73,.55),ORANGE)
    fig.suptitle('Cap strip, horizon wings and null infinity — in one coordinate picture',fontsize=17,y=.96)
    fig.text(.5,.91,'Orange: one horizon sheet, from its planar cap patch to its outer wings. Green: ordinary future null infinity.',ha='center',fontsize=11,color='#52616b')
    handles=[Line2D([],[],color=ORANGE,lw=3,label='Horizon and cap'),Line2D([],[],color=GREEN,lw=3,label='Null infinity'),Line2D([],[],color=RIM,lw=2,label='Excluded rims'),Line2D([],[],color=view.TRAVELER,lw=3,label='Traveler')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.075),ncol=4,frameon=False)
    fig.text(.5,.035,'One injective map, with a smooth stretch to make the cap visible. Height is a plotting coordinate, not time.\nThe cap and null infinity remain separate; the horizon sheet connects their neighborhoods. Only front/future surfaces are shown.',ha='center',fontsize=10,color='#52616b')
    for suffix in ['png','svg']:fig.savefig(OUT/f'unified_attachments.{suffix}',dpi=180)
    plt.close(fig)


def write_viewer(scene):
    template=Path(__file__).with_name('global_convex_viewer.html').read_text(encoding='utf-8')
    template=template.replace('Alcubierre spacetime — global conformal metric domain','Alcubierre bubble — unified attachment view')
    start=template.index('<header>');end=template.index('<script>')
    html='''<header><h1>Cap, horizon wings and null infinity in one picture</h1><p class="sub">Every surface uses the same global coordinate map and the same smooth display stretch. Rotate to see the cap strip and the two wing contacts. Height is not physical time.</p></header>
<main><div class="view"><canvas id="plot"></canvas><div class="badge">Drag to rotate · scroll to zoom · shift-drag to pan.<br>One attachment map, not a flat-cone Penrose embedding.</div></div><aside>
<h2>Camera</h2><button id="global">All attachments</button><button id="front">Cap and wings</button><button id="rear">Null infinity</button>
<h2>Visible geometry</h2><div id="layers"></div>
<p class="note">The solid orange curves are null generators. Planar generators end on the C+ curve of the open cap strip. Outer generators end at Q+ and Q− on green null infinity.</p>
<p class="note">Magenta: the same traveler crossing at E. Red: excluded cap rims. Black: the rider and its end. The thin orange grid lines are finite physical-time sections.</p>
<p class="note">Only front/future surfaces are shown. Surface mesh cuts are not new boundaries. No smooth attachment of the cap rim to null infinity is drawn.</p>
<p class="note">This reuses the verified global coordinates as an attachment map, with a smooth invertible stretch. It does not give height the meaning of time or impose 45° light cones.</p>
</aside></main>'''
    template=template[:start]+html+template[end:]
    template=template.replace('let az=-.9,el=.38,zoom=1,center=[0,0,0]','let az=-.61,el=.56,zoom=.9,center=[1,0,1]')
    template=template.replace('Same global Z coordinates in every view','One common coordinate map; height is not time')
    template=template.replace("az=-.9;el=.38;zoom=1;center=[0,0,0]","az=-.61;el=.56;zoom=.9;center=[1,0,1]")
    template=template.replace('az=0;el=Math.atan(.5);zoom=9;center=[1.45,0,0]','az=-.4;el=.7;zoom=1.5;center=[2.1,0,2.65]')
    template=template.replace('az=Math.PI;el=-Math.atan(.5);zoom=9;center=[-1.45,0,0]','az=-1.08;el=.3;zoom=1.3;center=[0,0,.85]')
    template=template.replace('__SCENE_DATA__',json.dumps(scene,separators=(',',':')))
    (OUT/'unified_attachments.html').write_text(template,encoding='utf-8')


if __name__=='__main__':
    audit=globalmap.audit()
    scene,report=make_scene()
    report['global_map_checks']={k:audit[k] for k in ['max_inverse_error','max_cap_formula_error','max_scri_normal_null_error','cap_scri_separating_functional_gap']}
    # All meshes are finite; the display transformation is analytically injective.
    for m in scene['meshes']:assert np.all(np.isfinite(m['vertices']))
    (OUT/'unified_attachment_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    (OUT/'unified_attachment_scene.json').write_text(json.dumps(scene,separators=(',',':')),encoding='utf-8')
    draw(scene);write_viewer(scene);print(json.dumps(report,indent=2))
