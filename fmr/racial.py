import pandas as pd
import numpy as np


def the_groupby(ts):
    """Group by fields for a timeseries with a `date` field.

    Args:
        ts: a data frame with a `date` datetime field
    Returns:
        A result suitable for the groupby() method
    """
    groupby = []
    groupby.append(ts.date.dt.year)
    groupby.append(ts.date.dt.month)
    groupby.append(ts.date.dt.day)
    return groupby


def get_ts(data):
    """Take a dataframe and convert it to a timeseries.

    Args:
        data: a data frame
    Returns:
        A panda dateframe with a `date` datetime field
    """
    ts = data['Date received'].to_frame()
    ts.columns = ['date']
    ts = pd.to_datetime(ts['date']).to_frame()
    ts.groupby(the_groupby(ts))
    return ts


def get_minority_ts(data):
    threshold = data.percentage_black.quantile(q=0.75)
    data_minority = data[data.percentage_black > threshold]
    return get_ts(data_minority)


def anomaly(x, mean, std):
    """Return whether a measurement is an anomaly.

    Args:
        x: the measurement
        mean: the mean of the distribution from which x is measured
        std: the standard deviation of the distribution from which x is measured
    Returns:
        True if x is anomalous, otherwise False
    """
    return x > 0.45


class Racial(object):
    def __init__(self, complaints, zipcodes):
        """Initialize a malicious racial discrimination finder thingy.

        Args:
            complaints: pandas dataframe containing complaints data
            zipcodes: pandas dataframe containing zipcode demographic data
        """
        complaints["zipcode"] = complaints["ZIP code"].astype(str)
        zipcodes["zipcode"] = zipcodes.zipcode.astype(str)
        self.data = pd.merge(complaints, zipcodes, on='zipcode', how='inner')

    def _background_ratio_stats(self, product):
        data_product = self.data[self.data.Product == product]
        all_companies = data_product.Company.unique()
        ratios = {}
        for company in all_companies:
            data_company = data_product[data_product.Company == company]
            data_company_ts = get_ts(data_company).count()
            data_company_minority_ts = get_minority_ts(data_company).count()
            ratio_ts = data_company_minority_ts.divide(data_company_ts, fill_value=0.0)
            ratios[company] = ratio_ts.mean()
        mean = np.mean(ratios.values())
        std = np.std(ratios.values())
        return { "ratios": ratios, "mean": mean, "std": std }


    def bad_companies(self, product):
        """Find potentially bad companies under the given product.

        Args:
            product: (str) the product corresponding to the complaints data
        Returns:
            list of companies which could be potentially bad
        """
        stats = self._background_ratio_stats(product)
        return [company for company, ratio in stats["ratios"].items() if anomaly(ratio, stats["mean"], stats["std"])]


    def _is_bad(self, company, product):
        """Determines whether or not the company is potentially bad for the product.

        Args:
            company: (str) the company corresponding to the complaints data
            product: (str) the product corresponding to the complaints data
        Returns:
            True if the company is potentially bad, otherwise False
        """
        stats = self._background_ratio_stats(product)
        company_ratio = stats["ratios"][company]
        return anomaly(stats["ratios"][company], stats["mean"], stats["std"])


    def is_bad(self, company):
        """Determines whether or not the company is potentially bad for any product areas.

        Args:
            company: (str) the company corresponding to the complaints data
        Returns:
            dictionary mapping all products to the result of _is_bad for that product.
        """
        data_company = self.data[self.data.Company == company]
        all_products = data_company.Product.unique()
        return { product: self._is_bad(company, product) for product in all_products }
