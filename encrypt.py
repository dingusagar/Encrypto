import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random



class Encrypto:

    chucksize = 64*1024
    extension = '.encrypted'


    def __init__(self):
        pass

    def getKey(self,password):
        hasher = SHA256.new(password.encode('utf-8'))
        return hasher.digest()

    def encrypt(self,password,filename):
        key = self.getKey(password)
        outputFile = filename+self.extension
        filesize = str(os.path.getsize(filename)).zfill(16)
        IV = Random.new().read(16)
        encrpytor = AES.new(key, AES.MODE_CBC, IV)

        with open(filename,'rb') as infile:
            with open(outputFile,'wb') as outfile:
                outfile.write(filesize.encode('utf-8'))
                outfile.write(IV)

                while True:
                    chuck = infile.read(self.chucksize)

                    if len(chuck) == 0:
                        break
                    elif len(chuck)%16 !=0:
                        chuck += b' ' * (16 - (len(chuck) % 16))

                    outfile.write(encrpytor.encrypt(chuck))

        return outputFile


    def decrypt(self,password,filename):
        key = self.getKey(password)
        outputFile = filename[:len(filename)-len(self.extension)]  

        with open(filename,'rb') as infile:
            filesize = int(infile.read(16))
            IV = infile.read(16)
            decryptor = AES.new(key,AES.MODE_CBC,IV)

            with open(outputFile,'wb') as outfile:
                while True:
                    chuck = infile.read(self.chucksize)
                    if len(chuck) == 0:
                        break
                    outfile.write(decryptor.decrypt(chuck))
                
                outfile.truncate(filesize)
        return outputFile
    
    


def Main():
	compression_ratio = 1
	encrypto = Encrypto()
	choice = input('Press E for Encrpytion & D for Decryption  : ')
	if choice == 'E':
	    filename = input("Filename ? ")
	    password = input("Password ? ")

	    
	    encrypto.encrypt(password,filename+".zip")

	    print("Encrypting..")
	elif choice == 'D':
	    filename = input("Filename ? ")
	    password = input("Password ? ")
	    decryptedFileName = encrypto.decrypt(password,filename)

	    print("Decrypting..")
	else:
	    print("Invalid Choice ..closing")

if __name__ == '__main__':
    Main()
