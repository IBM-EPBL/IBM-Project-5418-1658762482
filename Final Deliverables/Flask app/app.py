from flask import Flask,render_template,request
import operator
import numpy 
import cv2
from tensorflow.keras.models import load_model
import os
from werkzeug.utils import secure_filename
import time 


app=Flask(__name__,template_folder="templates")
model=load_model("temp.h5")


@app.route('/',methods=['GET','POST'])
def home():
    return render_template("home.html")

@app.route('/intro')
def intro():
    return render_template("intro.html")

@app.route('/image1',methods=['GET','POST'])
def image1():
    return render_template("launch.html")


@app.route('/predict',methods=['GET','POST'])
def launch():
    if request.method=="POST":
       

        f=request.files["image"]
        basepath=os.path.dirname(__file__)
        file_path=os.path.join(basepath,'uploads',secure_filename(f.filename))
        f.save(file_path)
        print(file_path)
        #capture video
        time.sleep(2)
        cap=cv2.VideoCapture(0)
        con=True
        image1=cv2.imread(file_path)
        buffer=1
        zv=0
        while True:
            if not con:
                cap=cv2.VideoCapture(0)
                con = True
            buffer-=1
            success,frame=cap.read()
            if success==False:
                continue
            frame=cv2.flip(frame,1)
            x1=int(0.5*frame.shape[1])
            y1=10
            x2=frame.shape[1]-10
            y2=int(0.5*frame.shape[1])
            cv2.rectangle(frame,(x1-1,y1-1),(x2+1,y2+1),(255,0,0),1)
            roi=frame[y1:y2,x1:x2]
            roi=cv2.resize(roi,(128,128))
            cv2.imshow("gesture",roi)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # time.sleep(1)
            
            # success,frame=cap.read()
            
            cap.release()
            
            roi=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
            _,test_image=cv2.threshold(roi,120,255,cv2.THRESH_BINARY)
            if not buffer>0:
                
                print("inside loop")

                result=model.predict(test_image.reshape(1,128,128,1))

                res = numpy.argmax(result)
                if numpy.amax(result) <=0.25:
                    continue

                print(res)

                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
                if res==1:
                    # cv2.destroyWindow("Fixed Resizing")
                    resized=cv2.resize(image1,(400,400))
                    cv2.imshow("Fixed Resizing",resized)
                    print("before resize")
                    buffer=00
                    
                    con=False
                    time.sleep(3)
                    #cv2.waitKey(5000)
                    # # print("after resize")
                    key=cv2.waitKey(3000)
                    if(key & 0xFF)==ord('1'):
                        cv2.destroyWindow("Fixed Resizing")
                elif res==2:
                    print("insode else",res)
                    buffer=00
                    con=False
                    time.sleep(3)
                    continue

                elif res==3:
                    # cv2.destroyWindow("blurred")
                    blurred=cv2.GaussianBlur(image1,(11,11),0)
                    cv2.imshow("blurred",blurred)
                    print("before blur")
                    buffer=00
                    # cap.release()
                    con=False
                    time.sleep(3)
                    #cv2.waitKey(5000)
                    key=cv2.waitKey(3000)
                    # print("after blur")
                    if(key & 0xFF)==ord('3'):
                        cv2.destroyWindow("blurred")
                    # #time.sleep(5)
                elif res==4:
                    # cv2.destroyWindow("rectangle")
                    cv2.rectangle(image1,(480,170),(650,420),(0,0,255),2)
                    cv2.imshow("rectangle",image1)
                    # cv2.waitKey(1)
                    print("before rec")
                    buffer=00
                    # cap.release()
                    con=False
                    time.sleep(3)
                    #cv2.waitKey(5000)
                    key=cv2.waitKey(3000)
                    print("after rec")
                    if(key & 0xFF)==ord('2'):
                        cv2.destroyWindow("rectangle")
                    #time.sleep(5)
                elif res==5:
                    cv2.destroyWindow("blurred")
                    cv2.destroyWindow("rotated")
                    cv2.destroyWindow("rectangle")
                    cv2.destroyWindow("Fixed Resizing")
                    buffer=00
                    # cap.release()
                    con=False
                    time.sleep(3)
                    # break
                    # time.sleep(3)
                else:
                    (h,w,d)=image1.shape    
                    center=(w//2,h//2)
                    M=cv2.getRotationMatrix2D(center,-45,1.0)
                    rotated=cv2.warpAffine(image1,M,(w,h))
                    cv2.imshow("rotated",rotated)
                    buffer=00
                    # cap.release()
                    con=False
                    time.sleep(3)
                    #cv2.waitKey(5000)
                    # print("before rotate")
                    key=cv2.waitKey(3000)
                    print("after rotate")
                    if(key & 0xFF)==ord('2'):
                        cv2.destroyWindow("rotated")
                    
                print("inside buffer",res)
            print("outside if buffer",res)

        cap.release()
        cv2.destroyAllWindows()
    return render_template("home.html")
if __name__ == "__main__":
   # running the app
    app.run(debug=False)