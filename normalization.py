import torch

def normalization(feat_mat, norm_type):
    """
    This function performs feature normalization according to the paper
    :param feat_mat: lfcc mat / mfcc mat / Logspec (pytorch tensor)
    :param norm_type: one of the three: 'min_max_[0,1]', 'mean', 'mean_and_std'
    :return: normalized feature mat
    """

    if norm_type == 'min_max_[0,1]':
        min = torch.min(feat_mat)
        max = torch.max(feat_mat)
        normalized_feat_mat = (feat_mat - min) / (max - min)


    elif norm_type == 'mean':
        min = torch.min(feat_mat)
        max = torch.max(feat_mat)
        mean = torch.mean(feat_mat)
        normalized_feat_mat = (feat_mat - mean) / (max - min)


    elif norm_type == 'mean_and_std':
        mean = torch.mean(feat_mat)
        std = torch.std(feat_mat)
        normalized_feat_mat = (feat_mat - mean) / (std)


        return normalized_feat_mat