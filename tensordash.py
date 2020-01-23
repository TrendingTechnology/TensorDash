from firebase.firebase import FirebaseApplication
import requests
import json
import keras

class FirebaseError(Exception):
    pass

class SendDataToFirebase(object):

    def __init__(self, key = None):

        try:

            firebase = FirebaseApplication('https://cofeeshop-tensorflow.firebaseio.com/')

        except:

            raise FirebaseError("Could Not connect to firebase")

    def sendMessage(self, key = None, params = None, ModelName = 'Sample Model'):

        epoch, loss, acc, val_loss, val_acc, status = params

        firebase = FirebaseApplication('https://cofeeshop-tensorflow.firebaseio.com/')

        result = firebase.put(key, '{}/Epoch {}'.format(ModelName, epoch + 1) , {'Epoch': epoch+1, 'Loss' : loss, 'Accuracy' : acc, 'Validation Loss': val_loss, 'Validation Accuracy' : val_acc, 'Model Status' : status})


#result = firebase.put(sample_key, 'model/Epoch {}'.format(epoch) , {'Loss' : 0.2, 'Accuracy' : 0.70})

SendData = SendDataToFirebase()


class Tensordash(keras.callbacks.Callback):

    def __init__(self, email = 'None', password = 'None',  ModelName = 'Sample_model'):

        
        self.ModelName = ModelName
        self.email = email
        self.password = password
    
    def on_train_begin(self, logs = {}):

        self.losses = []
        self.accuracy = []
        self.val_losses = []
        self.val_accuracy = []
        self.num_epochs = []

        headers = {'Content-Type': 'application/json',}

        params = (('key', 'AIzaSyDU4zqFpa92Jf64nYdgzT8u2oJfENn-2f8'),)

        val = {
            "email" : self.email,
            "password": self.password,
            "returnSecureToken": "false"
        }

        data = str(val)

        response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword', headers=headers, params=params, data=data)

        #response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=[AIzaSyDU4zqFpa92Jf64nYdgzT8u2oJfENn-2f8]', headers=headers, data=data)

        output = response.json()

        self.key = output['localId']


    def on_epoch_end(self, epoch, logs = {}):

        self.losses.append(logs.get('loss'))
        self.accuracy.append(logs.get('accuracy'))
        self.val_losses.append(logs.get('val_loss'))
        self.val_accuracy.append(logs.get('val_accuracy'))
        self.num_epochs.append(epoch)

        
        self.loss = float("{0:.6f}".format(self.losses[-1]))

        if self.accuracy[-1] == None:
            self.acc = "Not Specified"
        else:
            self.acc = float("{0:.6f}".format(self.accuracy[-1]))

        if self.val_losses[-1] == None:
            self.val_loss = "Not Specified"
        else:
            self.val_loss = float("{0:.6f}".format(self.val_losses[-1]))

        if self.val_accuracy[-1] == None:
            self.val_acc = "Not Specified"
        else:
            self.val_acc = float("{0:.6f}".format(self.val_accuracy[-1]))
    
        values = [epoch, self.loss, self.acc, self.val_loss, self.val_acc, 'Running']

        SendData.sendMessage(key = self.key, params = values, ModelName = self.ModelName)

    def on_train_end(self, epoch, logs = {}):

        epoch = self.num_epochs[-1]

        self.loss = float("{0:.6f}".format(self.losses[-1]))

        if self.accuracy[-1] == None:
                self.acc = "Not Specified"
        else:

            self.acc = float("{0:.6f}".format(self.accuracy[-1]))

        if self.val_losses[-1] == None:
                self.val_loss = "Not Specified"
        else:

            self.val_loss = float("{0:.6f}".format(self.val_losses[-1]))

        if self.val_accuracy[-1] == None:
                self.val_acc = "Not Specified"
        else:

            self.val_acc = float("{0:.6f}".format(self.val_accuracy[-1]))

        values = [epoch, self.loss, self.acc, self.val_loss, self.val_acc, 'Running']

    #    print(values)

        SendData.sendMessage(key = self.key, params = values, ModelName = self.ModelName)