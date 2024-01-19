from django.shortcuts import render
from django.views import View
from .forms import UploadForm
from django.http import HttpResponse,JsonResponse
from .models import Upload
import pandas as pd
import openpyxl
import math

# Create your views here.

def read_file(file_path):
    # Check the file extension
    if file_path.endswith('.xlsx'):
        # Read Excel file
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        # Read CSV file
        df = pd.read_csv(file_path)
    else:
        # Handle other file types or raise an error
        raise ValueError(f"Unsupported file type: {file_path}")

    return df

class FinacialData(View):

    def get(self, request):
        form = UploadForm()  
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance=form.save()

            #uploaded file path
            matching_file=Upload.objects.get(id=instance.id)
        
            
            # df=pd.read_excel(f"media//{matching_file}")
            file_path=f"media//{matching_file}"
            df=read_file(file_path)
            l=[]
            total_returns=0
            variance=0
            for index,item in df.iterrows():
               if index>0:
                    daily_return_value=(df.iloc[index,4]/df.iloc[index-1,4])-1
                    l.append(daily_return_value)
                    total_returns+=daily_return_value
                    
            daily_return=pd.Series(l)
            mean=total_returns/df.shape[0]
           
            for i in daily_return:
                variance+=(i-mean)**2
            variance=variance/df.shape[0]
            daily_volatility=math.sqrt(variance)
          
            annualsied_volatility=daily_volatility*(math.sqrt(df.shape[0]))
            
            return JsonResponse({'daily_returns':f"{daily_return}",'daily_volatility':f"{daily_volatility}",'annualsied_volatility':f"{annualsied_volatility}"})
        else:
            print(form.errors)
            return HttpResponse('Form is not valid')
