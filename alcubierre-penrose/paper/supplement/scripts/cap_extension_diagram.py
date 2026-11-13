"""Build Figures 1 and 2 only after checking the 2+1 quotient geometry.

Figure 1b restores the radial direction of the actual spherical sech
bubble. Figure 2b restores it for the explicit affine-W cap collar.
The 3D light cones come from the full quotient metric, not an extrusion
of a Minkowski diamond. Figure 2a and 2b use the same timelike geodesic.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

from meridional_geometry import FrontCollar,plot_coordinates,verify_geometry
from meridional_diagrams import meridional_panel,rounded_figure

BASE=Path(__file__).resolve().parent
PAPER_FIGURES=BASE.parent.parent/"figures"
B=np.pi/2
AF=-np.pi/6
BLUE="#e0edf7"
AMBER="#f7dfb6"
PALE_AMBER="#fbefd9"
GREEN="#187c75"
RED="#b63732"

plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Arial","DejaVu Sans"],
    "mathtext.fontset":"stixsans","pdf.fonttype":42,"ps.fonttype":42,"font.size":12})


def xy(a,b):
    return (np.asarray(b)-np.asarray(a))/2,(np.asarray(b)+np.asarray(a))/2


def front_xy(p,q):
    x,t=plot_coordinates(p,q)
    bx,bt=xy(AF,B)
    return x+bx,t+bt


def null_rectangle(a0,a1,b0,b1):
    return np.column_stack(xy(np.array([a0,a1,a1,a0]),np.array([b0,b0,b1,b1])))


def patch_rectangle(p0,p1,q0,q1):
    return np.column_stack(front_xy(np.array([p0,p1,p1,p0]),np.array([q0,q0,q1,q1])))


def axial_panel(ax,sol,tcross):
    ax.set_aspect("equal");ax.axis("off")
    for a0,a1,color in [(-B,AF,"#edf3f7"),(AF,-AF,BLUE),(-AF,B,"#edf3f7")]:
        ax.add_patch(Polygon(null_rectangle(a0,a1,-B,B),facecolor=color,edgecolor="none"))
    outline=np.array([(0,-B),(B,0),(0,B),(-B,0),(0,-B)])
    ax.plot(*outline.T,color="0.35",lw=1.3)
    p0,q0=.75,.22
    for plo,phi,color in [(-p0,0,PALE_AMBER),(0,p0,AMBER)]:
        ax.add_patch(Polygon(patch_rectangle(plo,phi,-q0,0),facecolor=color,edgecolor="none",zorder=2))
    border=patch_rectangle(-p0,p0,-q0,0)
    for i,j in [(0,1),(1,2),(3,0)]:
        ax.plot(border[[i,j],0],border[[i,j],1],color="0.4",lw=1.1,ls=(0,(2,3)),zorder=3)
    for ah in (AF,-AF):
        ax.plot(*xy(np.array([ah,ah]),np.array([-B,B])),color="#397799",lw=1.8,ls="--")
    ax.plot(*front_xy(np.array([-p0,p0]),np.zeros(2)),color=GREEN,lw=2.8,zorder=4)
    ax.plot(*front_xy(np.zeros(2),np.array([-q0,0])),color="#397799",lw=1.8,ls="--",zorder=4)
    ax.text(-.73,.15,"I",fontsize=15,ha="center")
    ax.text(0,.03,"II\nbubble\ninterior",fontsize=12,ha="center",va="center")
    ax.text(.75,-.15,"III",fontsize=15,ha="center")
    for x,y,label in [(0,B,r"$i^+$"),(0,-B,r"$i^-$"),(-B,0,r"$i^0_L$"),(B,0,r"$i^0_R$")]:
        ax.text(x+.12*np.sign(x),y+.12*np.sign(y),label,ha="center",va="center",fontsize=12)
    bx,bt=front_xy(0,0)
    ax.scatter([bx],[bt],s=28,color="0.1",zorder=6)
    ax.annotate(r"$B=C^+$",xy=(bx,bt),xytext=(1.55,.29),ha="center",arrowprops={"arrowstyle":"-","color":"0.35"})
    ax.scatter([-np.pi/3],[-np.pi/6],s=22,color="0.2",zorder=5)
    ax.annotate("added patch",xy=front_xy(.05,-.16),xytext=(1.28,1.30),ha="center",color="#795016",arrowprops={"arrowstyle":"->","color":"#795016"})
    tau=np.linspace(0,sol.t[-1],240)
    p,q=sol.sol(tau)[:2]
    gx,gt=front_xy(p,q)
    ax.plot(gx,gt,color=RED,lw=2.5,zorder=6)
    ax.annotate("",xy=(gx[-1],gt[-1]),xytext=(gx[-28],gt[-28]),arrowprops={"arrowstyle":"-|>","color":RED,"lw":2})
    xc,tc=front_xy(*sol.sol(tcross)[:2])
    ax.scatter([xc],[tc],s=22,color=RED,zorder=7)
    ax.annotate("traveler",xy=(gx[-1],gt[-1]),xytext=(1.71,1.00),ha="center",color=RED,arrowprops={"arrowstyle":"-","color":RED})
    ax.set_xlim(-1.85,2.05);ax.set_ylim(-1.83,1.85)
    ax.set_title("(a) Original patch and front attachment",fontsize=13,pad=15)
    ax.text(.02,-1.98,"Transverse radius suppressed",ha="center",fontsize=10,color="0.35")


def main():
    # No figure is authored before these independent geometry checks pass.
    verify_geometry()
    cap=FrontCollar("cap")
    sol,tcross=cap.geodesic()
    pcross=sol.sol(tcross)[0]
    # Positive null-coordinate normalization changes the point along the
    # boundary, but not the crossing sector or its order relative to B.
    for scale in (.2,1.,5.):
        phat=pcross/scale
        old_u=np.arctan((phat-1)/(2*(phat+1)))
        old_cross=np.array(xy(old_u,B))
        old_tip=np.array(xy(-np.arctan(.5),B))
        assert old_cross[0]<old_tip[0] and old_cross[1]>old_tip[1]
        assert np.isclose(old_cross.sum(),B)
    print("Figure 1 correspondence checked with explicit positive normalization factors.")
    PAPER_FIGURES.mkdir(parents=True,exist_ok=True)
    rounded_figure()
    fig=plt.figure(figsize=(12,6.3))
    grid=fig.add_gridspec(1,2,width_ratios=[1,1.25],wspace=.12)
    axial_panel(fig.add_subplot(grid[0,0]),sol,tcross)
    meridional_panel(fig.add_subplot(grid[0,1],projection="3d"),"cap",
        "(b) Capped front with a transverse direction restored")
    fig.subplots_adjust(left=.025,right=.97,top=.91,bottom=.12)
    for suffix in ("pdf","png"):
        target=PAPER_FIGURES/f"cap_extension_conformal.{suffix}"
        fig.savefig(target,dpi=220,bbox_inches="tight",facecolor="white")
        print(target)
    plt.close(fig)


if __name__ == "__main__":
    main()
