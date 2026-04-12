import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load vectorized data (from title-based preprocessing)
X_train = pickle.load(open("models/X_train.pkl", "rb"))
X_test = pickle.load(open("models/X_test.pkl", "rb"))
y_train = pickle.load(open("models/y_train.pkl", "rb"))
y_test = pickle.load(open("models/y_test.pkl", "rb"))

# Model (works well for short text like titles)
model = LogisticRegression(max_iter=2000, class_weight='balanced')

print("Training model on titles...")
model.fit(X_train, y_train)

# Predictions
pred = model.predict(X_test)

# Accuracy
acc = accuracy_score(y_test, pred)
print("Accuracy:", acc)

# Save model
pickle.dump(model, open("models/best_model.pkl", "wb"))

print("✅ Model trained on titles & saved successfully")