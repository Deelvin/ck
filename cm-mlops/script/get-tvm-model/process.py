import os
import tempfile
import tvm
from tvm import relay
from tvm.driver.tvmc.model import TVMCModel
from tvm.driver.tvmc.frontends import load_model

max_batchsize = os.environ['CM_ML_MODEL_MAX_BATCH_SIZE']
input_shapes = os.environ.get('CM_ML_MODEL_INPUT_SHAPES', '').strip()

if input_shapes == '':
    print('')
    width = os.environ.get('CM_ML_MODEL_IMAGE_WIDTH', '')
    height = os.environ.get('CM_ML_MODEL_IMAGE_HEIGHT', '')
    
    if width == '' or height == '':
        raise RuntimeError(
            "Error: CM_ML_MODEL_INPUT_SHAPES environment variable is not defined!")
        
    if os.environ.get("CM_TVM_FRONTEND_FRAMEWORK") == "onnx":
        import onnx
        onnx_model = onnx.load(os.environ.get('CM_ML_MODEL_FILE_WITH_PATH'))
        input_all = [node.name for node in onnx_model.graph.input]
        input_initializer =  [node.name for node in onnx_model.graph.initializer]
        net_feed_input = list(set(input_all)  - set(input_initializer))
        input_shapes = f"\"{net_feed_input[0]}\": (BATCH_SIZE, 3, {height}, {width})"

input_shapes = input_shapes.replace('BATCH_SIZE', str(max_batchsize))
model_path = os.environ.get('CM_ML_MODEL_FILE_WITH_PATH')

print('TVM model: ' + model_path)

# Check if load precompiled model
compiled_model = os.path.join(os.getcwd(), 'model-tvm.so')
if model_path.endswith('.so') or model_path.endswith('.dylib'):
    compiled_model = model_path

    if not os.path.isfile(compiled_model):
        print('')
        raise RuntimeError(
            f"Error: Model file {compiled_model} not found!")
else:

    build_conf = {}
    params = {}
    
    shape_dict = eval('{' + input_shapes + '}')
    tvmc_model = load_model(path=model_path, shape_dict=shape_dict)
    mod, params = tvmc_model.mod, tvmc_model.params

    opt_lvl = int(os.environ.get('CM_MLPERF_TVM_OPT_LEVEL', 3))

    target = os.environ.get('CM_MLPERF_TVM_TARGET',
                            f"llvm -num-cores {os.environ.get('CM_HOST_CPU_TOTAL_CORES', '1')}")

    target_host = None

    tvm_target = tvm.target.Target(target, host=target_host)

    tune_model = os.environ.get('CM_TUNE_TVM_MODEL', 'no') == 'yes'

    work_dir = ''

    use_vm = os.environ.get('CM_TVM_USE_VM', 'no') == 'yes'

    if tune_model:
        from tvm import meta_schedule as ms

        work_dir = os.path.join(os.getcwd(), "metaschedule_workdir")
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)

        print("Extracting tasks...")
        extracted_tasks = ms.relay_integration.extract_tasks(
            mod, tvm_target, params
        )
        tasks, task_weights = ms.relay_integration.extracted_tasks_to_tune_contexts(
            extracted_tasks, work_dir, strategy="evolutionary"
        )

        print("Begin tuning...")
        evaluator_config = ms.runner.config.EvaluatorConfig(
            number=1,
            repeat=10,
            enable_cpu_cache_flush=True
        )
        database = ms.tune.tune_tasks(
            tasks=tasks,
            task_weights=task_weights,
            work_dir=work_dir,
            max_trials_global=20000,
            num_trials_per_iter=64,
            max_trials_per_task=512,
            builder=ms.builder.LocalBuilder(),
            runner=ms.runner.LocalRunner(
                evaluator_config=evaluator_config
            ),
        )

    if work_dir == '':
        work_dir = os.environ.get('CM_TUNE_TVM_MODEL_WORKDIR', '')

    if work_dir != '':
        database = ms.database.JSONDatabase(f"{work_dir}/database_workload.json",
                                            f"{work_dir}/database_tuning_record.json",
                                            allow_missing=False)

        build_conf["relay.backend.use_meta_schedule"] = True

        with tvm.transform.PassContext(opt_level=opt_lvl, config=build_conf):
            if use_vm:
                vm_exec = ms.relay_integration.compile_relay(
                    database=database,
                    mod=mod,
                    target=tvm_target,
                    params=params,
                    backend="vm"
                )
            else:
                lib = ms.relay_integration.compile_relay(
                    database, mod, tvm_target, params)

    else:
        with tvm.transform.PassContext(opt_level=opt_lvl, config=build_conf):
            if use_vm:
                vm_exec = tvm.relay.backend.vm.compile(
                    mod, target, params=params)
            else:
                lib = relay.build(mod, target=tvm_target, params=params)

    if use_vm:
        path_consts = os.path.join(tempfile.mkdtemp(
            dir=os.getcwd(), suffix="-tvm-tmp"), "consts")
        code_path = os.path.join(os.getcwd(), "vm_exec_code.ro")

        vm_exec.move_late_bound_consts(path_consts, byte_limit=256)

        code, lib = vm_exec.save()

        with open(code_path, "wb") as file:
            file.write(code)

    with open(os.path.join(os.getcwd(), "tvm_executor"), "w") as file:
        file.write("virtual_machine" if use_vm else "graph_executor")

    lib.export_library(compiled_model)
    print('TVM compiled model: ' + compiled_model)
