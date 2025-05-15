
import joblib
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier


class MatchWinner:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.encoders = {}
        self.xbg_model = None

    def load_data(self):
        self.df = pd.read_csv(self.data_path)

    def encode_features(self):
        team_columns = ['team_1', 'team_2', 'toss_winner', 'home_team']
        winner_column = 'winner'

        # Combine team columns to fit a shared team encoder
        team_names = pd.concat([self.df[col] for col in team_columns]).unique()
        team_names = sorted(team_names)

        team_encoder = LabelEncoder()
        team_encoder.fit(team_names)

        # Encode all team columns (including home_team) using shared encoder
        for col in team_columns:
            self.df[col] = team_encoder.transform(self.df[col])
            self.encoders[col] = team_encoder

        # Encode winner
        self.df[winner_column] = team_encoder.transform(self.df[winner_column])
        self.encoders[winner_column] = team_encoder

        # Encode remaining categorical (e.g., venue, match_type, toss_decision)
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                encoder = LabelEncoder()
                self.df[col] = encoder.fit_transform(self.df[col])
                self.encoders[col] = encoder

    def train_model(self):
        X = self.df.drop(columns=['winner'])
        y = self.df['winner']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

        xbg_model = XGBClassifier(
            use_label_encoder=False,
            eval_metric='mlogloss',
            learning_rate=0.01,
            n_estimators=350,
            max_depth=8,
            subsample=0.8,
            colsample_bytree=0.8
        )
        xbg_model.fit(X_train, y_train)
        self.xbg_model = xbg_model

        y_pred = xbg_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        # print(classification_report(y_test, y_pred))
        print(f"Model trained! Accuracy: {round(accuracy, 2)}")

    def save_model(self, model_path='api/trained_model/model.pkl', encoders_path='api/trained_model/encoders.pkl'):
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(self.xbg_model, model_path)
        joblib.dump(self.encoders, encoders_path)
        print("Model and Encoders saved")


model = MatchWinner('./final_data.csv')
model.load_data()
model.encode_features()
model.train_model()
model.save_model()
