import numpy as np
from typing import Annotated, Literal, TypeVar

# Type Annotations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

DType = TypeVar("DType", bound=np.generic)

Vec3    = Annotated[np.typing.NDArray[DType], Literal[3]]
Mat33   = Annotated[np.typing.NDArray[DType], Literal[3, 3]]
Vec4    = Annotated[np.typing.NDArray[DType], Literal[4]]
Mat44   = Annotated[np.typing.NDArray[DType], Literal[4, 4]]
Mat444  = Annotated[np.typing.NDArray[DType], Literal[4, 4, 4]]
Mat4444 = Annotated[np.typing.NDArray[DType], Literal[4, 4, 4, 4]]


# SI Units ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

KG_PER_GRAM = 1.0e-3
GRAM_PER_KG = 1 / KG_PER_GRAM
M_PER_CM = 1.0e-2
CM_PER_M = 1 / M_PER_CM

# Geometrized Units ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 1.0 = c = G = k

CM_PER_GRAM = 0.7425e-28 # G/c^2 = 1.0
GRAM_PER_CM = 1 / CM_PER_GRAM
M_PER_KG = CM_PER_GRAM * M_PER_CM * GRAM_PER_KG
KG_PER_M = 1 / M_PER_KG
CM_PER_ERG = 0.826e-49   # G/c^4 = 1.0
ERG_PER_CM = 1 / CM_PER_ERG
CM_PER_KELVIN = 1.14e-65 # G*k/c^4 = 1.0
KELVIN_PER_CM = 1 / CM_PER_KELVIN
CM_PER_INV_GAUSS = 3.48e24 # c^2/G^1/2
INV_GAUSS_PER_CM = 1 / CM_PER_INV_GAUSS

# Constants ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# planck? constant, g*cm^2/sec -> kg*m^2/s
h_bar = (1.054e-27) * KG_PER_GRAM * (M_PER_CM**2)

# newton's gravitational constant, cm^3/g*sec^2 -> m^3/(kg*s^2)
G = (6.670e-8) * (M_PER_CM**3) / KG_PER_GRAM

# speed of light, international cm/sec -> m/s
c = (2.99793e10) * M_PER_CM
c_2 = c**2
c_3 = c**3
c_4 = c**4

# Planck length, m
L_star = np.sqrt(h_bar * G / c_3)

# mass of Earth, conventional grams -> kg
M_E_conv = 5.98e27 * KG_PER_GRAM

# density of Earth, conventional g / cm^3 -> kg / m^3
rho_E_conv = 5.52 * KG_PER_GRAM * 1/(M_PER_CM**3)

# mass of Sun, conventional grams -> kg
M_Sun = 1.989e33 * KG_PER_GRAM

# Special Relativity ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def relativistic_gamma(v: Vec3):
    # gamma correction factor of special relativity
    v2 = v[0]**2 + v[1]**2 + v[2]**2
    gamma = 1 / np.sqrt(1 - v2)
    return gamma

def four_velocity(vj: Vec3) -> Vec4:
    # 3-velocity = vj = dxj/dt = components of "ordinary velocity" ie v/c, or rapidity
    if any(np.abs(vj) >= 1): raise Exception("Error! velocity must be geometrized, ie 0<v<1")
    u = Vec4((4,1))
    gamma = relativistic_gamma(vj)
    u[0] = gamma # dt/dtau
    for j in range(1,4):
        u[j] = vj[j-1] * gamma # dxj/dtau
        
    return u
    
def four_momentum(u: Vec4, m: float) -> Vec4:
    # u = 4-velocity
    # m = mass
    p = m * u
    return p

def relativistic_momentum(v: Vec3, m: float):
    # p^2 = m^2*v^2 / (1 - v^2)
    v2 = v[0]**2 + v[1]**2 + v[2]**2
    gamma = 1 / np.sqrt(1 - v2)
    p2 = m**2 * v2 / gamma
    return np.sqrt(p2)

def p_to_E(v: Vec3, m: float):
    # E2 = E^2, squared energy
    E2 = (relativistic_momentum(v, m) * c)**2 + (m * c_2)**2
    return np.sqrt(E2)

def mv_to_E(v, m):
    E2 = relativistic_gamma(v) * m**2
    return np.sqrt(E2)

# Metrics ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ETA_LORENTZ = np.eye(4)
ETA_LORENTZ[0,0] *= -1

class Metric():
    def __init__(self, eta: Mat44 = ETA_LORENTZ):
        # eta = eta_alpha_beta, 4x4 matrix defining metric
        # default to basic Lorentz coordinate metric
        self.eta = eta
        
    def scalar_product(self, u, v):
        prod = 0.0
        for alpha in range(4):
            for beta in range(4):
                prod += self.eta[alpha, beta] * u[alpha] * v[beta]
        return prod
    
    def scalar_prod_matmul(self, u: Vec4, v: Vec4):
        return u.reshape(1,4) @ self.eta @ u.reshape(4,1)
    
class Lorentz_Metric(Metric):
    def scalar_product(self, u: Vec4, v: Vec4):
        return -u[0]*v[0] + u[1]*v[1] + u[2]*v[2] + u[3]*v[3]
        
# Tensor Math Stuff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def fourvec_to_oneform(vec:np.ndarray, metric:Metric) -> np.ndarray:
    form = np.zeros((1,4))
    if isinstance(metric, Lorentz_Metric):
        form[0] = -vec[0]
        form[1] = vec[1]
        form[2] = vec[2]
        form[3] = vec[3]
    else:
        for alpha in range(4):
            for beta in range(4):
                form[alpha] += metric.eta[alpha, beta] * vec[beta]
    
    return form

def oneform_to_fourvec(form:np.ndarray, metric:Metric) -> np.ndarray:
    # valid since eta^alpha^beta = eta_alpha_beta for all alpha, beta
    # ie eta^alpha^beta, the inverse of eta_alpha_beta, is equal to eta_alpha_beta
    # therefore, in component form, lowering an index to convert a vector to a 1-form
    # is exactly the same operation as raising an index to convert a 1-form to a vector
    return fourvec_to_oneform(form, metric) 

class FourVector():
    def __init__(self,
                 v:np.ndarray = np.zeros((1,4)), 
                 g:Metric = Lorentz_Metric(), 
                 iname:str = 'alpha'):
        self.data = v
        self.g = g
        self.index_list = {'contravariant'  : [iname],
                           'covariant'      : []}
        
    @classmethod
    def from_OneForm(cls, oneform):
        # create a FourVector object from a OneForm object
        # this is done by raising the index, ie multiplying by the metric
        g = oneform.g
        v = oneform_to_fourvec(oneform.data, g)
        return cls(v, g)
        
    def __array__(self, dtype=None, copy=None):
        return self.data # allows numpy ufuncs to access
    
    def __repr__(self):
        # nice format for printing
        return (f"{self.__class__.__name__} with components\n"
                f"[{self.data[0]}, {self.data[1]}, {self.data[2]}, {self.data[3]}]")
        
    def dot(self, other):
        # dot product (aka scalar product) of this vector with another,
        # carried out using the metric tensor
        return self.g.scalar_product(self.data, other.data)
    
    def lower_index(self, iname:str):
        # lower a contravariant index by multiplying by the metric
        if iname in self.index_list['contravariant']:
            v_tilde = fourvec_to_oneform(self.data, self.g)
            # idx = np.nonzero(self.index_list['contravariant'] == iname)
            # self.index_list['contravariant'].pop(idx)
            # self.index_list['covariant'].insert(idx, iname)
            return OneForm(v_tilde, self.g, iname)
        else:
            raise Exception('No matching index name found!')
        
class OneForm():
    def __init__(self, 
                 v_tilde:np.ndarray = np.zeros((1,4)), 
                 g:Metric = Lorentz_Metric(), 
                 iname:str = 'alpha'):
        self.data = v_tilde
        self.g = g
        self.index_list = {'contravariant'  : [],
                           'covariant'      : [iname]}
        
    @classmethod
    def from_FourVector(cls, fourvector):
        g = fourvector.g
        oneform = fourvec_to_oneform(fourvector, g)
        return cls(oneform, g)
        
    def __array__(self, dtype=None, copy=None):
        return self.data
    
    def __repr__(self):
        return (f"{self.__class__.__name__} with components\n"
                f"[{self.data[0]}, {self.data[1]}, {self.data[2]}, {self.data[3]}]")
        
    def raise_index(self, iname:str):
        # raise a covariant index by multiplying by the metric
        if iname in self.index_list['covariant']:
            v = oneform_to_fourvec(self.data, self.g)
            return FourVector(v, self.g, iname)
        else:
            raise Exception('No matching index name found!')
        
    def contraction(self, other:FourVector):
        # contraction of self with other, 
        # <sigma, v> = sigma_alpha * v^alpha
        return np.dot(self.data, other.data)

def scalar_product(u, v, g:Metric = Lorentz_Metric()):
    match (u, v):
        
        case (np.ndarray, np.ndarray):
            # default assumption is that the inputs are four-vectors
            return g.scalar_product(u, v)
        
        case (FourVector(), FourVector()):
            # g(u^alpha, v^beta) = u^alpha * v^beta * eta_alpha_beta
            return g.scalar_product(u.data, v.data)
        
        case (OneForm(), OneForm()):
            # g(u_alpha, v_beta) = u_alpha * v_beta * eta^alpha^beta
            # simplification due to eta^alpha^beta = eta_alpha_beta
            return g.scalar_product(u.data, v.data)
        
        case (FourVector(), OneForm()):
            # g(u^alpha, v_alpha) = u^alpha * v_beta, no extra metric required
            return np.dot(u, v)

def contraction(sigma, v, g:Metric = Lorentz_Metric()):
    match (sigma, v):

        case (np.ndarray, np.ndarray):
            # default assumption is that sigma is a 1-form and v is a 4-vector
            return np.dot(sigma, v)
        
        case (OneForm(), FourVector()):
            return sigma.contraction(v)

# Riemann ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class Riemann():
    def __init__(self, R: Mat4444):
        self.R = R
        
    def Riemann(self, u: Vec4, v: Vec4, w: Vec4):
        r = Vec4([0.0, 0.0, 0.0, 0.0])
        for alpha in range(4):
            for beta in range(4):
                for gamma in range(4):
                    for delta in range(4):
                        r[alpha] += self.R[alpha, beta, gamma, delta] * u[beta] * v[gamma] * w[delta]

def Riemann_Newton(m, r):
    m_r3 = m / r**3
    return np.array([[m_r3, 0,     0     ],
                     [0,    m_r3,  0     ],
                     [0,    0,    -2*m_r3]])

# Equation of Geodesic Separation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Geo_sep():
    def __init__(self, R: Mat4444, u0: Vec4, xi0: Vec4):
        self.R = Riemann(R) # Riemann curvature tensor
        state = np.array([u0[0], u0[1], u0[2], u0[3], xi0[0], xi0[1], xi0[2], xi0[3]])
        self.r = self.update_r(state)
        
    def update_r(self, state):
        u = state[0:3] # 4-velocity of fiducial geodesic
        xi = state[4:7] # perpendicular separation of neighboring geodesic from the fiducial
        return self.R.Riemann(u, xi, u)
        
    def eval(self, state):
        self.r = self.update_r(state)
        
        d2xi_dtau2 = self.r
        return d2xi_dtau2
    
# Newtonian acceleration of separation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Newton_sep():
    def __init__(self, m):
        self.Gm_c2 = G * m / c_2
        
    def eval(self, state, r: float):
        xi = state[0:2]
        dxi = state[3:5]
        Gm_c2r3 = self.Gm_c2 / r**3
        
        ddxi_x = -Gm_c2r3 * xi[0]
        ddxi_y = -Gm_c2r3 * xi[1]
        ddxi_z = 2 * Gm_c2r3 * xi[2]
        
        dstate = np.array([dxi[0], dxi[1], dxi[2], ddxi_x, ddxi_y, ddxi_z])
        return dstate

# Lorentz Force Equation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Lorentz_force():
    def __init__(self, F, e, m):
        self.F = F # Electromagnetic Field tensor
        self.m = m # particle mass
        self.e = e # particle charge
        self.e_m = self.e / self.m
        
    def update_F(self, state):
        # in reality, this would be an electromagnetic field evaluation
        return self.F
        
    def eval(self, state):
        self.F = self.update_F(state)
        
        x = state[0:3]
        dx_dtau = state[4:7]
        
        d2x_dtau2 = np.zeros((4,1))
        for alpha in range(4):
            for beta in range(4):
                d2x_dtau2[alpha] -= self.e_m * self.F[alpha][beta] * dx_dtau[alpha]
                
        dstate = np.array([ dx_dtau[0],   dx_dtau[1],   dx_dtau[2],   dx_dtau[3],
                           d2x_dtau2[0], d2x_dtau2[1], d2x_dtau2[2], d2x_dtau2[3]])
        return dstate

# Tests ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# if __name__ == '__main__':
    