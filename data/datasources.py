from __future__ import division

import collections
import csv
import extractor


class DataSource(object):
  """ACS datasource.

  Knows how to read a data source, extract features, and aggreate them
  accross multiple rows.
  """
  def __init__(self, path=None, aggregation_key=None, feature_extractors=None):
    self.path = path
    self.aggregation_key = aggregation_key if aggregation_key else None
    self.feature_extractors = feature_extractors if feature_extractors else []
    self.the_file = open(self.path)

  def rows(self):
    self.the_file = open(self.path)
    the_reader = csv.DictReader(self.the_file)
    next(the_reader)
    return the_reader

  def extract_and_aggregate(self):
    features = collections.defaultdict(dict)
    for feature_extractor in self.feature_extractors:
      feature = collections.defaultdict(list)
      for row in self.rows():
        try:
          key = self.aggregation_key(row)
          value = feature_extractor.extract(row)
          feature[key].append(value)
        except Exception:
          pass
      for key, values in feature.items():
        aggregates = feature_extractor.aggregate(values)
        for k, v in aggregates.items():
          features[key][k] = v
    return features


def median_income_datasource():
  path = "input_data/ACS_14_5YR_S1901_with_ann.csv"

  def extract(row):
    return { "median_income": int(row["HC02_EST_VC02"]) }

  def aggregate(values):
    num = len(values)
    total = sum(i["median_income"] for i in values)
    return { "median_income": total / num }

  median_income_feature_extractor = extractor.FeatureExtractor(extract, aggregate)
  return DataSource(
    path=path,
    feature_extractors=[median_income_feature_extractor]
  )


def race_datasource():
  path = "input_data/ACS_14_5YR_B02001_with_ann.csv"

  def extract(row):
    return {
      "total": float(row["HD01_VD01"]),
      "white": float(row["HD01_VD02"]),
      "black": float(row["HD01_VD03"]),
      "asian": float(row["HD01_VD05"]),
      "other": float(row["HD01_VD07"]),
      "two_or_more": float(row["HD01_VD08"])
    }

  def aggregate(values):
    total = 0
    white = 0
    black = 0
    asian = 0
    other = 0
    two_or_more = 0
    for value in values:
      total += value["total"]
      white += value["white"]
      black += value["black"]
      asian += value["asian"]
      other += value["other"]
      two_or_more += value["two_or_more"]
    return {
      "percentage_white": white / (total+1),
      "percentage_black": black / (total+1),
      "percentage_asian": asian / (total+1),
      "percentage_other": other / (total+1),
      "percentage_two_or_more": two_or_more / (total+1)
    }

  feature_extractor = extractor.FeatureExtractor(extract, aggregate)
  return DataSource(
    path=path,
    feature_extractors=[feature_extractor]
  )


def employment_datasource():
  path = "input_data/ACS_14_5YR_S2301_with_ann.csv"
  def extract(row):
    return {
      "unemployment_rate": float(row["HC04_EST_VC01"])
    }
  def aggregate(values):
    num = len(values)
    total = sum(i["unemployment_rate"] for i in values)
    return { "unemployment_rate": total / num }
  feature_extractor = extractor.FeatureExtractor(extract, aggregate)
  return DataSource(
    path=path,
    feature_extractors=[feature_extractor]
  )


def sex_datasource():
  path = "input_data/ACS_14_5YR_S0101_with_ann.csv"

  def extract(row):
    return {
      "total": float(row["HC01_EST_VC01"]),
      "male": float(row["HC02_EST_VC01"]),
      "female": float(row["HC03_EST_VC01"])
    }

  def aggregate(values):
    total = 0
    male = 0
    female = 0
    for value in values:
      total += value["total"]
      male += value["male"]
      female += value["female"]
    return {
      "percentage_male": male / (total+1),
      "percentage_female": female / (total+1)
    }

  feature_extractor = extractor.FeatureExtractor(extract, aggregate)
  return DataSource(
    path=path,
    feature_extractors=[feature_extractor]
  )


def language_datasource():
  path = "input_data/ACS_14_5YR_S1601_with_ann.csv"

  def extract(row):
    return {
      "total": float(row["HC01_EST_VC01"]),
      "english_well": float(row["HC02_EST_VC01"]) * float(row["HC01_EST_VC01"]),
      "english_poor": float(row["HC03_EST_VC01"]) * float(row["HC01_EST_VC01"]),
      "spanish_lang": float(row["HC01_EST_VC04"]),
      "asian_lang": float(row["HC01_EST_VC06"]) * float(row["HC01_EST_VC01"]),
    }

  def aggregate(values):
    total = 0
    english_well = 0
    english_poor = 0
    spanish_lang = 0
    asian_lang = 0
    for value in values:
      total += value["total"]
      english_well += value["english_well"]
      english_poor += value["english_poor"]
      spanish_lang += value["spanish_lang"]
      asian_lang += value["asian_lang"]
    return {
      "english_well_per": english_well / total,
      "english_poor_per": english_poor / total,
      "spanish_lang": spanish_lang,
      "asian_lang": asian_lang
    }
  
  feature_extractor = extractor.FeatureExtractor(extract, aggregate)
  return DataSource(
    path=path,
    feature_extractors=[feature_extractor]
  )
