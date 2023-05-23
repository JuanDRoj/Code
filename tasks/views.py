from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import PrivateKeys,AddressData

import bitcoin
from eth_utils import keccak, to_checksum_address



# Create your views here.

#FUNCTIONS




def generate_btc_address():
    """Generate a new BTC address"""
    private_key = bitcoin.random_key()
    public_key = bitcoin.privkey_to_pubkey(private_key)
    btc_address = bitcoin.pubkey_to_address(public_key)
    
    return btc_address


def validate_private_key(user_id,crypto_type):
    """Validate the private key"""
    user_exist=PrivateKeys.objects.filter(user_id=user_id).filter(type=crypto_type)
    
    if crypto_type=='BTC':
        private_key = bitcoin.random_key()
    if crypto_type=='ETH':
        private_key = keccak(text='your_secret_key').hex()

    if(user_exist):
        user_exist.update(
            private_key=private_key
        )
        #private_key=user_exist.values()[0]['private_key']
    else:
        
        PrivateKeys.objects.create(
            private_key=private_key,
            type=crypto_type,
            user_id=user_id
        )

    return private_key


def generate_address(crypto_type,private_key,user_id):

    """Generate the addres depending on crypto_type"""

    address=None

    if crypto_type=='BTC':
            public_key = bitcoin.privkey_to_pubkey(private_key)
            address = bitcoin.pubkey_to_address(public_key)
    if crypto_type=='ETH':
            public_key = keccak(bytes.fromhex(private_key)[1:]).hex()
            address = to_checksum_address('0x' + public_key[-40:])

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
       
        private_key=validate_private_key(user_id,crypto_selection)

        
        
        if(private_key):
            address=generate_address(crypto_selection,private_key,user_id)

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