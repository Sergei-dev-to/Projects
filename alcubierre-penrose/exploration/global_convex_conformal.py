"""One global bounded coordinate map, with regular scri and cap attachments.

Coordinates are the gradient of a strictly convex potential. The image is
the interior of an explicit convex body. The same metric is rescaled by
the already verified global conformal factor. Residual boundary faces
retain approach directions and are allowed to be singular.
"""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import root, brentq
from scipy.integrate import solve_ivp
from scipy.spatial import ConvexHull
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import capped_horizon_atlas as cap
from proper_conformal_completion import global_factor

OUT=Path(__file__).resolve().parents[1]/'output/global_convex_conformal'
A,B,BETA,C,D,WIDTH=1.,.15,1.45,.04,.04,.15
OFFSET=2.
SY=1/cap.APERTURE
L=np.array([[-2.,1.,0.],[0.,0.,SY]])
LX=L[0]
ET=np.array([1.,0.,0.])
EX=np.array([0.,1.,0.])
GLX,GLW=leggauss(64)


def radial(z):
    """H(|z|), its gradient and its positive-definite Hessian."""
    z=np.asarray(z); s=np.sqrt(1+np.sum(z*z,axis=-1))
    value=s-np.log1p(s)
    grad=z/(1+s)[...,None]
    hess=np.eye(z.shape[-1])/(1+s)[...,None,None]
    hess=hess-z[..., :,None]*z[...,None,:]/(s*(1+s)**2)[...,None,None]
    return value,grad,hess


def one(z):
    s=np.sqrt(1+z*z)
    return s-np.log1p(s),z/(1+s),1/(s*(1+s))


def exterior_potential(w):
    w=np.asarray(w,dtype=float); t=w[...,0]; xy=w[...,1:]
    rr=np.linalg.norm(xy,axis=-1)
    value,grad,hess=radial(w)
    value=A*value;grad=A*grad;hess=A*hess
    vp,hp,hpp=one(t+rr);vm,hm,hpm=one(t-rr)
    value+=B*(vp+vm)
    nr=np.divide(xy,rr[...,None],out=np.zeros_like(xy),where=rr[...,None]>1e-12)
    dr=B*(hp-hm);dtt=B*(hpp+hpm);dtr=B*(hpp-hpm)
    grad[...,0]+=B*(hp+hm)
    grad[...,1:]+=dr[...,None]*nr
    hess[...,0,0]+=dtt
    hess[...,0,1:]+=dtr[...,None]*nr
    hess[...,1:,0]+=dtr[...,None]*nr
    tang=np.divide(dr,rr,out=np.array(2*B*one(t)[2],copy=True),where=rr>1e-12)
    nn=nr[..., :,None]*nr[...,None,:]
    hess[...,1:,1:]+=dtt[...,None,None]*nn+tang[...,None,None]*(np.eye(2)-nn)
    return value,grad,hess


def front_potential(w):
    w=np.asarray(w,dtype=float);t=w[...,0]
    z=w@L.T;x=z[...,0]
    value,gz,hz=radial(z)
    value=C*value+BETA*w[...,1]-OFFSET
    grad=C*(gz@L)+BETA*EX
    hess=C*np.einsum('ai,...ab,bj->...ij',L,hz,L)
    q=np.logaddexp(0,-t)
    sigmoid=1/(1+np.exp(-np.clip(t,-700,700)))
    qt=-(1-sigmoid);qtt=sigmoid*(1-sigmoid)
    # Stable negative-t derivative even when sigmoid rounds to one.
    qt=-np.exp(-np.logaddexp(0,t))
    qtt=np.exp(-np.logaddexp(0,t)-np.logaddexp(0,-t))
    ss=x-1;rad=np.hypot(ss,q)
    value+=D*rad
    grad+=D*((ss/rad)[...,None]*LX+(q*qt/rad)[...,None]*ET)
    hss=q*q/rad**3
    hst=-ss*q*qt/rad**3
    htt=q*qtt/rad+qt*qt*ss*ss/rad**3
    hess+=D*(hss[...,None,None]*np.outer(LX,LX)
             +hst[...,None,None]*(np.outer(LX,ET)+np.outer(ET,LX))
             +htt[...,None,None]*np.outer(ET,ET))
    return value,grad,hess


def rear_potential(w):
    value,grad,hess=front_potential(-np.asarray(w))
    return value,-grad,hess


def smooth_max(pa,pb):
    av,ag,ah=pa;bv,bg,bh=pb;diff=av-bv
    weight=cap.step((diff+WIDTH)/(2*WIDTH))
    curvature=cap.stepprime((diff+WIDTH)/(2*WIDTH))/(2*WIDTH)
    mid=(diff>-WIDTH)&(diff<WIDTH)
    correction=np.maximum(diff,0.)
    if np.any(mid):
        ds=np.atleast_1d(diff)[np.atleast_1d(mid)]
        half=(ds+WIDTH)/2
        nodes=-WIDTH+half[:,None]*(GLX+1)
        integ=half*np.sum(GLW*cap.step((nodes+WIDTH)/(2*WIDTH)),axis=-1)
        correction=np.array(correction,copy=True)
        if correction.ndim==0:correction[...]=integ[0]
        else:correction[mid]=integ
    delta=ag-bg
    return (bv+correction,weight[...,None]*ag+(1-weight)[...,None]*bg,
            weight[...,None,None]*ah+(1-weight)[...,None,None]*bh
            +curvature[...,None,None]*delta[..., :,None]*delta[...,None,:])


def potential(w):
    return smooth_max(exterior_potential(w),smooth_max(front_potential(w),rear_potential(w)))


def coordinates(t,x,y):
    t,x,y=np.broadcast_arrays(t,x,y)
    return potential(np.stack([t,x+2*t,y],axis=-1))[1]


def inverse(z,guess=None):
    guess=np.zeros(3) if guess is None else np.asarray(guess)
    result=root(lambda w:potential(w)[1]-z,guess,jac=lambda w:potential(w)[2],tol=2e-10)
    if not result.success and np.linalg.norm(result.fun)>1e-9:
        raise RuntimeError(result.message)
    t,xx,y=result.x
    return np.array([t,xx-2*t,y]),float(np.linalg.norm(result.fun))


def cap_map(q,lam,y):
    """Exact front branch in regular cap coordinates; also valid for signed q."""
    q,lam,y=np.broadcast_arrays(np.asarray(q),np.asarray(lam),np.asarray(y))
    aq=np.empty_like(q,dtype=np.result_type(q,lam,y,float))
    small=np.abs(q)<1e-5
    aq[small]=1-q[small]/2+q[small]**2/3-q[small]**3/4+q[small]**4/5
    aq[~small]=np.log1p(q[~small])/q[~small]
    x=1+q*lam;s=np.sqrt(1+x*x+(SY*y)**2)
    den=np.sqrt(lam*lam+aq*aq)
    zx=BETA+C*x/(1+s)+D*lam/den
    zy=C*SY*SY*y/(1+s)
    zt=-2*C*x/(1+s)+D*(-2*lam/den-q*aq/((1+q)*den))
    return np.stack([zt,zx,zy],axis=-1)


def cap_jac(q,lam,y):
    args=np.array([q,lam,y],dtype=complex);result=[]
    for k in range(3):
        z=args.copy();z[k]+=1e-25j
        result.append(np.imag(cap_map(*z))/1e-25)
    return np.array(result).T


def scri_map(u,theta,past=False):
    u,theta=np.broadcast_arrays(u,theta);hh=one(u)[1]
    if past:tt=-A/np.sqrt(2)+B*(hh-1);rr=A/np.sqrt(2)+B*(hh+1)
    else:tt=A/np.sqrt(2)+B*(hh+1);rr=A/np.sqrt(2)+B*(1-hh)
    return np.stack([tt,rr*np.cos(theta),rr*np.sin(theta)],axis=-1)


def scri_jac(u,theta):
    n=np.array([np.cos(theta),np.sin(theta)])
    nr=np.array([-np.sin(theta),np.cos(theta)])
    radius=A/np.sqrt(2)+B*(1-one(u)[1])
    jr=np.r_[A*u/(2*np.sqrt(2))-(A+B)/2,
             (-A*u/(2*np.sqrt(2))-(A+B)/2)*n]
    ju=B*one(u)[2]*np.r_[1.,-n]
    ja=np.r_[0.,radius*nr]
    return np.column_stack([jr,ju,ja])


def stationary_end(x,y):
    x,y=np.broadcast_arrays(x,y);s=np.sqrt(1+x*x+(SY*y)**2)
    k=np.sign(x-1)
    zx=BETA+C*x/(1+s)+D*k
    return np.stack([-2*(zx-BETA),zx,C*SY*SY*y/(1+s)],axis=-1)


def support(n):
    n=np.asarray(n);tt=n[...,0];rr=np.linalg.norm(n[...,1:],axis=-1)
    z=n@L.T
    ext=A*np.linalg.norm(n,axis=-1)+2*B*np.maximum(np.abs(tt),rr)
    front=BETA*n[...,1]+C*np.linalg.norm(z,axis=-1)+D*np.hypot(z[...,0],np.minimum(tt,0))
    rear=-BETA*n[...,1]+C*np.linalg.norm(z,axis=-1)+D*np.hypot(z[...,0],np.maximum(tt,0))
    return np.maximum(ext,np.maximum(front,rear))


def audit():
    # Uniform branch dominance at ordinary null infinity and bubble ends.
    scri_margin=A*np.sqrt(2)+2*B-(BETA+3*C+np.sqrt(10)*D)
    bubble_margin=2*BETA-(A*np.sqrt(5)+4*B)
    assert scri_margin>0 and bubble_margin>0 and SY**2<=3
    rng=np.random.default_rng(20261101)
    physical=rng.uniform([-5,-3,-2],[5,3,2],size=(90,3))
    w=physical.copy();w[:,1]+=2*w[:,0]
    _,z,hess=potential(w)
    mineig=float(np.min(np.linalg.eigvalsh(hess)))
    assert mineig>0
    inverse_errors=[];null_errors=[]
    for p,zz,hh in zip(physical[:15],z[:15],hess[:15]):
        back,_=inverse(zz)
        inverse_errors.append(float(np.max(np.abs(back-p))))
        t,x,y=p;v=float(cap.shift(x,y))+2
        gm=np.array([[v*v-1,-v,0],[-v,1,0],[0,0,1.]])
        inv=np.linalg.inv(hh);om=float(global_factor(t,x,y))
        unphys=om*om*inv.T@gm@inv
        alpha=.71;k=np.array([1,v+np.cos(alpha),np.sin(alpha)])
        mapped=hh@k
        null_errors.append(abs(float(mapped@unphys@mapped))/(1+np.linalg.norm(mapped)**2*np.linalg.norm(unphys)))
    assert max(inverse_errors)<2e-7 and max(null_errors)<1e-12
    # Finite-difference verification of the analytic Hessian, including blend zones.
    hes_errors=[]
    for ww in w[:12]:
        hs=potential(ww)[2];eps=1e-5
        fd=np.column_stack([(potential(ww+eps*np.eye(3)[i])[1]-potential(ww-eps*np.eye(3)[i])[1])/(2*eps) for i in range(3)])
        hes_errors.append(float(np.max(np.abs(fd-hs))))
    assert max(hes_errors)<2e-7
    cap_errors=[];cap_dets=[];cap_null=[]
    for lam in (-2.,-.4,0.,1.5):
        for yy in (-.5,0.,.5):
            for qq in (.01,.003):
                actual=coordinates(-np.log(qq),1+qq*lam,yy)
                cap_errors.append(float(np.max(np.abs(actual-cap_map(qq,lam,yy)))))
            jj=cap_jac(0.,lam,yy)
            ss=np.sqrt(2+(SY*yy)**2)
            fyy=SY**2/(1+ss)-SY**4*yy**2/(ss*(1+ss)**2)
            det_expected=-C*D*D*fyy/(1+lam*lam)**2
            assert abs(np.linalg.det(jj)-det_expected)<1e-14
            gm=np.array([[lam*lam,-1,0],[-1,0,0],[0,0,1.]])
            inv=np.linalg.inv(jj);gg=inv.T@gm@inv/(1+lam*lam)
            normal=np.array([1.,2.,0.])
            cap_null.append(abs(float(normal@np.linalg.inv(gg)@normal)))
            cap_dets.append(float(np.linalg.det(gg)))
    assert max(cap_errors)<1e-10 and max(cap_null)<1e-12 and max(cap_dets)<0
    scri_errors=[];scri_null=[]
    for u in (-3.,0.,2.):
        for theta in (0.,np.pi/3,2.,np.pi):
            target=scri_map(u,theta)
            for rr in (10000.,100000.):
                ww=np.array([rr+u,rr*np.cos(theta),rr*np.sin(theta)])
                zv=potential(ww)[1]
                scri_errors.append(dict(R=rr,error=float(np.linalg.norm(zv-target))))
                assert np.max(np.abs(zv-exterior_potential(ww)[1]))<1e-13
            jj=scri_jac(u,theta);assert abs(np.linalg.det(jj))>1e-6
            gm=np.array([[0,1,0],[1,0,0],[0,0,1.]])
            inv=np.linalg.inv(jj);gg=inv.T@gm@inv
            normal=np.array([1.,np.cos(theta),np.sin(theta)])
            scri_null.append(abs(float(normal@np.linalg.inv(gg)@normal)))
    assert max(scri_null)<1e-12
    horizon=cap.build_horizon();yy=.9;xx=float(horizon.h(yy))
    rider=stationary_end(0.,0.);wing=stationary_end(xx,yy)
    assert np.linalg.norm(wing-rider)>.02
    # Cap infinite labels attach to x=1 +/- stationary-face curves, not to rider.
    left=stationary_end(1-1e-8,.3)
    right=stationary_end(1+1e-8,.3)
    assert np.linalg.norm(cap_map(0.,-1e6,.3)-left)<1e-8
    assert np.linalg.norm(cap_map(0.,1e6,.3)-right)<1e-8
    separation=2*BETA-(3*A/np.sqrt(2)+4*B)
    assert separation>0
    # Horizon-to-scri incidence, including the half-generator below its focal cut.
    wing_scri=[];um=-horizon.C/2
    for uu in (um,um-.7,um-2.):
        errors=[]
        for rr in (1e4,1e5):
            theta=np.pi/3+np.arccos(1-(um-uu)/rr)
            tt=rr+uu;xx=rr*np.cos(theta)-2*tt;yy=rr*np.sin(theta)
            assert abs(xx-float(horizon.h(yy)))<1e-9
            errors.append(float(np.linalg.norm(coordinates(tt,xx,yy)-scri_map(uu,np.pi/3))))
        assert errors[1]<errors[0]
        wing_scri.append(dict(u=uu,errors=errors))
    # Wall/rim mixed approaches land at the specified rim label, not at the rider.
    rim_errors=[]
    for lam in (-.2,-1.):
        for qq in (1e-4,1e-7):
            xx=1+qq*lam;target=1-xx*xx
            yy=brentq(lambda yy:float(cap.psi(yy))-target,cap.APERTURE,1.,xtol=1e-14)
            mapped=coordinates(-np.log(qq),xx,yy)
            expected=cap_map(0.,lam,cap.APERTURE)
            rim_errors.append(dict(q=qq,cap_lambda=lam,y=yy,
                                   error=float(np.linalg.norm(mapped-expected))))
    report=dict(parameters=dict(A=A,B=B,BETA=BETA,C=C,D=D,transverse_scale=SY,branch_offset=OFFSET),
       uniform_scri_dominance_margin=scri_margin,bubble_dominance_margin=bubble_margin,
       minimum_sampled_hessian_eigenvalue=mineig,max_inverse_error=max(inverse_errors),
       max_hessian_difference=max(hes_errors),max_normalized_null_error=max(null_errors),
       max_cap_formula_error=max(cap_errors),max_cap_normal_null_error=max(cap_null),
       max_scri_normal_null_error=max(scri_null),scri_convergence=scri_errors,
       front_cap_rescaled_metric_determinants=cap_dets,
       rider_point=rider.tolist(),sending_wing_end=wing.tolist(),
       rider_wing_separation=float(np.linalg.norm(wing-rider)),
       cap_scri_separating_functional_gap=separation,
       horizon_scri_attachment_checks=wing_scri,wall_rim_attachment_checks=rim_errors,
       scope='Global bounded conformal metric representation; residual boundary is singular/resolved. Not equivalent to the chronological c-boundary; display height is not asserted temporal.')
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


def domain_mesh():
    # Support points of the three convex bodies whose convex hull is K.
    count=2200;zz=1-2*(np.arange(count)+.5)/count
    theta=np.arange(count)*np.pi*(3-np.sqrt(5))
    ns=np.stack([zz,np.sqrt(1-zz*zz)*np.cos(theta),np.sqrt(1-zz*zz)*np.sin(theta)],axis=-1)
    pts=[]
    for n in ns:
        tt=n[0];r=np.linalg.norm(n[1:]);sp=n@L.T
        ext=A*n
        if abs(tt)>r:ext=ext+2*B*np.sign(tt)*ET
        else:ext=ext+2*B*np.r_[0,n[1:]/r]
        pts.append(ext)
        for sign in (1,-1):
            base=sign*BETA*EX+C*(sp/np.linalg.norm(sp))@L
            ta=min(tt,0) if sign==1 else max(tt,0)
            den=np.hypot(sp[0],ta)
            pts.append(base+D*(sp[0]*LX+ta*ET)/den)
    # Include exact boundary circles of scri and stadium facets.
    aa=np.linspace(0,2*np.pi,180,endpoint=False)
    for past in (False,True):
        for uu in (-1e8,1e8):pts.extend(scri_map(uu,aa,past))
    for sign in (1,-1):
        for ang in aa:
            pts.append(sign*(BETA*EX+(C*np.cos(ang)+D*np.sign(np.cos(ang)))*LX+C*np.sin(ang)*L[1]))
    pts=np.asarray(pts);hull=ConvexHull(pts)
    used=np.unique(hull.simplices);lookup=np.full(len(pts),-1,dtype=int);lookup[used]=np.arange(len(used))
    return pts[used],lookup[hull.simplices]


def grid_faces(n,m):
    return np.array([[i*m+j,(i+1)*m+j,(i+1)*m+j+1] for i in range(n-1) for j in range(m-1)]
                    +[[i*m+j,(i+1)*m+j+1,i*m+j+1] for i in range(n-1) for j in range(m-1)])


def scene():
    vertices,faces=domain_mesh()
    meshes=[dict(name='Singular / resolved boundary',vertices=vertices.tolist(),faces=faces.tolist(),color='#aeb8c4',opacity=.16)]
    lines=[]
    for past,color,label in ((False,'#398cb5','Future null infinity'),(True,'#5474bd','Past null infinity')):
        hvals=np.linspace(-.999,.999,25);us=2*hvals/(1-hvals*hvals)
        angles=np.linspace(0,2*np.pi,85)
        uu,aa=np.meshgrid(us,angles,indexing='ij')
        vv=scri_map(uu,aa,past).reshape(-1,3)
        meshes.append(dict(name=label,vertices=vv.tolist(),faces=grid_faces(len(us),len(angles)).tolist(),color=color,opacity=.42))
    for sign,color,label in ((1,'#d68a26','Front cap'),(-1,'#9a60af','Rear cap')):
        kval=np.linspace(-.9999,.9999,41);ys=np.linspace(-cap.APERTURE,cap.APERTURE,19)
        kk,yy=np.meshgrid(kval,ys,indexing='ij');ll=kk/np.sqrt(1-kk*kk)
        vv=sign*cap_map(0.,ll,yy)
        meshes.append(dict(name=label,vertices=vv.reshape(-1,3).tolist(),faces=grid_faces(len(kval),len(ys)).tolist(),color=color,opacity=.9))
        for yval in (-cap.APERTURE,cap.APERTURE):
            lines.append(dict(name=label+' rim',points=(sign*cap_map(0.,kval/np.sqrt(1-kval*kval),yval)).tolist(),color='#b52f3e',width=3))
    times=np.linspace(-9,9,1601)
    rider=coordinates(times,0*times,0*times)
    lines.append(dict(name='Central rider',points=rider.tolist(),color='#242328',width=3))
    # Bubble wall and horizons in the SAME global coordinates.
    ywall=np.linspace(-1,1,100);xx=np.sqrt(np.maximum(1-cap.psi(ywall),0))
    wallx=np.r_[xx,-xx[::-1],xx[0]];wally=np.r_[ywall,ywall[::-1],ywall[0]]
    for tt in (-5.,-2.,0.,2.,5.):
        lines.append(dict(name='Bubble wall',points=coordinates(tt,wallx,wally).tolist(),color='#218982',width=1.2))
    ts=np.linspace(-7,7,81);tt,ss=np.meshgrid(ts,np.arange(len(wallx)),indexing='ij')
    wallmesh=coordinates(tt,wallx[ss],wally[ss])
    meshes.append(dict(name='Stationary-limit wall tube',vertices=wallmesh.reshape(-1,3).tolist(),
                       faces=grid_faces(len(ts),len(wallx)).tolist(),color='#37a293',opacity=.12))
    horizon=cap.build_horizon()
    for sign in (1,-1):
        for tt in (-4.,0.,4.):
            yy=np.linspace(-8,8,220);xx=sign*horizon.h(yy)
            lines.append(dict(name='Communication horizons',points=coordinates(tt,xx,yy).tolist(),color='#b56c40' if sign==1 else '#8655a2',width=1))
    # Actual null generators; time samples become logarithmic in the flat tail.
    def gen_rhs(tt,z):
        yy=z[0];xx=float(horizon.h(yy));vv=float(cap.shift(xx,yy))
        return [np.sqrt(max(vv*vv-1,0))/(-vv)]
    past=solve_ivp(gen_rhs,[0,-15],[.9],rtol=2e-10,atol=1e-12,dense_output=True)
    future=solve_ivp(gen_rhs,[0,1000],[.9],rtol=2e-10,atol=1e-12,dense_output=True)
    ts=np.r_[np.linspace(-15,0,600),np.geomspace(.003,1000,900)]
    ys=np.where(ts<=0,past.sol(np.minimum(ts,0))[0],future.sol(np.maximum(ts,0))[0])
    gen=coordinates(ts,horizon.h(ys),ys)
    lines.append(dict(name='Sending null generator',points=gen.tolist(),color='#b4512b',width=2.5))
    lines.append(dict(name='Receiving null generator',points=(-gen).tolist(),color='#7445a1',width=2.5))
    for angle in (-np.pi/3,np.pi/3):
        us=np.r_[-1e5,np.linspace(-20,-horizon.C/2,100)]
        vv=scri_map(us,angle)
        lines.append(dict(name='Horizon contact at null infinity',points=vv.tolist(),color='#b4512b',width=2.5))
        lines.append(dict(name='Horizon contact at null infinity',points=(-vv).tolist(),color='#7445a1',width=2.5))
    points=[dict(name='Future rider end',point=stationary_end(0.,0.).tolist(),color='#111111'),
            dict(name='Past rider end',point=(-stationary_end(0.,0.)).tolist(),color='#111111')]
    return dict(meshes=meshes,lines=lines,points=points)


def draw_static(data):
    fig=plt.figure(figsize=(13,7.5));ax=fig.add_subplot(121,projection='3d');detail=fig.add_subplot(122)
    for mesh in data['meshes']:
        vv=np.array(mesh['vertices']);ff=np.array(mesh['faces'])
        collection=Poly3DCollection(vv[ff][:,:,[1,2,0]],facecolors=mesh['color'],edgecolors='none',alpha=mesh['opacity'])
        ax.add_collection3d(collection)
    for line in data['lines']:
        if line['name']=='Communication horizons':continue
        vv=np.array(line['points']);ax.plot(vv[:,1],vv[:,2],vv[:,0],color=line['color'],lw=line['width']*.65)
    for item in data['points']:
        vv=np.array(item['point']);ax.scatter(vv[1],vv[2],vv[0],c=item['color'],s=16)
    ax.set(xlim=(-1.65,1.65),ylim=(-1.35,1.35),zlim=(-1.4,1.4),xlabel='$Z_X$',ylabel='$Z_y$',zlabel='$Z_t$')
    ax.set_box_aspect((3.3,2.7,2.8));ax.view_init(elev=21,azim=-58)
    ax.set_title('One bounded domain for the entire original patch',fontsize=11)
    # An affine view of the actual global front facet, not another chart.
    ang=np.linspace(0,2*np.pi,801)
    facet=BETA*EX+(C*np.cos(ang)+D*np.sign(np.cos(ang)))[:,None]*LX+C*np.sin(ang)[:,None]*L[1]
    detail.fill(facet[:,1],facet[:,2],color='#ece6d5',alpha=.75)
    ks=np.linspace(-.999999,.999999,101);ls=ks/np.sqrt(1-ks*ks)
    lo=cap_map(0.,ls,-cap.APERTURE);hi=cap_map(0.,ls,cap.APERTURE)
    detail.fill(np.r_[lo[:,1],hi[::-1,1]],np.r_[lo[:,2],hi[::-1,2]],color='#e4ad53',alpha=.8)
    for vv in (lo,hi):detail.plot(vv[:,1],vv[:,2],color='#b52f3e',lw=2)
    for lam in (-1e6,0.,1e6):
        vv=cap_map(0.,lam,np.linspace(-cap.APERTURE,cap.APERTURE,100))
        detail.plot(vv[:,1],vv[:,2],color='#9c6a27',lw=.8,ls='--' if lam==0 else '-')
    rp=stationary_end(0.,0.);detail.plot(rp[1],rp[2],'ko');detail.annotate('rider end',rp[[1,2]],xytext=(rp[1]-.028,-.027),arrowprops=dict(arrowstyle='->'),fontsize=9)
    yy=.9;hx=float(cap.build_horizon().h(yy));hp=stationary_end(hx,yy)
    detail.plot(hp[1],hp[2],'o',color='#b56c40');detail.annotate('outer sending-wing end',hp[[1,2]],xytext=(BETA-.075,.052),arrowprops=dict(arrowstyle='->'),fontsize=8)
    detail.text(BETA+.01,0,'regular\ncap',ha='center',va='center',fontsize=9)
    detail.text(BETA-.05,-.052,'Resolved stationary ends\n(singular metric)',ha='center',fontsize=9)
    detail.set(xlabel='$Z_X$',ylabel='$Z_y$',title='Front face: exact affine enlargement')
    detail.set_aspect('equal');detail.grid(alpha=.12)
    fig.suptitle('Global 2+1 conformal metric diagram with singular boundary pieces',fontsize=14)
    fig.text(.5,.025,'Blue: ordinary null infinity. Gold/purple: regular cap crossings. Red: singular rims. Gray: resolved/singular boundary.\nDisplay axes are coordinates, not a universal time direction; causal cones come from the rescaled metric.',ha='center',fontsize=9)
    fig.subplots_adjust(left=.03,right=.98,bottom=.12,top=.90,wspace=.12)
    fig.savefig(OUT/'global_conformal_domain.png',dpi=190)
    plt.close(fig)


if __name__=='__main__':
    result=audit()
    data=scene()
    rng=np.random.default_rng(991);normals=rng.normal(size=(500,3));normals/=np.linalg.norm(normals,axis=1)[:,None]
    meshvertices=np.array(data['meshes'][0]['vertices'])
    gaps=support(normals)-np.max(normals@meshvertices.T,axis=1)
    assert np.min(gaps)>-1e-12 and np.max(gaps)<.005
    result['maximum_sampled_rendering_support_deficit']=float(np.max(gaps))
    (OUT/'checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (OUT/'scene.json').write_text(json.dumps(data,separators=(',',':')),encoding='utf-8')
    template=Path(__file__).with_name('global_convex_viewer.html').read_text(encoding='utf-8')
    (OUT/'global_conformal_domain.html').write_text(template.replace('__SCENE_DATA__',json.dumps(data,separators=(',',':'))),encoding='utf-8')
    draw_static(data)
    print(json.dumps({k:v for k,v in result.items() if k not in ('scri_convergence','front_cap_rescaled_metric_determinants')},indent=2))
