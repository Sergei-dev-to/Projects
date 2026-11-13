"""Verified transverse attachments of the planar cap and outer null wings.

An attachment atlas linked to the axial diagram, not a flat-cone embedding.
The exterior panel uses r=1/R, u=t-R and the laboratory polar angle.
"""
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from connect_2p1_penrose import OpticalMap, AF, AR, B, SCRI
import useful_2p1_view as view

OUT=view.OUT
ORANGE=view.SEND
RIM='#a74054'


def exterior(t,x,y):
    X=x+2*t;R=np.hypot(X,y)
    return 1/R,t-R,np.arctan2(y,X)


def cylinder(r,u,theta):
    # Merely a display of the boundary chart, with r=0 on the cylinder.
    radius=1/(1+2*np.asarray(r))
    return radius*np.cos(theta),radius*np.sin(theta),u


def calculate():
    h,base=view.cap.audit()
    c=h.C;um=-c/2;tm=np.pi/3
    errors=[];nulls=[];generators=[]
    # Same finite generator event F in the physical and scri charts.
    for sign in [-1,1]:
        y0=sign*1.6;x0=float(h.h(y0));t=np.linspace(0,300,2001)
        X=x0+t/2;y=y0+sign*np.sqrt(3)*t/2;x=X-2*t
        r,u,theta=exterior(t,x,y)
        errors.append(float(np.max(np.abs(x-h.h(y)))))
        errors.append(float(np.max(np.abs(r*(u-um)+1-np.cos(theta-sign*tm)))))
        assert abs(u[-1]-um)<.002 and abs(theta[-1]-sign*tm)<.005
        # Laboratory velocity has unit norm and constant components.
        nulls.append(abs(-1+.5**2+(np.sqrt(3)/2)**2))
        generators.append((t,x,y,r,u,theta))
    assert max(errors)<1e-10 and max(nulls)<1e-14
    # Every finite u<um in the surface closure is realized, although a
    # single fixed generator always ends at u=um.
    sequence_errors=[]
    for deficit in [.2,1.,2.]:
        for r in [1e-2,1e-4,1e-6]:
            th=tm+np.arccos(1-r*deficit);u=um-deficit
            R=1/r;t=R+u;y=R*np.sin(th);x=R*np.cos(th)-2*t
            sequence_errors.append(abs(x-(c-np.sqrt(3)*y)))
            assert y>view.cap.Y_EXTERIOR
    assert max(sequence_errors)<1e-8
    # Open cap: induced metric at q=0 is dy^2 (null along p).
    collar=view.FrontCollar('cap');sol,cross=collar.geodesic()
    g=collar.metric_pq(.4,0,.3)
    assert np.allclose(g[np.ix_([0,2],[0,2])],[[0,0],[0,1]])
    report=dict(theta_M_degrees=60,u_M=um,intercept=c,
        generator_and_null_plane_error=max(errors),null_tangent_error=max(nulls),
        surface_closure_sequence_error=max(sequence_errors),
        cap='q=0, p real, |y|<0.6; induced metric dy^2',
        cap_generator_endpoint_curve='p=q=0, |y|<0.6',
        ordinary_future_scri='r=0, u finite, theta periodic; induced metric dtheta^2',
        sending_wing_closure='theta=+/-pi/3, u<=u_M',
        fixed_sending_generator_endpoints='theta=+/-pi/3, u=u_M',
        scope='Matched boundary and physical charts; no global flat-cone embedding, no cap-rim continuation')
    (OUT/'horizon_attachment_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return h,um,tm,generators,collar,sol,cross,report


def draw(data):
    h,um,tm,gens,collar,sol,cross,report=data
    opt=OpticalMap(collar)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
    fig=plt.figure(figsize=(16,12),facecolor='white')
    axial=fig.add_axes([.035,.56,.43,.32]);axial.set_aspect('equal');axial.axis('off')
    capax=fig.add_axes([.52,.55,.44,.33],projection='3d')
    body=fig.add_axes([.035,.13,.43,.32],projection='3d')
    scri=fig.add_axes([.52,.13,.44,.32],projection='3d')
    fig.suptitle('From boundary lines to boundary surfaces',fontsize=22,y=.97)
    fig.text(.5,.927,'The cap opens into a strip. The transverse horizon wings reach a different surface: ordinary null infinity.',ha='center',fontsize=12,color='#52616b')
    # A: exact reduced map, with labels shared with the cap chart.
    def seg(a0,b0,a1,b1,col,**kw):
        p=opt.xy(np.array([a0,a1]),np.array([b0,b1]));axial.plot(*p.T,color=col,**kw)
    axial.add_patch(Polygon(opt.xy(np.array([AF,AF,AR,AR]),np.array([-B,B,B,-B])),facecolor='#eee4c3',alpha=.6))
    for a0,b0,a1,b1,col in [(B,-B,B,B,SCRI),(AR,B,B,B,SCRI),(-B,-B,-B,B,SCRI),(-B,-B,AF,-B,SCRI),(-B,B,AR,B,ORANGE),(AF,-B,B,-B,view.RECEIVE)]:
        seg(a0,b0,a1,b1,col,lw=2.5)
    seg(AF,-B,AF,B,ORANGE,lw=1.5,ls='--');seg(AR,-B,AR,B,view.RECEIVE,lw=1.5,ls='--')
    t=np.linspace(-30,30,600);axial.plot(*opt.point(t,np.zeros_like(t)).T,color='#28343b',lw=1.5)
    p,q=sol.sol(np.linspace(0,sol.t[-1],240))[:2];axial.plot(*opt.cap(p,q).T,color=view.TRAVELER,lw=2)
    cp=opt.xy(AF,B);ep=opt.cap(sol.sol(cross)[0],0);pp=opt.xy(AR,B)
    for pt,col in [(cp,ORANGE),(ep,view.TRAVELER),(pp,'#28343b')]:axial.scatter(*pt,c=col,s=22,zorder=5)
    axial.annotate('E: traveler crossing',xy=ep,xytext=(1.48,1.28),color=view.TRAVELER,fontsize=9,arrowprops=dict(arrowstyle='-',color=view.TRAVELER))
    axial.annotate('C⁺ becomes a curve →',xy=cp,xytext=(1.48,.65),color=ORANGE,fontsize=9,arrowprops=dict(arrowstyle='-',color=ORANGE))
    axial.text(pp[0]-.13,pp[1]+.18,'P⁺',fontsize=10)
    axial.text(-1.2,.7,'green: null infinity',color=SCRI,rotation=45,fontsize=10,ha='center')
    axial.text(.78,-.60,'front\nexterior',color='#52616b',ha='center',fontsize=9)
    axial.set(xlim=(-1.85,3.0),ylim=(-1.7,1.8),title='A. The 1+1 reference diagram')
    # B: regular physical cap strip and the actual horizon patch crossing it.
    p,y=np.meshgrid(np.linspace(-.4,.8,35),np.linspace(-.6,.6,30))
    capax.plot_surface(p/2,y,p/2,color=ORANGE,alpha=.27,shade=False,linewidth=0)
    for y0 in [-.6,.6]:capax.plot([-.2,.4],[y0,y0],[-.2,.4],color=RIM,lw=2,ls='--')
    q,y=np.meshgrid(np.linspace(0,.38,25),np.linspace(-.599,.599,30))
    capax.plot_surface(q/2,y,-q/2,color=ORANGE,alpha=.15,shade=False,linewidth=0)
    capax.plot([0,0],[-.6,.6],[0,0],color=ORANGE,lw=4)
    capax.plot([0,.18],[.3,.3],[0,-.18],color=ORANGE,lw=1.7,ls='--')
    # Highlight the selected 1+1 cap line and the same massive traveler.
    capax.plot([-.2,.4],[.3,.3],[-.2,.4],color=ORANGE,lw=1.2)
    p,q=sol.sol(np.linspace(0,sol.t[-1],240))[:2]
    capax.plot((p+q)/2,np.full_like(p,.3),(p-q)/2,color=view.TRAVELER,lw=2.7)
    pe=sol.sol(cross)[0];capax.scatter(pe/2,.3,pe/2,color=view.TRAVELER,s=25)
    capax.text(pe/2,.3,.37,'E',color=view.TRAVELER,fontsize=12)
    capax.text(-.04,-.48,.05,'C⁺ curve',color=ORANGE,fontsize=10)
    capax.text(-.20,.62,-.18,'excluded rim',color=RIM,fontsize=9)
    capax.text(.28,-.53,.35,'q = 0: open crossing strip',color=ORANGE,fontsize=9)
    capax.text(.19,-.3,-.20,'p = 0: planar horizon',color='#926027',fontsize=9)
    capax.set(xlim=(-.25,.45),ylim=(-.72,.72),zlim=(-.25,.45),xlabel='X',ylabel='transverse y',zlabel='time T',title='B. Orange boundary → an open null strip')
    capax.view_init(elev=18,azim=-40);capax.set_box_aspect([1,1.5,1])
    capax.set_xticks([0,.3]);capax.set_yticks([-.6,0,.6]);capax.set_zticks([0,.3])
    fig.text(.54,.505,'The planar horizon meets the cap along C⁺: p = q = 0.\nThe traveler crosses elsewhere on the strip. Its rims are not regular attachments.',fontsize=10,color='#52616b')
    # C: entire stationary front sheet at finite physical times.
    y,t=np.meshgrid(np.linspace(-3,3,160),np.linspace(-1,3,24))
    body.plot_surface(h.h(y),y,t,color=ORANGE,alpha=.22,shade=False,linewidth=0)
    for yc in [-.6,.6]:body.plot([1,1],[yc,yc],[-1,3],color=RIM,ls=':',lw=1.5)
    body.plot([1,1],[.3,.3],[-1,3],color=ORANGE,lw=3)
    body.plot([0,0],[0,0],[-1,3],color='#28343b',lw=2)
    for sign,gen in zip([-1,1],gens):
        t,x,y,r,u,theta=gen;sel=(t<=1.5)
        body.plot(x[sel],y[sel],t[sel],color=ORANGE,lw=2.5)
        body.scatter(x[0],y[0],0,c=ORANGE,s=28)
        body.text(x[0]-.15,y[0],-.35,'F−' if sign<0 else 'F+',color=ORANGE,fontsize=10)
    body.text2D(.60,.94,'planar generators → C⁺',transform=body.transAxes,color=ORANGE,fontsize=9)
    body.text(-2.7,2.8,1.0,'wing → Q+',color=ORANGE,fontsize=9)
    body.text(-2.7,-3.1,1.6,'wing → Q−',color=ORANGE,fontsize=9)
    body.set(xlim=(-3.2,1.5),ylim=(-3.1,3.1),zlim=(-1,3.3),xlabel='comoving x',ylabel='transverse y',zlabel='time t',title='C. The wings join the planar patch at finite time')
    body.view_init(elev=19,azim=-35);body.set_box_aspect([4.7,6.2,4.3]);body.set_zticks([-1,1,3])
    fig.text(.055,.075,'Finite-time view: the sheet is smooth across y = ±0.6.\nIts planar generators end on the cap; its outer generators escape to null infinity.',fontsize=10,color='#52616b')
    # D: actual exterior chart, displayed as a cylinder at r=0.
    angles=np.linspace(-np.pi,np.pi,100);ul=np.linspace(um-2,um+.65,25)
    aa,uu=np.meshgrid(angles,ul)
    scri.plot_surface(*cylinder(np.zeros_like(aa),uu,aa),color=SCRI,alpha=.07,shade=False,linewidth=0)
    for u in [um-2,um+.65]:scri.plot(np.cos(angles),np.sin(angles),np.full_like(angles,u),color=SCRI,alpha=.4,lw=.8)
    for theta,label in [(0,'axial θ = 0'),(np.pi,'axial θ = π')]:
        scri.plot([np.cos(theta)]*2,[np.sin(theta)]*2,[um-2,um+.65],color=SCRI,lw=1.5,ls='--')
        scri.text(np.cos(theta),np.sin(theta),um+.73,label,color=SCRI,fontsize=8)
    for sign,gen in zip([-1,1],gens):
        # Display both angular sides of each wing, clipping to exact flat exterior.
        rr,dd=np.meshgrid(np.linspace(0,.8,75),np.linspace(0,2,80))
        for branch in [-1,1]:
            th=sign*(tm+branch*np.arccos(1-rr*dd));u=um-dd
            transverse=np.divide(np.abs(np.sin(th)),rr,out=np.full_like(rr,np.inf),where=rr>0)
            valid=(sign*np.sin(th)>0)&(transverse>=view.cap.Y_EXTERIOR+.02)
            xp,yp,zp=cylinder(rr,u,th)
            scri.plot_surface(np.where(valid,xp,np.nan),np.where(valid,yp,np.nan),np.where(valid,zp,np.nan),color=ORANGE,alpha=.23,shade=False,linewidth=0,rstride=2,cstride=2)
        us=np.linspace(um-2,um,100)
        scri.plot(np.full_like(us,np.cos(tm)),np.full_like(us,sign*np.sin(tm)),us,color=ORANGE,lw=3)
        scri.scatter(np.cos(tm),sign*np.sin(tm),um,color=ORANGE,s=38)
        scri.text(np.cos(tm)+.08,sign*np.sin(tm),um+.1,'Q+' if sign>0 else 'Q−',color=ORANGE,fontsize=11)
        t,x,y,r,u,theta=gen
        scri.plot(*cylinder(r,u,theta),color=ORANGE,lw=2.2)
        scri.scatter(*cylinder(r[0],u[0],theta[0]),color=ORANGE,s=25)
        scri.text(*cylinder(r[0],u[0]-.16,theta[0]),'F+' if sign>0 else 'F−',color=ORANGE,fontsize=9)
    scri.set(xlim=(-1.2,1.2),ylim=(-1.2,1.2),zlim=(um-2.1,um+.9),zlabel='retarded time u',title='D. Green boundary → null infinity with an angle')
    scri.set_xticks([]);scri.set_yticks([]);scri.set_zticks([um-2,um-1,um],['uM − 2','uM − 1','uM'])
    scri.view_init(elev=18,azim=-30);scri.set_box_aspect([2.4,2.4,3.])
    fig.text(.54,.075,'The same F± generators end at Q±: θ = ±60°, u = uM.\nBold orange half-lines show the closure of the whole wing, u ≤ uM.',fontsize=10,color='#52616b')
    fig.text(.5,.025,'Matched physical and boundary charts, not one Euclidean conformal embedding. Cylinder height is retarded time; its top and bottom are plotting cuts.\nPast null infinity and the rear horizon follow by time reversal and longitudinal reflection. No smooth attachment through a cap rim is asserted.',ha='center',fontsize=9,color='#52616b')
    for suffix in ['png','svg']:fig.savefig(OUT/f'horizon_boundary_attachments.{suffix}',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    data=calculate();draw(data);print(json.dumps(data[-1],indent=2))
