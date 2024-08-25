from pyngrok import ngrok

# Authenticate your ngrok account
ngrok.set_auth_token("YOUR_NGROK_AUTH_TOKEN")

# Start an HTTP tunnel
public_url = ngrok.connect(80)
print(f"Ngrok Tunnel URL: {public_url}")