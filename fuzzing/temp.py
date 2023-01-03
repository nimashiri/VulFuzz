import torch
import numpy as np
arg_1_tensor = torch.rand([0, 0, 1, 2, 3, 0], dtype=torch.float64)
arg_1 = arg_1_tensor.clone()
arg_2_tensor = torch.rand([1, 2, 3, 0], dtype=torch.float64)
arg_2 = arg_2_tensor.clone()
arg_3 = 95063276620
try:
    res = torch.tensordot(arg_1, arg_2, dims=arg_3,)
except Exception as e:
    print("Error:"+str(e))
