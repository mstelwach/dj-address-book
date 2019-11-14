echo
echo "Witaj!"
echo
echo "Ten skrypt pozwoli na skonfigurowanie aplikacji przed jej pierwszym uruchomieniem."
echo "Baza danych zostanie odpowiednio skonfigurowana."
echo "W tym czasie na ekranie pojawi się wiele komunikatów"
echo "ABY INSTALACJA POWIODŁA SIĘ MUSISZ MIEĆ DOSTĘP DO INTERNETU"
read -n1 -r -p "Naciśnij dowolny klawisz, by kontynuować."

echo
echo "Tworzę nowe środowisko"
virtualenv -p python3 venv

echo "Instaluję niezbędne narzędzia do uruchomienia aplikacji"
source ./venv/bin/activate
pip3 install -r requirements.txt

echo "Pierwsza migracja tabeli do bazy danych"
python manage.py makemigrations
python manage.py migrate

echo "Tworzymy konto, niech będzie z prawami administracyjnymi"
python manage.py createsuperuser

echo "Dostarczamy początkowe dane dla modeli"
python manage.py loaddata db.json

echo "Super, czas na uruchomienie aplikacji! Pamiętaj o rejestracji :)"
python manage.py runserver
