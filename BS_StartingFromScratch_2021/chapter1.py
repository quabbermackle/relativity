'''
Chapter 1
Newton's and Einstein's Gravity

1.1 A Brief Review of Newton's Gravity

    x_i = i is subscript (downstairs, contravariant)
    x^i = i is superscript (upstairs, covariant)
    x**i = raised to the ith power
    
    see Appendix A for explanation of indices

    F^N = m_G * g   (1.1)
    
        F^N = gravitational force
        m_G = gravitational mass (distinct from inertial mass m_I)
        g = gravitational field
    
    g is always irrotational (curl = 0), meaning it is "conservative"
    - such a field can be written as the gradient of a scalar function
    
    g = -D * Phi    (1.2)
    
        Phi = Newtonian potential
        D = 3d spatial gradient operator (nabla or 'del' is reserved for 4d)
    
    Index notation:
    
        g_i = -D_i * Phi = -d/dx^i * Phi = -d_i * Phi   (1.3)
        
            d_i = shorthand for the partial derivative with respect to spatial coordinate x^i
            i = [1,2,3] (the spatial directions)
            
    Newtonian equations of motion
    
        m_I * a = F^N = -m_G * D * Phi          (1.4)
        m_I * a_i = F^N_i = -m_G * D_i * Phi
        
    under the Newtonian assumption that m_G = m_I (1.5),
    
        a_i = dv_i/dt = -D_i * Phi  (1.6)
        
            v_i = spatial velocity
            note that this equation implies all objects fall at the same rate, independent of mass
            - aka "the (weak) equivalence principle"
            
    Einstein summation convention: 
    - sum over all allowed values of two repeated indices, one upstairs and one downstairs
    
        for example:
            v dot w = v^i * w_i     (dot product between vectors v and w)
            x_i * x^i = x**2
            d_j (x_i * x^i) = 2x_j
            
    Newtonian tidal deviation equation (relative acceleration)
        
        d^2 delta_x_i / dt^2 = -delta_x^j (d_j * d_i * Phi)     (1.10)
        
        Newtonian tidal tensor (rank-2):
        
            R_ij = d_i * d_j * Phi  (1.11)
            
        d^2 delta_x_i / dt^2 = -R_ij * delta_x^j    (1.12)
            
    Tensors (see Appendix A for details)
        
        rank-n tensor carries n indices
        
        rank-0 tensor = scalar, no indices
        rank-1 tensor = vector, one index
        rank-2 tensor = two indices, can be displayed as a matrix
        
    Newtonian field equation (also called Poisson equation)
    - from Newton's universal law of gravitation
    
        D^2 * Phi = 4 * pi * G * rho_0  (1.13)
        
            rho_0 = rest-mass density (distinct from total mass-energy density rho)
            D^2 = the Laplace operator
            G = the gravitational constant (set = 1)
            
        D^2 * Phi = d^2/dx^2 * Phi + d^2/dy^2 * Phi + d^2/dz^2 * Phi = R^i_i    (1.14)
        
            R = R^i_i = trace of the tidal tensor
            
        R = 4 * pi * G * rho_0  (1.15)
        
    Box 1.1 Important gravitational quantities
    -----------------------------------------------------------------------------------------------------------------
    |                       |                       | Newton                    | Einstein                          |
    -----------------------------------------------------------------------------------------------------------------
    | Fundamental quantity  |                       | potential Phi             | metric g_ab                       |
    -----------------------------------------------------------------------------------------------------------------
    | Equation of motion    | first derivative      | D_i*Phi                   | Christoffel symbols (4)Gamma^a_bc |
    -----------------------------------------------------------------------------------------------------------------
    | Geodesic deviation    | second derivatives    | D_j*D_j*Phi               | Riemann tensor (4)R^a_bcd         |
    -----------------------------------------------------------------------------------------------------------------
    | Field equation l.h.s  | trace of 2nd derivs.  | D^2*Phi                   | Einstein tensor G_ab              |
    -----------------------------------------------------------------------------------------------------------------
    | Field equation        |                       | D^2*Phi = 4*pi*G*rho_0    | G_ab = (8*pi*G/c**4) * T_ab       |
    -----------------------------------------------------------------------------------------------------------------
    
    Note that in Einstein's theory, each object or eqn is a tensor of rank 2 higher than its Newtonian counterpart
    
1.2 A First Acquaintance with Einstein's Gravity

    1.2.1 The Metric
    
        line element between two points whose coordinates differ by dx^a:
        
            ds**2 = g_ab * dx^a * dx^b  (1.18)
            
                g_ab = the metric tensor
                indexes a and b run from 0 to 3, with 0 denoting time
                note that the line element is invariant under coordinate transformations
                
        Minkowski metric (flat spacetime):
        
            g_ab = eta_ab = | -1 0 0 0 |    (1.19)
                            |  0 1 0 0 |
                            |  0 0 1 0 |
                            |  0 0 0 1 |
                            
            note that this assumes units where the speed of light is unity (c = 1)
            
        Geometrized units:
            express time and space using the same units
            let us express time in units of distance using the speed of light
            express time and space in units of length such that c = 1
            express mass in the same units of length, thus G = 1 as well
            length, time, and mass all have the same unit
            mass / length and similar are dimensionless quantities
            
            Recover physical units by reinserting appropriate powers of constants G and c (see exercise 1.12)
            
        use the metric and the cartesian displacement vector dx^a = (dt, dx, dy, dz):
        
            ds**2 = -dt**2 + dx**2 + dy**2 + dz**2  (1.20)
            
            - generalization of Pythagorean theorem for flat spacetimes
            
            Three different types of intervals possible:

                ds**2 > 0 : Space-like
                    - the separation in space dominates
                    - Proper distance dl = (ds**2)**1/2
                    - Can be measured by a meter stick
                    - Causally disconnected, information cannot be transmitted
                
                ds**2 < 0 : Time-like
                    - the separation in time dominates
                    - Proper time dtau = (-ds**2)**1/2
                    - Can be measured by a clock
                    - Causally connected, information can be sent from one to the other
                    
                ds**2 = 0 : Light-like
                    - aka null intervals
                    - light travels along trajectories whose events are separated by light-like intervals
                    - all such trajectories emitted from a point form the light cone of that point
                    - future light cone emanates from event to times t > 0
                    - past light cone with apex at event shows light rays emitted at t < 0 that arrive at the event

        In spherical polar coordinates (t,R,theta,phi), the Minkowski metric becomes:
        
            g_ab = eta_ab = | -1    0   0       0                       |    (1.21)
                            |  0    1   0       0                       |
                            |  0    0   R**2    0                       |
                            |  0    0   0       R**2 * sin(theta)**2    |
                            
            and the line element becomes
            
                ds**2   = -dt**2 + dR**2 + (R**2 * dtheta**2) + (R**2 * sin(theta)**2 * dphi**2)
                        = -dt**2 + dR**2 + (R**2 * dOmega**2)
                        
                    with solid angle dOmega**2 = dtheta**2 + (sin(theta)**2 * dphi**2)
'''

import numpy as np

# minkowski metric in cartesian coordinates
ETA_AB_CART = np.array([[-1., 0., 0., 0.],
                        [ 0., 1., 0., 0.],
                        [ 0., 0., 1., 0.],
                        [ 0., 0., 0., 1.]])

# minkowski metric in spherical polar coordinates
def eta_ab_polar(R, theta):
    R2 = R**2
    s2theta = np.sin(theta)**2
    return np.array([   [-1., 0., 0., 0.],
                        [ 0., 1., 0., 0.],
                        [ 0., 0., R2, 0.],
                        [ 0., 0., 0., R2*s2theta]])

# kronecker delta
def kronecker(i, j):
    if i == j: return 1
    else: return 0
    