import sys

def add_email_to_list(email):
  """Appends an email to the subscribers.txt file."""
  try:
    with open('subscribers.txt', 'a') as f:
      f.write(email + '\n')
    return f"Email {email} added to subscribers list."
  except Exception as e:
    return f"Error adding email: {e}"

if __name__ == '__main__':
  if len(sys.argv) > 1:
    email_to_add = sys.argv[1]
    result = add_email_to_list(email_to_add)
    print(result)
  else:
    print("Please provide an email address as a command-line argument.")
    print("Example: python add_email.py example@example.com")
