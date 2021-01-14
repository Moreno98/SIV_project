import numpy as np

def pearson_correlation(X, Y):
    covariance = np.cov(X,Y)[0][1]
    X_std = np.std(X)
    Y_std = np.std(Y)
    if((X_std == 0) or (Y_std == 0)):
        pc = 0.0000
    else:
        pc = covariance/(X_std*Y_std)
    return round(pc, 4)


def get_correlation_matrix(features):
    correlation_matrix = []

    for f0 in features:
        f0 = features[f0]
        row = []
        for f1 in features:
            f1 = features[f1]
            row.append(pearson_correlation(f0, f1))
        correlation_matrix.append(row)
    return correlation_matrix

def get_190_features(features):
    c_mat = get_correlation_matrix(features)
    features = []
    for i in range(len(c_mat)):
        for j in range(len(c_mat[0])):
            if (i<j):
                features.append(c_mat[i][j])
    return features