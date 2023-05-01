from cmind import utils
import os

def preprocess(i):

    os_info = i['os_info']

    env = i['env']

    meta = i['meta']

    automation = i['automation']

    quiet = (env.get('CM_QUIET', False) == 'yes')

    return {'return':0}

def postprocess(i):

    env = i['env']
    
    env["CM_MLPERF_TINY_SOURCE"] = os.path.join(os.getcwd(), "tiny")
    env["CM_MLPERF_TINY_KWS_MODELS_PATH"] = os.path.join(os.getcwd(), "tiny", "benchmark", "training", "keyword_spotting", "trained_models")
    env["CM_MLPERF_TINY_AD_MODELS_PATH"] = os.path.join(os.getcwd(), "tiny", "benchmark", "training", "anomaly_detection", "trained_models")
    env["CM_MLPERF_TINY_IC_MODELS_PATH"] = os.path.join(os.getcwd(), "tiny", "benchmark", "training", "image_classification", "trained_models")
    env["CM_MLPERF_TINY_VWW_MODELS_PATH"] = os.path.join(os.getcwd(), "tiny", "benchmark", "training", "visual_wake_words", "trained_models")
    env["CM_MLPERF_TINY_REFERENCE_SUBMISSION"] = os.path.join(os.getcwd(), "tiny", "benchmark", "reference_submission")

    return {'return':0}
