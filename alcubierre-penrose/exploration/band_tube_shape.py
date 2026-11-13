"""Interior coordinate image; its uniformly pinched closure is RETIRED.

The boundary identification fails open chronology: fixed-position points
on an outer sending wing converge to the proposed future rider point.
See notes/joint_boundary_limits.md sections 6--10 and rider_endpoint_audit.py.

Uses the bounded capped profile and horizons already audited. A transverse
coordinate Y=Omega*y exposes the pinching suggested by the axial diagram.
Finite physical cap crossings remain nonzero-width triangular null faces.
This is only a coordinate closure, not a causal or conformal completion.
"""
from pathlib import Path
import json

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator

import capped_horizon_atlas as cap

OUT = cap.OUT
WEIGHT = 2.
A = cap.APERTURE
TMAX = (WEIGHT+1)/2


class Tube:
    def __init__(self):
        self.horizon = cap.build_horizon()
        self.ymax = self.horizon.C/cap.CONE
        self.xjoin = .9
        sol = solve_ivp(lambda x,z:[2/(1-float(cap.shift(x,0))**2)],
                        [0,self.xjoin],[0.],method="DOP853",rtol=2e-13,atol=2e-14,
                        max_step=.002,dense_output=True)
        assert sol.success
        self.Jinner = sol.sol
        self.delta = float(sol.sol(self.xjoin)[0]-self.Jquad(self.xjoin))
        self.C0 = 4*np.exp(self.delta+self.hfun(1.))
        zeta = np.r_[np.arctanh(np.linspace(0,self.xjoin,4000)),
                     np.linspace(np.arctanh(self.xjoin)+1e-6,40,8000)]
        x = np.tanh(zeta)
        jvals = np.where(x<=self.xjoin,self.Jinner(np.minimum(x,self.xjoin))[0],
                         2*zeta+self.hfun(x)+self.delta)
        self.inverse = PchipInterpolator(jvals,zeta,extrapolate=False)
        # The inverse horizon is needed only for spatial sections of the tube.
        y = np.r_[A,np.linspace(.601,.64,1000),np.linspace(.64001,self.ymax,4000)]
        hh = self.horizon.h(y)
        xx, indices = np.unique(hh[::-1],return_index=True)
        ys = y[::-1][indices]
        ys[-1] = A
        self.inverse_horizon = PchipInterpolator(xx,ys,extrapolate=False)

    @staticmethod
    def hfun(x):
        return 2/np.sqrt(3)*np.arctan(x/np.sqrt(3))

    def Jquad(self,x):
        return np.log((1+x)/(1-x))+self.hfun(x)

    def Jpos(self,x):
        x=np.asarray(x,dtype=float)
        shape=x.shape
        flat=x.reshape(-1)
        safe=np.minimum(flat,1-1e-15)
        ans=np.where(flat<=self.xjoin,self.Jinner(np.minimum(flat,self.xjoin))[0],
                     self.Jquad(safe)+self.delta)
        return ans.reshape(shape)

    def Cpos(self,x):
        x=np.asarray(x,dtype=float)
        v=cap.shift(x,0)
        ordinary=(1-v*v)*np.exp(self.Jpos(x))
        stable=np.exp(self.delta+self.hfun(x))*(1+x)**2*(x*x+3)/4
        return np.where(x<=self.xjoin,ordinary,stable)

    def coordinates(self,alpha,beta):
        alpha,beta=np.broadcast_arrays(np.asarray(alpha,dtype=float),np.asarray(beta,dtype=float))
        shape=alpha.shape
        af=alpha.reshape(-1);bf=beta.reshape(-1)
        assert np.max(np.abs(af))<WEIGHT and np.max(np.abs(bf))<1
        lp=np.log(WEIGHT+af)-np.log(WEIGHT-af)
        lq=np.log1p(-bf)-np.log1p(bf)
        lf=lp+lq
        z=np.abs(lf)
        xp=np.tanh(self.inverse(z))
        xx=-np.sign(lf)*xp
        # A convenient smooth conformal gauge, agreeing with the unit-axial
        # gauge on all four regular boundary faces. This avoids attributing
        # profile-dependent interior ripples to the underlying tube topology.
        omega=np.sqrt(WEIGHT/self.C0)*(1-(af/WEIGHT)*bf)
        return xx.reshape(shape),omega.reshape(shape),lp.reshape(shape),lq.reshape(shape)

    def section(self,time,n=601):
        lo=max(-WEIGHT,2*time-1)
        hi=min(WEIGHT,2*time+1)
        al=np.linspace(lo+1e-11*(hi-lo),hi-1e-11*(hi-lo),n)
        be=2*time-al
        x,omega,_,_=self.coordinates(al,be)
        radius=self.inverse_horizon(np.abs(x))
        width=omega*radius
        return time-al,width


def audit(tube):
    # Positive J' is nondecreasing. A right Riemann sum is an analytic
    # upper bound on J. The threshold is decreasing as v decreases.
    edges=np.linspace(0,tube.xjoin,1801)
    v=cap.shift(edges,0)
    jp=2/(1-v*v)
    ju=np.r_[0,np.cumsum(np.diff(edges)*jp[1:])]
    threshold=lambda vv:(2+vv)*(1+vv)/((4+vv)*(1-vv))
    upper=float(np.max(np.exp(ju[1:])*threshold(v[:-1])))
    # In the remaining affine collar an elementary separate bound applies.
    collar_upper=float(np.exp(tube.delta+tube.hfun(1))*(3-tube.xjoin**2)*4/
                        (6*(3+tube.xjoin**2)))
    assert max(upper,collar_upper)<1.65<WEIGHT

    # Numerical reconstruction of F(x) and axis/conformal normalization.
    rng=np.random.default_rng(20261030)
    aa=rng.uniform(-WEIGHT+.0001,WEIGHT-.0001,4000)
    bb=rng.uniform(-.9999,.9999,4000)
    x,o,lp,lq=tube.coordinates(aa,bb)
    J=np.sign(x)*tube.Jpos(np.abs(x))
    assert np.max(np.abs(J+lp+lq))<3e-7
    # Norm and orientation of the time function for the actual full tube.
    y=tube.inverse_horizon(np.abs(x))*rng.uniform(-.999,.999,len(x))
    v0=cap.shift(x,0);vf=cap.shift(x,y)
    fu=2*WEIGHT*np.exp(-np.logaddexp(0,lp)-np.logaddexp(0,-lp))
    fw=2*np.exp(-np.logaddexp(0,lq)-np.logaddexp(0,-lq))
    tt=(fu+fw)/2
    tx=-(fu/(v0+1)+fw/(v0-1))/2
    adv=tt+vf*tx
    margin=(adv-np.abs(tx))/(fu+fw)
    assert np.min(margin)>0
    for time in (-12.,-5.,0.,5.,12.):
        z=np.tanh(time/2)
        _,omega,_,_=tube.coordinates(WEIGHT*z,z)
        exact=np.sqrt(WEIGHT/tube.C0)/np.cosh(time/2)**2
        assert abs(float(omega)-exact)<1e-12
    # Future physical face: x->1, q->0, finite p. The width stays positive.
    face_errors=[]
    for alpha in (-1.5,0.,1.5):
        _,om,_,_=tube.coordinates(alpha,1-1e-11)
        exact=(WEIGHT-alpha)/np.sqrt(WEIGHT*tube.C0)
        face_errors.append(abs(float(om)-exact))
    assert max(face_errors)<1e-8
    # Entire display-time sections shrink uniformly, with a limiting scale.
    sections=[]
    for eps in (.1,.03,.01,.003,.001):
        xx,ww=tube.section(TMAX-eps)
        sections.append(dict(epsilon=eps,longitudinal_width=float(np.ptp(xx)),
                             transverse_diameter=float(2*np.max(ww)),
                             scaled_transverse_diameter=float(2*np.max(ww)/eps)))
    assert all(sections[i+1]['transverse_diameter']<sections[i]['transverse_diameter']
               for i in range(len(sections)-1))
    assert abs(sections[-1]['scaled_transverse_diameter']-
               sections[-2]['scaled_transverse_diameter'])<.03
    report=dict(null_coordinate_weight=WEIGHT,front_coefficient_C0=tube.C0,
                max_required_weight_bound=upper,collar_weight_bound=collar_upper,
                sampled_normalized_time_margin=float(np.min(margin)),
                max_primitive_inversion_error=float(np.max(np.abs(J+lp+lq))),
                future_face_errors=face_errors,pinch_sections=sections,
                conclusion="Coordinate image pinches, but its endpoint topology fails open chronology; not a causal/conformal completion.")
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'band_tube_shape_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report


def draw(tube):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig=plt.figure(figsize=(13,9))
    ax=fig.add_axes([.015,.11,.66,.79],projection='3d')
    teal,orange,purple='#087d80','#bd542c','#7751a0'
    # Complete curved horizon faces bounding the communication region.
    y=np.r_[A,np.linspace(.602,.64,45),np.linspace(.642,tube.ymax,160)]
    sig=np.linspace(-1+1e-7,1-1e-7,180)
    yy,ss=np.meshgrid(y,sig)
    x=tube.horizon.h(yy)
    F=np.exp(-tube.Jpos(x))
    F=np.where(x>=1-1e-14,0,F)
    den=1+ss+F*(1-ss)
    be=(1+ss-F*(1-ss))/den
    al=WEIGHT*ss
    om=np.sqrt(WEIGHT/tube.C0)*(1-ss*be)
    X=(be-al)/2;T=(be+al)/2;Y=om*yy
    for sign in (-1,1):
        ax.plot_surface(X,sign*Y,T,color=teal,alpha=.32,linewidth=0,shade=False,
                        rstride=3,cstride=3)
        ax.plot_surface(-X,sign*Y,-T,color=orange,alpha=.27,linewidth=0,shade=False,
                        rstride=3,cstride=3)
    # Planar portions of the original horizons, and distinct physical exit faces.
    b=np.linspace(-1,1,80);eta=np.linspace(-A,A,45)
    bb,ee=np.meshgrid(b,eta)
    om=np.sqrt(WEIGHT)/np.sqrt(tube.C0)*(1+bb)
    ax.plot_surface((bb+WEIGHT)/2,om*ee,(bb-WEIGHT)/2,color=teal,alpha=.35,shade=False)
    ax.plot_surface(-(bb+WEIGHT)/2,om*ee,-(bb-WEIGHT)/2,color=orange,alpha=.30,shade=False)
    al=np.linspace(-WEIGHT,WEIGHT,100)
    aa,ee=np.meshgrid(al,eta)
    om=(WEIGHT-aa)/np.sqrt(WEIGHT*tube.C0)
    XF=(1-aa)/2;TF=(1+aa)/2;YF=om*ee
    ax.plot_surface(XF,YF,TF,color=purple,alpha=.28,shade=False)
    ax.plot_surface(-XF,YF,-TF,color=purple,alpha=.18,shade=False)
    # Rim edges are excluded from the smooth cap attachment.
    for sign in (-1,1):
        oy=A*(WEIGHT-al)/np.sqrt(WEIGHT*tube.C0)
        ax.plot((1-al)/2,sign*oy,(1+al)/2,color='#ac3550',lw=1.1,ls='--')
        ax.plot(-(1-al)/2,sign*oy,-(1+al)/2,color='#ac3550',lw=1.1,ls='--')
    # The original axial band is the central plane through this volume.
    pminus=((WEIGHT-1)/2,0,-TMAX)
    pplus=((1-WEIGHT)/2,0,TMAX)
    cplus=((1+WEIGHT)/2,0,(1-WEIGHT)/2)
    cminus=(-(1+WEIGHT)/2,0,-(1-WEIGHT)/2)
    ax.add_collection3d(Poly3DCollection([[pminus,cplus,pplus,cminus]],
                       facecolors='.6',alpha=.08,edgecolors='.5',linewidths=.7))
    z=np.linspace(-1,1,200)
    ax.plot((1-WEIGHT)*z/2,np.zeros_like(z),(1+WEIGHT)*z/2,color='black',lw=2)
    ax.scatter([pminus[0],pplus[0]],[0,0],[-TMAX,TMAX],facecolors='white',edgecolors='black',s=45)
    ax.text(pplus[0]-.1,0,TMAX+.1,r'$P^+$: infinite rider time',fontsize=10)
    ax.text(pminus[0]-.6,0,-TMAX-.18,r'$P^-$: infinite rider time',fontsize=10)
    ax.text(1.15,.15,-.1,'Regular future\ncap-crossing face',color=purple,fontsize=10)
    # Spatial sections at fixed plotted time.
    for time in (0.,1.25):
        xx,ww=tube.section(time)
        xloop=np.r_[xx,xx[::-1],xx[:1]]
        yloop=np.r_[ww,-ww[::-1],ww[:1]]
        ax.plot(xloop,yloop,np.full_like(xloop,time),color='.25',lw=.8)
    ax.set(xlabel='X',ylabel='Y',zlabel='Diagram time T',
           xlim=(-1.7,1.7),ylim=(-1.6,1.6),zlim=(-1.75,1.75))
    ax.set_box_aspect((1,.8,1.2),zoom=1.05)
    ax.view_init(elev=17,azim=-61)
    ax.set_title('The full region that can both signal and hear the rider',fontsize=13,pad=17)
    ax2=fig.add_axes([.73,.47,.25,.37])
    for time,col in ((0.,'#444444'),(.8,'#42838b'),(1.25,'#9360a0'),(1.45,'#b44d44')):
        xx,ww=tube.section(time)
        center=(1-WEIGHT)/(1+WEIGHT)*time
        xx=xx-center
        ax2.plot(np.r_[xx,xx[::-1],xx[:1]],np.r_[ww,-ww[::-1],ww[:1]],color=col,
                 label=f'T = {time:g}')
    ax2.set(xlim=(-1.5,1.5),ylim=(-1.5,1.5),xlabel='X relative to the central rider',ylabel='Y',
            title='Sections shrink toward '+r'$T=1.5$')
    ax2.set_aspect('equal');ax2.grid(alpha=.12);ax2.legend(fontsize=8)
    fig.text(.73,.31,'Teal / orange: communication horizons\nPurple: regular finite-time crossings\n'
             'Gray middle plane: the axial band\nDashed edges: excluded cap rim',
             fontsize=10,linespacing=1.6)
    fig.text(.5,.035,'Conformal image of the communication tube. Purple faces retain finite width at regular crossings; '
             'the pointed rider ends remain uncompleted corner limits.\n'
             'The axial band is a central section through this volume.',ha='center',fontsize=10)
    fig.savefig(OUT/'band_tube_shape.png',dpi=185,bbox_inches='tight',pad_inches=.25)
    plt.close(fig)


if __name__=='__main__':
    tube=Tube()
    audit(tube)
    draw(tube)
