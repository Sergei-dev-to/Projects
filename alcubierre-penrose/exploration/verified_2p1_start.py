"""Verified local 2+1 boundary charts; no background cone construction.

Start from the physical metric, check the exact cap pullback symbolically,
and draw two independent regular neighborhoods. No global boundary gluing
or rider-end attachment is asserted. Uses the existing global conformal
factor without changing its cap or exterior normalization.
"""
from pathlib import Path
import json
import sys

import numpy as np
import sympy as sp

import capped_horizon_atlas as profile
import proper_conformal_completion as completion

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/verified_2p1_start'
sys.path.insert(0,str(ROOT/'paper/supplement/scripts'))
from meridional_geometry import FrontCollar


def check():
    # Independent exact cap pullback, including the transverse component.
    t,x,y,s=sp.symbols('t x y s',real=True,positive=True)
    h=2/sp.sqrt(3)*sp.atan(x/sp.sqrt(3))
    P=s*(1-x)/(1+x);Q=s*sp.exp(-h)
    p=P*sp.exp(t);q=Q*sp.exp(-t)
    J=sp.Matrix([p,q,y]).jacobian([t,x,y])
    C=(1+x)**2*(x*x+3)*sp.exp(h)/(4*s*s)
    gpq=sp.Matrix([[0,C/2,0],[C/2,0,0],[0,0,1]])
    v=-(1+x*x)/2
    physical=sp.Matrix([[v*v-1,-v,0],[-v,1,0],[0,0,1]])
    difference=(J.T*gpq*J-physical).applyfunc(sp.simplify)
    assert difference==sp.zeros(3)
    assert sp.simplify(gpq.det()+C*C/4)==0
    assert sp.simplify(sp.diff(P*Q,x).subs(x,1))!=0
    # T=(p-q)/2, X=(p+q)/2: this holds for arbitrary positive C,Omega.
    cc,om=sp.symbols('C Omega',positive=True)
    JT=sp.Matrix([[1,0,1],[1,0,-1],[0,1,0]]) # (p,q,y) from (X,y,T)
    base=sp.Matrix([[0,cc/2,0],[cc/2,0,0],[0,0,1]])
    normalized=sp.simplify(om*om*JT.T*base*JT)
    assert normalized==om*om*sp.diag(cc,1,-cc)
    assert normalized.inv()[2,2]==-1/(om*om*cc)

    collar=FrontCollar('cap')
    phi=[];omega=[];null_res=[];matching=[]
    for pp in np.linspace(.08,.85,11):
        for qq in np.linspace(-.08,.12,13):
            factor,xx=completion.cap_extension_factor(pp,qq,collar)
            c=collar.C(xx)
            phi.append(xx*xx-1);omega.append(factor)
            assert factor>0 and c>0
            assert abs(xx*xx-1)<.25 # actual globally bounded W is affine here
            for yy in (-.59,0.,.59):
                assert abs(float(profile.shift(xx,yy))-collar.v0(xx))<1e-14
                if qq>0:
                    tt=np.log(collar.pq_factors(xx)[1]/qq)
                    matching.append(abs(float(completion.global_factor(tt,xx,yy))-factor))
            a=np.linspace(0,2*np.pi,101)
            directions=np.array([np.cos(a),np.sqrt(c)*np.sin(a),np.ones_like(a)])
            g=factor*factor*np.diag([c,1,-c])
            residual=np.einsum('in,ij,jn->n',directions,g,directions)
            null_res.append(float(np.max(np.abs(residual))))
    assert max(matching)<1e-12 and max(null_res)<1e-12

    sol,cross=collar.geodesic()
    vals=sol.sol(np.linspace(0,sol.t[-1],200))
    norms=[collar.C(collar.x_from_product(pp*qq))*dp*dq
           for pp,qq,dp,dq in vals.T]
    assert max(abs(np.array(norms)+1))<2e-9
    assert np.all(vals[2]-vals[3]>0) # future-increasing plotted T
    assert vals[1,0]>0>vals[1,-1]

    # Full exterior metric and its boundary, not a lower-dimensional slice.
    r=sp.symbols('r',positive=True);z=1-r;d=r*r+z*z
    exterior=sp.Matrix([[-z*z,-r/sp.sqrt(d),0],
                        [-r/sp.sqrt(d),1/d,0],[0,0,r*r]])/d
    assert sp.simplify(exterior.det()+r*r/d**3)==0
    assert sp.simplify(exterior.inv()[0,0])==-1
    boundary=exterior.subs(r,1)
    assert boundary==sp.Matrix([[0,-1,0],[-1,1,0],[0,0,1]])
    assert boundary.inv()[1,1]==0
    a=np.linspace(0,2*np.pi,101)
    directions=np.array([np.ones_like(a),1+np.cos(a),np.sin(a)])
    extres=float(np.max(np.abs(np.einsum('in,ij,jn->n',directions,np.array(boundary).astype(float),directions))))
    assert extres<2e-15
    # Every finite event displayed in the exterior panel lies in chi=0,
    # where the actual profile is identically flat and Omega is omega_inf.
    for rr in (.94,.97,.999):
        R=rr/(1-rr)
        for tau in (-1.,0.,1.):
            time=tau+np.sqrt(1+R*R)
            for theta in np.linspace(0,2*np.pi,21):
                xx=R*np.cos(theta)-2*time;yy=R*np.sin(theta)
                assert xx*xx+yy*yy>9 and profile.shift(xx,yy)==-2
                assert abs(float(completion.global_factor(time,xx,yy))-1/np.sqrt(1+R*R))<1e-14
    report=dict(symbolic_physical_cap_pullback='exact zero residual',
        cap_metric_in_X_y_T='Omega^2 diag(C,1,-C)',
        cap_inverse_time_metric='-1/(Omega^2 C) < 0',
        cap_phi_range=[min(phi),max(phi)],cap_min_Omega=min(omega),
        cap_factor_match_error=max(matching),cap_null_error=max(null_res),
        cap_crossing_proper_time=float(cross),
        cap_crossing_p=float(sol.sol(cross)[0]),
        geodesic_unit_norm_error=float(max(abs(np.array(norms)+1))),
        scri_boundary_metric=np.array(boundary).astype(float).tolist(),
        scri_inverse_time_metric=-1,scri_null_error=extres,
        boundaries='Cap: q=0, Omega>0. Ordinary future scri: r=1, Omega=0, dOmega != 0.',
        scope='Two verified local boundary neighborhoods. No global gluing or rider/rim/spatial ends claimed.')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2,default=str)+'\n')
    print(json.dumps(report,indent=2,default=str))
    return collar,sol,cross


def draw(collar,sol,cross):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    plt.rcParams.update({'font.size':10,'axes.titlesize':13})
    purple='#73519e';orange='#cc7928';red='#bd3835';blue='#397ba6'
    fig=plt.figure(figsize=(13,7))
    capax=fig.add_axes([.015,.19,.49,.65],projection='3d')
    extax=fig.add_axes([.52,.19,.46,.65],projection='3d')

    pp,yy=np.meshgrid(np.linspace(.08,.85,40),np.linspace(-.599,.599,45))
    capax.plot_surface(pp/2,yy,pp/2,color=purple,alpha=.28,shade=False)
    for py in (-.6,.6):
        capax.plot([.04,.425],[py,py],[.04,.425],color=red,ls='--',lw=1.3)
    # Local coordinate grid, with no assertion that these finite cuts
    # are spacetime boundaries.
    for qq in (-.08,.12):
        for py in (-.6,.6):
            pp=np.linspace(.08,.85,50)
            capax.plot((pp+qq)/2,np.full_like(pp,py),(pp-qq)/2,color='.65',lw=.6,ls=':')
    vals=sol.sol(np.linspace(0,sol.t[-1],200))
    xx=(vals[0]+vals[1])/2;tt=(vals[0]-vals[1])/2
    capax.plot(xx,np.full_like(xx,.30),tt,color='#222222',lw=2.5)
    crossing=sol.sol(cross);cx=crossing[0]/2
    capax.scatter([cx],[.3],[cx],color='#222222',s=24,depthshade=False)
    i=80
    capax.quiver(xx[i],.3,tt[i],xx[i+25]-xx[i],0,tt[i+25]-tt[i],
                 color='#222222',arrow_length_ratio=.45,lw=1.8)
    # Correct null cone at q=0: C=2, including transverse directions.
    pt=np.array([.13,-.18,.13]);a=np.linspace(0,2*np.pi,101)
    D=np.array([np.cos(a),np.sqrt(2)*np.sin(a),np.ones_like(a)])
    ring=pt[:,None]+.065*D
    capax.plot(*ring,color=red,lw=1.3)
    for j in range(0,100,10):capax.plot(*np.array([pt,ring[:,j]]).T,color=red,lw=.7)
    capax.text(.44,.05,.22,'original side\nq > 0',fontsize=9)
    capax.text(.24,.02,.43,'continued side\nq < 0',fontsize=9)
    capax.set(xlim=(-.025,.53),ylim=(-.70,.70),zlim=(-.025,.53),
              xlabel='X = (p+q)/2',ylabel='y',zlabel='T = (p-q)/2')
    capax.set_title('Planar cap: finite, regular crossing',pad=20)
    capax.view_init(elev=17,azim=-58);capax.set_box_aspect((1,1.45,1))

    # Exterior compact radial chart, only in its verified near-scri collar.
    # It is a cylinder here because tau is not compactified or identified.
    theta=np.linspace(0,2*np.pi,121)
    for tau in np.linspace(-1,1,9):
        extax.plot(np.cos(theta),np.sin(theta),np.full_like(theta,tau),color=blue,alpha=.6,lw=.7)
    for angle in np.linspace(0,2*np.pi,17):
        extax.plot([np.cos(angle)]*2,[np.sin(angle)]*2,[-1,1],color=blue,alpha=.4,lw=.7)
    th,zz=np.meshgrid(theta,np.linspace(-1,1,25))
    extax.plot_surface(np.cos(th),np.sin(th),zz,color=blue,alpha=.06,shade=False)
    # At theta=-pi/2 the exterior future cone in (tau,r,theta) is
    # (1,1+cos a,sin a); push it into the cylindrical drawing.
    angle=-np.pi/2;pt=np.array([np.cos(angle),np.sin(angle),-.15])
    a=np.linspace(0,2*np.pi,101)
    radial=1+np.cos(a);angular=np.sin(a)
    D=np.array([radial*np.cos(angle)-angular*np.sin(angle),
                radial*np.sin(angle)+angular*np.cos(angle),np.ones_like(a)])
    ring=pt[:,None]+.14*D
    extax.plot(*ring,color=red,lw=1.3)
    for j in range(0,100,10):extax.plot(*np.array([pt,ring[:,j]]).T,color=red,lw=.7)
    extax.quiver(np.cos(angle),np.sin(angle),.25,0,0,.35,color=blue,arrow_length_ratio=.25,lw=2)
    extax.text(-.5,.15,.05,'physical side\nr < 1',fontsize=10)
    extax.set(xlim=(-1.3,1.3),ylim=(-1.4,1.3),zlim=(-1.1,1.2),
              xlabel='r cos(theta)',ylabel='r sin(theta)',zlabel='tau')
    extax.set_title('Ordinary future null infinity: r = 1',pad=20)
    extax.view_init(elev=17,azim=-58);extax.set_box_aspect((1,1,1))
    fig.suptitle('A verified starting point: two distinct null surfaces',fontsize=17,y=.97)
    fig.text(.265,.84,'Omega > 0; the physical metric continues',ha='center',color=purple)
    fig.text(.75,.84,'Omega = 0; the conformal metric is regular',ha='center',color=blue)
    fig.text(.255,.16,r'$\widehat g=\Omega^2[C(pq)(dX^2-dT^2)+dy^2]$',ha='center',fontsize=13)
    fig.text(.75,.16,r'$\widehat g|_{r=1}=-2\,d\tau\,dr+dr^2+d\theta^2$',ha='center',fontsize=13)
    handles=[Line2D([0],[0],color=red,label='Actual future null directions'),
             Line2D([0],[0],color='#222222',lw=2,label='Freely falling traveler'),
             Line2D([0],[0],color=red,ls='--',label='Cap rim excluded')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.065),ncol=3,frameon=False)
    fig.text(.5,.025,'Local charts only. Their global connection and the rider ends are not represented. No double-cone identifications.',
             ha='center',fontsize=10)
    fig.savefig(OUT/'verified_boundary_neighborhoods.png',dpi=180,bbox_inches='tight',pad_inches=.2)
    plt.close(fig)


if __name__=='__main__':
    draw(*check())
