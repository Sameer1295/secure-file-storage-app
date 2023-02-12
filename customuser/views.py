from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
def generate_ecc_key_pair(user):
    # Generate the ECC key pair
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key = private_key.public_key()

    # Serialize the private key
    private_key_serialized = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Serialize the public key
    public_key_serialized = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Store the serialized keys in the database
    user.public_key = public_key_serialized.decode('utf-8')
    user.private_key = private_key_serialized.decode('utf-8')
    user.save()
