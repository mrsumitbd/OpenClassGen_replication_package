class Trapezoidal_example_integrator:

    @staticmethod
    def integrate_predefined(rhs, jac, y0, xout, **kwargs):
        tol = kwargs.get('tol', 1e-6)
        maxiter = kwargs.get('maxiter', 10)
        y0 = np.array(y0, dtype=float)
        xout = np.array(xout, dtype=float)
        n_steps = len(xout)
        n_eq = y0.size
        Y = np.zeros((n_steps, n_eq))
        Y[0] = y0

        for i in range(n_steps - 1):
            x_n = xout[i]
            x_np1 = xout[i+1]
            h = x_np1 - x_n
            y_n = Y[i].copy()
            y_np1 = y_n.copy()

            f_n = rhs(x_n, y_n)

            for _ in range(maxiter):
                f_np1 = rhs(x_np1, y_np1)
                g = y_np1 - y_n - 0.5 * h * (f_n + f_np1)
                if np.linalg.norm(g, np.inf) < tol:
                    break
                J_np1 = jac(x_np1, y_np1)
                I = np.eye(n_eq)
                Jg = I - 0.5 * h * J_np1
                delta = np.linalg.solve(Jg, g)
                y_np1 -= delta

            Y[i+1] = y_np1

        return Y