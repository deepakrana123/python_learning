def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:3000/reset-password?token={token}"
    print(f"[Simulated Email] Reset link for {email}: {reset_link}")
