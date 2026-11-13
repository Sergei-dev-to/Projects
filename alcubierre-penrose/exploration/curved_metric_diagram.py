"""Metric-faithful visualization of the regular conformal completion.

The main chart covers the finite original spacetime and open ordinary scri.
An equivalent exterior gauge includes the ordinary exterior i+/- vertices.
Cap passages are shown in their own regular boundary-crossing chart.
Excluded rider/spatial/rim corners are not assigned physical identifications.
"""
import json
import sys

import numpy as np

import capped_horizon_atlas as cap
import cone_point_classifier as chart
import color_full_cone as coloring
import proper_conformal_completion as proper

OUT=cap.OUT
RED='#bf3d36'


def diagram_factor(t,x,y):
    # A smooth positive conformal gauge, equal to the previously checked
    # cap factor near the aperture and to the full ESU factor in the exterior.
    chi=1-cap.step((x*x+y*y-4)/5)
    R=np.hypot(x+2*t,y)
    log_es=-.5*np.log1p((t-R)**2)-.5*np.log1p((t+R)**2)+np.log(2.)
    return chi*proper.cap_factor(t,x)+(1-chi)*np.exp(log_es)


def jacobian(t,x,y):
    lab=x+2*t;R=np.hypot(lab,y)
    if R<1e-10:
        k=2/(1+t*t)
        return np.array([[2*k,k,0],[0,0,k],[k,0,0]])
    dr=np.array([2*lab/R,lab/R,y/R])
    dt=np.array([1.,0,0])
    du=(dt-dr)/(1+(t-R)**2);dv=(dt+dr)/(1+(t+R)**2)
    dc=dv-du;dz=dv+du
    ch=np.arctan(t+R)-np.arctan(t-R)
    k=ch/R;dk=(dc-k*dr)/R
    return np.array([k*np.array([2.,1,0])+lab*dk,
                     k*np.array([0.,0,1])+y*dk,dz])


def metric(t,x,y):
    v=float(cap.shift(x,y));om=float(diagram_factor(t,x,y))
    old=np.array([[v*v-1,-v,0],[-v,1,0],[0,0,1.]])
    J=jacobian(t,x,y);inverse=np.linalg.inv(J)
    return om*om*inverse.T@old@inverse


def esu_metric(point):
    X,Y,T=point;ch=np.hypot(X,Y)
    if ch<1e-10:return np.diag([1.,1.,-1.])
    n=np.array([X,Y])/ch;m=np.array([-Y,X])/ch
    result=np.zeros((3,3));result[2,2]=-1
    result[:2,:2]=np.outer(n,n)+(np.sin(ch)/ch)**2*np.outer(m,m)
    return result


def null_cone(t,x,y,n=65):
    v=float(cap.shift(x,y));angle=np.linspace(0,2*np.pi,n)
    old=np.array([np.ones(n),v+np.cos(angle),np.sin(angle)])
    J=jacobian(t,x,y)
    return J@old,J@np.array([1.,v,0.])


def audit():
    null_res=[];external_res=[];time_values=[]
    samples=[(0.,0.,0.),(.45,0.,0.),(1.5,0.,0.),(-1.5,0.,0.),
             (0.,0.,1.4),(0.,.85,.3),(0.,2.,1.),(0.,3.,1.)]
    for t,x,y in samples:
        G=metric(t,x,y);e=np.linalg.eigvalsh(G)
        assert e[0]<0<e[1]
        dirs,K=null_cone(t,x,y)
        raw=np.einsum('in,ij,jn->n',dirs,G,dirs)
        scale=np.linalg.norm(G)*np.sum(dirs*dirs,axis=0)
        null_res.append(float(np.max(np.abs(raw)/scale)))
        assert K@G@K<0
        if cap.shift(x,y)==-2 and x*x+y*y>=9:
            external_res.append(float(np.max(np.abs(G-esu_metric(chart.forward(t,x,y))))))
        time_values.append(dict(t=t,x=x,y=y,
                                inverse_metric_height=float(np.linalg.inv(G)[2,2]),
                                future_normal_height_velocity=float(K[2])))
    assert max(null_res)<1e-12
    assert max(external_res)<1e-12
    # Full exterior vertices are regular in this equivalent exterior gauge:
    # there is a neighborhood of each ordinary i+/- where chi=0 exactly.
    for t in (-100.,100.):
        x=-2*t;y=.4
        assert x*x+y*y>9
        assert abs(float(diagram_factor(t,x,y))-
                   (np.cos(chart.forward(t,x,y)[2])+np.cos(np.hypot(*chart.forward(t,x,y)[:2]))))<1e-14
    # The new and old gauges have a finite, positive ratio on each finite scri cut.
    gauge_errors=[]
    for tau in (-2.,0.,2.):
        R=1e7;t=tau+np.sqrt(1+R*R);x=R-2*t;y=0.
        ratio=float(diagram_factor(t,x,y)/proper.global_factor(t,x,y))
        gauge_errors.append(abs(ratio-1/np.sqrt(1+tau*tau)))
    assert max(gauge_errors)<1e-6
    # Actual outgoing null direction at the bubble center. Its background
    # ESU norm is positive, making the difference in cone fields explicit.
    d=jacobian(0.,0.,0.)@np.array([1.,1.,0.])
    actual=float(d@metric(0.,0.,0.)@d)
    background=float(d@esu_metric(chart.forward(0.,0.,0.))@d)
    assert abs(actual)<1e-13 and background>1
    sys.path.insert(0,str(cap.ROOT/'paper/supplement/scripts'))
    from meridional_geometry import FrontCollar
    collar=FrontCollar('cap')
    capres=[]
    for p in (-.4,0.,.4):
        om,x=proper.cap_extension_factor(p,0.,collar)
        C=collar.C(x)
        G=om*om*np.diag([C,1.,-C])  # (X,y,T), X=(p+q)/2, T=(p-q)/2
        ang=np.linspace(0,2*np.pi,65)
        D=np.array([np.cos(ang),np.sqrt(C)*np.sin(ang),np.ones_like(ang)])
        capres.append(float(np.max(np.abs(np.einsum('in,ij,jn->n',D,G,D)))))
        assert np.linalg.det(G)<0 and om>0
    assert max(capres)<1e-13
    # The interior map has incompatible boundary limits at (pi,0,0).
    # Fixed-p cap crossings have positive Omega, whereas the rider end
    # and spatial infinity have Omega -> 0. They cannot be one boundary
    # point of this conformal completion, regardless of interior coloring.
    limits=[]
    for time in (5.,10.,20.):
        rider=chart.forward(time,0.,0.)
        spatial=chart.forward(0.,np.exp(time),0.)
        q=np.exp(-time);p=.4
        om,xx=proper.cap_extension_factor(p,q,collar)
        tt=np.log(collar.pq_factors(xx)[1]/q)
        crossing=chart.forward(tt,xx,.3)
        target=np.array([np.pi,0.,0.])
        limits.append(dict(parameter=time,
            rider_distance=float(np.linalg.norm(rider-target)),
            rider_Omega=float(diagram_factor(time,0.,0.)),
            spatial_distance=float(np.linalg.norm(spatial-target)),
            spatial_Omega=float(diagram_factor(0.,np.exp(time),0.)),
            cap_distance=float(np.linalg.norm(crossing-target)),
            cap_Omega=float(om)))
    cap_limit=float(proper.cap_extension_factor(.4,0.,collar)[0])
    assert limits[-1]['rider_Omega']<1e-8 and cap_limit>.5
    report=dict(normalized_actual_null_cone_errors=null_res,
                exterior_ESU_metric_errors=external_res,
                time_height_checks=time_values,
                center_outgoing_null_direction=d.tolist(),actual_null_norm=actual,
                background_reference_norm=background,
                scri_gauge_ratio_errors=gauge_errors,
                cap_null_cone_errors=capres,
                incompatible_boundary_limits=limits,
                cap_boundary_Omega=cap_limit,
                finding='Inverse coloring is valid. The cone height is not a temporal coordinate in the bubble. Actual light cones must be drawn; excluded ends cannot be identified by this chart.',
                scope='Regular conformal-metric visualization with a cap chart; not a completed unified ideal-boundary diagram.')
    (OUT/'curved_metric_diagram_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report


def draw(horizon,purple,teal,walls,tubes):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap,BoundaryNorm
    fig=plt.figure(figsize=(16,11))
    ax=fig.add_axes([.005,.13,.63,.75],projection='3d')
    ax1=fig.add_axes([.70,.60,.28,.24])
    ax2=fig.add_axes([.68,.18,.31,.33],projection='3d')
    theta=np.linspace(0,2*np.pi,130)
    # Open ordinary scri, excluding the unresolved waist. Ordinary exterior
    # timelike vertices are included in the equivalent ESU exterior gauge.
    for sign in (-1,1):
        for z in np.linspace(.10,np.pi-.04,10):
            r=np.pi-z
            ax.plot(r*np.cos(theta),r*np.sin(theta),np.full_like(theta,sign*z),
                    color='#587ea7',alpha=.23,lw=.65)
        for ang in np.linspace(0,2*np.pi,17):
            z=np.linspace(.10,np.pi,110);r=np.pi-z
            ax.plot(r*np.cos(ang),r*np.sin(ang),sign*z,color='#587ea7',alpha=.23,lw=.65)
    ax.plot(np.pi*np.cos(theta),np.pi*np.sin(theta),0*theta,color='.5',ls='--',lw=.7)
    for z in tubes:ax.plot_surface(*z,color=coloring.TEAL,alpha=.08,shade=False,rstride=5,cstride=5,linewidth=0)
    for z in walls:ax.plot_surface(*z,color=coloring.PURPLE,alpha=.17,shade=False,rstride=5,cstride=5,linewidth=0)
    # A small inverse-classified volume sample retains the actual colors.
    rng=np.random.default_rng(888)
    for points,color in ((teal,coloring.TEAL),(purple,coloring.PURPLE)):
        ii=rng.choice(len(points),min(6000,len(points)),replace=False)
        a=points[ii]
        ax.scatter(a[:,0],a[:,1],a[:,2],s=1.5,c=color,alpha=.04,linewidths=0,depthshade=False)
    time=np.sinh(np.linspace(-3.7,3.7,500));rider=chart.forward(time,0*time,0*time)
    ax.plot(*rider,color=coloring.ORANGE,lw=2.2)
    # Red tangent null cones from the ACTUAL rescaled metric, not the background.
    for sample in ((0.,0.,0.),(1.5,0.,0.),(-1.5,0.,0.),(0.,0.,1.4)):
        point=chart.forward(*sample);D,K=null_cone(*sample)
        scale=.40/np.max(np.linalg.norm(D,axis=0))
        ring=point[:,None]+scale*D
        ax.plot(*ring,color=RED,lw=1)
        for j in range(0,D.shape[1],8):
            ax.plot(*np.array([point,ring[:,j]]).T,color=RED,lw=.7,alpha=.7)
        ax.quiver(*point,*(scale*K),color=RED,arrow_length_ratio=.3,linewidth=1.4)
    ax.text(1.1,0,2.1,'ordinary scri+',color='#416c9c',fontsize=10)
    ax.text(1.1,0,-2.1,'ordinary scri−',color='#416c9c',fontsize=10)
    ax.text(0,0,np.pi+.06,'ordinary exterior i+',fontsize=9)
    ax.text(0,0,-np.pi-.16,'ordinary exterior i−',fontsize=9)
    for sign in (-1,1):
        z=chart.forward(sign*20.,0.,0.)
        ax.scatter(*z,facecolors='white',edgecolors=coloring.ORANGE,s=28)
        ax.text(sign*2.55,-.20,sign*.23,'rider approach\n(end unresolved)',fontsize=8,color='#9b6018')
    ax.set(xlim=(-3.4,3.4),ylim=(-3.4,3.4),zlim=(-3.4,3.4),xlabel='x_c',ylabel='y_c',zlabel='z_c (not a global time)')
    ax.view_init(elev=16,azim=-66);ax.set_box_aspect((1,1,1.08),zoom=1.04)
    ax.set_title('Inverse coloring with the actual null cones',fontsize=13,pad=18)
    axis,img=coloring.section(horizon,'axial',n=701)
    colors=ListedColormap(['white',coloring.TEAL,coloring.PURPLE])
    ax1.imshow(img,origin='lower',extent=(-np.pi,np.pi,-np.pi,np.pi),
               cmap=colors,norm=BoundaryNorm([-.5,.5,1.5,2.5],3),interpolation='nearest',aspect='equal')
    ax1.plot(rider[0],rider[2],color=coloring.ORANGE,lw=2)
    for tt in (-1.5,0.,1.5):
        p=chart.forward(tt,0.,0.);J=jacobian(tt,0.,0.)
        dirs=np.array([J@np.array([1.,-1.,0.]),J@np.array([1.,1.,0.])])
        scale=.43/np.max(np.linalg.norm(dirs[:,[0,2]],axis=1))
        for D in dirs:
            end=p+scale*D
            ax1.annotate('',xy=(end[0],end[2]),xytext=(p[0],p[2]),
                         arrowprops=dict(arrowstyle='->',lw=1.2,color=RED))
        K=J@np.array([1.,0.,0.]);end=p+scale*K
        ax1.annotate('',xy=(end[0],end[2]),xytext=(p[0],p[2]),
                     arrowprops=dict(arrowstyle='->',lw=1.4,color='#222222'))
    ax1.set(xlim=(-np.pi,np.pi),ylim=(-1.30,1.30),xlabel='x_c',ylabel='z_c',
            title='Axial check: red = actual future null directions')
    # Separate regular cap chart: same global conformal metric, Omega>0.
    from meridional_geometry import FrontCollar
    collar=FrontCollar('cap');ys=np.linspace(-.598,.598,35)
    p=np.linspace(-.7,.7,45);pp,yy=np.meshgrid(p,ys)
    ax2.plot_surface(pp/2,yy,pp/2,color='#7751a0',alpha=.27,shade=False)
    q=np.linspace(-.14,.14,35);qq,yy=np.meshgrid(q,ys)
    ax2.plot_surface(qq/2,yy,-qq/2,color=coloring.TEAL,alpha=.3,shade=False)
    ax2.plot(np.zeros_like(ys),ys,np.zeros_like(ys),color=coloring.TEAL,lw=2)
    sol,tau=collar.geodesic();z=sol.sol(np.linspace(0,sol.t[-1],160))
    ax2.plot((z[0]+z[1])/2,np.full(160,.3),(z[0]-z[1])/2,color='black',lw=2)
    event=sol.sol(tau)
    ax2.scatter([(event[0]+event[1])/2],[.3],[(event[0]-event[1])/2],color='black',s=22)
    ax2.scatter([0,0],[-.6,.6],[0,0],facecolors='white',edgecolors=RED,s=24)
    point=np.array([.18,-.2,.18]);a=np.linspace(0,2*np.pi,65)
    D=np.array([np.cos(a),np.sqrt(2)*np.sin(a),np.ones_like(a)])
    ring=point[:,None]+.07*D
    ax2.plot(*ring,color=RED,lw=.9)
    for j in range(0,65,8):ax2.plot(*np.array([point,ring[:,j]]).T,color=RED,lw=.6)
    ax2.set(xlim=(-.4,.42),ylim=(-.7,.7),zlim=(-.4,.5),xlabel='X_cap',ylabel='y',zlabel='T_cap')
    ax2.set_title('Regular cap crossing: Omega > 0',pad=15)
    ax2.view_init(elev=19,azim=-61);ax2.set_box_aspect((1,1.2,1))
    fig.suptitle('Checked interior picture: the boundary corner remains unresolved',fontsize=17,y=.965)
    fig.text(.08,.085,'Purple = bubble interior; teal = additional communication region; orange = rider.\n'
             'Red cones preserve the actual warp null directions. The cone height is an arbitrary coordinate.',fontsize=10)
    fig.text(.70,.085,'Purple plane: cap exit q = 0; teal: horizon p = 0.\nBlack curve: timelike crossing. Open red marks: excluded rim.',fontsize=10)
    fig.text(.5,.025,'Regular-part conformal visualization with a separate cap chart. Rider, rim and spatial corners remain unadjoined.\n'
             'This is not a completed single-domain Penrose diagram; the usual flat-cone causal reading is invalid inside the bubble.',
             ha='center',fontsize=10)
    fig.savefig(OUT/'actual_curved_conformal_metric.png',dpi=180,bbox_inches='tight',pad_inches=.25)
    plt.close(fig)


if __name__=='__main__':
    audit()
    h=cap.build_horizon()
    purple,teal,_=coloring.sample(h)
    walls,tubes,_=coloring.surface_geometry(h)
    draw(h,purple,teal,walls,tubes)
