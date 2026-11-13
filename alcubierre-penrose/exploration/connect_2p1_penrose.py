"""Match the physical 2+1 view to the exact axial conformal diagram.

Uses the same bounded capped profile and the same timelike geodesic as
useful_2p1_view.py. The global optical coordinates are integrated from that
profile, not borrowed from the sech example. In the front affine collar
they agree exactly with the existing regular p,q chart.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
import useful_2p1_view as view

OUT=view.OUT
B=np.pi/2
AF,AR=-np.pi/6,np.pi/6
SCRI='#21836b'


class OpticalMap:
    def __init__(self, collar):
        # f'= -1/(v+1). Subtract its exact two logarithmic poles.
        def rhs(x,z):
            v=float(view.cap.shift(x,0))
            residual=0. if abs(x*x-1)<=.25 else -1/(v+1)+2/(1-x*x)
            return [residual,1/(1-v)]
        self.sol=solve_ivp(rhs,[0,3],[0,0],rtol=2e-12,atol=2e-13,
                           max_step=.006,dense_output=True)
        assert self.sol.success
        self.fshift=np.log(collar.scale)-self.sol.sol(1)[0]
        self.wshift=-(self.sol.sol(1)[1]-collar.h(1))-np.log(collar.scale)
        self.base3=np.log(.5)+self.sol.sol(3)[0]
        self.g3=self.sol.sol(3)[1]

    def fg(self,x):
        x=np.asarray(x,dtype=float);a=np.abs(x);ac=np.minimum(a,3.)
        r,g=self.sol.sol(ac)
        f=np.log(np.abs((1-ac)/(1+ac)))+r
        f=np.where(a>3,self.base3+(a-3),f)
        g=np.where(a>3,self.g3+(a-3)/3,g)
        return np.sign(x)*f+self.fshift,np.sign(x)*g+self.wshift

    @staticmethod
    def xy(a,b):
        return np.stack([(np.asarray(b)-a)/2,(np.asarray(b)+a)/2],axis=-1)

    def ab(self,t,x):
        f,g=self.fg(x);u=np.asarray(t)+f;w=np.asarray(t)+g
        angle=np.arctan(np.exp(np.clip(u,-700,700)))
        a=np.where(x < -1,(2/3)*(np.pi-angle)-np.pi/6,
                   np.where(x>1,-(2/3)*angle-np.pi/6,(2/3)*angle-np.pi/6))
        b=B-2*np.arctan(np.exp(np.clip(-w,-700,700)))
        return a,b

    def point(self,t,x):
        return self.xy(*self.ab(t,np.asarray(x)))

    def cap(self,p,q):
        return self.xy(AF+(2/3)*np.arctan(p),B-2*np.arctan(q))


def audit(data,opt):
    collar=data[4];sol,cross=collar.geodesic()
    tau=np.linspace(0,cross-.0001,220)
    p,q=sol.sol(tau)[:2]
    x=np.array([collar.x_from_product(z) for z in p*q])
    t=np.log(collar.pq_factors(x)[1]/q)
    error=float(np.max(np.abs(opt.point(t,x)-opt.cap(p,q))))
    assert error<2e-10
    # Independently differentiate numerically integrated optical functions.
    xs=np.array([-2.2,-1.2,-.9,-.65,0,.65,.9,1.2,2.2])
    eps=2e-5
    fp,gp=opt.fg(xs+eps);fm,gm=opt.fg(xs-eps)
    fx=(fp-fm)/(2*eps);gx=(gp-gm)/(2*eps);v=view.cap.shift(xs,0)
    residual=max(np.max(np.abs(-1-2*v*fx+(1-v*v)*fx*fx)),
                 np.max(np.abs(-1-2*v*gx+(1-v*v)*gx*gx)))
    assert residual<2e-6
    # Future temporal orientation and conformality on all three regions.
    samples=[]
    for xx in xs:
        for tt in [-3.,0.,3.]:
            dt=(opt.point(tt+eps,xx)-opt.point(tt-eps,xx))/(2*eps)
            dx=(opt.point(tt,xx+eps)-opt.point(tt,xx-eps))/(2*eps)
            vv=float(view.cap.shift(xx,0))
            norm=-dt[1]**2-2*vv*dt[1]*dx[1]+(1-vv*vv)*dx[1]**2
            assert norm<0 and dt[1]+vv*dx[1]>0
            # g'=factor*(dX^2-dT^2), pulled back to t,x.
            jac=np.column_stack([dt,dx]);flat=jac.T@np.diag([1.,-1.])@jac
            physical=np.array([[vv*vv-1,-vv],[-vv,1.]])
            samples.append(float(np.max(np.abs(flat/flat[1,1]-physical))))
    assert max(samples)<2e-6
    # Both ordinary future null infinities are reached by exterior null rays.
    f,g=opt.fg(-200.)
    a,b=opt.ab(-g,-200.)  # w=0; leftgoing null ray
    assert abs(a-B)<1e-12 and abs(b)<1e-12
    a2,b2=opt.ab(-f,-200.)  # u=0; other exterior null family
    assert a2>AR and abs(b2-B)<1e-12
    pcross=float(sol.sol(cross)[0]);crossxy=opt.cap(pcross,0)
    across=AF+(2/3)*np.arctan(pcross)
    assert AF<across<AR
    # The drawn added rectangle must stay within the actual affine collar.
    for pp in [-.32,.7]:
        for qq in [-.14,0]:
            assert abs(collar.x_from_product(pp*qq)**2-1)<.25
    # Exact finite-t cut event for both physical and conformal views.
    def original_time(s):
        pp,qq=sol.sol(s)[:2];xx=collar.x_from_product(pp*qq)
        return float(np.log(collar.pq_factors(xx)[1]/qq))
    tau4=brentq(lambda s:original_time(s)-4,0,cross-1e-8)
    report=dict(profile='Same bounded capped profile as useful_2p1_view.py',
        slice='y=0.3; identical induced metric to y=0 throughout the planar slab',
        same_event_map_error=error,optical_null_gradient_residual=float(residual),
        conformal_pullback_error=max(samples),
        traveler_cap_crossing_xy=crossxy.tolist(),traveler_cap_crossing_alpha=across,
        cap_generator_end_alpha=AF,rider_future_end_alpha=AR,
        future_scri='alpha=pi/2, or beta=pi/2 with alpha>pi/6',
        front_crossing_boundary='beta=pi/2, -pi/2<alpha<pi/6',
        ordinary_scri_limit_checks='Both exterior null families checked',
        tau_t4=tau4,tau_crossing=float(cross),
        scope='Exact axial conformal map with a regular front collar; not a global 2+1 completion or a maximal-extension claim')
    (OUT/'penrose_connection_checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return sol,cross,tau4,report


def draw(data,opt,sol,cross,tau4):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    fig=plt.figure(figsize=(16,9.4),facecolor='white')
    physical=fig.add_axes([.015,.22,.38,.64],projection='3d')
    ax=fig.add_axes([.40,.18,.58,.69])
    ax.set_aspect('equal');ax.axis('off')
    fig.suptitle('Where the cap crossing sits in the Penrose diagram',fontsize=21,y=.97)
    fig.text(.5,.92,'The highlighted transverse slice has an exact 1+1 diagram. The same traveler appears in both views.',ha='center',fontsize=12,color='#52616b')
    h=data[0];ys=np.linspace(-1.8,1.8,120);ts=np.linspace(-2,4,20)
    yy,tt=np.meshgrid(ys,ts)
    for sign,col in [(1,view.SEND),(-1,view.RECEIVE)]:
        physical.plot_surface(sign*h.h(yy),yy,tt,color=col,alpha=.12,shade=False,linewidth=0)
        physical.plot([sign,sign],[.3,.3],[-2,4],color=col,lw=3)
        physical.plot(sign*h.h(ys),ys,np.full_like(ys,-2),color=col,alpha=.65,lw=1)
    xx,tslice=np.meshgrid(np.linspace(-1.65,1.65,12),np.linspace(-2,4,12))
    physical.plot_surface(xx,np.full_like(xx,.3),tslice,color='#a5adb8',alpha=.12,shade=False,linewidth=0)
    physical.plot([0,0],[.3,.3],[-2,4],color='#252f37',lw=2)
    curve=data[5];physical.plot(*curve.T,color=view.TRAVELER,lw=3)
    for label,s in [('A',0),('B',tau4)]:
        p,q=sol.sol(s)[:2];x=data[4].x_from_product(p*q)
        t=np.log(data[4].pq_factors(x)[1]/q)
        physical.scatter(x,.3,t,c=view.TRAVELER,s=30)
        physical.text(x+.12,.3,t,label,color=view.TRAVELER,fontsize=12,weight='bold')
    # An actual escaping null ray in the same planar slice.
    def rhs(t,z):return [float(view.cap.shift(z[0],.3))-1]
    light=solve_ivp(rhs,[-1,4],[0],rtol=1e-11,atol=1e-12,dense_output=True,max_step=.02)
    lt=np.linspace(-1,4,300);lx=light.sol(lt)[0];keep=lx>=-2.3
    physical.plot(lx[keep],np.full(np.sum(keep),.3),lt[keep],color=SCRI,lw=2,ls='--')
    physical.text(-2.3,.3,.2,'light escapes',color=SCRI,fontsize=9)
    physical.text(.75,.3,4.55,'toward crossing E\nas t → ∞',color=view.TRAVELER,fontsize=10)
    physical.set(xlim=(-2.4,2.4),ylim=(-1.9,1.9),zlim=(-2,4.8),xlabel='comoving x',ylabel='transverse y',zlabel='time t')
    physical.set_box_aspect([4.8,3.8,6.8]);physical.view_init(elev=17,azim=-66)
    physical.set_title('Physical 2+1 view',pad=16,fontsize=14)
    fig.text(.05,.125,'Gray slice: y = 0.3, inside the planar slab.\nA and B are finite-time events. E lies beyond this plot.\nThe central rider has the same 1+1 trajectory as the black line.',fontsize=10,color='#52616b')

    def segment(a0,b0,a1,b1,col,lw=2.5,**kw):
        pts=opt.xy(np.array([a0,a1]),np.array([b0,b1]));ax.plot(*pts.T,color=col,lw=lw,**kw)
    ax.add_patch(Polygon(opt.xy(np.array([-B,-B,B,B]),np.array([-B,B,B,-B])),facecolor='#f3f5f7',edgecolor='none'))
    ax.add_patch(Polygon(opt.xy(np.array([AF,AF,AR,AR]),np.array([-B,B,B,-B])),facecolor='#eee4c3',alpha=.65,edgecolor='none'))
    # Ordinary scri and cap-extendible ends are deliberately separate colors.
    segment(B,-B,B,B,SCRI);segment(AR,B,B,B,SCRI)
    segment(-B,-B,-B,B,SCRI);segment(-B,-B,AF,-B,SCRI)
    segment(-B,B,AR,B,view.SEND)
    segment(AF,-B,B,-B,view.RECEIVE)
    segment(AF,-B,AF,B,view.SEND,lw=1.7,ls='--')
    segment(AR,-B,AR,B,view.RECEIVE,lw=1.7,ls='--')
    # A small, explicitly local extension collar. Other edges are chart cuts.
    border=opt.cap(np.array([-.32,.7,.7,-.32]),np.array([0,0,-.14,-.14]))
    ax.add_patch(Polygon(border,facecolor='#f7dfb6',alpha=.8,edgecolor='none',zorder=2))
    ax.plot(*np.vstack([border[1:],border[:1]]).T,color='#a99061',lw=1,ls=':')
    pc=np.linspace(-.32,.7,150);ax.plot(*opt.cap(pc,np.zeros_like(pc)).T,color=view.SEND,lw=3)
    segment(AF,B,AF,B+.22,view.SEND,lw=1.5,ls='--')
    t=np.linspace(-32,32,1200);rider=opt.point(t,np.zeros_like(t))
    ax.plot(*rider.T,color='#252f37',lw=2)
    # The leftgoing ray is w=constant and therefore exactly a 45-degree line.
    a0,b0=opt.ab(-1,np.array(0.));segment(float(a0),float(b0),B,float(b0),SCRI,lw=1.8,ls='--')
    endpoint=opt.xy(B,b0);ax.scatter(*endpoint,c=SCRI,s=28,zorder=7)
    tau=np.linspace(0,sol.t[-1],600);p,q=sol.sol(tau)[:2];trav=opt.cap(p,q)
    ax.plot(*trav.T,color=view.TRAVELER,lw=3,zorder=8)
    ax.annotate('',xy=trav[-1],xytext=trav[-70],arrowprops=dict(arrowstyle='->',color=view.TRAVELER,lw=2))
    events={label:opt.cap(*sol.sol(s)[:2]) for label,s in [('A',0),('B',tau4),('E',cross)]}
    for label,pt in events.items():ax.scatter(*pt,c=view.TRAVELER,s=23,zorder=9)
    ax.annotate('A',xy=events['A'],xytext=(.27,.38),color=view.TRAVELER,weight='bold',arrowprops=dict(arrowstyle='-',color=view.TRAVELER),fontsize=11)
    ax.annotate('B: t = 4',xy=events['B'],xytext=(.10,.64),color=view.TRAVELER,arrowprops=dict(arrowstyle='-',color=view.TRAVELER),fontsize=10)
    ax.annotate('E: cap crossing\nfinite traveler proper time',xy=events['E'],xytext=(1.48,1.30),fontsize=10,color=view.TRAVELER,arrowprops=dict(arrowstyle='-',color=view.TRAVELER))
    ax.annotate('added cap neighborhood',xy=opt.cap(.1,-.12),xytext=(1.44,.96),fontsize=10,color='#876538',arrowprops=dict(arrowstyle='-',color='#876538'))
    cp=opt.xy(AF,B);rp=opt.xy(AR,B)
    ax.scatter(*cp,c=view.SEND,s=34,zorder=8)
    ax.annotate('C⁺: end of the front\nhorizon generator',xy=cp,xytext=(1.42,.42),fontsize=10,color=view.SEND,arrowprops=dict(arrowstyle='-',color=view.SEND))
    ax.scatter(*rp,facecolors='white',edgecolors='#252f37',s=45,zorder=8)
    ax.annotate('P⁺: rider end\ninfinite proper time',xy=rp,xytext=(.42,1.71),fontsize=10,color='#252f37',arrowprops=dict(arrowstyle='-',color='#252f37'))
    ax.text(-1.32,.69,'ordinary future\nnull infinity',ha='center',color=SCRI,fontsize=10,rotation=45)
    ax.text(.20,1.34,'ordinary future\nnull infinity',ha='center',color=SCRI,fontsize=9,rotation=-45)
    ax.text(1.12,-.83,'ordinary past\nnull infinity',ha='center',color=SCRI,fontsize=10,rotation=45)
    ax.text(-.25,-1.38,'ordinary past\nnull infinity',ha='center',color=SCRI,fontsize=9,rotation=-45)
    ax.text(-1.10,-.66,'past rear-cap boundary',ha='center',color=view.RECEIVE,fontsize=9,rotation=-45)
    ax.text(0,-.10,'communication\nband',ha='center',fontsize=11,color='#71643a',rotation=45)
    ax.text(-.72,.03,'rear exterior',ha='center',fontsize=10,color='#52616b')
    ax.text(.78,-.10,'front exterior',ha='center',fontsize=10,color='#52616b')
    ax.text(-B-.05,0,'spatial\ninfinity',ha='right',va='center',fontsize=9,color='#52616b')
    ax.text(B+.05,0,'spatial\ninfinity',ha='left',va='center',fontsize=9,color='#52616b')
    ax.set(xlim=(-2.05,2.35),ylim=(-1.76,1.90))
    ax.set_title('Exact 1+1 conformal diagram of that slice',fontsize=14,pad=14)
    fig.text(.48,.13,'E is on the orange boundary, not on green null infinity.\nC⁺, E and P⁺ are distinct. Dotted edges of the added patch are chart cuts.',fontsize=11,color='#364c57')
    handles=[Line2D([],[],color=view.SEND,lw=2,label='Front horizon / future cap boundary'),Line2D([],[],color=view.RECEIVE,lw=2,label='Rear horizon / past cap boundary'),Line2D([],[],color=SCRI,lw=2,label='Ordinary null infinity'),Line2D([],[],color=view.TRAVELER,lw=2,label='Traveler')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.035),ncol=4,frameon=False,fontsize=10)
    for ext in ['png','svg']:
        fig.savefig(OUT/f'penrose_connection.{ext}',dpi=180)
    plt.close(fig)


if __name__=='__main__':
    data=view.calculate();opt=OpticalMap(data[4]);sol,cross,tau4,report=audit(data,opt)
    draw(data,opt,sol,cross,tau4)
    print(json.dumps(report,indent=2))
