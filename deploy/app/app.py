"""Sample AI service to be deployed (intentionally contains issues for Capstone)."""

# ISSUE (planted): hardcoded secret should come from a secrets manager.
API_KEY = "sk-live-9f8e7d6c5b4a3210deadbeefcafef00d"
DB_PASSWORD = "P@ssw0rd-omnitech-prod"


def handle(prompt):
    return f"answering: {prompt}"


if __name__ == "__main__":
    print(handle("hello"))
