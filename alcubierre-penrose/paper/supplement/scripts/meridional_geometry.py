"""Checked 2+1 quotient geometry for the rounded and capped front views.

Suppressing phi in g4=g3+rho**2 dphi**2 gives the exact causal quotient,
g3=-dt**2+(dx-v(x,rho)dt)**2+drho**2. No conformal flatness is assumed.
The axis-adapted p,q chart is pulled back from this metric BEFORE plotting.
"""
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import expi


AF = -np.pi/6
BF = np.pi/2
BASE = Path(__file__).resolve().parent


def plot_coordinates(p, q):
    """X,T relative to the front bifurcation point, same orientation as Fig. 2a."""
    aa = (2/3)*np.arctan(p)
    bb = -2*np.arctan(q)
    return (bb-aa)/2, (bb+aa)/2


class FrontCollar:
    def __init__(self, kind):
        self.kind = kind
        if kind == "cap":
            self.L, self.kappa, self.a = 1., 1., .6
            h0 = self.h(1.)
            self.scale = np.sqrt(2*np.exp(h0))
        elif kind == "rounded":
            self.L = float(np.arccosh(2.))
            self.kappa, self.a = np.sqrt(3)/2, 0.
            raw_pprime = -np.exp(self.kappa*self.L)/(1-np.exp(-2*self.L))
            raw_q = np.exp(-self.kappa*self.h(self.L))
            self.scale = np.sqrt(-1/(raw_pprime*raw_q))
        else:
            raise ValueError(kind)

    def h(self, x):
        x = np.asarray(x)
        if self.kind == "cap":
            return 2/np.sqrt(3)*np.arctan(x/np.sqrt(3))
        return x/3+4/(3*np.sqrt(5))*np.arctan((3*np.exp(x)-2)/np.sqrt(5))

    def v0(self, x):
        x = np.asarray(x)
        return -(1+x*x)/2 if self.kind == "cap" else 2/np.cosh(x)-2

    def v0prime(self, x):
        return -x if self.kind == "cap" else -2*np.tanh(x)/np.cosh(x)

    def pq_factors(self, x):
        """p=P(x)e^(k*t), q=Q(x)e^(-k*t); smooth P(L)=0."""
        x = np.asarray(x)
        if self.kind == "cap":
            pp = self.scale*(1-x)/(1+x)
        else:
            pp = self.scale*np.exp(self.kappa*x)*np.expm1(self.L-x)/(1-np.exp(-x-self.L))
        qq = self.scale*np.exp(-self.kappa*self.h(x))
        return pp, qq

    def F(self, x):
        p, q = self.pq_factors(x)
        return p*q

    def Fprime(self, x):
        pp, qq = self.pq_factors(x)
        if self.kind == "cap":
            pp_x = -2*self.scale/(1+x)**2
        else:
            den = 1-np.exp(-x-self.L)
            num = np.expm1(self.L-x)
            pp_x = self.kappa*pp+self.scale*np.exp(self.kappa*x)*(
                -np.exp(self.L-x)/den-num*np.exp(-x-self.L)/den**2)
        qq_x = self.kappa*qq/(self.v0(x)-1)
        return pp_x*qq+pp*qq_x

    def x_from_product(self, z):
        if abs(z) < 1e-15:
            return self.L
        return brentq(lambda x: self.F(x)-z,self.L-.4,self.L+.5,xtol=2e-14)

    def C(self, x):
        if self.kind == "cap":
            return (1+x)**2*(x*x+3)*np.exp(self.h(x))/(4*self.scale**2)
        if abs(x-self.L) < 2e-8:
            return 2/self.kappa
        # Stable factorization of v0+1 at the horizon.
        vp = -2*np.sinh((x+self.L)/2)*np.sinh((x-self.L)/2)/np.cosh(x)
        vm = self.v0(x)-1
        return -vp*vm/(self.kappa**2*self.F(x))

    def dlogC_dz(self, x):
        if self.kind == "cap":
            dlog_dx = 2/(1+x)+2*x/(x*x+3)+2/(x*x+3)
        elif abs(x-self.L) < 2e-7:
            dlog_dx = self.kappa-.5/self.kappa
        else:
            vv = self.v0(x)
            dlog_dx = 2*(vv*self.v0prime(x)-self.kappa)/(vv*vv-1)
        return dlog_dx/self.Fprime(x)

    @staticmethod
    def eta(u):
        u = np.asarray(u,dtype=float)
        ans = np.zeros_like(u)
        mask = u > 1e-8
        uu = u[mask]
        ans[mask] = uu*np.exp(-1/uu)+expi(-1/uu)
        return ans

    def psi(self, rho):
        # eta''>0, with flat matching at rho=a and psi(1)=1.
        return self.eta((np.asarray(rho)**2-self.a**2)/.2)/self.eta((1-self.a**2)/.2)

    def shift(self, x, rho):
        if self.kind == "cap":
            # This is exactly W(Phi)=-1-Phi/2 in the plotted collar.
            return -(1+x*x+self.psi(rho))/2
        return 2/np.cosh(np.hypot(x,rho))-2

    def wall_x(self, rho):
        if self.kind == "cap":
            return np.sqrt(1-self.psi(rho))
        return np.sqrt(self.L*self.L-np.asarray(rho)**2)

    def original_jacobian(self,p,q):
        x = self.x_from_product(p*q)
        xx_p, xx_q = q/self.Fprime(x), p/self.Fprime(x)
        tt_p = xx_p/(self.v0(x)-1)
        tt_q = -1/(self.kappa*q)+xx_q/(self.v0(x)-1)
        return x,np.array([[tt_p,tt_q,0.],[xx_p,xx_q,0.],[0.,0.,1.]])

    def metric_pq(self,p,q,rho):
        x = self.x_from_product(p*q)
        if self.kind == "cap" and rho <= self.a:
            if q <= 0 and rho >= self.a:
                raise ValueError("The cap rim is not an attached endpoint")
            cc = self.C(x)
            return np.array([[0.,cc/2,0.],[cc/2,0.,0.],[0.,0.,1.]])
        if q <= 0:
            raise ValueError("No 2+1 extension specified outside the open cap")
        x,jac = self.original_jacobian(p,q)
        v = self.shift(x,rho)
        old = np.array([[v*v-1,-v,0.],[-v,1.,0.],[0.,0.,1.]])
        return jac.T@old@jac

    @staticmethod
    def pq_from_plot_jacobian(p,q):
        ap = 2/(3*(1+p*p))
        bq = -2/(1+q*q)
        # Original order (p,q,rho), plot order (X,rho,T).
        return np.array([[-1/ap,0,1/ap],[1/bq,0,1/bq],[0,1.,0]])

    def conformal_factor(self,p,q):
        return 3*self.C(self.x_from_product(p*q))*(1+p*p)*(1+q*q)/4

    def metric_plot(self,p,q,rho):
        jac = self.pq_from_plot_jacobian(p,q)
        return jac.T@self.metric_pq(p,q,rho)@jac/self.conformal_factor(p,q)

    def null_directions(self,p,q,rho,theta):
        """Future tangent null cone, normalized to dT=1, in (X,rho,T)."""
        if self.kind == "cap" and rho < self.a:
            om = np.sqrt(self.conformal_factor(p,q))
            return np.array([np.cos(theta),om*np.sin(theta),np.ones_like(theta)]).T
        x,jac = self.original_jacobian(p,q)
        vv = self.shift(x,rho)
        old = np.array([np.ones_like(theta),vv+np.cos(theta),np.sin(theta)])
        vv_plot = np.linalg.solve(self.pq_from_plot_jacobian(p,q),np.linalg.solve(jac,old)).T
        if np.min(vv_plot[:,2]) <= 0:
            raise ValueError("Plot time is not future-increasing at this cone")
        return vv_plot/vv_plot[:,2,None]

    def geodesic(self):
        if self.kind != "cap":
            raise ValueError("Only the capped geodesic is continued")
        p0,q0 = .58,.12
        c0 = self.C(self.x_from_product(p0*q0))
        # E>1 selects a trajectory that can be traced back to the flat core.
        dp0 = 1/4
        dq0 = -1/(c0*dp0)
        def rhs(tau,z):
            p,q,dp,dq = z
            x = self.x_from_product(p*q)
            der = self.dlogC_dz(x)
            return [dp,dq,-q*der*dp*dp,-p*der*dq*dq]
        sol = solve_ivp(rhs,[0,.13],[p0,q0,dp0,dq0],rtol=2e-11,atol=1e-12,dense_output=True,max_step=.003)
        if not sol.success:
            raise RuntimeError(sol.message)
        tcross = brentq(lambda t: sol.sol(t)[1],0,sol.t[-1],xtol=1e-13)
        return sol,tcross


def verify_geometry():
    # Independent symbolic pullback for an arbitrary transverse shift.
    p,q,k,v0,v,c = sp.symbols("p q k v0 v C",nonzero=True,real=True)
    jac = sp.Matrix([[(v0+1)/(2*k*p),(v0-1)/(2*k*q),0],
                     [(v0*v0-1)/(2*k*p),(v0*v0-1)/(2*k*q),0],
                     [0,0,1]])
    old = sp.Matrix([[v*v-1,-v,0],[-v,1,0],[0,0,1]])
    pulled = (jac.T*old*jac).applyfunc(sp.factor)
    axial = pulled.subs(v,v0).applyfunc(sp.simplify)
    cc = (1-v0*v0)/(k*k*p*q)
    assert sp.simplify(axial[0,0]) == sp.simplify(axial[1,1]) == 0
    assert sp.simplify(axial[0,1]-cc/2) == 0
    assert sp.simplify(pulled.det()+cc**2/4) == 0
    delta = sp.symbols("delta",real=True)
    gqq = pulled[1,1].subs(v,v0+delta)
    assert sp.simplify(gqq-(v0-1)**2*(delta**2-2*delta)/(4*k*k*q*q)) == 0
    # In the normalized regular chart v0 -> -1, so this detects the
    # 1/q^2 obstruction at every fixed rho outside the aperture.
    assert sp.simplify((q*q*gqq).subs(v0,-1)-(delta**2-2*delta)/k**2) == 0

    # Independent curvature check: a general curved cap collar is not a
    # 3D Minkowski diagram with an extra Euclidean coordinate.
    tt,xx,rr=sp.symbols("t x rho",real=True)
    vv=-(1+xx**2)/2
    g3=sp.Matrix([[vv**2-1,-vv,0],[-vv,1,0],[0,0,1]])
    gi=g3.inv()
    coords=(tt,xx,rr)
    ga=[[[sp.simplify(sum(gi[i,l]*(sp.diff(g3[l,j],coords[h])+sp.diff(g3[l,h],coords[j])-sp.diff(g3[j,h],coords[l])) for l in range(3))/2) for h in range(3)] for j in range(3)] for i in range(3)]
    ric=sp.Matrix(3,3,lambda i,j:sp.simplify(sum(sp.diff(ga[l][i][j],coords[l])-sp.diff(ga[l][i][l],coords[j])+sum(ga[l][l][m]*ga[m][i][j]-ga[l][j][m]*ga[m][i][l] for m in range(3)) for l in range(3))))
    scalar=sp.simplify(sum(gi[i,j]*ric[i,j] for i in range(3) for j in range(3)))
    assert scalar == 3*xx**2+1
    assert sp.diff(-scalar/4,xx) == -3*xx/2

    report = ["2+1 quotient pullback: exact symbolic checks passed.",
        "det(g_pq_rho) = -C^2/4; product metric only where v=v0.",
        "Outside aperture: q^2 g_qq -> (delta^2-2 delta)/kappa^2 > 0."]
    for kind in ("cap","rounded"):
        collar=FrontCollar(kind)
        assert abs(collar.Fprime(collar.L)+1)<1e-12
        for sample in (collar.L-.15,collar.L-.04,collar.L+.04,collar.L+.15):
            pv,qv=collar.pq_factors(sample)
            qprime=collar.kappa*qv/(collar.v0(sample)-1)
            pprime=collar.Fprime(sample)/qv-pv*qprime/qv
            assert abs(pprime+collar.kappa*pv/(collar.v0(sample)+1))<2e-12
        max_null=0.; max_det=0.; max_time=-np.inf
        for pp in (-.5,0.,.6):
            for qq in (.035,.12,.2):
                for rho in (0.,.3,.6,.76):
                    if kind == "rounded" and rho > .6:
                        continue
                    gg=collar.metric_plot(pp,qq,rho)
                    eig=np.linalg.eigvalsh(gg)
                    assert eig[0]<0<eig[1]
                    max_time=max(max_time,np.linalg.inv(gg)[2,2])
                    assert np.linalg.inv(gg)[2,2]<0
                    dirs=collar.null_directions(pp,qq,rho,np.linspace(0,2*np.pi,40))
                    err=np.max(np.abs(np.einsum('ni,ij,nj->n',dirs,gg,dirs)))
                    max_null=max(max_null,err)
                    x=collar.x_from_product(pp*qq)
                    det=np.linalg.det(collar.metric_pq(pp,qq,rho))
                    max_det=max(max_det,abs(det+collar.C(x)**2/4))
                    assert err<2e-8
        report.append(f"{kind}: tangent null-cone residual <= {max_null:.3g}; determinant error <= {max_det:.3g}; T temporal on checked collar (max norm {max_time:.4g}).")
    cap=FrontCollar("cap")
    phi_min=cap.x_from_product(.75*.22)**2-1
    phi_max=cap.x_from_product(-.75*.22)**2-1+cap.psi(.78)
    assert -.9<phi_min<phi_max<.9
    report.append(f"Entire plotted cap collar has {phi_min:.4g} <= Phi <= {phi_max:.4g}; it fits within a smooth global W with affine segment |Phi|<0.9.")
    for pp in (-.5,0.,.6):
        for qq in (-.15,0.,.15):
            gg=cap.metric_plot(pp,qq,.3)
            om2=cap.conformal_factor(pp,qq)
            assert np.allclose(gg,np.diag([1,1/om2,-1]),atol=2e-11)
    sol,tcross=cap.geodesic()
    tau=np.linspace(0,sol.t[-1],200)
    pp,qq,dp,dq=sol.sol(tau)
    norm=np.array([cap.C(cap.x_from_product(pv*qv))*dpp*dqq for pv,qv,dpp,dqq in zip(pp,qq,dp,dq)])
    energy=np.array([cap.kappa*cap.C(cap.x_from_product(pv*qv))*(qv*dpp-pv*dqq)/2 for pv,qv,dpp,dqq in zip(pp,qq,dp,dq)])
    assert np.max(abs(norm+1))<2e-9
    assert np.ptp(energy)<2e-9
    assert energy[0]>1
    assert qq[0]>0>qq[-1]
    report.append(f"Capped unit timelike geodesic: max norm error {np.max(abs(norm+1)):.3g}, crossing proper time {tcross:.12g}, p={sol.sol(tcross)[0]:.12g}.")
    report.append(f"Geodesic E={energy[0]:.12g}>1 (accessible from flat core); energy drift <= {np.ptp(energy):.3g}.")
    for rho in (.62,.68,.76):
        delta=cap.shift(cap.L,rho)-cap.v0(cap.L)
        assert delta<0
    # A product curved 2D metric plus drho^2 is generally not conformally
    # flat: Cotton_{rho rho x}=-(d/dx)R_2/4. For this collar R_2=3x^2+1.
    report.append("Cap collar R_2=3x^2+1, Cotton_(rho,rho,x)=-3x/2: the 3D chart is not conformally Minkowski.")
    text="\n".join(report)+"\n"
    out=BASE/"output/sech"
    out.mkdir(parents=True,exist_ok=True)
    (out/"meridional_geometry_check.txt").write_text(text,encoding="utf-8")
    print(text)


if __name__ == "__main__":
    verify_geometry()
