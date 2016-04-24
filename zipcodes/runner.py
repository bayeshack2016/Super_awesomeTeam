import collections
import csv
import datasources
import extractor


def x_std_aggregation_key(row):
  try:
    row_geography = row["GEO.display-label"]
    splitted = row_geography.split(" ")
    zipcode = splitted[1]
    zipcode = str(int(zipcode))
    return zipcode[0] + zipcode[1] + zipcode[2] + "XX"
  except Exception:
    return "000XX"


def x_zipcode_feature_extractor():
  def extract(row):
    return { "zipcode": x_std_aggregation_key(row) }
  def aggregate(values):
    return values[0]
  return extractor.FeatureExtractor(extract, aggregate)


def std_aggregation_key(row):
  try:
    row_geography = row["GEO.display-label"]
    splitted = row_geography.split(" ")
    zipcode = splitted[1]
    zipcode = str(int(zipcode))
    return zipcode
  except Exception:
    return "000000"


def zipcode_feature_extractor():
  def extract(row):
    return { "zipcode": std_aggregation_key(row) }
  def aggregate(values):
    return values[0]
  return extractor.FeatureExtractor(extract, aggregate)


def extract_features(datasources):
  features = collections.defaultdict(dict)
  for datasource in datasources:
    for key, value in datasource.extract_and_aggregate().items():
      for k, v in value.items():
        features[key][k] = v
  return features


if __name__ == "__main__":
  OUT_NAME = "xx_all_us.csv"
  AGG_KEY = x_std_aggregation_key
  ZIP_EXT = x_zipcode_feature_extractor

  #datasources = [datasources.race_datasource(), datasources.median_income_datasource(), datasources.employment_datasource(), datasources.sex_datasource(), datasources.language_datasource()]
  datasources = [datasources.race_datasource()]
  for datasource in datasources:
    datasource.aggregation_key = AGG_KEY
    datasource.feature_extractors.append(ZIP_EXT())

  results = extract_features(datasources)
  keys = list(results[next(iter(results.keys()))].keys())
  keys.remove("zipcode")
  keys = ["zipcode"] + keys
  with open(OUT_NAME, "w") as output_file:
    writer = csv.DictWriter(output_file, fieldnames=keys)
    writer.writeheader()
    for zipcode, row in results.items():
      writer.writerow(row)
