from __future__ import print_function, absolute_import

import torch
import numpy as np
import time
import sys

def synthetic(n, nnz):
    """This function generates a synthetic matrix."""
    begin = time.time()
    # TODO: distribute as power law?
    #       (closer to real distribution)
    v = torch.abs(torch.randn([nnz]))
    # TODO: make non-neg
    v = v.type(torch.DoubleTensor)
    ind = torch.rand(2, nnz) * torch.Tensor([n, n]).repeat(nnz, 1).transpose(0, 1)
    # TODO: fix ind (only diag right now)
    ind = ind.type(torch.LongTensor)

    cooccurrence = torch.sparse.DoubleTensor(ind, v, torch.Size([n, n])).coalesce()
    vocab = None
    words = None
    end = time.time()
    print("Generating synthetic data:", end - begin)

    return cooccurrence, vocab, words

def normalize(x, x0=None):
    # TODO: is it necessary to reorder columns by magnitude
    # TODO: more numerically stable implementation?
    begin = time.time()
    norm = torch.norm(x, 2, 0, True).squeeze()
    dim, = norm.shape
    print("\n" + " ".join(["{:10.2f}".format(n) for n in norm]))
    sys.stdout.flush()
    try:
        temp, r = torch.qr(x)
    except RuntimeError as e:
        print("ERROR: QR decomposition has run into a problem")
        print("Older versions of pytoch had a memory leak in QR:")
        print("    https://github.com/pytorch/pytorch/issues/3009")
        print("Updating pytorch may fix this issue.")
        sys.stdout.flush()
        raise e
    if np.isnan(torch.sum(temp)):
        # qr seems to occassionally be unstable and result in nan
        print("WARNING: QR decomposition resulted in NaNs")
        print("         Normalizing, but not orthogonalizing")
        sys.stdout.flush()
        # TODO: should a little bit of jitter be added to make qr succeed?
        x = x.div(norm.expand_as(x))
        if x0 is not None:
            x0 = x0.div(norm.expand_as(x0))
    else:
        x = temp
        if x0 is not None:
            x0 = torch.mm(x0, torch.inverse(r))
    end = time.time()
    print("Normalizing took", end - begin)
    sys.stdout.flush()

    return x, x0

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
