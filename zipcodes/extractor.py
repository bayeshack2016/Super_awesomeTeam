from __future__ import division

import collections


class FeatureExtractor(object):
  """Extracts and aggreated features.
  
  It's pretty much just a class of two functions that are named nicely. I
  could have used named tuple but I didn't.
  """
  def __init__(self, row_extractor=None, row_aggregator=None):
    self.row_extractor = row_extractor
    self.row_aggregator = row_aggregator

  def extract(self, row):
    return self.row_extractor(row)

  def aggregate(self, values):
    return self.row_aggregator(values)
