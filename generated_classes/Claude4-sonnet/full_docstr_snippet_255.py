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
        self.count += 1
        fig, ax = plt.subplots(figsize=self.figsize)
        correlation_matrix = data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax)
        plt.title('Correlation Heatmap')
        plt.tight_layout()
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
            Baseline period.
        projection_period   : list(str)
            Projection periods.
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

        Returns
        -------
        matplotlib.figure
            Baseline plot

        '''
        self.count += 1
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot actual values
        ax.plot(y_true.index, y_true.values, label='Actual', color='blue', linewidth=2)
        
        # Plot predicted values
        ax.plot(y_true.index, y_pred, label='Predicted', color='red', linestyle='--', linewidth=2)
        
        # Add vertical lines for baseline and projection periods
        if baseline_period:
            ax.axvline(pd.to_datetime(baseline_period[0]), color='green', linestyle=':', alpha=0.7, label='Baseline Start')
            ax.axvline(pd.to_datetime(baseline_period[1]), color='green', linestyle=':', alpha=0.7, label='Baseline End')
        
        if projection_period:
            ax.axvline(pd.to_datetime(projection_period[0]), color='orange', linestyle=':', alpha=0.7, label='Projection Start')
            ax.axvline(pd.to_datetime(projection_period[1]), color='orange', linestyle=':', alpha=0.7, label='Projection End')
        
        ax.set_xlabel('Date')
        ax.set_ylabel(output_col)
        ax.set_title(f'{model_name} - {site} (Adj R²: {adj_r2:.3f})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return fig