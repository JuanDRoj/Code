from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import PrivateSeeds,AddressData

import mnemonic
import bitcoin
from eth_utils import keccak, to_checksum_address
from cryptography.fernet import Fernet


# Create your views here.

#FUNCTIONS
def generate_seed():
    """Generates a seed."""
    seed = mnemonic.Mnemonic(language='english').generate(strength=128)
    seed=seed.encode('utf-8')
    return seed


def btc_address(seed,existing_addresses):
    """Generates a btc address from single seed"""
    master_private_key = bitcoin.bip32_master_key(seed)
    i=0
    if existing_addresses:
        address=existing_addresses[0]
        while address in existing_addresses:
            child_private_key = bitcoin.bip32_ckd(master_private_key, i)
            child_public_key = bitcoin.bip32_extract_key(child_private_key)
            address = bitcoin.pubkey_to_address(child_public_key)
            i=i+1
    else:
        child_private_key = bitcoin.bip32_ckd(master_private_key, 0)
        child_public_key = bitcoin.bip32_extract_key(child_private_key)
        address = bitcoin.pubkey_to_address(child_public_key)

    return address

def eth_addresses(seed,existing_addresses):
    """Generates an eth address from single seed"""
    seed_hash = keccak(seed)
    private_key = seed_hash.hex()
    if existing_addresses:
        address=existing_addresses[0]
        while address in existing_addresses:
            public_key = keccak(bytes.fromhex(private_key)[1:]).hex()
            address = to_checksum_address('0x' + public_key[-40:])
            private_key = hex(int(private_key, 16) + 1)[2:]
    else:
        public_key = keccak(bytes.fromhex(private_key)[1:]).hex()
        address = to_checksum_address('0x' + public_key[-40:])


    return address  


def validate_seed(user_id):
    """Validate seed"""
    user_exist=PrivateSeeds.objects.filter(user_id=user_id)
    
    if(user_exist):
        user_data=user_exist.values()[0]
        key=user_data['seed_key'].encode()
        crypter=Fernet(key)
        seed=crypter.decrypt(user_data['seed'].encode())
    else:
        key=Fernet.generate_key()
        crypter=Fernet(key)
        seed=generate_seed()
        encrypted_seed=str(crypter.encrypt(seed),'utf8')
        str_key=str(key,'utf8')
        PrivateSeeds.objects.create(
            seed=encrypted_seed,
            user_id=user_id,
            seed_key=str_key
        )

    return seed


def generate_address(crypto_type,seed,user_id):

    """Generate the addres depending on crypto_type"""
    address=None
    addresses=[row['address'] for row in AddressData.objects.filter(user_id=user_id).filter(type=crypto_type).values()]
    
    if crypto_type=='BTC':
            address = btc_address(seed,addresses)
    if crypto_type=='ETH':
            address = eth_addresses(seed,addresses)

    AddressData.objects.create(
            address=address,
            type=crypto_type,
            user_id=user_id
        )

    return address


#SCREENS

@csrf_exempt
@login_required
def main_menu(request):
    user = get_user(request)
    return render(request,"home.html",{"user_name":user})



@csrf_exempt
@login_required
def generate_screen(request):
    user = get_user(request)
    user_id=request.user.id

    if(request.method == "POST"):

        crypto_selection=request.POST.get('crypto_type')
       
        seed=validate_seed(user_id)

        if(seed):
            address=generate_address(crypto_selection,seed,user_id)
            if(address):
                return redirect('tasks:list')
         

    return render(request,"generate.html",{"user_name":user})


@login_required
def list_screen(request):
    user = get_user(request)
    user_id=request.user.id
    address_data=list(AddressData.objects.filter(user_id=user_id).values())

    return render(request,"list.html",{"user_name":user,'address_data':address_data})


@csrf_exempt
@login_required
def retrieve_screen(request):
    user = get_user(request)
    address_data={}
    if(request.method == "POST"):
        id_input=request.POST.get('id')
        address_data=AddressData.objects.filter(id=id_input).values()
        if address_data:
            address_data=address_data[0]

    return render(request,"retrieve.html",{"user_name":user,'address_data':address_data})

def logout_func(request):
    auth_logout(request)
    return redirect('login:login')