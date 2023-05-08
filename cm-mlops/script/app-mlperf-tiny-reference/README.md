<details>
<summary>Click here to see the table of contents.</summary>

* [Description](#description)
* [Information](#information)
* [Usage](#usage)
  * [ CM installation](#cm-installation)
  * [ CM script automation help](#cm-script-automation-help)
  * [ CM CLI](#cm-cli)
  * [ CM Python API](#cm-python-api)
  * [ CM GUI](#cm-gui)
  * [ CM modular Docker container](#cm-modular-docker-container)
* [Customization](#customization)
  * [ Variations](#variations)
  * [ Default environment](#default-environment)
* [Script workflow, dependencies and native scripts](#script-workflow-dependencies-and-native-scripts)
* [Script output](#script-output)
* [New environment keys (filter)](#new-environment-keys-(filter))
* [New environment keys auto-detected from customize](#new-environment-keys-auto-detected-from-customize)
* [Maintainers](#maintainers)

</details>

*Note that this README is automatically generated - don't edit! See [more info](README-extra.md).*

### Description


See [more info](README-extra.md).

#### Information

* Category: *Modular MLPerf benchmarks.*
* CM GitHub repository: *[mlcommons@ck](https://github.com/mlcommons/ck/tree/master/cm-mlops)*
* GitHub directory for this script: *[GitHub](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny)*
* CM meta description for this script: *[_cm.json](_cm.json)*
* CM "database" tags to find this script: *app,mlperf,mlcommons,tiny,reference*
* Output cached?: *False*
___
### Usage

#### CM installation

[Guide](https://github.com/mlcommons/ck/blob/master/docs/installation.md)

##### CM pull repository

```cm pull repo mlcommons@ck```

##### CM script automation help

```cm run script --help```

#### CM CLI

1. `cm run script --tags=app,mlperf,mlcommons,tiny,reference[,variations] `

2. `cm run script "app mlperf mlcommons tiny reference[,variations]" `

3. `cm run script ee58aa6fa9f44e44 `

* `variations` can be seen [here](#variations)

* `input_flags` can be seen [here](#script-flags-mapped-to-environment)

#### CM Python API

<details>
<summary>Click here to expand this section.</summary>

```python

import cmind

r = cmind.access({'action':'run'
                  'automation':'script',
                  'tags':'app,mlperf,mlcommons,tiny,reference'
                  'out':'con',
                  ...
                  (other input keys for this script)
                  ...
                 })

if r['return']>0:
    print (r['error'])

```

</details>


#### CM GUI

```cm run script --tags=gui --script="app,mlperf,mlcommons,tiny,reference"```

Use this [online GUI](https://cKnowledge.org/cm-gui/?tags=app,mlperf,mlcommons,tiny,reference) to generate CM CMD.

#### CM modular Docker container

*TBD*

___
### Customization


#### Variations

  * Group "**system**"
    <details>
    <summary>Click here to expand this section.</summary>

    * **`_mbed`** (default)
      - Environment variables:
        - *CM_MLPERF_TINY_RTOS_NAME*: `mbed`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get,mbed
             - CM script: [get-mbed](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-mbed)
    * `_zephyr`
      - Environment variables:
        - *CM_MLPERF_TINY_RTOS_NAME*: `zephyr`
      - Workflow:
        1. ***Read "deps" on other CM scripts***
           * get,zephyr
             - CM script: [get-zephyr](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-zephyr)
           * get,zephyr-sdk
             - CM script: [get-zephyr-sdk](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-zephyr-sdk)

    </details>


  * Group "**use_case**"
    <details>
    <summary>Click here to expand this section.</summary>

    * `_anomaly_detection`
      - Environment variables:
        - *CM_MLPERF_TINY_USE_CASE*: `anomaly_detection`
        - *CM_MLPERF_TINY_DATASET*: `ToyADMOS`
        - *CM_MLPERF_TINY_MODEL_NAME*: `Deep AutoEncoder`
      - Workflow:
    * `_image_classification`
      - Environment variables:
        - *CM_MLPERF_TINY_USE_CASE*: `image_classification`
        - *CM_MLPERF_TINY_DATASET*: `Cifar10`
        - *CM_MLPERF_TINY_MODEL_NAME*: `ResNet`
      - Workflow:
    * `_keyword_spotting`
      - Environment variables:
        - *CM_MLPERF_TINY_USE_CASE*: `keyword_spotting`
        - *CM_MLPERF_TINY_DATASET*: `Speech Commands`
        - *CM_MLPERF_TINY_MODEL_NAME*: `DS-CNN`
      - Workflow:
    * `_visual_wake_words`
      - Environment variables:
        - *CM_MLPERF_TINY_USE_CASE*: `visual_wake_words`
        - *CM_MLPERF_TINY_DATASET*: `Visual Wake Words Dataset`
        - *CM_MLPERF_TINY_MODEL_NAME*: `MobileNet`
      - Workflow:

    </details>


#### Default variations

`_mbed`
#### Default environment

<details>
<summary>Click here to expand this section.</summary>

These keys can be updated via `--env.KEY=VALUE` or `env` dictionary in `@input.json` or using script flags.


</details>

___
### Script workflow, dependencies and native scripts

<details>
<summary>Click here to expand this section.</summary>

  1. ***Read "deps" on other CM scripts from [meta](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/_cm.json)***
     * detect,os
       - CM script: [detect-os](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/detect-os)
     * get,sys-utils-cm
       - CM script: [get-sys-utils-cm](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-sys-utils-cm)
     * get,python
       * CM names: `--adr.['python', 'python3']...`
       - CM script: [get-python3](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-python3)
     * get,mlcommons,tiny,src
       * CM names: `--adr.['tiny-src']...`
       - CM script: [get-mlperf-tiny-src](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/get-mlperf-tiny-src)
  1. ***Run "preprocess" function from [customize.py](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/customize.py)***
  1. Read "prehook_deps" on other CM scripts from [meta](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/_cm.json)
  1. ***Run native script if exists***
     * [run.sh](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/run.sh)
  1. ***Read "posthook_deps" on other CM scripts from [meta](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/_cm.json)***
     * tiny,flush
       * `if (CM_MLPERF_SKIP_RUN not in on)`
       - *Warning: no scripts found*
  1. ***Run "postrocess" function from [customize.py](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/customize.py)***
  1. Read "post_deps" on other CM scripts from [meta](https://github.com/mlcommons/ck/tree/master/cm-mlops/script/app-mlperf-tiny/_cm.json)
</details>

___
### Script output
#### New environment keys (filter)

* `CM_MLPERF_*`
#### New environment keys auto-detected from customize

___
### Maintainers

* [Open MLCommons taskforce on automation and reproducibility](https://github.com/mlcommons/ck/blob/master/docs/taskforce.md)