"""Invert interior double-cone Cartesian coordinates and classify the bubble.

The map is a global interior coordinate map of the actual spacetime. Its
boundary is not asserted to be a resolved warp-spacetime conformal boundary.
Zc denotes compactified TIME, not a third original spatial coordinate.
"""
import json
import numpy as np
import capped_horizon_atlas as cap


def forward(t,x,y,speed=2.):
    """Original comoving (t,x,y) -> cone Cartesian (Xc,Yc,Zc)."""
    t,x,y=np.broadcast_arrays(t,x,y)
    lab=x+speed*t
    radius=np.hypot(lab,y)
    aa=np.arctan(t-radius);bb=np.arctan(t+radius)
    chi=bb-aa
    factor=np.divide(chi,radius,out=np.ones_like(radius,dtype=float),where=radius!=0)
    # At the spatial origin both spatial products vanish, so the removable
    # factor's chosen value is irrelevant to the forward image.
    return np.array([factor*lab,factor*y,aa+bb])


def inverse(Xc,Yc,Zc,speed=2.):
    """Cone interior -> original comoving coordinates; reject boundary points."""
    Xc,Yc,Zc=np.broadcast_arrays(np.asarray(Xc,dtype=float),np.asarray(Yc,dtype=float),
                                 np.asarray(Zc,dtype=float))
    chi=np.hypot(Xc,Yc)
    if np.any(np.abs(Zc)+chi>=np.pi):
        raise ValueError('The point must be strictly inside |Zc|+hypot(Xc,Yc)<pi.')
    omega=np.cos(Zc)+np.cos(chi)
    if np.any(omega<=0):
        raise ValueError('Nonpositive denominator: not an interior point in this chart.')
    tt=np.sin(Zc)/omega
    factor=np.sinc(chi/np.pi)/omega
    labx=factor*Xc
    yy=factor*Yc
    return np.array([tt,labx-speed*tt,yy])


def classify(Xc,Yc,Zc):
    t,x,y=inverse(Xc,Yc,Zc)
    phi=x*x+cap.psi(y)-1
    shift=cap.shift(x,y)
    return dict(t=float(t),comoving_x=float(x),signed_y=float(y),
                wall_function=float(phi),shift=float(shift),
                relative_to_wall='inside' if phi<0 else 'outside' if phi>0 else 'on wall',
                flat_core=bool(shift==0),flat_exterior=bool(shift==-2))


def audit():
    rng=np.random.default_rng(20261030)
    t=rng.uniform(-10,10,2000);x=rng.uniform(-4,4,2000);y=rng.uniform(-3,3,2000)
    mapped=forward(t,x,y)
    recovered=inverse(*mapped)
    err=float(np.max(np.abs(recovered-np.array([t,x,y]))))
    assert err<2e-10
    results=[]
    for original in ((0.,0.,0.),(0.,.8,0.),(0.,1.2,0.),(0.,0.,1.2),
                     (4.,0.,0.),(4.,1.2,0.),(-4.,0.,0.)):
        z=forward(*original)
        state=classify(*z)
        expected=original[1]**2+cap.psi(original[2])-1
        assert (state['wall_function']<0)==(expected<0)
        results.append(dict(cone_coordinates=z.tolist(),classification=state))
    # Boundary data have no finite inverse in this chart.
    try:
        inverse(0.,0.,np.pi)
    except ValueError:
        pass
    else:
        raise AssertionError('Boundary was incorrectly accepted')
    report=dict(max_roundtrip_error=err,examples=results,
                scope='Exact interior inverse and pointwise wall classification; no resolved boundary claimed.')
    (cap.OUT/'cone_point_classifier_check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    audit()
