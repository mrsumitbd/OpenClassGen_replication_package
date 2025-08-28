class Plot_Data:
    ''' This class contains functions for displaying various plots.
   
    Attributes
    ----------
    count    : int
        Keeps track of the number of figures.
    '''

    def __init__(self, figsize=(18,5)):
        ''' Constructor.

        Parameters
        ----------
        figsize : tuple
            Size of figure.
        '''
        self.figsize = figsize
        self.count = 0

    def correlation_plot(self, data):
        ''' Create heatmap of Pearson's correlation coefficient.

        Parameters
        ----------
        data    : pd.DataFrame()
            Data to display.

        Returns
        -------
        matplotlib.figure
            Heatmap.
        '''
        corr = data.corr()
        fig, ax = plt.subplots(figsize=self.figsize)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
                    cbar_kws={"shrink": .8})
        ax.set_title("Correlation Heatmap")
        self.count += 1
        return fig

    def baseline_projection_plot(self, y_true, y_pred, 
                                baseline_period, projection_period,
                                model_name, adj_r2,
                                data, input_col, output_col, model,
                                site):
        ''' Create baseline and projection plots.

        Parameters
        ----------
        y_true              : pd.Series()
            Actual y values.
        y_pred              : np.ndarray
            Predicted y values.
        baseline_period     : list(str)
            Baseline period [start, end].
        projection_period   : list(str)
            Projection period [start, end].
        model_name          : str
            Optimal model's name.
        adj_r2              : float
            Adjusted R2 score of optimal model.
        data                : pd.Dataframe()
            Data containing real values.
        input_col           : list(str)
            Predictor column(s).
        output_col          : str
            Target column.
        model               : func
            Optimal model.
        site                : str
            Site identifier.

        Returns
        -------
        matplotlib.figure
            Baseline plot
        '''
        # align predictions to true index
        y_pred_series = pd.Series(y_pred, index=y_true.index)
        # slice baseline and projection
        start_b, end_b = baseline_period
        start_p, end_p = projection_period
        y_true_b = y_true.loc[start_b:end_b]
        y_pred_b = y_pred_series.loc[start_b:end_b]
        y_true_p = y_true.loc[start_p:end_p]
        y_pred_p = y_pred_series.loc[start_p:end_p]

        fig, ax = plt.subplots(figsize=self.figsize)
        # plot baseline
        ax.plot(y_true_b.index, y_true_b.values, label='Actual (Baseline)', color='blue')
        ax.plot(y_pred_b.index, y_pred_b.values, label='Predicted (Baseline)', color='orange')
        # plot projection
        ax.plot(y_pred_p.index, y_pred_p.values, label='Predicted (Projection)', color='red', linestyle='--')
        # if actual for projection exists
        if not y_true_p.empty:
            ax.plot(y_true_p.index, y_true_p.values, label='Actual (Projection)', color='green', linestyle='--')
        # boundary line
        boundary = pd.to_datetime(end_b)
        ax.axvline(boundary, color='gray', linestyle='--', label='Projection Start')
        # labels and title
        ax.set_xlabel("Date")
        ax.set_ylabel(output_col)
        title = f"{model_name} | Adjusted R² = {adj_r2:.3f}"
        ax.set_title(title)
        # footer text
        txt = (
            f"Site: {site}\n"
            f"Model: {model}\n"
            f"Inputs: {', '.join(input_col)}"
        )
        fig.text(0.02, 0.02, txt, fontsize=9, va='bottom')
        ax.legend(loc='upper left')
        self.count += 1
        return fig