"""Time-oriented 2+1 physical geometry, with a matched regular cap detail.

Main coordinates are (x,y,t), with genuine future-increasing t. The cap
detail uses (X,y,T)=((p+q)/2,y,(p-q)/2), with g=C(dX^2-dT^2)+dy^2.
Both views show the same timelike geodesic. Finite plot cuts are not infinity.
"""
import json
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import capped_horizon_atlas as cap
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/useful_2p1_view'
sys.path.insert(0,str(ROOT/'paper/supplement/scripts'))
from meridional_geometry import FrontCollar

SEND,RECEIVE,TRAVELER,WALL='#c47727','#487aaa','#b33565','#7b898c'
TMIN,TMAX=-2.,4.


def null_rhs(t,z):
    x,y,px,py=z;p=np.hypot(px,py);v=float(cap.shift(x,y));vx,vy=cap.gradient(x,y)
    return [v+px/p,py/p,-vx*px,-vy*px]


def calculate():
    horizon=cap.build_horizon();ycrit=horizon.C/cap.CONE
    rays=[];energy_errors=[];sending_margins=[]
    for angle in (0.,1.05,np.pi):
        sol=solve_ivp(null_rhs,[-1.5,TMAX],[0,0,np.cos(angle),np.sin(angle)],
                      method='DOP853',rtol=2e-11,atol=2e-12,dense_output=True,max_step=.025)
        ts=np.linspace(-1.5,TMAX,900);zs=sol.sol(ts);x,y,px,py=zs
        energies=cap.shift(x,y)*px+np.hypot(px,py)
        energy_errors.append(float(np.max(np.abs(energies-energies[0]))))
        sending_margins.append(float(np.max(x-horizon.h(y))))
        keep=(x>=-2.4)&(x<=2.4)&(np.abs(y)<=2.05)
        rays.append(np.column_stack([x[keep],y[keep],ts[keep]]))
    assert max(energy_errors)<2e-8 and max(sending_margins)<0
    # Tangency of the two stationary null sheets.
    yy=np.linspace(.68,2.05,300);xx=horizon.h(yy);vv=cap.shift(xx,yy)
    slope=-np.sqrt(vv*vv-1)
    normals_res=1+slope*slope-vv*vv
    assert np.max(np.abs(normals_res))<2e-15
    def rhs(t,z):
        y=z[0];x=float(horizon.h(y));v=float(cap.shift(x,y))
        return [np.sqrt(max(v*v-1,0))/(-v)]
    back=solve_ivp(rhs,[0,TMIN],[.92],rtol=1e-11,atol=1e-12,dense_output=True)
    front=solve_ivp(rhs,[0,TMAX],[.92],rtol=1e-11,atol=1e-12,dense_output=True)
    ts=np.linspace(TMIN,TMAX,400)
    yg=np.where(ts<0,back.sol(np.minimum(ts,0))[0],front.sol(np.maximum(ts,0))[0])
    sg=np.column_stack([horizon.h(yg),yg,ts]);sg=sg[np.abs(sg[:,1])<=2.05]
    # Reflection reverses time; use the same displayed interval after shifting.
    rg=sg.copy();rg[:,0]*=-1;rg[:,2]=TMIN+TMAX-rg[:,2];rg=rg[::-1]
    collar=FrontCollar('cap');sol,cross=collar.geodesic()
    proper=np.linspace(0,sol.t[-1],650);p,q,dp,dq=sol.sol(proper)
    x=np.array([collar.x_from_product(z) for z in p*q]);cc=collar.C(x)
    norms=cc*dp*dq
    assert np.max(np.abs(norms+1))<2e-9 and np.all(dp-dq>0)
    assert np.max(np.abs(x*x-1))<.25
    assert np.max(np.abs(cap.shift(x,.3)-collar.v0(x)))<1e-14
    capcurve=np.column_stack([(p+q)/2,np.full_like(p,.3),(p-q)/2])
    mask=q>0;t=np.log(collar.pq_factors(x[mask])[1]/q[mask])
    maincurve=np.column_stack([x[mask],np.full(np.sum(mask),.3),t]);maincurve=maincurve[maincurve[:,2]<=TMAX]
    assert len(maincurve)>5
    # Match individual events through the exact map and check t increases.
    pp,qq=collar.pq_factors(maincurve[:,0]);pp*=np.exp(maincurve[:,2]);qq*=np.exp(-maincurve[:,2])
    reconstructed=np.column_stack([(pp+qq)/2,maincurve[:,1],(pp-qq)/2])
    original=capcurve[mask][:len(maincurve)]
    match=float(np.max(np.abs(reconstructed-original)))
    assert match<1e-12 and np.all(np.diff(maincurve[:,2])>0)
    crossing=sol.sol(cross);cp=np.array([crossing[0]/2,.3,crossing[0]/2])
    # Frozen tangent cones are vector data, not finite geodesic trajectories.
    cone_checks=[]
    for x0,y0 in ((0,0),(1,0),(-.65,1.7)):
        v=float(cap.shift(x0,y0));a=np.linspace(0,2*np.pi,100)
        cone_checks.append(float(np.max(np.abs(-1+(v+np.cos(a)-v)**2+np.sin(a)**2))))
    report=dict(scope='Finite-time physical geometry plus a matched regular cap neighborhood; not a global conformal diagram.',
        original_inverse_time_norm=-1,cap_inverse_time_norm='-1/C < 0',
        maximum_null_energy_error=max(energy_errors),largest_sending_barrier_value=max(sending_margins),
        horizon_null_normal_error=float(np.max(np.abs(normals_res))),
        traveler_unit_norm_error=float(np.max(np.abs(norms+1))),same_event_coordinate_match_error=match,
        crossing_proper_time=float(cross),cap_crossing_p=float(crossing[0]),
        maximum_tangent_null_error=max(cone_checks),communication_half_width=ycrit,
        main_time_window=[TMIN,TMAX],cap_boundary='q=0, |y|<0.6; regular physical crossing; not scri')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return horizon,rays,sg,rg,collar,maincurve,capcurve,cp,report


def line_arrow(ax,points,color,index=None,length=12):
    if len(points)<3:return
    i=len(points)//2 if index is None else index;j=min(i+length,len(points)-1)
    d=points[j]-points[i]
    ax.quiver(*points[i],*d,color=color,arrow_length_ratio=.45,lw=1.5)


def cone(ax,point,shift,height=.32,color='#626b72',cap_C=None):
    angles=np.linspace(0,2*np.pi,100)
    if cap_C is None:directions=np.array([shift+np.cos(angles),np.sin(angles),np.ones_like(angles)]).T
    else:directions=np.array([np.cos(angles),np.sqrt(cap_C)*np.sin(angles),np.ones_like(angles)]).T
    ring=np.asarray(point)+height*directions
    ax.plot(*ring.T,color=color,lw=1.0,alpha=.8)
    for j in range(0,100,12):ax.plot(*np.array([point,ring[j]]).T,color=color,lw=.65,alpha=.6)


def draw(data):
    h,rays,sg,rg,collar,maincurve,capcurve,cp,report=data
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig=plt.figure(figsize=(15,10),facecolor='white')
    ax=fig.add_axes([.015,.20,.56,.66],projection='3d')
    spatial=fig.add_axes([.64,.58,.31,.28])
    detail=fig.add_axes([.60,.15,.38,.34],projection='3d')
    fig.suptitle('What the transverse dimension adds to a warp-bubble diagram',fontsize=18,y=.965)
    fig.text(.5,.922,'Time points upward. Horizon wings surround a two-way communication tube; only an open planar cap has a regular crossing.',ha='center',fontsize=11,color='#40525b')
    ys=np.linspace(-2.05,2.05,180);ts=np.linspace(TMIN,TMAX,35)
    yy,tt=np.meshgrid(ys,ts);hh=h.h(yy)
    for sign,col in ((1,SEND),(-1,RECEIVE)):
        ax.plot_surface(sign*hh,yy,tt,color=col,alpha=.13,shade=False,linewidth=0,rstride=2,cstride=3)
        for tcut in (TMIN,TMAX):ax.plot(sign*h.h(ys),ys,np.full_like(ys,tcut),color=col,lw=.9,alpha=.5)
        ycap,tcap=np.meshgrid(np.linspace(-cap.APERTURE,cap.APERTURE,30),ts)
        ax.plot_surface(np.full_like(ycap,sign),ycap,tcap,color=col,alpha=.22,shade=False,linewidth=0)
        for rim in (-cap.APERTURE,cap.APERTURE):ax.plot([sign,sign],[rim,rim],[TMIN,TMAX],color='#a74054',lw=1,ls=':')
    yl=np.linspace(-report['communication_half_width'],report['communication_half_width'],250)
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    loop=np.column_stack([np.r_[h.h(yl),-h.h(yl[::-1])],np.r_[yl,yl[::-1]],np.full(2*len(yl),TMIN)])
    ax.add_collection3d(Poly3DCollection([loop],facecolor='#e9dcac',alpha=.35,edgecolor='none'))
    ax.plot([0,0],[0,0],[TMIN,TMAX],color='#20282d',lw=2.5)
    ax.quiver(0,0,2.4,0,0,.65,color='#20282d',arrow_length_ratio=.25,lw=1.6)
    ax.text(-.22,-.12,4.13,'rider',fontsize=10,color='#20282d')
    for points,col in ((sg,SEND),(rg,RECEIVE)):
        ax.plot(*points.T,color=col,lw=2.4);line_arrow(ax,points,col)
    for ray in rays:
        ax.plot(*ray.T,color='#7e6131',lw=1.4,ls='--');line_arrow(ax,ray,'#7e6131')
    ax.plot(*maincurve.T,color=TRAVELER,lw=3);line_arrow(ax,maincurve,TRAVELER,index=max(0,len(maincurve)-30),length=18)
    ax.text(1.12,.30,4.15,'traveler continues\nin cap coordinates →',fontsize=8,color=TRAVELER)
    cone(ax,[0,0,-1.95],0,.32)
    cone(ax,[1,0,-.65],-1,.32)
    cone(ax,[-.65,1.7,.4],-2,.30)
    ax.set(xlim=(-2.45,2.45),ylim=(-2.1,2.1),zlim=(TMIN,4.35),
           xlabel='comoving x',ylabel='transverse y',zlabel='time t',title='A. The horizons are sheets, not two lines')
    ax.set_box_aspect((4.9,4.2,6.35));ax.view_init(elev=20,azim=-64)
    ax.set_xticks([-2,-1,0,1,2]);ax.set_yticks([-2,-1,0,1,2]);ax.set_zticks([-2,0,2,4])
    fig.text(.07,.13,'Top and bottom are finite-time cuts.\nSmall wire cones show local null directions.',fontsize=9,color='#56656d')
    # Constant-time spatial section: the most direct transverse interpretation.
    sy=np.linspace(-2.05,2.05,700);sh=h.h(sy)
    spatial.fill_betweenx(sy,-sh,sh,where=sh>=0,color='#e9dcac',alpha=.65)
    spatial.plot(sh,sy,color=SEND,lw=2);spatial.plot(-sh,sy,color=RECEIVE,lw=2)
    wy=np.linspace(-1,1,400);wx=np.sqrt(np.maximum(1-cap.psi(wy),0))
    spatial.plot(wx,wy,color=WALL,ls='--',lw=1);spatial.plot(-wx,wy,color=WALL,ls='--',lw=1)
    for sign,col in ((1,SEND),(-1,RECEIVE)):
        spatial.plot([sign,sign],[-cap.APERTURE,cap.APERTURE],color=col,lw=4)
        spatial.scatter([sign,sign],[-cap.APERTURE,cap.APERTURE],c='#a74054',s=15,zorder=5)
    spatial.plot(0,0,'o',color='#20282d',ms=4)
    spatial.text(0,.32,'two-way\ncommunication',ha='center',va='center',fontsize=9)
    spatial.annotate('planar cap',xy=(1,0),xytext=(1.35,.6),arrowprops=dict(arrowstyle='->',color=SEND),color=SEND,fontsize=9)
    spatial.set(xlim=(-2.25,2.25),ylim=(-2.05,2.05),xlabel='x',ylabel='y',title='B. A slice at one time')
    spatial.set_aspect('equal');spatial.grid(alpha=.12)
    # Regular cap detail, using the same geodesic and a true temporal T.
    pp,yy=np.meshgrid(np.linspace(.14,.82,35),np.linspace(-.599,.599,35))
    detail.plot_surface(pp/2,yy,pp/2,color=SEND,alpha=.25,linewidth=0,shade=False)
    for rim in (-.6,.6):detail.plot([.07,.41],[rim,rim],[.07,.41],color='#a74054',lw=2,ls='--')
    detail.plot(*capcurve.T,color=TRAVELER,lw=2.7);detail.scatter(*cp,c=TRAVELER,s=25,depthshade=False)
    line_arrow(detail,capcurve,TRAVELER,index=360,length=65)
    cone(detail,[.16,-.22,.16],0,.07,cap_C=2)
    # Two exact longitudinal null directions in the product chart.
    for direction in (-1,1):
        ss=np.linspace(0,.13,60);detail.plot(.13+direction*ss,np.full_like(ss,-.27),.09+ss,color='#7e6131',ls='--',lw=1)
    detail.text(.43,.05,.13,'original patch\nq > 0',fontsize=8,color='#52616b')
    detail.text(.12,.04,.43,'continued patch\nq < 0',fontsize=8,color='#52616b')
    detail.set(xlim=(-.02,.50),ylim=(-.68,.68),zlim=(-.02,.50),xlabel='X',ylabel='y',zlabel='time T',title='C. The same traveler crosses an open cap')
    detail.set_box_aspect((1,1.6,1));detail.view_init(elev=15,azim=-40)
    detail.set_xticks([0,.2,.4]);detail.set_yticks([-.6,0,.6]);detail.set_zticks([0,.2,.4])
    fig.text(.635,.070,'T=(p−q)/2 increases to the future; X and T share a scale.\nThe transverse axis is compressed for visibility.\nThe crossing q=0 is regular and is not null infinity.',fontsize=8.5,color='#52616b')
    handles=[Line2D([0],[0],color=SEND,lw=3,label='Sending horizon'),Line2D([0],[0],color=RECEIVE,lw=3,label='Receiving horizon'),
             Line2D([0],[0],color=TRAVELER,lw=3,label='Same traveler in A and C'),Line2D([0],[0],color='#7e6131',ls='--',label='Selected null rays')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.025),ncol=4,frameon=False,fontsize=9)
    fig.savefig(OUT/'useful_2p1_geometry.png',dpi=190)
    plt.close(fig)
    return


def viewer_data(data):
    h,rays,sg,rg,collar,maincurve,capcurve,cp,report=data
    def vertices(xyz):return np.asarray(xyz)[...,[2,0,1]].reshape(-1,3).tolist()
    def faces(n,m):return [[i*m+j,(i+1)*m+j,(i+1)*m+j+1] for i in range(n-1) for j in range(m-1)]+[[i*m+j,(i+1)*m+j+1,i*m+j+1] for i in range(n-1) for j in range(m-1)]
    def line(name,xyz,col,width=2):return dict(name=name,points=vertices(xyz),color=col,width=width)
    main=dict(meshes=[],lines=[],points=[])
    ts=np.linspace(TMIN,TMAX,10);ys=np.linspace(-2.05,2.05,110);yy,tt=np.meshgrid(ys,ts)
    for sign,col,label in ((1,SEND,'Sending horizon'),(-1,RECEIVE,'Receiving horizon')):
        main['meshes'].append(dict(name=label,vertices=vertices(np.stack([sign*h.h(yy),yy,tt],axis=-1)),faces=faces(len(ts),len(ys)),color=col,opacity=.20))
        yc,tc=np.meshgrid(np.linspace(-.6,.6,20),ts)
        main['meshes'].append(dict(name='Planar horizon patches',vertices=vertices(np.stack([np.full_like(yc,sign),yc,tc],axis=-1)),faces=faces(len(ts),20),color=col,opacity=.3))
        for y in (-.6,.6):main['lines'].append(line('Rim worldlines',[[sign,y,TMIN],[sign,y,TMAX]],'#a74054',1.3))
    main['lines'].append(line('Central rider',[[0,0,TMIN],[0,0,TMAX]],'#20282d',3))
    main['lines'].append(line('Traveler',maincurve,TRAVELER,3))
    for r in rays:main['lines'].append(line('Null rays from the rider',r,'#7e6131',2))
    for r,col in ((sg,SEND),(rg,RECEIVE)):main['lines'].append(line('Horizon generators',r,col,3))
    y=np.linspace(-report['communication_half_width'],report['communication_half_width'],250)
    loop=np.column_stack([np.r_[h.h(y),-h.h(y[::-1]),h.h(y[:1])],np.r_[y,y[::-1],y[:1]],np.full(2*len(y)+1,TMIN)])
    main['lines'].append(line('Communication footprint',loop,'#9b8a53',2))
    main['points'].append(dict(name='rider',point=[TMAX,0,0],color='#20282d'))
    def addcone(scene,pt,v,height=.32,cc=None):
        aa=np.linspace(0,2*np.pi,65)
        dirs=np.column_stack([v+np.cos(aa),np.sin(aa),np.ones_like(aa)]) if cc is None else np.column_stack([np.cos(aa),np.sqrt(cc)*np.sin(aa),np.ones_like(aa)])
        ring=pt+height*dirs
        scene['lines'].append(line('Local tangent light cones',ring,'#66747c',1.2))
        for j in range(0,64,8):scene['lines'].append(line('Local tangent light cones',[pt,ring[j]],'#66747c',.8))
    for pt,v in (([0,0,-1.95],0),([1,0,-.65],-1),([-.65,1.7,.4],-2)):addcone(main,np.array(pt),v)
    detail=dict(meshes=[],lines=[],points=[])
    pp,yy=np.meshgrid(np.linspace(.14,.82,20),np.linspace(-.6,.6,30),indexing='ij')
    detail['meshes'].append(dict(name='Regular crossing q = 0',vertices=vertices(np.stack([pp/2,yy,pp/2],axis=-1)),faces=faces(20,30),color=SEND,opacity=.4))
    for yy in (-.6,.6):detail['lines'].append(line('Excluded rims',[[.07,yy,.07],[.41,yy,.41]],'#a74054',2.5))
    detail['lines'].append(line('Traveler',capcurve,TRAVELER,3))
    detail['points'].append(dict(name='crossing',point=[cp[2],cp[0],cp[1]],color=TRAVELER))
    for direct in (-1,1):
        ss=np.linspace(0,.13,60);detail['lines'].append(line('Longitudinal null directions',np.column_stack([.13+direct*ss,np.full_like(ss,-.27),.09+ss]),'#7e6131',2))
    addcone(detail,np.array([.16,-.22,.16]),0,.07,cc=2)
    return dict(main=main,cap=detail)


if __name__=='__main__':
    data=calculate();draw(data)
    scenes=viewer_data(data)
    template=Path(__file__).with_name('useful_2p1_viewer.html').read_text(encoding='utf-8')
    (OUT/'useful_2p1_geometry.html').write_text(template.replace('__SCENE_DATA__',json.dumps(scenes,separators=(',',':'))),encoding='utf-8')
    print(json.dumps(data[-1],indent=2))
