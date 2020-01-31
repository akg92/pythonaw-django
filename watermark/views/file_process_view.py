import time
import os
import sys
import shutil
from django.http import HttpResponse
from rest_framework import views
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser
from rest_framework.response  import Response
class FileUploadView(views.APIView):
    parser_classes = ( FileUploadParser, MultiPartParser)
    absolute_dir = 'datafolder/'
    jar_location = './jar/remove-watermark.jar'
    ## get absolute path
    def get_file_path(self, file_name):
        return os.path.join(FileUploadView.absolute_dir, file_name)

    ## set in and out file name
    def set_file_name(self,file_name):
        file_name = file_name if file_name.endswith(".pdf") else file_name+".pdf" 
        file_name = file_name.replace("/","")
        file_name = file_name.replace(" ", "_")
        self.original_filename = file_name
        current_time = str(time.time())
        self.in_file_name = self.get_file_path(current_time + file_name+'.pdf')
        self.out_file_name = self.get_file_path(current_time +'_out_' +file_name +'.pdf')
    ## save file 
    def save(self, file_obj):
        with open(self.in_file_name,'wb') as f:
            f.write(file_obj)

    ## delete file
    def delete_file(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

            
    ## cleanup all the temporary files
    def cleanup(self):
        self.delete_file(self.in_file_name)
        self.delete_file(self.out_file_name)

    ## def generate the file
    def remove_water_mark(self):
        command = 'java -jar "{}" "{}" "{}"'.format(FileUploadView.jar_location, self.in_file_name, self.out_file_name)
        os.system(command)

    ## def return created file
    def return_processed_file(self):
        ## execute command
        self.remove_water_mark()
        ## wait for the file completion
        total_wait = 0
        ## need total wait time limit
        while(not os.path.exists(self.out_file_name) and total_wait < 120):
            time.sleep(2)
            total_wait += 2
        
        if(total_wait > 120):
            self.cleanup(self.in_file_name)
            return Response(status=500)
        ## 
        response = None
        with open(self.out_file_name, 'rb') as f:
            response = HttpResponse(content_type='application/pdf')
            # print(self.original_filename)
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(self.original_filename)
            response.write(f.read())
        
        ## call cleanup
        self.cleanup()
        return response

    def put(self, request,filename , format=None):
        file_obj = request.data
        print(file_obj.keys())
        name = filename
        self.set_file_name(filename)
        self.save(file_obj['file'].read())
        return self.return_processed_file()
        # ...
        # do some stuff with uploaded file
        # ...
        # return Response(status=204)

    def get(self, request):
        return Response("Hello", status = 200)