import string
import randon

def generate_password(length=12):
  # our characters pool
  chars = string.ascii_letters + string.digits + string.puntual

# pick random characters 'length' times
password= ''.join(random.choice(chars) for _ in range(length):
return password 
