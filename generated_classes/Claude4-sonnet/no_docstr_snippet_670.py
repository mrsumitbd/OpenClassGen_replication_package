class Trapezoidal_example_integrator:

    @staticmethod
    def integrate_predefined(rhs, jac, y0, xout, **kwargs):
        rtol = kwargs.get('rtol', 1e-6)
        atol = kwargs.get('atol', 1e-9)
        max_iter = kwargs.get('max_iter', 100)
        
        y0 = np.asarray(y0, dtype=float)
        xout = np.asarray(xout, dtype=float)
        
        n_points = len(xout)
        n_vars = len(y0)
        
        y_result = np.zeros((n_points, n_vars))
        y_result[0] = y0
        
        y_current = y0.copy()
        
        for i in range(1, n_points):
            x_prev = xout[i-1]
            x_curr = xout[i]
            h = x_curr - x_prev
            
            y_prev = y_current.copy()
            
            def residual(y_new):
                f_prev = rhs(x_prev, y_prev)
                f_new = rhs(x_curr, y_new)
                return y_new - y_prev - 0.5 * h * (f_prev + f_new)
            
            def jacobian_residual(y_new):
                J = jac(x_curr, y_new)
                return np.eye(n_vars) - 0.5 * h * J
            
            y_guess = y_prev + h * rhs(x_prev, y_prev)
            
            try:
                y_new = fsolve(residual, y_guess, fprime=jacobian_residual, 
                              xtol=rtol, maxfev=max_iter)[0] if n_vars == 1 else fsolve(residual, y_guess, fprime=jacobian_residual, xtol=rtol, maxfev=max_iter)
                y_current = y_new
                y_result[i] = y_current
            except:
                y_current = y_guess
                y_result[i] = y_current
        
        return xout, y_result