import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.datasets import make_circles

# Make 1000 examples
n = 1000

# Create circles
X, y = make_circles(n, noise=0.03, random_state=0)
type(y), type(X)
X.shape, y.shape
X[:10]
y[:10]

# Let's visualize the data
circles = pd.DataFrame({"X0": X[:, 0], "X1": X[:, 1], "Label": y})
plt.scatter(circles["X0"], circles["X1"])
plt.xlabel("X0")
plt.ylabel("X1")
plt.legend()

# Set the random seed so that we get the same random values
tf.random.set_seed(0)

## 1. Build Model
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation("relu"))
model.add(tf.keras.layers.Dense(10))
model.add(tf.keras.layers.Activation("sigmoid"))
model.add(tf.keras.layers.Dense(1))

## 2. Compile Model
learning_rate = 0.001
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(),
    optimizer=optimizer,
    metrics=["accuracy", tf.keras.metrics.Precision()],
)
## 3. Fit Model
model.fit(X, y, epochs=20)
model.summary()


def plot_decision_boundary(model, X, y, threshold=0.5, cmap="RdBu"):
    # Generate a grid of points covering the input space
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))

    # Make predictions for each point in the grid
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])

    # Apply threshold to convert probabilities into class predictions
    Z = (Z > threshold).astype(int)

    # Reshape predictions to match grid shape
    Z = Z.reshape(xx.shape)

    # Plot decision boundary
    plt.contourf(xx, yy, Z, cmap=cmap, alpha=0.8)

    # Plot data points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap, edgecolors="k")

    # Set plot limits
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())

    # Add labels and title
    plt.xlabel("Feature 1")
    plt.ylabel("Feature 2")
    plt.title("Decision Boundary")

    # Show plot
    plt.show()


plot_decision_boundary(model=model, X=X, y=y)
