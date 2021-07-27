import numpy as np
import random


def spec_average(lfcc, frequency_masking_para=12,
                 time_masking_para=80, frequency_mask_num=1, time_mask_num=0, specavg = True):
    """
    :param lfcc: feature tensor. in our case was of dimensions 60X450
    :param frequency_masking_para: max number of bins to mask in frequency
    :param time_masking_para: max number of consecutive steps to mask in time
    :param frequency_mask_num: number of masks in frequency
    :param time_mask_num: number of masks in time
    :param specavg: True  = SpecAverage. False = SpecAugment.
    :return: masked feature
    """
    if specavg:
        avg = lfcc.mean()
        val = avg
    else: # Don't put average, put 0
        val = 0

    v = lfcc.shape[0]
    tau = lfcc.shape[1]

    # Step 1 : Frequency masking
    for i in range(frequency_mask_num):
        f = np.random.uniform(low=0.0, high=frequency_masking_para)
        f = int(f)
        f0 = random.randint(0, v-f)
        lfcc[f0:f0+f, :] = val

    # Step 2 : Time masking
    for i in range(time_mask_num):
        t = np.random.uniform(low=0.0, high=time_masking_para)
        t = int(t)
        t0 = random.randint(0, tau-t)
        lfcc[:, t0:t0+t] = val

    return lfcc
