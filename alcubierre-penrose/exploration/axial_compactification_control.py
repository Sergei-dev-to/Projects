"""Compare the known 1+1 warp chart to the failed background map.

Compute boundary limits and a core-launched timelike geodesic before making
an annotated causal diagram. The boundary's regularity type is not inferred
from its being drawn as an outer diamond edge.
"""
from pathlib import Path
import sys

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"paper/supplement/scripts"))
from sech_extension import Params,compact

mp.mp.dps=75
RF=mp.acosh(2)
K=mp.sqrt(3)/2
A=mp.atan(mp.mpf('.5'))
B=mp.pi/2
OUT=ROOT/"output/global_2p1"


def shift(x):
    return 2/mp.cosh(x)-2


def u0(region,x):
    e1=mp.exp(-x-RF);e2=mp.exp(-x+RF)
    if region=="I": lam=(e1-1)/(e2-1)
    elif region=="II":lam=(1-e1)/(e2-1)
    else:lam=(1-e1)/(1-e2)
    return x-2/mp.sqrt(3)*mp.log(lam)


def w0(x):
    return x/3+4/(3*mp.sqrt(5))*mp.atan((3*mp.exp(x)-2)/mp.sqrt(5))


def xy(alpha,beta):
    return np.array([float((beta-alpha)/2),float((beta+alpha)/2)])


def endpoint_for_u(region,u):
    if region=="I":raw=mp.mpf('.5')+mp.exp(-K*u)
    elif region=="II":raw=mp.mpf('.5')*mp.tanh(K*u/2)
    else:raw=-mp.mpf('.5')-mp.exp(K*u)
    return xy(mp.atan(raw),B)


def audit():
    # Check the actual null-coordinate equations against the inverse metric.
    for region,points in [("I",[-3,-2]),("II",[-.8,0,.9]),("III",[1.8,2.5])]:
        for xx in map(mp.mpf,points):
            vv=shift(xx)
            du=mp.diff(lambda x:u0(region,x),xx)
            dw=mp.diff(w0,xx)
            assert abs(du+1/(vv+1))<mp.mpf('1e-65')
            assert abs(dw+1/(vv-1))<mp.mpf('1e-65')
            for gradx in (du,dw):
                assert abs(-1-2*vv*gradx+(1-vv*vv)*gradx*gradx)<mp.mpf('1e-64')
            for tt in (-3,0,3):
                uu=tt+u0(region,xx);ww=tt+w0(xx)
                def reg_u(z):
                    if region=="I":return mp.mpf('.5')+mp.exp(-K*z)
                    if region=="II":return mp.mpf('.5')*mp.tanh(K*z/2)
                    return -mp.mpf('.5')-mp.exp(K*z)
                au=mp.diff(lambda z:mp.atan(reg_u(z)),uu)
                bw=1/(1+ww*ww)
                t_t=(au+bw)/2;t_x=(au*du+bw*dw)/2
                assert -t_t*t_t-2*vv*t_t*t_x+(1-vv*vv)*t_x*t_x<0
                assert t_t+vv*t_x>0
    v0,v=sp.symbols("v0 v",real=True)
    delta=sp.symbols("delta",real=True)
    normu=-1+2*v/(v0+1)+(1-v*v)/(v0+1)**2
    normw=-1+2*v/(v0-1)+(1-v*v)/(v0-1)**2
    assert sp.factor(normu.subs(v,v0+delta)-delta*(2-delta)/(v0+1)**2)==0
    assert sp.factor(normw.subs(v,v0+delta)+delta*(2+delta)/(v0-1)**2)==0

    # Massive outgoing geodesic, unit mass E=sqrt(2), core launch x=0,t=-2.
    launch_time=mp.mpf(-2)
    ee=mp.sqrt(2)
    def D(x):return mp.sqrt(ee*ee-1+shift(x)**2)
    tau_end=mp.quad(lambda x:1/D(x),[0,RF])
    # Subtract the exact logarithmic pole before integrating stationary time.
    residual_limit=1/(2*ee*ee)-mp.mpf('.5')/(2*K*K)
    def residual(x):
        dd=RF-x
        if abs(dd)<mp.mpf('1e-30'):return residual_limit
        vv=shift(x)
        return (ee/D(x)-vv)/(1-vv*vv)-1/(K*dd)
    regular_time=mp.quad(residual,[0,RF])
    delta_small=mp.mpf('1e-27')
    cfront=u0("II",RF-delta_small)-mp.log(delta_small)/K
    u_end=launch_time+regular_time+mp.log(RF)/K+cfront
    crossing=endpoint_for_u("II",u_end)
    center_future=xy(A,B)
    front_end=xy(-A,B)
    assert front_end[0]>crossing[0]>center_future[0]
    assert front_end[1]<crossing[1]<center_future[1]
    assert tau_end<RF

    # Independent finite-delta approach to that same endpoint.
    for ds in (mp.mpf('1e-4'),mp.mpf('1e-8')):
        xx=RF-ds
        tt=launch_time+mp.quad(residual,[0,xx])+mp.log(RF/ds)/K
        assert abs(tt+u0("II",xx)-u_end)<5*ds

    # Check the ordinary null-infinity portions with EXACT null rays of the
    # warp metric, not background straight lines passing through the bubble.
    xleft=mp.mpf(-1000);xright=mp.mpf(1000)
    t_rightgoing=-u0("I",xleft)
    assert t_rightgoing>0
    assert t_rightgoing+w0(xleft)>600
    assert mp.atan(mp.mpf('1.5'))>A
    t_leftgoing=-w0(xleft)
    assert t_leftgoing>0
    assert t_leftgoing+u0("I",xleft)<-600
    t_past_rightgoing=-u0("III",xright)
    assert t_past_rightgoing<0
    assert t_past_rightgoing+w0(xright)<-600
    t_past_leftgoing=-w0(xright)
    assert t_past_leftgoing<0
    assert t_past_leftgoing+u0("III",xright)>600

    # Analytic 2D null branches: u=const gives dx/dlambda=E, hence
    # finite affine distance to RF. On the front generator itself,
    # lambda_* - lambda is proportional to exp(-kappa*t).
    # In the background lab chart ALL these approaches collapse to i0_R.
    report=[
        "Actual null-coordinate equations checked at points in all three regions.",
        "Known diagram time T is future temporal in the actual 1+1 metric (checked throughout the three-region samples).",
        f"RF={mp.nstr(RF,12)}, kappa={mp.nstr(K,12)}.",
        f"Bubble center future end P+ = {center_future}; proper time infinite.",
        f"Front stationary null end C+ = {front_end}; affine time finite.",
        f"Core launch at t=-2, massive E=sqrt(2): elapsed tau_*={mp.nstr(tau_end,14)}, u_*={mp.nstr(u_end,14)}, endpoint={crossing}.",
        "The same center/front approaches go to background (Xcompact,Tcompact)=(pi/2,0).",
        "Future ordinary scri: alpha=pi/2, and beta=pi/2 with alpha>atan(1/2).",
        "Future finite-parameter front boundary: beta=pi/2 with alpha<atan(1/2).",
        "Past ordinary scri: alpha=-pi/2, and beta=-pi/2 with alpha<-atan(1/2).",
        "Past finite-parameter rear boundary: beta=-pi/2 with alpha>-atan(1/2).",
        "Positive-time fixed interior positions all approach P+, not the diagram's exterior i+ vertex.",
        "Off axis, axial du norm = delta(2-delta)/(v0+1)^2, dw norm = -delta(2+delta)/(v0-1)^2.",
        "Therefore the 1+1 optical coordinates do not remain null when the transverse shift differs.",
    ]
    OUT.mkdir(parents=True,exist_ok=True)
    text="\n".join(report)+"\n"
    (OUT/"axial_control_check.txt").write_text(text,encoding="utf-8")
    print(text)
    return crossing,tau_end


def draw(crossing):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","DejaVu Sans"],
        "mathtext.fontset":"stixsans","font.size":12})
    b,a=float(B),float(A)
    fig,ax=plt.subplots(figsize=(10.4,8.1))
    ax.set_aspect("equal");ax.axis("off")
    blue,green,orange,red="#226a9c","#218c71","#cb7a22","#b63732"
    def segment(al0,al1,be0,be1,color):
        pts=np.array([xy(al0,be0),xy(al1,be1)])
        ax.plot(pts[:,0],pts[:,1],color=color,lw=3.0,zorder=3)
    # Four outside null edges, subdivided by their PHYSICAL limiting type.
    segment(b,b,-b,b,blue)
    segment(a,b,b,b,blue)
    segment(-b,a,b,b,green)
    segment(-b,-b,-b,b,blue)
    segment(-b,-a,-b,-b,blue)
    segment(-a,b,-b,-b,green)
    for aa in (-a,a):
        pts=np.array([xy(aa,-b),xy(aa,b)])
        ax.plot(pts[:,0],pts[:,1],color="0.45",lw=1.3,ls="--")

    ts=np.linspace(-160,160,2400)
    xc,tc=compact("II",ts,np.zeros_like(ts),Params())
    past=xy(-a,-b);future=xy(a,b)
    ax.plot(np.r_[past[0],xc,future[0]],np.r_[past[1],tc,future[1]],color=orange,lw=2.5)
    ax.scatter([past[0],future[0]],[past[1],future[1]],s=70,facecolors="white",edgecolors=orange,lw=2,zorder=6)

    # Timelike geodesic plotted in z=-log[(RF-x)/RF], which removes the
    # logarithmic pole from the ODE and keeps the approach numerically stable.
    rf,kk=float(RF),float(K)
    def rhs(z,state):
        ds=rf*np.exp(-z);xx=rf-ds
        vp=2*np.sinh(rf-ds/2)*np.sinh(ds/2)/np.cosh(xx)
        vv=-1+vp;dd=np.sqrt(1+vv*vv)
        return [ds*(np.sqrt(2)/dd-vv)/(vp*(2-vp)),ds/dd]
    sol=solve_ivp(rhs,[0,70],[-2,0],rtol=1e-11,atol=1e-12,dense_output=True,max_step=.15)
    assert sol.success
    zs=np.linspace(0,70,1300)
    ts=sol.sol(zs)[0]
    ds=rf*np.exp(-zs);xx=rf-ds
    ul=ts+xx-2/np.sqrt(3)*(np.log1p(-np.exp(-xx-rf))-np.log(np.expm1(ds)))
    wl=ts+xx/3+4/(3*np.sqrt(5))*np.arctan((3*np.exp(xx)-2)/np.sqrt(5))
    alpha=np.arctan(.5*np.tanh(kk*ul/2));beta=np.arctan(wl)
    gx,gt=(beta-alpha)/2,(beta+alpha)/2
    ax.plot(np.r_[gx,crossing[0]],np.r_[gt,crossing[1]],color=red,lw=2.6,zorder=5)
    ax.scatter([crossing[0]],[crossing[1]],s=45,color=red,zorder=7)

    cp=xy(-a,b);cm=xy(a,-b)
    ax.scatter([cp[0],cm[0]],[cp[1],cm[1]],s=55,color="0.1",zorder=7)
    ax.annotate(r"$C^+$: finite affine end",xy=cp,xytext=(1.38,.30),ha="left",fontsize=11,
        arrowprops={"arrowstyle":"-","color":"0.3"})
    ax.annotate(r"$P^+$: center's future end" "\n" "infinite proper time",xy=future,xytext=(-.20,1.34),ha="center",fontsize=11,color=orange,
        arrowprops={"arrowstyle":"-","color":orange})
    ax.annotate("traveler's finite proper-time end",xy=crossing,xytext=(1.40,.85),ha="left",fontsize=11,color=red,
        arrowprops={"arrowstyle":"-","color":red})
    ax.text(cm[0]-.10,cm[1]+.10,r"$C^-$",ha="right",fontsize=13)
    ax.text(past[0]-.10,past[1]-.06,r"$P^-$",ha="right",fontsize=13,color=orange)
    for x,t,label in [(0,b,r"$i^+$"),(0,-b,r"$i^-$"),(-b,0,r"$i^0_L$"),(b,0,r"$i^0_R$")]:
        ax.text(x+.13*np.sign(x),t+.13*np.sign(t),label,ha="center",va="center",fontsize=13)
    ax.text(-.65,.04,"I",ha="center",fontsize=14)
    ax.text(0,.04,"II",ha="center",fontsize=14)
    ax.text(.65,.04,"III",ha="center",fontsize=14)
    handles=[Line2D([0],[0],color=blue,lw=3,label="ordinary null infinity"),
        Line2D([0],[0],color=green,lw=3,label="extendible boundary of the 1+1 metric"),
        Line2D([0],[0],color=orange,lw=2.5,label="bubble center"),
        Line2D([0],[0],color=red,lw=2.5,label="outgoing freely falling traveler")]
    ax.legend(handles=handles,loc="lower left",bbox_to_anchor=(-.02,-.10),frameon=False,fontsize=11,ncol=2)
    ax.set_xlim(-1.95,2.85);ax.set_ylim(-1.88,1.88)
    ax.set_title("Known 1+1 warp diagram: different parts of the outer edge have different meanings",fontsize=13,pad=20)
    fig.subplots_adjust(left=.03,right=.98,bottom=.13,top=.91)
    path=OUT/"axial_boundary_control.png"
    fig.savefig(path,dpi=200,bbox_inches="tight",facecolor="white")
    plt.close(fig)
    print(path)


if __name__=="__main__":
    crossing,tau=audit()
    draw(crossing)
