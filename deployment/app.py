from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
# import h5py

app = Flask(__name__)

dic = {0 : 'happy', 1 : 'sad'}

model = load_model('happysadmodel.h5')
# file_name = "happysadmodel.h5"
# model= h5py.File("happysadmodel.h5", 'r')

model.make_predict_function()

def predict_label(img_path):
	i = image.load_img(img_path, target_size=(256, 256))
	i = image.img_to_array(i)/255.0
	i = i.reshape(1, 256, 256, 3)
	# p = model.predict_classes(i)
	p = (model.predict(i) > 0.5).astype("int32")
	print("hello-----------------------------------------")
	print (dic)
	return dic[p[0][0]]


# routes
@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template("index.html")

@app.route("/about")
def about_page():
	return "Please subscribe  Artificial Intelligence Hub..!!!"

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = img.filename	
		img.save(img_path)

		p = predict_label(img_path)

	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(port=3000, debug = True)