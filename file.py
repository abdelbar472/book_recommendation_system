import numpy as np

arr = np.load("embeddings.npy")
np.savetxt("file.csv", arr, delimiter=",")
