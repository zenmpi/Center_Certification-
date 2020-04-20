import zipfile #подключаем модуль
zname=r'cert.rar'
name = 'skypework1234@gmail.com'
newzip = zipfile.ZipFile(zname, 'w')
newzip.write('{}.pfx'.format(name))
newzip.setpassword(b'1')
newzip.close() #закрываем архив