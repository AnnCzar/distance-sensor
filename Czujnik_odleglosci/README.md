# Projekt Pomiaru Odległości z Arduino

## Przegląd
Projekt polega na stworzeniu aplikacji z interfejsem graficznym (GUI) w Pythonie przy użyciu bibliotek Tkinter i Matplotlib do interakcji z czujnikiem odległości opartym na Arduino. Aplikacja odczytuje na żywo pomiary odległości z czujnika i wizualizuje dane na wykresie. Oferuje różne tryby pomiarowe (ciągły, pojedynczy oraz zakresowy), pozwala użytkownikowi wybrać jednostki pomiaru oraz umożliwia zapis zebranych danych do pliku CSV.

## Składniki:
1. **Interfejs Graficzny (GUI)**:
   - **Połączenie Szeregowe**: Pozwala użytkownikowi na połączenie z płytką Arduino poprzez określony port szeregowy i szybkość transmisji.
   - **Tryby Pomiarowe**: Oferuje opcje ciągłego pomiaru, pojedynczego pomiaru oraz pomiaru w określonym zakresie odległości.
   - **Wybór Jednostek Odległości**: Umożliwia użytkownikowi wybór jednostek: milimetry, centymetry, decymetry oraz metry.
   - **Wykres Odległości**: Dynamiczne wyświetlanie pomiarów odległości na wykresie.
   - **Zapis Pomiarów**: Możliwość zapisu zebranych danych do pliku CSV w celu dalszej analizy lub archiwizacji.
   - **Widgety Wyświetlające**: Wyświetlanie na bieżąco zmierzonej odległości oraz komunikatów ostrzegawczych na podstawie ustawień zakresu pomiarowego.

2. **Kod Pythona (Klasa Sensor)**:
   - Nawiązywanie komunikacji z Arduino poprzez port szeregowy.
   - Implementacja funkcji pomiarowych dla trybów: pojedynczego, ciągłego oraz zakresowego.
   - Konwersja odczytów odległości na wybrane jednostki (mm, cm, dm, m).
   - Dynamiczne tworzenie wykresu z użyciem Matplotlib.
   - Obsługa wątków dla równoczesnych operacji pomiarowych i tworzenia wykresu.
   - Funkcjonalność zapisu zebranych danych do pliku CSV.

3. **Kod Arduino**:
   - Wykorzystanie czujnika ultradźwiękowego do pomiaru odległości.
   - Przesyłanie danych odległości do komputera przez komunikację szeregową.
   - Aktywacja buzzera w celu powiadamiania o obiektach znajdujących się w określonym zakresie odległości.

## Instrukcje Konfiguracji:
1. **Konfiguracja Sprzętowa**:
   - Podłączenie czujnika ultradźwiękowego do płytki Arduino zgodnie z określoną konfiguracją pinów (trigPin i echoPin).
   - Podłączenie buzzera do powiadomień o obiektach w określonym zakresie odległości.

2. **Konfiguracja Oprogramowania**:
   - **Arduino IDE**: Wgranie dostarczonego kodu na płytkę Arduino.
   - **Środowisko Python**: Upewnienie się, że Python jest zainstalowany na komputerze. Instalacja wymaganych bibliotek przy użyciu `pip install tkinter matplotlib pyserial`.

3. **Uruchamianie Aplikacji**:
   - Uruchomienie skryptu Pythona (`sensor_app.py`) w celu uruchomienia aplikacji GUI.
   - Określenie portu szeregowego i szybkości transmisji do połączenia z Arduino.
   - Wybór trybu pomiaru oraz jednostek (mm, cm, dm, m) zgodnie z wymaganiami.
   - Uruchamianie i zatrzymywanie pomiarów oraz obserwacja na bieżąco wyświetlanych danych na wykresie.
   - Zapis zebranych danych do pliku CSV w celu dalszej analizy.

## Uwagi:
- Upewnienie się, że Arduino jest odpowiednio zasilane i podłączone do komputera.
- Dostosowanie kodu Arduino oraz skryptu Pythona do własnych potrzeb.
- Niniejszy plik README zapewnia ogólny przegląd. Szczegółowe komentarze w kodzie wyjaśniają specyficzne funkcjonalności i logikę działania.

## Autor:
- Opracowane przez [Twoje Imię/Nazwisko]
- Kontakt: [Twój Email]

Możesz swobodnie rozbudować ten readme o dodatkowe szczegóły, kroki rozwiązywania problemów lub instrukcje dostosowania do konkretnych wymagań projektowych i użytkowników.
