#!/bin/bash

pytest -q /media/nimashiri/SSD1/mxnet/tests/python/onnx/test_models.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/onnx/test_operators.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/profiling/test_nvtx.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/quantization/test_quantization.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/test_quantization_gpu.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/train/test_autograd.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_attr.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_autograd.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_base.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_control_flow.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_gluon_data_vision.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_hawkesll.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_intgemm.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_io.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_krprod.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_operator.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_optimizer.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_contrib_stes_op.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_deferred_compute.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_dynamic_shape.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_engine.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_engine_import.py
pytest -q /media/nimashiri/SSD1/mxnet/tests/python/unittest/test_exc_handling.py