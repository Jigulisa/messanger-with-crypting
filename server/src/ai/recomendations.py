import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# TODO(Jigulisa): вообще тут надо запрос делать
X, _ = make_blobs(n_samples=300, centers=5, cluster_std=0.60, random_state=42)

inertia_values = []
k_range = range(1, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    inertia_values.append(kmeans.inertia_)


plt.plot(k_range, inertia_values, "bo-")
plt.xlabel("Количество кластеров k")
plt.ylabel("Sum of squared distances (Inertia)")
plt.title("Метод локтя для выбора числа кластеров")
plt.show()
