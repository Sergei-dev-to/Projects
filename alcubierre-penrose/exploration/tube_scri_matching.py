"""Match the pinched tube to scri through a genuine flat-region overlap.

Produces overlapping conformal-chart views, not an unproved single global
coordinate embedding. The same finite event and the same exact null ray
are represented in both. Cap exits are followed into their physical local
continuation separately from ordinary null infinity.
"""
import json
import sys

import numpy as np
from scipy.integrate import quad

import band_tube_shape as band
import capped_horizon_atlas as cap

OUT=cap.OUT
W=band.WEIGHT
TEAL,ORANGE,PURPLE,BLUE='#087d80','#bd542c','#7751a0','#3c75b4'


def exterior(t,x,y):
    t,x,y=np.broadcast_arrays(t,x,y)
    lab=x+cap.SPEED*t
    rr=np.hypot(lab,y)
    theta=np.arctan2(y,lab)
    U=np.arctan(t-rr);V=np.arctan(t+rr)
    time=U+V;chi=V-U
    return np.array([chi*np.cos(theta),chi*np.sin(theta),time])


def overlap(t,x,y,tube):
    # The chosen overlap is also in the axial flat core, v0(x)=0.
    assert np.max(np.abs(x))<.5
    sigma=np.tanh((t-x)/2)
    beta=np.tanh((t+x)/2)
    alpha=W*sigma
    omega=np.sqrt(W/tube.C0)*(1-sigma*beta)
    return np.array([(beta-alpha)/2,omega*y,(beta+alpha)/2])


def tube_jacobian(t,x,y,tube):
    s=np.tanh((t-x)/2);b=np.tanh((t+x)/2)
    da=np.array([W*(1-s*s)/2,-W*(1-s*s)/2,0])
    db=np.array([(1-b*b)/2,(1-b*b)/2,0])
    om=np.sqrt(W/tube.C0)*(1-s*b)
    dom=-np.sqrt(W/tube.C0)*(da/W*b+s*db)
    return np.array([(db-da)/2,y*dom+np.array([0,0,om]),(db+da)/2]),om


def exterior_jacobian(t,x,y):
    lab=x+2*t;rr=np.hypot(lab,y);theta=np.arctan2(y,lab)
    dr=np.array([2*lab/rr,lab/rr,y/rr])
    dth=np.array([-2*y/rr**2,-y/rr**2,lab/rr**2])
    dt=np.array([1,0,0])
    dU=(dt-dr)/(1+(t-rr)**2)
    dV=(dt+dr)/(1+(t+rr)**2)
    TT=np.arctan(t-rr)+np.arctan(t+rr)
    chi=np.arctan(t+rr)-np.arctan(t-rr)
    dc=dV-dU
    jac=np.array([np.cos(theta)*dc-chi*np.sin(theta)*dth,
                  np.sin(theta)*dc+chi*np.cos(theta)*dth,dV+dU])
    radial=np.array([np.cos(theta),np.sin(theta)])
    tang=np.array([-np.sin(theta),np.cos(theta)])
    metric=np.zeros((3,3));metric[2,2]=-1
    metric[:2,:2]=np.outer(radial,radial)+(np.sin(chi)/chi)**2*np.outer(tang,tang)
    omega=np.cos(TT)+np.cos(chi)
    return jac,metric,omega


def crossing(tube):
    sys.path.insert(0,str(cap.ROOT/'paper/supplement/scripts'))
    from meridional_geometry import FrontCollar
    collar=FrontCollar('cap')
    lq=quad(lambda x:1/(float(cap.shift(x,0))-1),0,tube.xjoin,
            epsabs=1e-12,epsrel=1e-12)[0]
    kq=np.exp(lq+tube.hfun(tube.xjoin))
    kp=np.exp(-tube.delta)/kq
    rp,rq=kp/collar.scale,kq/collar.scale
    sol,tau=collar.geodesic()
    z=sol.sol(np.linspace(0,sol.t[-1],200))
    pp,qq=rp*z[0],rq*z[1]
    sigma=(pp-1)/(pp+1);beta=(1-qq)/(1+qq)
    alpha=W*sigma
    omega=np.sqrt(W/tube.C0)*(1-sigma*beta)
    xyz=np.array([(beta-alpha)/2,.3*omega,(beta+alpha)/2])
    event=sol.sol(tau)
    pstar=rp*event[0]
    omega_exit=np.sqrt(W/tube.C0)*2/(pstar+1)
    # Original-side retarded-time limits for THIS finite crossing label.
    limits=[]
    for qvalue in (np.exp(-10),np.exp(-20),np.exp(-40)):
        x=collar.x_from_product(pstar*qvalue/(rp*rq))
        qfactor=rq*collar.pq_factors(x)[1]
        t=np.log(qfactor/qvalue)
        ulab=t-np.hypot(x+2*t,.3)
        limits.append(float(ulab))
    return xyz,dict(global_p_at_crossing=float(pstar),
                    conformal_factor_at_crossing=float(omega_exit),
                    original_side_retarded_times=limits)


def audit(tube):
    y0=1.4;x0=tube.horizon.C-cap.CONE*y0
    assert 0<x0<.5 and cap.shift(x0,-y0)==-2
    k=np.array([1.,-1.5,-cap.CONE/2])
    g=np.array([[3.,2.,0],[2.,1.,0],[0,0,1.]])
    assert abs(k@g@k)<1e-14
    te=(tube.ymax-y0)/(cap.CONE/2)
    residuals=[]
    for t in np.linspace(-.04,te,12):
        x=x0-1.5*t;y=-y0-cap.CONE*t/2
        assert cap.shift(x,y)==-2 and x>=-1e-12
        jt,om=tube_jacobian(t,x,y,tube)
        je,ge,oe=exterior_jacobian(t,x,y)
        assert abs(np.linalg.det(jt))>1e-6 and abs(np.linalg.det(je))>1e-6
        residuals.append(float(np.max(np.abs(je.T@ge@je-oe*oe*g))))
        gt=np.linalg.inv(jt).T@(om*om*g)@np.linalg.inv(jt)
        transition=jt@np.linalg.inv(je)
        inverse=np.linalg.inv(transition)
        assert np.max(np.abs(gt-(om/oe)**2*inverse.T@ge@inverse))<1e-10
        assert abs((jt@k)@gt@(jt@k))<1e-11
        assert (jt@k)[2]>0 and (je@k)[2]>0
    assert max(residuals)<1e-12
    theta=np.arccos(.5);uM=-tube.horizon.C/2
    TM=np.pi/2+np.arctan(uM);chiM=np.pi-TM
    end=np.array([chiM*np.cos(theta),-chiM*np.sin(theta),TM])
    tfar=1e7
    far=exterior(tfar,x0-1.5*tfar,-y0-cap.CONE*tfar/2)
    assert np.max(np.abs(far-end))<1e-6
    # The untouched background map reverses diagram time on the actual rider.
    ctime=exterior(np.array([10.,20.]),np.array([0.,0.]),np.array([0.,0.]))[2]
    assert ctime[1]<ctime[0]
    _,capdata=crossing(tube)
    assert capdata['conformal_factor_at_crossing']>0
    assert np.all(np.diff(capdata['original_side_retarded_times'])<0)
    report=dict(match_event=dict(t=0.,x=float(x0),y=-y0,
                                 tube_coordinates=overlap(0.,x0,-y0,tube).tolist(),
                                 exterior_coordinates=exterior(0.,x0,-y0).tolist()),
                horizon_generator_leaves_tube_at_time=float(te),
                exact_null_vector=k.tolist(),
                metric_transition_max_error=max(residuals),
                future_scri_endpoint=dict(theta=-theta,u=uM,display=end.tolist()),
                naive_background_rider_times=ctime.tolist(),cap_crossing=capdata,
                scope='Matched conformal atlas; no single global coordinate embedding or corner completion claimed.')
    (OUT/'tube_scri_matching_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report


def render_tube(ax,tube):
    y=np.r_[cap.APERTURE,np.linspace(.602,.64,30),np.linspace(.642,tube.ymax,130)]
    s=np.linspace(-1+1e-7,1-1e-7,150)
    yy,ss=np.meshgrid(y,s);x=tube.horizon.h(yy)
    f=np.exp(-tube.Jpos(x));f=np.where(x>=1-1e-14,0,f)
    d=1+ss+f*(1-ss)
    beta=(1+ss-f*(1-ss))/d;alpha=W*ss
    om=np.sqrt(W/tube.C0)*(1-ss*beta)
    X=(beta-alpha)/2;T=(beta+alpha)/2;Y=om*yy
    for sign in (-1,1):
        ax.plot_surface(X,sign*Y,T,color=TEAL,alpha=.22,linewidth=0,shade=False,rstride=3,cstride=3)
        ax.plot_surface(-X,sign*Y,-T,color=ORANGE,alpha=.20,linewidth=0,shade=False,rstride=3,cstride=3)
    eta=np.linspace(-cap.APERTURE,cap.APERTURE,35)
    bb,ee=np.meshgrid(np.linspace(-1,1,70),eta)
    om=np.sqrt(W/tube.C0)*(1+bb)
    ax.plot_surface((bb+W)/2,om*ee,(bb-W)/2,color=TEAL,alpha=.24,shade=False)
    ax.plot_surface(-(bb+W)/2,om*ee,-(bb-W)/2,color=ORANGE,alpha=.22,shade=False)
    aa,ee=np.meshgrid(np.linspace(-W,W,90),eta)
    om=(W-aa)/np.sqrt(W*tube.C0)
    ax.plot_surface((1-aa)/2,om*ee,(1+aa)/2,color=PURPLE,alpha=.30,shade=False)
    ax.plot_surface(-(1-aa)/2,om*ee,-(1+aa)/2,color=PURPLE,alpha=.19,shade=False)
    z=np.linspace(-1,1,200)
    ax.plot((1-W)*z/2,0*z,(1+W)*z/2,color='black',lw=1.7)
    ax.scatter([(1-W)/2,(W-1)/2],[0,0],[band.TMAX,-band.TMAX],facecolors='white',edgecolors='black',s=35)
    ax.text((1-W)/2,0,band.TMAX+.12,r'$P^+$',fontsize=12)
    ax.text((W-1)/2,0,-band.TMAX-.17,r'$P^-$',fontsize=12)
    ax.set(xlim=(-1.7,1.7),ylim=(-1.6,1.6),zlim=(-1.8,1.8),xlabel='X',ylabel='Y',zlabel='T')
    ax.view_init(elev=15,azim=-62);ax.set_box_aspect((1,.85,1.2),zoom=1.05)


def render_exterior(ax,tube):
    th=np.linspace(0,2*np.pi,130)
    for sign in (-1,1):
        for time in np.linspace(.08,np.pi-.12,9):
            rr=np.pi-time
            ax.plot(rr*np.cos(th),rr*np.sin(th),np.full_like(th,sign*time),color=BLUE,lw=.6,alpha=.25)
        for ang in np.linspace(0,2*np.pi,17):
            time=np.linspace(.04,np.pi,100);rr=np.pi-time
            ax.plot(rr*np.cos(ang),rr*np.sin(ang),sign*time,color=BLUE,lw=.6,alpha=.25)
    ax.plot(np.pi*np.cos(th),np.pi*np.sin(th),0*th,color='.4',ls='--',lw=1)
    uM=-tube.horizon.C/2;thetaM=np.pi/3
    U=np.linspace(-np.pi/2+.02,np.arctan(uM)-1e-5,90);u=np.tan(U)
    d=(uM-u)/2.5;b=cap.CONE/2+d;r=np.sqrt(d*d+d*cap.CONE)
    lo=2*np.arctan(.5/(b+r));hi=2*np.arctan((b+r)/1.5)
    s=np.linspace(-1,1,81)
    angle=np.where(s[None,:]<0,thetaM+(thetaM-lo[:,None])*s[None,:],
                   thetaM+(hi[:,None]-thetaM)*s[None,:])
    den=2*np.sin((angle-thetaM)/2)**2
    radius=np.divide((uM-u)[:,None],den,out=np.full_like(den,np.inf),where=den>1e-26)
    v=uM+radius*(1+np.cos(angle-thetaM))
    T=U[:,None]+np.arctan(v);chi=np.arctan(v)-U[:,None]
    x=chi*np.cos(angle);y=chi*np.sin(angle)
    for sign in (-1,1):
        ax.plot_surface(x,sign*y,T,color=TEAL,alpha=.15,linewidth=0,shade=False,rstride=3,cstride=3)
        ax.plot_surface(-x,sign*y,-T,color=ORANGE,alpha=.13,linewidth=0,shade=False,rstride=3,cstride=3)
        ub=np.linspace(-50,uM,180);tb=np.pi/2+np.arctan(ub);cb=np.pi-tb
        ax.plot(cb*.5,sign*cb*cap.CONE/2,tb,color=TEAL,lw=2)
        ax.plot(-cb*.5,sign*cb*cap.CONE/2,-tb,color=ORANGE,lw=2)
    ax.text(.6,0,2.7,'scri+',color=BLUE,fontsize=15)
    ax.text(.6,0,-2.7,'scri−',color=BLUE,fontsize=15)
    ax.set(xlim=(-3.2,3.2),ylim=(-3.2,3.2),zlim=(-3.2,3.2))
    ax.set_box_aspect((1,1,1.1),zoom=1.22);ax.view_init(elev=17,azim=-62);ax.set_axis_off()


def draw(tube,report):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import proj3d
    from matplotlib.patches import ConnectionPatch
    fig=plt.figure(figsize=(15,9))
    ax1=fig.add_axes([.01,.18,.47,.68],projection='3d')
    ax2=fig.add_axes([.52,.18,.47,.68],projection='3d')
    render_tube(ax1,tube);render_exterior(ax2,tube)
    ax1.set_title('Tube chart: horizons and regular cap faces',fontsize=13,pad=20)
    ax2.set_title('Exterior chart: ordinary past and future null infinity',fontsize=13,pad=20)
    x0=report['match_event']['x'];y0=1.4;te=report['horizon_generator_leaves_tube_at_time']
    tin=np.linspace(-.04,te,150)
    inside=overlap(tin,x0-1.5*tin,-y0-cap.CONE*tin/2,tube)
    ax1.plot(*inside,color='#00565b',lw=3.5)
    match1=np.array(report['match_event']['tube_coordinates'])
    match2=np.array(report['match_event']['exterior_coordinates'])
    ax1.scatter(*match1,color='black',s=35);ax1.text(*(match1+np.array([.05,-.1,.04])),'A',fontsize=13)
    ax2.scatter(*match2,color='black',s=35);ax2.text(*(match2+np.array([.08,-.1,.03])),'A',fontsize=13)
    # The same exact affine null generator continues through the shared region.
    times=np.r_[np.linspace(-.04,2,90),np.geomspace(2.01,1e7,200)]
    ray=exterior(times,x0-1.5*times,-y0-cap.CONE*times/2)
    endpoint=np.array(report['future_scri_endpoint']['display'])
    ax2.plot(*ray,color='#00565b',lw=3.2);ax2.scatter(*endpoint,color=TEAL,s=42)
    ax2.text(*(endpoint+np.array([.08,-.1,.12])),'Future wing endpoint',color=TEAL,fontsize=9)
    # Receiving generator is the time-reversed, x-reflected upper wing.
    past=exterior(-times,-x0+1.5*times,y0+cap.CONE*times/2)
    ax2.plot(*past,color=ORANGE,lw=2.5)
    ax2.scatter(-endpoint[0],-endpoint[1],-endpoint[2],color=ORANGE,s=35)
    # Physical cap passage has a separate continuation, not an ordinary-scri endpoint.
    curve,_=crossing(tube)
    ax1.plot(*curve,color=PURPLE,lw=3)
    d=curve[:,-1]-curve[:,-5]
    ax1.quiver(*curve[:,-1],*d,length=2.5,normalize=False,color=PURPLE,arrow_length_ratio=.4)
    ax1.text(.65,.15,.75,'Cap crossing\n→ continued patch',color=PURPLE,fontsize=10)
    fig.suptitle('Checked tube-to-infinity connections in overlapping conformal charts',fontsize=18,y=.96)
    fig.text(.05,.13,'Purple: finite-time physical crossings, with positive conformal factor.\n'
             'The pinched rider ends remain distinct, unattached limits.',fontsize=10)
    fig.text(.56,.13,'Teal / orange wings meet ordinary null infinity, where the factor vanishes.\n'
             'Dashed base: unresolved spatial corner; no tube end is identified there.',fontsize=10)
    fig.text(.5,.035,'A is the same finite event in both charts. The highlighted ray is the same null geodesic. '
             'Charts overlap in an exactly flat part of the tube.\n'
             'This is a matched atlas, not a single completed coordinate domain. Signed meridional double; fold Y and −Y for the angular quotient.',
             ha='center',fontsize=10)
    fig.canvas.draw()
    p1=proj3d.proj_transform(*match1,ax1.get_proj())[:2]
    p2=proj3d.proj_transform(*match2,ax2.get_proj())[:2]
    link=ConnectionPatch(p1,p2,coordsA=ax1.transData,coordsB=ax2.transData,
                         arrowstyle='<->',color='.45',ls='--',lw=1.1,shrinkA=8,shrinkB=8)
    fig.add_artist(link)
    fig.savefig(OUT/'tube_to_scri_matched.png',dpi=180,bbox_inches='tight',pad_inches=.25)
    plt.close(fig)


if __name__=='__main__':
    tube=band.Tube()
    report=audit(tube)
    draw(tube,report)
