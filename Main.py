!pip install deepface opencv-python-headless from deepface import DeepFace
import cv2
from IPython.display import display, Javascript
from google.colab.output import eval_js
from base64 import b64decode

# ------------------ Local Movie Database ------------------ #
movies_db = {
    "happy": [
        {"title": "The Grand Budapest Hotel", "rating": 8.1, "overview": "A comedy about a legendary concierge and a hotel lobby boy."},
        {"title": "Forrest Gump", "rating": 8.8, "overview": "Life is like a box of chocolates..."},
        {"title": "The Intouchables", "rating": 8.5, "overview": "A comedy-drama about friendship across social classes."}
    ],
    "sad": [
        {"title": "Schindler's List", "rating": 9.0, "overview": "The true story of Schindler saving lives during WWII."},
        {"title": "The Pursuit of Happyness", "rating": 8.0, "overview": "A struggling father overcomes hardships for his son."},
        {"title": "A Beautiful Mind", "rating": 8.2, "overview": "Biography of John Nash and his struggles with schizophrenia."}
    ],
    "angry": [
        {"title": "Gladiator", "rating": 8.5, "overview": "A former Roman General seeks revenge against the emperor."},
        {"title": "Mad Max: Fury Road", "rating": 8.1, "overview": "Post-apocalyptic road war action film."}
    ],
    "surprise": [
        {"title": "Inception", "rating": 8.8, "overview": "A thief steals secrets through dreams."},
        {"title": "Interstellar", "rating": 8.6, "overview": "A team travels through a wormhole to save humanity."}
    ],
    "fear": [
        {"title": "The Conjuring", "rating": 7.5, "overview": "Paranormal investigators help a family haunted by a dark presence."},
        {"title": "A Quiet Place", "rating": 7.5, "overview": "Family survives in silence to avoid monsters."}
    ],
    "neutral": [
        {"title": "The Shawshank Redemption", "rating": 9.3, "overview": "Two imprisoned men bond over years."},
        {"title": "Forrest Gump", "rating": 8.8, "overview": "Life story of a man witnessing historical events."}
    ],
    "disgust": [
        {"title": "Se7en", "rating": 8.6, "overview": "Two detectives hunt a serial killer using the seven deadly sins."},
        {"title": "Silence of the Lambs", "rating": 8.6, "overview": "A young FBI agent consults a cannibalistic killer to catch another killer."}
    ]
}

# ------------------ Colab Webcam Capture ------------------ #

def take_photo(filename='captured.jpg'):
    js = Javascript("""
    async function takePhoto(){
      const video = document.createElement('video');
      const stream = await navigator.mediaDevices.getUserMedia({video: true});
      document.body.appendChild(video);
      video.srcObject = stream;
      await video.play();
      await new Promise(resolve => requestAnimationFrame(resolve));
      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      stream.getTracks().forEach(t => t.stop());
      document.body.removeChild(video);
      return canvas.toDataURL('image/jpeg', 0.95);
    }
    takePhoto();
    """)
    display(js)
    data = eval_js('takePhoto()')
    image_bytes = b64decode(data.split(',')[1])
    with open(filename, 'wb') as f:
        f.write(image_bytes)
    return filename

# ------------------ Emotion Detection ------------------ #

def detect_emotion(image_path):
    print("🔍 Detecting emotion...")
    result = DeepFace.analyze(img_path=image_path, actions=['emotion'], enforce_detection=False)
    emotion = result[0]['dominant_emotion']
    print(f"🎭 Detected Emotion: {emotion}")
    return emotion

# ------------------ Recommend Movies ------------------ #

def recommend_movies():
    print("📸 Opening webcam...")
    img = take_photo()
    emotion = detect_emotion(img)
    
    movies = movies_db.get(emotion, movies_db['neutral'])
    
    print(f"\n🎬 MOVIE RECOMMENDATIONS FOR {emotion.upper()}\n")
    for m in movies:
        print(f"➡️ {m['title']} ⭐ {m['rating']}")
        print(m['overview'])
        print("--------------------------------------")

# ------------------ RUN SYSTEM ------------------ #

recommend_movies()
