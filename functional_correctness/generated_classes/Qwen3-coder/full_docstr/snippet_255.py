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
        
        # Calculate correlation matrix
        corr_matrix = data.corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, linewidths=0.5, ax=ax)
        ax.set_title('Pearson Correlation Heatmap')
        
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
        
        # Convert y_pred to series if it's numpy array
        if isinstance(y_pred, np.ndarray):
            y_pred = pd.Series(y_pred, index=y_true.index)
        
        # Plot actual values
        ax.plot(y_true.index, y_true.values, label='Actual', marker='o', linewidth=2)
        
        # Plot predicted values
        ax.plot(y_pred.index, y_pred.values, label='Predicted', marker='s', linewidth=2)
        
        # Add labels and title
        ax.set_xlabel('Time')
        ax.set_ylabel(output_col)
        ax.set_title(f'{site} - {model_name} Model (Adj R² = {adj_r2:.3f})')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add vertical line to separate baseline and projection periods if both exist
        if baseline_period and projection_period:
            # Find the end of baseline period
            baseline_end = baseline_period[-1] if isinstance(baseline_period, list) else baseline_period
            if baseline_end in y_true.index:
                ax.axvline(x=baseline_end, color='red', linestyle='--', alpha=0.7, 
                          label='Baseline/Projection Boundary')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig