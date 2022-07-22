from flask import Flask, request, jsonify
import mimetypes
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'C:\\Users\\uzoma\\OneDrive\\Desktop\\queenshub\\video-storing\\upload-video'
ALLOWED_EXTENSIONS = {'mp4','mkv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024
# video not exceed of 10 minutes length
def check_video_duration(file):
    if file.content_length > 10 * 60 * 1024 * 1024:
        return False
    return True


def check_max_file_size(file):
    if file.content_length > app.config['MAX_CONTENT_LENGTH']:
        return False
    return True
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
          

# to recieve the video uploaded 
@app.route('/videoupload', methods=['POST'])
def upload_file():
    file = request.files["user_file"]
    if file and allowed_file(file.filename) and check_video_duration(file) and check_max_file_size(file):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("hello")
        return jsonify({"message": "File uploaded successfully"})
    else:
        return jsonify({"message": "File not uploaded"})

#get list of files in the upload folder

@app.route('/getvideo', methods=['GET'])
def get_video():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    time = [os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)) for x in files]   
    size = [x/1024/1024 for x in size]
    name = [os.path.splitext(x)[0] for x in files]
    type = [mimetypes.guess_type(os.path.join(app.config['UPLOAD_FOLDER'], x)) for x in files]
    data = {'name': name, 'time': time, 'size': size, 'type': type}
    return jsonify(data)



@app.route('/validatevideo', methods=['POST'])
def validate_video():
    size = request.form['size']
    type = request.form.get('type')
    # charges for video of below 500 MB and $10 for video of above 500 MB
    if size < 500 and type == 'video/mp4':
        return jsonify({"charge": "$5"})
    elif size > 500 and type == 'video/mp4':
        return jsonify({"charge": "$12.5"})
#additional charges $12.5 if video is under 6 minutes 18 seconds and $20 if video is above 6 minutes 18 seconds
    elif size < 500 and type == 'video/mkv':
        return jsonify({"charge": "$12.5"})
    elif size > 500 and type == 'video/mkv':
        return jsonify({"charge": "$20"})


  



    










  

    

   

    




    






    





    

    

        


    


        
    
