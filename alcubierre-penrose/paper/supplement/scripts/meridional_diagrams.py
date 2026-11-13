"""Render checked meridional causal charts, with actual quotient light cones.

Run meridional_geometry.verify_geometry BEFORE calling these renderers.
The plots are coordinate views of a specified conformally rescaled 2+1
metric, not embeddings in Minkowski space. rho=0 is the symmetry axis.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from meridional_geometry import FrontCollar,plot_coordinates
from sech_extension import Params,compact,horizons,w_coord


FIGURES=Path(__file__).resolve().parent.parent.parent/"figures"
BLUE="#397eac"
GREEN="#218c71"
RED="#b63732"


def tangent_cone(ax,collar,p,q,rho,height=.045):
    theta=np.linspace(0,2*np.pi,48)
    directions=collar.null_directions(p,q,rho,theta)
    metric=collar.metric_plot(p,q,rho)
    assert np.max(np.abs(np.einsum('ni,ij,nj->n',directions,metric,directions)))<2e-8
    x,t=plot_coordinates(p,q)
    vertex=np.array([x,rho,t])
    rim=vertex+height*directions
    faces=[[vertex,rim[i],rim[i+1]] for i in range(len(rim)-1)]
    ax.add_collection3d(Poly3DCollection(faces,facecolor="0.25",edgecolor="none",alpha=.10))
    ax.plot(*rim.T,color="0.20",lw=.7)
    for j in range(0,len(rim)-1,8):
        pair=np.array([vertex,rim[j]])
        ax.plot(*pair.T,color="0.3",lw=.55)


def meridional_panel(ax,kind,title):
    collar=FrontCollar(kind)
    pmax,qmax=.75,.22
    rhomax=.78 if kind=="cap" else .65
    rho=np.linspace(0,rhomax,80)
    qgrid=np.geomspace(.009,qmax,95)
    rr,qq=np.meshgrid(rho,qgrid,indexing="ij")
    xx=collar.wall_x(rr)
    pp=collar.F(xx)/qq
    x,t=plot_coordinates(pp,qq)
    mask=(pp>pmax)|(pp<0)
    x=np.where(mask,np.nan,x)
    t=np.where(mask,np.nan,t)
    # This surface is exactly v(x,rho)=-1, parameterized in the original
    # spacetime by q>0, not an assumed null tube.
    ax.plot_surface(x,rr,t,color=BLUE,alpha=.34,rstride=2,cstride=3,
        edgecolor="none",shade=False)
    for j in [0,20,40,60,79]:
        ax.plot(x[j],rr[j],t[j],color=BLUE,lw=.7,alpha=.75)

    # The rho=0 plane is the regularized axial view. Its frame is a chart cut.
    p_outline=np.array([-pmax,pmax,pmax,-pmax,-pmax])
    q_outline=np.array([qmax,qmax,0,0,qmax])
    x0,t0=plot_coordinates(p_outline,q_outline)
    ax.plot(x0,np.zeros_like(x0),t0,color="0.55",lw=.75,ls=(0,(2,3)))
    ax.add_collection3d(Poly3DCollection([np.column_stack([x0[:-1],np.zeros(4),t0[:-1]])],
        facecolor="#e0edf7",alpha=.10,edgecolor="none"))

    if kind=="cap":
        # q=0 is a REGULAR NULL surface only over the open transverse disk.
        pv=np.linspace(-pmax,pmax,48)
        rv=np.linspace(0,collar.a,32)
        p_sheet,r_sheet=np.meshgrid(pv,rv)
        xs,ts=plot_coordinates(p_sheet,np.zeros_like(p_sheet))
        ax.plot_surface(xs,r_sheet,ts,color=GREEN,alpha=.24,shade=False,
            edgecolor="none")
        for rline in (0,collar.a):
            ax.plot(xs[0],np.full_like(pv,rline),ts[0],color=GREEN if rline==0 else RED,
                lw=1.4,ls="-" if rline==0 else (0,(2,2)))
        # Continuation of the stationary cap generators through the disk B.
        qn=np.linspace(-qmax,0,35)
        qn_grid,rn_grid=np.meshgrid(qn,np.linspace(0,collar.a,25))
        xn,tn=plot_coordinates(np.zeros_like(qn_grid),qn_grid)
        ax.plot_surface(xn,rn_grid,tn,color=BLUE,alpha=.13,shade=False,edgecolor="none")
        ax.plot(np.zeros(2),[0,collar.a],np.zeros(2),color="0.15",lw=2)
        ax.scatter([0],[collar.a],[0],s=50,facecolors="white",edgecolors=RED,
            linewidths=1.6,depthshade=False)
        # The exact same numerical geodesic is used in Figure 2a.
        sol,tcross=collar.geodesic()
        tau=np.linspace(0,sol.t[-1],260)
        p,q=sol.sol(tau)[:2]
        gx,gt=plot_coordinates(p,q)
        ax.plot(gx,np.full_like(gx,.30),gt,color=RED,lw=2.8)
        xcross,tcross_plot=plot_coordinates(*sol.sol(tcross)[:2])
        ax.scatter([xcross],[.30],[tcross_plot],s=20,color=RED,depthshade=False)
        tangent_cone(ax,collar,.06,.13,.14)
        tangent_cone(ax,collar,.10,-.12,.43)
        rw=.71; qw=.15
        pw=collar.F(collar.wall_x(rw))/qw
        tangent_cone(ax,collar,pw,qw,rw,height=.035)
        ax.text2D(.02,.91,"green: regular crossing aperture",transform=ax.transAxes,zorder=100,
            color=GREEN,fontsize=13)
        ax.text2D(.02,.85,"red: freely falling traveler",transform=ax.transAxes,zorder=100,
            color=RED,fontsize=13)
        ax.text2D(.02,.79,"blue: bubble wall",transform=ax.transAxes,zorder=100,
            color=BLUE,fontsize=13)
        ax.text(0,collar.a+.025,.035,"excluded\nrim",color=RED,fontsize=12)
        ax.set_yticks([0,collar.a])
        ax.set_yticklabels(["0",r"$a$"])
    else:
        # No surface or added region is drawn at q=0. The sole axial
        # generator endpoint is a proven pp-curvature singularity in 4D.
        qline=np.geomspace(.001,qmax,90)
        xa,ta=plot_coordinates(np.zeros_like(qline),qline)
        ax.plot(xa,np.zeros_like(xa),ta,color=BLUE,lw=1.8)
        ax.scatter([0],[0],[0],marker="x",s=65,color=RED,linewidths=2,depthshade=False)
        for rw,qw in [(.23,.15),(.47,.16)]:
            pw=collar.F(collar.wall_x(rw))/qw
            tangent_cone(ax,collar,pw,qw,rw,height=.04)
        ax.text2D(.02,.91,"no open crossing aperture",transform=ax.transAxes,zorder=100,
            color=RED,fontsize=13)
        ax.text2D(.02,.85,"axis endpoint: tidal singularity",transform=ax.transAxes,zorder=100,
            color=RED,fontsize=13)
        ax.text2D(.02,.79,"blue: bubble wall",transform=ax.transAxes,zorder=100,
            color=BLUE,fontsize=13)
        ax.set_yticks([0,.3,.6])

    ax.set_xlim(-.43,.38)
    ax.set_ylim(0,rhomax+.04)
    ax.set_zlim(-.43,.43)
    ax.set_xticks([-.3,0,.3])
    ax.set_zticks([-.3,0,.3])
    ax.set_xlabel(r"longitudinal $X$",labelpad=3,fontsize=13)
    ax.set_ylabel(r"radius $\rho$",labelpad=3,fontsize=13)
    ax.set_zlabel(r"time $T$",labelpad=3,fontsize=13)
    ax.tick_params(labelsize=11,pad=0)
    ax.set_box_aspect((1.05,1.10,1.25))
    ax.view_init(elev=22,azim=-58)
    ax.grid(False)
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.pane.set_facecolor((1,1,1,0))
        axis.pane.set_edgecolor((.8,.8,.8,.3))
    ax.set_title(title,fontsize=13,pad=12)


def reduced_sech_panel(ax):
    """Closed-form Fig. 1a, simplified for legibility beside the 3D view."""
    pp=Params(n_grid=1400)
    r1,r2=horizons(pp)
    eps=1e-6
    b=np.pi/2
    a=np.arctan(.5)
    def xy(u,w):
        return (np.asarray(w)-np.asarray(u))/2,(np.asarray(w)+np.asarray(u))/2
    for lo,hi,color in [(-b,-a,"#edf3f7"),(-a,a,"#e0edf7"),(a,b,"#edf3f7")]:
        uv=np.array([lo,hi,hi,lo]);wv=np.array([-b,-b,b,b])
        ax.add_patch(Polygon(np.column_stack(xy(uv,wv)),facecolor=color,edgecolor="none"))
    grids={"I":np.linspace(-7.5,r1-eps,1100),"II":np.linspace(r1+eps,r2-eps,1400),
        "III":np.linspace(r2+eps,7.5,1100)}
    for tt in (-5,-2.5,0,2.5,5):
        for region,xx in grids.items():
            x,t=compact(region,np.full_like(xx,tt),xx,pp)
            ax.plot(x,t,color="0.65",lw=.6,ls=(0,(5,4)))
    ts=np.linspace(-9,9,900)
    for region,positions in {"I":[r1-.6],"II":[-.6,.6],"III":[r2+.6]}.items():
        for pos in positions:
            x,t=compact(region,ts,np.full_like(ts,pos),pp)
            ax.plot(x,t,color="0.45",lw=.7)
    # Center is complete; its compactified endpoints are not the black tips.
    ts=np.linspace(-60,60,1600)
    xc,tc=compact("II",ts,np.zeros_like(ts),pp)
    end0=xy(+a,-b);end1=xy(-a,b)
    center_past=xy(-a,-b);center_future=xy(+a,b)
    ax.plot(np.r_[center_past[0],xc,center_future[0]],np.r_[center_past[1],tc,center_future[1]],
        color="#d07825",lw=2)
    for uu in (-a,a):
        ax.plot(*xy(np.full(2,uu),np.array([-b,b])),color=BLUE,lw=1.9,ls="--")
    outline=np.array([(0,-b),(b,0),(0,b),(-b,0),(0,-b)])
    ax.plot(*outline.T,color="0.3",lw=1.2)
    for point,label,offset in [(end1,r"$C^+$",(16,-4)),(end0,r"$C^-$",(-19,-3))]:
        ax.scatter([point[0]],[point[1]],color="0.1",s=34,zorder=6)
        ax.annotate(label,xy=point,xytext=offset,textcoords="offset points",fontsize=13)
    for xx,tt,label in [(-.65,.03,"I"),(0,.03,"II"),(.65,.03,"III")]:
        ax.text(xx,tt,label,ha="center",fontsize=15)
    for xx,tt,label in [(0,b,r"$i^+$"),(0,-b,r"$i^-$"),(-b,0,r"$i^0_L$"),(b,0,r"$i^0_R$")]:
        ax.text(xx+.14*np.sign(xx),tt+.13*np.sign(tt),label,ha="center",va="center",fontsize=13)
    ax.set_aspect("equal")
    ax.set_xlim(-1.88,1.88);ax.set_ylim(-1.83,1.83)
    ax.axis("off")
    ax.set_title("(a) Axial conformal diagram",fontsize=13,pad=12)
    ax.text(0,-2.00,"orange: bubble center; dashed blue: axial generators",ha="center",fontsize=10,color="0.35")


def rounded_figure():
    fig=plt.figure(figsize=(12,6.3))
    grid=fig.add_gridspec(1,2,width_ratios=[1,1.25],wspace=.12)
    reduced_sech_panel(fig.add_subplot(grid[0,0]))
    meridional_panel(fig.add_subplot(grid[0,1],projection="3d"),"rounded",
        "(b) Spherical front with a transverse direction restored")
    fig.subplots_adjust(left=.025,right=.97,top=.91,bottom=.12)
    for ext in ("pdf","png"):
        target=FIGURES/f"rounded_meridional_conformal.{ext}"
        fig.savefig(target,bbox_inches="tight",facecolor="white",dpi=220)
        print(target)
    plt.close(fig)
