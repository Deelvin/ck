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
    
    env["CM_GCC_ARM_PATH"] = os.path.join(os.getcwd(), "gcc-arm-none-eabi")
    
    if "+PATH" not in env:
        env["+PATH"] = []
    
    env["CM_GCC_ARM_BIN_PATH"] = os.path.join(env["CM_GCC_ARM_PATH"], "bin")
    env["+PATH"].append(env["CM_GCC_ARM_BIN_PATH"])

    return {'return':0}
