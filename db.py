import firebase_admin
from firebase_admin import credentials, firestore

path_to_key = "dora-556f1-firebase-adminsdk-4ujwi-bfddc6bd09.json"

cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = 'users'


def create_user(id_user):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc_ref.set({"id": id_user})


def check_user(id_user):
    collection_ref = db.collection('users')
    document_ref = collection_ref.document(str(id_user))
    document = document_ref.get()
    return document.exists


def check_avatar(id_user):
    collection_ref = db.collection('users')
    document_ref = collection_ref.document(str(id_user))
    document = document_ref.get().to_dict()
    return 'characteristic_avatar' in document.keys()


def type_avatar(id_user, characteristic):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc_ref.update({"characteristic_avatar": characteristic})


def get_type_avatar(id_user):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc = doc_ref.get().to_dict()
    return doc["characteristic_avatar"]


def add_text(id_user, text_user, text_bot):
    doc_ref = db.collection(collection_name).document(str(id_user))
    doc = doc_ref.get()
    dict_db = doc.to_dict()
    num = 0
    while len(dict_db) > 12:
        if "text_" + str(num) + "u" in dict_db:
            del dict_db["text_" + str(num) + "u"]
            del dict_db["text_" + str(num) + "b"]
        num += 1
    doc_ref.set(dict_db)
    num_field = len(doc.to_dict()) // 2 - 1
    if num_field < 0:
        num_field = 0
    doc_ref.update({"text_" + str(num_field) + 'u': text_user, "text_" + str(num_field) + 'b': text_bot})


def get_inf(id_user):
    history = db.collection(collection_name).document(str(id_user)).get().to_dict()
    history.pop('id', None)
    character = history['characteristic_avatar']
    history.pop('characteristic_avatar', None)
    messages = ''
    for value in history.values():
        messages += value
    return messages, character, len(history)
