import pandas as pd 

class Vanilla(object):
    def __init__(self, complaints):
        self.complaints = complaints 
        self.products = set(complaints.Product)

    def find_outliers(self, df):
        """Return a list of (positive) outlier companies

        Args:
            df - a dataframe containing a single product category

        Returns: 
            a list of outlier companies, or an empty list otherwise
        """
        freq = df.Company.value_counts()
        threshold = freq.mean() + (3 * freq.std())
        return list(freq[freq > threshold].index)


    def bad_companies(self, product):
        """Return any companies that have many more complaints 
        than other companies in its product category. 

        Args: 
            product - the product of interest

        Returns: 
            a list of companies 3 standard deviations above the mean 
            if they exist, None otherwise 
        """
        result = None
        if product not in self.products:
            return result 
        df = self.complaints 
        df_p = df[df.Product == product]
        outliers = self.find_outliers(df_p)
        if outliers:
            result = outliers
        return result 

    def is_bad(self, company):
        """Return all product categories this company is bad for. 

        Args:
            company - the name of the company of interest

        Results:
            a dictionary with True for any products this company 
            is an outlier for and False for the other categories
            it does not appear in  
        """
        result = {}
        for product in self.products:
            outliers = set(self.bad_companies(product))
            if company in outliers:
                result[product] = True
            else:
                result[product] = False
        return result

if __name__ == '__main__':
    test = pd.read_csv('Consumer_Complaints.csv')
    v = Vanilla(test)
    print v.bad_companies('Consumer Loan')
    # ['Wells Fargo & Company', 'Santander Consumer USA Holdings Inc', 'Ally Financial Inc.', 'Capital One', 'JPMorgan Chase & Co.', 'Citibank', 'Bank of America', 'Synchrony Financial', 'Toyota Motor Credit Corporation', 'U.S. Bancorp', 'GM Financial']
    print v.is_bad('JPMorgan Chase & Co.')
    # {'Debt collection': True, 'Prepaid card': False, 'Mortgage': True, 'Credit reporting': False, 'Student loan': False, 'Money transfers': False, 'Bank account or service': True, 'Credit card': True, 'Payday loan': False, 'Consumer Loan': True, 'Other financial service': True}
