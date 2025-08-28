class Trapezoidal_example_integrator:
    @staticmethod
    def integrate_predefined(rhs, jac, y0, xout, **kwargs):
        import numpy as np
        
        # Initialize arrays
        n_steps = len(xout) - 1
        y0 = np.array(y0)
        y = np.zeros((n_steps + 1, len(y0)))
        y[0] = y0
        
        # Get tolerance and max iterations from kwargs
        tol = kwargs.get('tol', 1e-10)
        max_iter = kwargs.get('max_iter', 50)
        
        # Time stepping loop
        for i in range(n_steps):
            h = xout[i+1] - xout[i]
            y_prev = y[i]
            
            # Initial prediction using Euler step
            y_pred = y_prev + h * rhs(xout[i], y_prev)
            y_new = y_pred.copy()
            
            # Newton iteration to solve the implicit trapezoidal rule
            for _ in range(max_iter):
                # Function value: f(y_new) = y_new - y_prev - h/2 * (rhs(x_i, y_prev) + rhs(x_{i+1}, y_new))
                f_val = y_new - y_prev - 0.5 * h * (rhs(xout[i], y_prev) + rhs(xout[i+1], y_new))
                
                # Jacobian: J = I - h/2 * jac(x_{i+1}, y_new)
                J = np.eye(len(y0)) - 0.5 * h * jac(xout[i+1], y_new)
                
                # Solve linear system: J * delta = -f_val
                delta = np.linalg.solve(J, -f_val)
                
                # Update solution
                y_new += delta
                
                # Check convergence
                if np.linalg.norm(delta) < tol:
                    break
            
            y[i+1] = y_new
        
        return y