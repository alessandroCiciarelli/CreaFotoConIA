  
import os
import tensorflow as tf
# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

import IPython.display as display
import streamlit as st

from PIL import Image
import numpy as np
import PIL.Image
from PIL import ImageEnhance


content_path = ""
style_path = ""
content_image=""
style_image=""
loopfind = 0
imgOk=os.path.dirname(__file__) +"/" + "white.jpg"
MYDIR = os.path.dirname(__file__) +"/"

@st.cache
def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img
  
@st.cache    
def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("<h1 style='text-align: center; background-color: black;font-size:16px;'><bold style='color:green;'>INTELLIGENZA<bold style='color:white;'>ARTIFICIALE<bold style='color:red;'>ITALIA</bold></bold></bold></h1>", unsafe_allow_html=True)
st.subheader('Usa la nostra Intelligenza Artificiale demo per toccare con mano di cosa può essere capace la nostra tecnologia !')

st.subheader('\n\n1) Selezionare la foto su cui applicare lo stile')
selected_option = st.file_uploader("Carica la tua immagine",type=["png","jpg","jpeg"],accept_multiple_files=False)

if (selected_option is not None) :
	st.write("Foto caricata con successo...")
	with open(os.path.join(MYDIR,selected_option.name),"wb") as f:
		f.write(selected_option.getbuffer())
	content_path = MYDIR + selected_option.name
	content_image = load_img(content_path)
	image = Image.open(selected_option)
	img_array = np.array(image)
	st.image(image)

st.subheader('\n\n2) Selezionare la foto da cui copiare lo stile')
selected_option2 = st.selectbox("Scegli lo stile di un Pittore famoso che vuoi applicare alla tua foto",('Van Gogh', 'Escher', 'Joan Mirò'))

if (selected_option2 is not None) :		
	st.write("Foto caricata con successo...")
	style_path = os.path.dirname(__file__) +"/" + selected_option2 + ".jpg"
	style_image = load_img(style_path)
	img_array2 = np.array(style_image)
	st.image(img_array2)

if(st.checkbox('Impostazioni immagine')):
	st.text('Utilizza le slide per modificare la \nfoto finale.\nDopo aver cambiato i valori di Default\nimpostati su 1,\npremi il pulsante per ricreare la foto')
	luminosita = st.slider('Seleziona la Luminosità', 0.3, 1.7, 1.0,0.01, format="%.2f")
	contrasto = st.slider('Seleziona il Contrasto', 0.3, 1.7, 1.0,0.01, format="%.2f")
	nitidezza = st.slider('Seleziona la Nitedezza',  0.3, 1.7, 1.0,0.01, format="%.2f")
	colore = st.slider('Seleziona il bilanciamento dei colori',  0.3, 1.7, 1.0,0.01, format="%.2f")
else:
	luminosita =1
	contrasto=1
	nitidezza=1
	colore=1

viewImg= st.image(imgOk)

st.subheader('\n\n')

c= False
b = st.button('Procedi con la Creazione della Nuova Foto')
if(b):
   stato = st.info("Attendi il caricamento, potrebbero volerci fino a 2 minuti, grazie")
   import tensorflow_hub as hub
   hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
   stato.info("Ci siamo quasi...")
   try:
	   stylized_image = hub_model(tf.constant(content_image),       tf.constant(style_image))[0]
	   imgOk = tensor_to_image(stylized_image)
	   enhancer = ImageEnhance.Color(imgOk)
	   imgOk = enhancer.enhance(colore)
	   enhancer = ImageEnhance.Brightness(imgOk)
	   imgOk = enhancer.enhance(luminosita)
	   enhancer = ImageEnhance.Contrast(imgOk)
	   imgOk = enhancer.enhance(contrasto)
	   enhancer = ImageEnhance.Sharpness(imgOk)
	   imgOk = enhancer.enhance(nitidezza)
	   viewImg.image(imgOk)
	   PhotoDef = imgOk
	   watermark = os.path.dirname(__file__) +"/" + "rotated_watermark.png"
	   watermark = Image.open(watermark)
	   (PhotoW, PhotoH) = PhotoDef.size
	   (WaterW, WaterH) = watermark.size
	   for n in range(int(PhotoH * 2 / WaterH)):

		   for i in range(int(PhotoW * 2 / WaterW + 1)):

			   imgOk.paste(watermark, ((-100 + i * WaterW) + n * -220, n * WaterH), watermark)

			   loopfind += 1

	   stato.success("Usa il tasto destro del mouse o tieni premuto sull' Immagine per salvarla")
	   viewImg.image(imgOk)
	   st.balloons()
	   os.remove(style_path)
	   os.remove(content_path)
	   st.markdown('<bold> Scarica la foto e condividila sui tuoi social network per supportarci </bold>\
	   <ul> \
	  <li><a href="https://www.facebook.com/sharer.php?u=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F" target="blank" rel="noopener noreferrer">Condividi su Facebook</a></li> \
	  <li><a href="https://twitter.com/intent/tweet?url=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F&text=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale." target="blank" rel="noopener noreferrer">Condividi su Twitter</a></li> \
	  <li><a href="https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.intelligenzaartificialeitalia.net%2F&title=IntelligenzaArtificialeItalia=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale.&source=IntelligenzaArtificialeItalia" target="blank" rel="noopener noreferrer">Condividi su Linkedin</a></li>\
	</ul>', unsafe_allow_html=True)
   except Exception as e:
   	print(e)
   	stato.error(str(e))
   
st.text("")
st.text("")
st.text("")
st.text("")
st.write("Proprietà intellettuale di [Intelligenza Artificiale Italia © ](https://intelligenzaartificialeitalia.net)")
st.write("Hai un idea e vuoi realizzare un Applicazione Web Intelligente? contatta il nostro [Team di sviluppatori © ](mailto:python.ai.solution@gmail.com)")
