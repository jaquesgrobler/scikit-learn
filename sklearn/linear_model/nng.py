"""
Non-Negative Garotte

Explain it here
"""

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
#         Jaques Grobler <jaques.grobler@inria.fr>
#
# License: BSD Style.


#imports
import numpy as np

#USE RELATIVE INPUTS INSTEAD.. TODO
from sklearn.linear_model.base import LinearModel
from sklearn.linear_model import LinearRegression, Lasso, lasso_path

def non_negative_garotte(X, y, alpha, tol=0.001):
    """
    TODO - non_negative_garotte docstring
    """
    # Obtain the ordinary least squares coefficients from our data
    coef_ols = LinearRegression(fit_intercept=False).fit(X, y).coef_

    X = X * coef_ols[np.newaxis, :]
    # find the shrinkage factor by minimising the sum of square residuals
    # under the restriction that it is positive (positive=True)
    shrink_coef = Lasso(alpha=alpha, fit_intercept=False,
                        positive=True, normalize=False,
                        tol=tol).fit(X, y).coef_

    # Shrunken betas
    coef = coef_ols * shrink_coef

    # Residual Sum of Squares
    rss = np.sum((y - np.dot(X, coef)) ** 2)
    return coef, shrink_coef, rss


def non_negative_garotte_path(X, y, alpha):
    """
    TODO - non_negative_garotte_path docstring
    Compute the Non-negative Garotte path

    """

    # Obtain the ordinary least squares coefficients from our data
    # TODO do it with RIDGE and alpha_ridge=0.0
    coef_ols = LinearRegression(fit_intercept=False).fit(X, y).coef_

    X = X * coef_ols[np.newaxis, :]
    # find the shrinkage factor by minimising the sum of square residuals
    # under the restriction that it is positive (positive=True)
    # lasso_path returns a list of models - below is a bit of a hack
    # to get the coefficients of a model (all are identical if you fix
    # alpha.. Is there a better way to do this?
    shrink_coef = lasso_path(X, y, positive=True, alpha=alpha)[0].coef_
    
    # Shrunken betas
    coef_path = coef_ols * shrink_coef

    # Residual Sum of Squares
    rss = np.sum((y - np.dot(X, coef)) ** 2)

    return coef_path, shrink_coef, rss

class NonNegativeGarrote(LinearModel):
    """NonNegativeGarrote - TODO description

    Ref:
    Breiman, L. (1995), "Better Subset Regression Using the Nonnegative
    Garrote," Technometrics, 37, 373-384. [349,351]

    Parameters
    ----------
    TODO

    Attributes
    ----------
    TODO

    Examples
    --------
    TODO

    See also
    --------
    TODO



    NOTES:
    alpha will be cross-validated
    """
    def __init__(self, alpha=0.35, fit_intercept=True, tol=1e-4, normalize=False,
                 copy_X=True):
        self.alpha = alpha
        self.fit_intercept = fit_intercept
        self.tol = tol
        self.normalize = normalize
        self.copy_X = copy_X

    def fit(self, X, y):
        """Fit the model using X, y as training data.

        parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            training data.

        y : array-like, shape = [n_samples]
            target values.

        returns
        -------
        self : object
            returns an instance of self.
        """
        X, y, X_mean, y_mean, X_std = LinearModel._center_data(X, y,
                self.fit_intercept, self.normalize, self.copy_X)

        self.coef_, self.shrink_coef_, self.rss_ = \
                                    non_negative_garotte(X, y, alpha)
        self._set_intercept(X_mean, y_mean, X_std)




