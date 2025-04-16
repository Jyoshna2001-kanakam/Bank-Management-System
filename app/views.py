from django.shortcuts import render,HttpResponse,redirect
from. models import Account
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
     return render(request,'index.html')

def create(request):
     if request.method=='POST':
          name=request.POST.get('name')
          dob=request.POST.get('dob')
          aadhar=request.POST.get('aadhar')
          mobile=request.POST.get('mobile')
          address=request.POST.get('address')
          email=request.POST.get('email')
          print(name,dob,aadhar,mobile,address,email)

          Account.objects.create(name=name,dob=dob,aadhar=aadhar,mobile=mobile,address=address,email=email)
          print("data added successfully")

          send_mail(f'Hello {name},', #subject
                    'Thank you for creating an account in our bank. \n Welcome to our family.\n FBH fraud bank of hyderabad  \n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[email],fail_silently=False)
          print("Mail sent")

     return render(request,'create.html')

def pin_gen(request):
     if request.method=='POST':
          otp=random.randint(100000,999999)
          acc=request.POST.get('acc')
          data=Account.objects.get(acc=acc)
          email=data.email
          send_mail(f'Hello {data.name},', #subject
                    f'The otp (one time password) is {otp}.Please do not share the otp with others.\n FBH fraud bank of hyderabad \n Welcome to our family. \n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[email],fail_silently=False)
          print("Mail sent")

          data.otp=otp
          data.save()
          return redirect('otp')
     return render(request,'pin.html')

def valid_otp(request):
     if request.method=='POST':
          acc=request.POST['acc']
          otp=int(request.POST['otp'])
          pin1=int(request.POST['pin1'])
          pin2=int(request.POST['pin2'])
          # print(acc,otp,pin1,pin2)
          if pin1==pin2:
               data=Account.objects.get(acc=acc)
               if data.otp==otp:
                    data.pin=pin2
                    data.save()
                    send_mail(f'Hello {data.name},', #subject
                    f'You have successfully generated the pin.Please do not share the pin with others.\n FBH fraud bank of hyderabad. \n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
                    print("Mail sent")
               else:
                    return HttpResponse("OTP mismatched")
          else:
               return HttpResponse("****** is not a valid pin ")

     return render(request,'valid_otp.html')

def balance(request):
     data=None
     msg=''
     bal=0
     f=False
     if request.method =='POST':
          acc=request.POST['acc']
          pin=request.POST['pin']
          # print(acc,pin)
          try:
               data=Account.objects.get(acc=int(acc))
          except:
               pass
          if data is not None:
               if data.pin ==int(pin):
                    bal=data.bal
                    f=True
               else:
                    msg='please enter valid pin'
          else:
               msg='Please enter valid account number'
     context={
          'bal':bal,
          'var':f,
          'msg':msg
     }          

     return render(request,'balance.html',context)
def withdraw(request):
     data=None
     msg=''
     if request.method=='POST':
          acc=int(request.POST['acc'])
          pin=int(request.POST['pin'])
          amt=int(request.POST['amt'])
          try:
               data=Account.objects.get(acc=acc)
          except:
               msg='Account not found'
               # print('Account not found')
          if data.pin ==pin:
               if data.bal>=amt and amt>0:
                    data.bal-=amt
                    data.save()
                    send_mail(f'Hello {data.name},', #subject
                    f'FBH fraud bank of hyderabad. \n from your {data.acc}\n {amt} as be withdraw from ATM the available balance is {data.bal}.\n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
                    print("Mail sent")
                    return redirect('index')
               else:
                    msg='Insufficient balance'
          else:
               msg='Please enter a valid pin'
     context={
          'msg':msg
     }
                    

     return render(request,'withdraw.html',context)

def deposite(request):
     data=None
     msg=''
     if request.method=='POST':
          acc=request.POST['acc']
          pin=request.POST['pin']
          amt=int(request.POST['amt'])
          try:
               data=Account.objects.get(acc=acc)
          except:
               msg='Account not found'
               # print('Account not found')
          if data.pin ==int(pin):
               if amt>=100 and amt<=1000:
                    data.bal+=amt
                    data.save()
                    send_mail(f'Hello {data.name},', #subject
                    f'FBH fraud bank of hyderabad. \n from your {data.acc}\n {amt} has been deposited .Your current balance is {data.bal}.\n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[data.email],fail_silently=False)
                    print("Mail sent")
                    return redirect('index')
               else:
                    msg='Insufficient balance'
          else:
               msg='Please enter a valid pin'
     context={
          'msg':msg
     }
     return render(request,'deposite.html',context)

def transfer(request):
     msg=''
     if request.method=='POST':
          f_acc=request.POST.get('f_acc')
          t_acc=request.POST.get('t_acc')
          pin=request.POST.get('pin')
          amt=request.POST.get('amt')
          # print(f_acc,t_acc,pin,amt)
          try:
               from_acc=Account.objects.get(acc=f_acc)
          except:
               msg='send account is not valid'
          try:
               to_acc=Account.objects.get(acc=t_acc)
          except:
               msg='reciever account is not valid'
          if from_acc.pin==int(pin):
               if int(amt)>100 and int(amt)<=10000 and int(amt)<=from_acc.bal:
                    from_acc.bal-=int(amt)
                    from_acc.save()
                    send_mail(f'Hello {from_acc.name} Account Transfer,', #subject
                    f'FBH fraud bank of hyderabad. \n from your {from_acc.acc}\n {amt} has been deposited .Your current balance is {from_acc.bal}.\n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[from_acc.email],fail_silently=False)
                    print("Mail sent")

                    to_acc.bal+=int(amt)
                    to_acc.save()
                    send_mail(f'Hello {to_acc.name} Account Transfer,', #subject
                    f'FBH fraud bank of hyderabad. \n {to_acc.acc}\n {amt} has been credited from {from_acc.acc} .Your current balance is {to_acc.bal}.\n Regards\n Manager(DJD-E1) \n', #body
                    settings.EMAIL_HOST_USER,[from_acc.email],fail_silently=False)
                    print("Mail sent")
               else:
                    msg='Enter the valid amount'
          else:
               msg='Invalid pin'

     return render(request,'transfer.html',{'msg':msg})