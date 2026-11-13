"""Color the full background double-cone interior by the inverse warp geometry.

Purple: Phi<0 (inside the chosen stationary-limit wall).
Teal: inside the rider communication tube, but outside that bubble interior.
The entire finite interior is classified; no resolved endpoint attachment
or future-temporal interpretation of the background height is asserted.
"""
import json
import numpy as np

import capped_horizon_atlas as cap
import cone_point_classifier as chart

OUT=cap.OUT
PURPLE,TEAL,ORANGE='#8655ad','#27999c','#d27c18'


def fields(X,Y,Z,horizon):
    t,x,y=chart.inverse(X,Y,Z)
    phi=x*x+cap.psi(y)-1
    ht=horizon.h(y)
    communication=np.abs(x)<ht
    bubble=phi<0
    return bubble,communication,phi,np.abs(x)-ht


def sample(horizon,n=181):
    axis=np.linspace(-np.pi,np.pi,n)
    XX,YY=np.meshgrid(axis,axis,indexing='xy')
    rr=np.hypot(XX,YY)
    purple=[];teal=[];counts=[0,0,0];violations=0
    for z in axis:
        valid=rr+abs(z)<np.pi-1e-10
        if not np.any(valid):continue
        x=XX[valid];y=YY[valid];zz=np.full(len(x),z)
        bubble,tube,_,_=fields(x,y,zz,horizon)
        violations+=int(np.count_nonzero(bubble&~tube))
        purple.append(np.array([x[bubble],y[bubble],zz[bubble]]).T)
        extra=tube&~bubble
        teal.append(np.array([x[extra],y[extra],zz[extra]]).T)
        counts[0]+=len(x);counts[1]+=int(np.count_nonzero(bubble));counts[2]+=int(np.count_nonzero(tube))
    assert violations==0
    return np.vstack(purple),np.vstack(teal),counts


def surface_geometry(horizon):
    # A logarithmic time mesh resolves the finite interior near its thin ends.
    time=np.sinh(np.linspace(-5.3,5.3,221))
    yw=np.linspace(-1,1,241)
    xw=np.sqrt(np.maximum(1-cap.psi(yw),0))
    yt=np.linspace(-horizon.C/cap.CONE,horizon.C/cap.CONE,281)
    xt=horizon.h(yt)
    walls=[];tubes=[];wall_res=[];tube_res=[];roundtrips=[]
    for sign in (-1,1):
        tt,yy=np.meshgrid(time,yw,indexing='ij')
        xx=np.broadcast_to(sign*xw,tt.shape)
        z=chart.forward(tt,xx,yy)
        recovered=chart.inverse(*z)
        wall_res.append(float(np.max(np.abs(recovered[1]**2+cap.psi(recovered[2])-1))))
        roundtrips.append(float(np.max(np.abs(recovered-np.array([tt,xx,yy])))))
        walls.append(z)
        tt,yy=np.meshgrid(time,yt,indexing='ij')
        xx=np.broadcast_to(sign*xt,tt.shape)
        z=chart.forward(tt,xx,yy)
        recovered=chart.inverse(*z)
        tube_res.append(float(np.max(np.abs(np.abs(recovered[1])-horizon.h(recovered[2])))))
        tubes.append(z)
    assert max(wall_res)<1e-7 and max(tube_res)<1e-7
    return walls,tubes,dict(max_bubble_surface_residual=max(wall_res),
                            max_communication_surface_residual=max(tube_res),
                            max_surface_roundtrip_error=max(roundtrips),
                            physical_time_extent=float(time[-1]))


def section(horizon,kind,n=701):
    axis=np.linspace(-np.pi,np.pi,n)
    P,Q=np.meshgrid(axis,axis)
    if kind=='axial':
        valid=abs(Q)+abs(P)<np.pi-1e-10
        X,Y,Z=P[valid],np.zeros(np.count_nonzero(valid)),Q[valid]
    else:
        valid=np.hypot(P,Q)<np.pi-1e-10
        X,Y,Z=P[valid],Q[valid],np.zeros(np.count_nonzero(valid))
    bubble,tube,_,_=fields(X,Y,Z,horizon)
    result=np.full(P.shape,np.nan)
    result[valid]=np.where(bubble,2,np.where(tube,1,0))
    if kind=='axial':assert np.all(bubble==tube)
    return axis,result


def draw(horizon,purple,teal,walls,tubes):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap,BoundaryNorm
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    fig=plt.figure(figsize=(15,11))
    ax=fig.add_axes([.015,.12,.63,.78],projection='3d')
    ax1=fig.add_axes([.72,.56,.26,.31])
    ax2=fig.add_axes([.72,.16,.26,.31])
    # Full cone: auxiliary coordinate boundary is shown for orientation.
    theta=np.linspace(0,2*np.pi,140)
    for sign in (-1,1):
        for zz in np.linspace(.05,np.pi-.05,12):
            rr=np.pi-zz
            ax.plot(rr*np.cos(theta),rr*np.sin(theta),np.full_like(theta,sign*zz),
                    color='#7389a4',lw=.6,alpha=.23)
        for ang in np.linspace(0,2*np.pi,17):
            zz=np.linspace(.02,np.pi,150);rr=np.pi-zz
            ax.plot(rr*np.cos(ang),rr*np.sin(ang),sign*zz,color='#7389a4',lw=.6,alpha=.23)
    ax.plot(np.pi*np.cos(theta),np.pi*np.sin(theta),0*theta,color='.45',ls='--',lw=.9)
    # These volume colors come from inverse-classified display-grid points.
    rng=np.random.default_rng(8301)
    for points,color in ((teal,TEAL),(purple,PURPLE)):
        chosen=points if len(points)<=14000 else points[rng.choice(len(points),14000,replace=False)]
        ax.scatter(chosen[:,0],chosen[:,1],chosen[:,2],c=color,s=1.7,alpha=.065,
                   linewidths=0,depthshade=False,rasterized=True)
    # Exact wall/horizon meshes complement the grid where the ends are thin.
    # Every finite mesh point was independently checked with the inverse.
    for z in tubes:
        ax.plot_surface(*z,color=TEAL,alpha=.12,shade=False,linewidth=0,rstride=4,cstride=4)
    for z in walls:
        ax.plot_surface(*z,color=PURPLE,alpha=.22,shade=False,linewidth=0,rstride=4,cstride=4)
    # Reference sections at actual rider times help reveal the nested volumes.
    for time0 in (-1.,0.,1.):
        for ys,xs,col in ((np.linspace(-1,1,241),None,PURPLE),
                          (np.linspace(-horizon.C/cap.CONE,horizon.C/cap.CONE,281),None,TEAL)):
            xs=np.sqrt(np.maximum(1-cap.psi(ys),0)) if col==PURPLE else horizon.h(ys)
            loopx=np.r_[xs,-xs[::-1],xs[:1]]
            loopy=np.r_[ys,ys[::-1],ys[:1]]
            loop=chart.forward(np.full_like(loopx,time0),loopx,loopy)
            ax.plot(*loop,color=col,lw=1.1 if time0==0 else .6,alpha=.8)
    time=np.sinh(np.linspace(-6,6,700))
    rider=chart.forward(time,0*time,0*time)
    ax.plot(*rider,c=ORANGE,lw=2.5)
    ax.scatter([-np.pi,np.pi],[0,0],[0,0],facecolors='white',edgecolors='.3',s=33)
    ax.text(np.pi,.03,.08,'t → +∞',fontsize=9)
    ax.text(-np.pi,.03,-.22,'t → −∞',fontsize=9)
    ax.set(xlim=(-3.3,3.3),ylim=(-3.3,3.3),zlim=(-3.3,3.3),
           xlabel='Cone x_c',ylabel='Cone y_c',zlabel='Cone z_c (background compact time)')
    ax.view_init(elev=16,azim=-66);ax.set_box_aspect((1,1,1.1),zoom=1.08)
    ax.set_title('Full double cone: inverse-classified interior',fontsize=14,pad=17)
    colors=ListedColormap(['#ffffff',TEAL,PURPLE]);norm=BoundaryNorm([-.5,.5,1.5,2.5],3)
    axis,img=section(horizon,'axial')
    ax1.imshow(img,origin='lower',extent=(-np.pi,np.pi,-np.pi,np.pi),cmap=colors,norm=norm,
               interpolation='nearest',aspect='equal')
    diamond=np.array([[0,np.pi],[np.pi,0],[0,-np.pi],[-np.pi,0],[0,np.pi]])
    ax1.plot(*diamond.T,color='.5',lw=.8)
    ax1.plot(rider[0],rider[2],color=ORANGE,lw=1.8)
    ax1.set(xlim=(-np.pi,np.pi),ylim=(-1.35,1.35),xlabel='Cone x_c',ylabel='Cone z_c',
            title='Axial waist slice: y_c = 0\nBubble and tube coincide on this slice',aspect='equal')
    for t in (-2.,-.5,.5,2.):
        z=chart.forward(t,0.,0.)
        ax1.scatter([z[0]],[z[2]],s=11,c=ORANGE)
        ax1.annotate(f't={t:g}',(z[0],z[2]),xytext=(0,7 if t>0 else -13),
                     textcoords='offset points',fontsize=7,ha='center')
    axis,img=section(horizon,'equator')
    ax2.imshow(img,origin='lower',extent=(-np.pi,np.pi,-np.pi,np.pi),cmap=colors,norm=norm,
               interpolation='nearest',aspect='equal')
    ax2.plot(np.pi*np.cos(theta),np.pi*np.sin(theta),color='.5',lw=.8)
    ax2.set(xlim=(-2.2,2.2),ylim=(-2.2,2.2),xlabel='Cone x_c',ylabel='Cone y_c',
            title='Equatorial slice: z_c = 0 (t = 0)')
    ax2.grid(alpha=.1)
    handles=[Patch(facecolor=PURPLE,label='Bubble interior: Φ < 0'),
             Patch(facecolor=TEAL,label='Communication tube outside bubble'),
             Line2D([0],[0],color=ORANGE,lw=2,label='Central rider')]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.075),ncol=3,frameon=False,fontsize=11)
    fig.suptitle('Where the capped bubble and its communication tube actually lie in the double cone',
                 fontsize=18,y=.96)
    fig.text(.5,.025,'Colors use the exact inverse at finite interior points. Surface meshes are independently inverse-checked.\n'
             'This background-coordinate image compresses different bubble ends at its waist; those boundary identifications remain unresolved.',
             ha='center',fontsize=10)
    fig.savefig(OUT/'inverse_colored_full_cone.png',dpi=180,bbox_inches='tight',pad_inches=.25)
    plt.close(fig)


def main():
    horizon=cap.build_horizon()
    purple,teal,counts=sample(horizon)
    walls,tubes,check=surface_geometry(horizon)
    # The center's compactified height turns over at |t|=1/sqrt(3).
    turn=chart.forward(1/np.sqrt(3),0.,0.)
    assert abs(turn[2]-np.pi/6)<1e-14
    report=dict(grid_resolution=181,interior_grid_points=counts[0],
                bubble_points=counts[1],communication_tube_points=counts[2],
                bubble_is_subset_of_tube=True,
                center_maximum_cone_height=float(turn[2]),
                **check,
                scope='Exact finite-interior coordinate image. Auxiliary cone boundary is not a resolved physical completion.')
    (OUT/'inverse_colored_full_cone_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    draw(horizon,purple,teal,walls,tubes)


if __name__=='__main__':
    main()
