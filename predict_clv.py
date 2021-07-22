from lifetimes import BetaGeoFitter

# inputs=['t','frequency','recency','T']
def predict(features):
  data=features["feature"].split(",")
  print(type(data))
  bgf_loaded = BetaGeoFitter(penalizer_coef=0.0)
  bgf_loaded.load_model('bgf.pkl')
  return bgf_loaded.predict(int(data[0]), int(data[1]), int(data[2]), int(data[3]))