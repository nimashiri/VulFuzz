#!/bin/bash

pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_ndarray.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/common/models.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/amp/common.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/quantization/common.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/train/common.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/profiling/simple_forward.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/array-api/test_data_interchange.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/subgraphs/test_amp_subgraph.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/subgraphs/test_conv_subgraph.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/subgraphs/test_fc_subgraph.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/subgraphs/test_matmul_subgraph.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/subgraphs/test_pow_mul_subgraph.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/test_amp.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/test_bf16_operator.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/test_dnnl.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/dnnl/test_quantization_dnnl.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/doctest/test_docstring.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_amp.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_amp_init.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_deferred_compute_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_device.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_extensions_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_fusion.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_gluon_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_gluon_model_zoo_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_gluon_transforms.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_kvstore_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_nccl.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_numpy_einsum.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_numpy_fallback.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_operator_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/gpu/test_profiler_gpu.py

