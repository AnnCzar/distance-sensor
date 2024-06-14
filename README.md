# Projekt Pomiaru Odległości z Arduino

## Autorzy:
- Anna Czarnasiak
- Marta Prucnal
  
## Przegląd
Celem projektu było stworzenie systemu pomiarowego składającego się z płytki Arduino Uno i ultradźwiękowego czujnika odległości. System służy do mierzenia odległości pomiędzy czujnikiem a otaczającymi go przedmiotami. Jest on połączony z komputerem, na którym otrzymywane wyniki są wyświetlane oraz zapisywane do pliku. Na interfejsie graficznym użytkownik ma możliwość  
wyboru sposobu pomiaru: ciągły pomiar, jednorazowy pomiar, pomiar w danym zakresie. Użytkownik może również wybrać w jakiej jednostce ma być przedstawiony wykonany pomiar (mm, cm, dm lub m). Na wykresie prezentowana jest historia pomiarów w zależności odległości od czasu, która jest również zapisywana do pliku csv.  


1. **Interfejs Graficzny (GUI)**:
   - **Możliwość wprowadzenia parametrów portu szeregowego**: Pozwala użytkownikowi na połączenie z płytką Arduino poprzez określony port szeregowy i szybkość transmisji.
   - **Tryby Pomiarowe**: Oferuje opcje ciągłego pomiaru, pojedynczego pomiaru oraz pomiaru w określonym zakresie odległości.
   - **Wybór Jednostek Odległości**: Umożliwia użytkownikowi wybór jednostek: milimetry, centymetry, decymetry oraz metry.
   - **Wykres Odległości**: Dynamiczne wyświetlanie pomiarów odległości na wykresie dla trybu ciągłego i dla danego zakresu.
   - **Zapis Pomiarów**: Możliwość zapisu zebranych danych do pliku CSV w celu dalszej analizy lub archiwizacji -tryb ciągły, tryb zakres.
   - **Widgety Wyświetlające**: Wyświetlanie na bieżąco zmierzonej odległości oraz komunikatów ostrzegawczych na podstawie ustawień zakresu pomiarowego.

2. **Kod Arduino**:
   - Wykorzystanie czujnika ultradźwiękowego do pomiaru odległości.
   - Przesyłanie danych odległości do komputera przez komunikację szeregową.
   - Aktywacja buzzera w celu powiadamiania o obiektach znajdujących się w określonym zakresie odległości.

## Uruchomienie programu:
1. **Konfiguracja Sprzętowa**:
   - Podłączenie czujnika ultradźwiękowego do płytki Arduino zgodnie z określoną konfiguracją pinów (trigPin i echoPin).
   - Podłączenie buzzera do powiadomień o obiektach w określonym zakresie odległości.

2. **Konfiguracja Oprogramowania**:
   - **Arduino IDE**: Wgranie dostarczonego kodu na płytkę Arduino.
   - **Środowisko Python**: Upewnienie się, że Python jest zainstalowany na komputerze. Instalacja wymaganych bibliotek przy użyciu `pip install tkinter matplotlib pyserial`.

3. **Uruchamianie Aplikacji**:
   - Uruchomienie skryptu Pythona (`main.py`) w celu uruchomienia aplikacji GUI.
   - Określenie portu szeregowego i szybkości transmisji do połączenia z Arduino.
   - Wybór trybu pomiaru oraz jednostek (mm, cm, dm, m) zgodnie z wymaganiami.
   - Uruchamianie i zatrzymywanie pomiarów oraz obserwacja na bieżąco wyświetlanych danych na wykresie.
