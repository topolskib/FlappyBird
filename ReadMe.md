FlappyBird

===============================

Repozytorium zawiera dwa foldery z różnymi wersjami gry FlappyBird - z podziałem na wersję online/offline.
Wersja online zapisuje wyniki na serwerze, co pozwala na emocjonującą rywalizację z graczami z całego świata!
Wersja offline nie ma tej możliwości, za to możemy w niej resetować wyniki.

Zawartość każdego z folderów:
 * folder `sounds` - zawiera pliki dźwiękowe,
 * folder `graphics` - zawiera pliki graficzne - postać gracza, oraz tło i przeszkody,
 * folder `cyfry` - zawiera pliki graficzne zawierające cyfry 0-9,
 * folder `resources` - zawiera najlepsze wyniki,
 * folder `source` - zawiera plik z kodem źródłowym danej wersji,
 * aplikację uruchamiającą grę - w wersji na Linuxa i Windowsa.

Uwaga - do uruchomienia gry poprzez aplikację nie potrzebujemy zainstalowanego pythona - wszystkie potrzebne biblioteki są wewnątrz pliku. Pozwala to na dotarcie do większej liczby graczy. Jeśli chcemy uruchomić grę bezpośrednio z pliku źródłowego, musimy najpierw przekopiować go poziom wyżej, tzn do głównego katalogu z daną wersją gry, aby umożliwić dostęp do folderów z danymi. Potrzebny jest także moduł pyglet.
Niestety aplikacje nie działają pod wszystkimi platformami - niektóre dystrybucje linuxa nie współpracują, jak i z rzadka niektóre Windowsy. 
Zasady gry:

Celem gracza jest utrzymywanie tytułowego ptaka w locie. Nie może on spaść na ziemię, wylecieć poza górną krawędź ekranu, ani uderzyć w przeszkodę. 

Sterowanie:

Jedynym potrzebnym klawiszem jest spacja - za jej pomocą skaczemy do góry. Ponadto, jeśli nie chcemy odrywać rąk od klawiatury, możemy rozpocząć nową grę klawiszem `N`.
Po rozpoczęciu gry ptak leci poziomo, i czeka na pierwszy podskok. Wtedy zaczynają się pojawiać przeszkody.

Wyjaśnienie dostępnych opcji:

Poziom trudności - poziom trudności. Oprócz 4 przygotowanych z góry poziomów, możemy także sami dostosować parametry - to automatycznie przełączy poziom trudności na `Niezdefiniowany`. 

Dźwięki - włącza lub wyłącza efekty dźwiękowe.

Czas między przeszkodami - określa czas, jaki mija między pojawianiem się kolejnych przeszkód. Oczywiście im większy, tym łatwiej - mamy wiecej czasu na dostosowanie wysokości do poziomu kolejnej przeszkody.

Modyfikator zasięgu przeszkód - zwiększenie jego wartości zmniejsza zakres możliwych wysokości przeszkód. Innymi słowy, im większy modyfikator, tym bliżej środka będą pojawiały się przeszkody, co ułatwia rozgrywkę.

Ruchome przeszkody - włącza lub wyłącza ruch przeszkód. Przeszkody ruszają się w górę i w dół.

Prędkość ruchu przeszkód - zmienia prędkość ruchu przeszkód. Aktywny tylko, jeśli poprzednia opcja została zaznaczona.

Ustawienia graficzne - pozwalają na zmianę ustawień graficznych. Opcja działa poprawnie tylko pod Linuxem, pod Windowsem liczniki zaczynają mierzyć czas innym tempem, i wszystko jest spowolnione.

Have Fun!


