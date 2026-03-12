"""
Profession themes configuration for KDP Notebook Generator.
Each theme defines visual identity: colors, icons, taglines, and content.
"""

# Colors as RGB tuples (0-255)
THEMES = {
    "budowlaniec": {
        "name_pl": "Budowlaniec",
        "name_en": "Construction Worker",
        "emoji": "🏗️",
        "tagline": "Notatnik Prawdziwego Budowlańca",
        "subtitle": "Plany, obliczenia i pomysły na budowie",
        "primary": (255, 140, 0),        # Orange
        "secondary": (50, 50, 50),        # Dark gray
        "accent": (255, 215, 0),          # Yellow
        "bg_light": (255, 248, 235),
        "text_dark": (30, 20, 10),
        "icon_color": (200, 100, 0),
        "cover_bg": (40, 30, 20),
        "pattern": "bricks",
        "thematic_pages": [
            {
                "title": "Dzienne Zadania Budowlane",
                "fields": ["Data:", "Budynek/Projekt:", "Brygada:", "Zadanie dnia:", "Materiały potrzebne:", "Uwagi bezpieczeństwa:", "Postęp prac (%):", "Problemy do rozwiązania:"],
                "icon": "hardhat"
            },
            {
                "title": "Pomiary i Obliczenia",
                "fields": ["Projekt:", "Sekcja:", "Długość:", "Szerokość:", "Wysokość:", "Powierzchnia (m²):", "Objętość (m³):", "Ilość materiału:", "Uwagi:"],
                "icon": "ruler"
            },
            {
                "title": "Lista Kontrolna BHP",
                "checks": ["Kask ochronny założony", "Obuwie ochronne", "Kamizelka odblaskowa", "Rękawice robocze", "Okularki ochronne (jeśli wymagane)", "Zabezpieczenie strefy roboczej", "Apteczka pierwszej pomocy dostępna", "Gaśnica na miejscu", "Plac chroniony przed osobami postronnymi", "Sprzęt sprawdzony przed użyciem"],
                "icon": "checklist"
            },
            {
                "title": "Harmonogram Prac",
                "type": "schedule",
                "slots": ["Poniedziałek:", "Wtorek:", "Środa:", "Czwartek:", "Piątek:", "Sobota:", "Suma godzin tygodniowo:"],
                "icon": "calendar"
            },
            {
                "title": "Kontakty na Budowie",
                "fields": ["Kierownik budowy:", "Tel.:", "Majster:", "Tel.:", "Inspektor nadzoru:", "Tel.:", "Brygadzista:", "Tel.:", "Pogotowie (112):", "Straż pożarna (998):"],
                "icon": "phone"
            }
        ]
    },

    "informatyk": {
        "name_pl": "Informatyk",
        "name_en": "IT Professional",
        "emoji": "💻",
        "tagline": "Notatnik Programisty",
        "subtitle": "Kod, algorytmy i rozwiązania",
        "primary": (0, 120, 215),         # Blue
        "secondary": (20, 20, 40),        # Dark navy
        "accent": (0, 255, 136),          # Green terminal
        "bg_light": (235, 245, 255),
        "text_dark": (10, 10, 30),
        "icon_color": (0, 90, 180),
        "cover_bg": (15, 15, 35),
        "pattern": "circuit",
        "thematic_pages": [
            {
                "title": "Bug Tracker / Issue Log",
                "fields": ["Data:", "Projekt:", "Issue ID:", "Opis błędu:", "Kroki reprodukcji:", "Oczekiwane zachowanie:", "Rzeczywiste zachowanie:", "Środowisko:", "Priorytet: □ Critical  □ High  □ Medium  □ Low", "Status: □ Open  □ In Progress  □ Resolved"],
                "icon": "bug"
            },
            {
                "title": "Sprint Planning",
                "fields": ["Sprint #:", "Daty: ___ – ___", "Cel sprintu:", "Story Points dostępne:", "Zadania do wykonania:"],
                "type": "sprint",
                "tasks": 8,
                "icon": "sprint"
            },
            {
                "title": "Architektura Systemu",
                "type": "diagram_space",
                "description": "Miejsce na diagram architektury / schemat bazy danych / przepływ danych",
                "labels": ["Komponent:", "Technologia:", "Wersja:", "Zależności:", "Notatki API:"],
                "icon": "architecture"
            },
            {
                "title": "Code Review Checklist",
                "checks": ["Kod działa zgodnie ze specyfikacją", "Testy jednostkowe napisane", "Dokumentacja zaktualizowana", "Brak hardcodowanych wartości", "Obsługa błędów zaimplementowana", "Bezpieczeństwo sprawdzone (SQL injection, XSS)", "Wydajność zoptymalizowana", "Nazwy zmiennych czytelne", "SOLID principles zachowane", "Code review ukończone"],
                "icon": "checklist"
            },
            {
                "title": "Meeting Notes / Stand-up",
                "fields": ["Data:", "Projekt:", "Uczestnicy:", "Co zrobiłem wczoraj:", "Co robię dzisiaj:", "Blokery:", "Decyzje podjęte:", "Następne kroki:", "Następne spotkanie:"],
                "icon": "meeting"
            }
        ]
    },

    "lekarz": {
        "name_pl": "Lekarz",
        "name_en": "Doctor / Medical",
        "emoji": "⚕️",
        "tagline": "Notatnik Medyczny",
        "subtitle": "Obserwacje kliniczne i wiedza medyczna",
        "primary": (0, 150, 136),         # Teal
        "secondary": (255, 255, 255),
        "accent": (220, 50, 50),          # Medical red
        "bg_light": (240, 255, 253),
        "text_dark": (10, 40, 35),
        "icon_color": (0, 120, 100),
        "cover_bg": (10, 60, 55),
        "pattern": "medical",
        "thematic_pages": [
            {
                "title": "Obserwacja Pacjenta",
                "fields": ["Data/Godzina:", "Pacjent (inicjały):", "Wiek:", "Główna dolegliwość:", "Wywiad:", "Badanie fizykalne:", "Ciśnienie:", "Tętno:", "Temperatura:", "SpO2:", "Rozpoznanie (ICD-10):", "Plan postępowania:"],
                "icon": "stethoscope"
            },
            {
                "title": "Dyżur – Notatki",
                "fields": ["Data dyżuru:", "Oddział:", "Liczba pacjentów:", "Przyjęcia:", "Wypisy:", "Konsultacje:", "Zabiegi/Procedury:", "Incydenty:", "Przekazanie dyżuru:"],
                "icon": "hospital"
            },
            {
                "title": "Notatki z Konferencji / Szkolenia",
                "fields": ["Temat:", "Prelegent:", "Data:", "Kluczowe informacje:", "Nowe badania/Guidelines:", "Do wdrożenia w praktyce:", "Literatura do przeczytania:"],
                "icon": "book"
            },
            {
                "title": "Skale i Kalkulatory Medyczne",
                "type": "reference",
                "content": [
                    "GLASGOW COMA SCALE",
                    "Otwieranie oczu: Spontanicznie=4, Na głos=3, Na ból=2, Brak=1",
                    "Odpowiedź słowna: Orientacja=5, Splątanie=4, Słowa=3, Dźwięki=2, Brak=1",
                    "Odpowiedź ruchowa: Wykonuje polecenia=6, Lokalizuje ból=5,",
                    "  Cofa kończynę=4, Zgięcie=3, Wyprost=2, Brak=1",
                    "",
                    "WELLS SCORE (DVT): ≥3 wysokie, 1-2 umiarkowane, ≤0 niskie",
                    "CURB-65: 0-1 leczenie ambulatoryjne, 2 hospitalizacja,",
                    "  ≥3 OIT",
                ],
                "icon": "calculator"
            },
            {
                "title": "Samokształcenie – Przypadek Kliniczny",
                "fields": ["Przypadek:", "Prezentacja:", "Diagnostyka różnicowa:", "Wykonane badania:", "Rozpoznanie ostateczne:", "Leczenie:", "Wynik:", "Wnioski i nauka:"],
                "icon": "case"
            }
        ]
    },

    "nauczyciel": {
        "name_pl": "Nauczyciel",
        "name_en": "Teacher",
        "emoji": "📚",
        "tagline": "Notatnik Nauczyciela",
        "subtitle": "Plany lekcji, uwagi i inspiracje",
        "primary": (156, 39, 176),        # Purple
        "secondary": (245, 240, 250),
        "accent": (255, 193, 7),          # Amber
        "bg_light": (252, 245, 255),
        "text_dark": (40, 10, 50),
        "icon_color": (120, 20, 150),
        "cover_bg": (50, 15, 65),
        "pattern": "books",
        "thematic_pages": [
            {
                "title": "Plan Lekcji",
                "fields": ["Data:", "Klasa:", "Przedmiot:", "Temat lekcji:", "Cel główny:", "Cele operacyjne:", "Metody nauczania:", "Pomoce dydaktyczne:", "Czas: 45 min", "Faza wstępna (5 min):", "Faza główna (30 min):", "Faza końcowa (10 min):", "Praca domowa:", "Oceny:"],
                "icon": "lesson"
            },
            {
                "title": "Rejestr Ocen – Klasa",
                "type": "grade_table",
                "description": "Tabela ocen uczniów",
                "icon": "grades"
            },
            {
                "title": "Obserwacje Ucznia",
                "fields": ["Uczeń:", "Klasa:", "Data:", "Mocne strony:", "Obszary do poprawy:", "Zachowanie:", "Frekwencja:", "Kontakt z rodzicami:", "Notatki:"],
                "icon": "student"
            },
            {
                "title": "Zebranie z Rodzicami",
                "fields": ["Data:", "Klasa:", "Temat zebrania:", "Frekwencja:", "Omówione tematy:", "Pytania od rodziców:", "Odpowiedzi:", "Ustalenia:", "Następne zebranie:"],
                "icon": "meeting"
            },
            {
                "title": "Pomysły na Lekcję / Projekty",
                "type": "ideas",
                "fields": ["Inspiracja:", "Temat projektu:", "Klasa:", "Czas realizacji:", "Potrzebne materiały:", "Powiązanie z programem:", "Sposób oceny:", "Uwagi:"],
                "icon": "idea"
            }
        ]
    },

    "kucharz": {
        "name_pl": "Kucharz",
        "name_en": "Chef / Cook",
        "emoji": "👨‍🍳",
        "tagline": "Notatnik Szefa Kuchni",
        "subtitle": "Przepisy, menu i sekrety kulinarne",
        "primary": (198, 40, 40),         # Red
        "secondary": (255, 245, 235),
        "accent": (255, 160, 0),          # Orange
        "bg_light": (255, 250, 245),
        "text_dark": (50, 20, 10),
        "icon_color": (160, 30, 30),
        "cover_bg": (60, 20, 15),
        "pattern": "kitchen",
        "thematic_pages": [
            {
                "title": "Przepis Kulinarny",
                "fields": ["Nazwa dania:", "Kuchnia:", "Porcje:", "Czas przygotowania:", "Czas gotowania:", "Poziom trudności:", "Składniki:", "", "", "", "Przygotowanie:", "Wskazówki serwowania:", "Parowanie z winem:"],
                "icon": "recipe"
            },
            {
                "title": "Menu Tygodniowe",
                "type": "weekly_menu",
                "days": ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"],
                "meals": ["Śniadanie", "Lunch", "Obiad", "Kolacja"],
                "icon": "menu"
            },
            {
                "title": "Lista Zakupów – Magazyn",
                "fields": ["Data:", "Dostawca:", "Kategoria:"],
                "type": "shopping",
                "categories": ["MIĘSO/RYBY", "WARZYWA/OWOCE", "NABIAŁ", "SUCHE/PRZYPRAWY", "INNE"],
                "icon": "shopping"
            },
            {
                "title": "Kalkulacja Kosztu Dania",
                "fields": ["Danie:", "Składnik | Ilość | Koszt jednostkowy | Koszt łączny", "", "", "", "", "Suma składników:", "Koszt pracy (%):", "Marża (%):", "Cena sprzedaży:", "Food Cost (%):"],
                "icon": "calculator"
            },
            {
                "title": "Notatki Degustacyjne",
                "fields": ["Danie:", "Data degustacji:", "Oceniający:", "Wygląd (1-10):", "Aromat (1-10):", "Smak (1-10):", "Tekstura (1-10):", "Ogólna ocena (1-10):", "Co zmienić:", "Co zachować:"],
                "icon": "tasting"
            }
        ]
    },

    "sportowiec": {
        "name_pl": "Sportowiec",
        "name_en": "Athlete",
        "emoji": "🏋️",
        "tagline": "Notatnik Sportowca",
        "subtitle": "Treningi, wyniki i cele sportowe",
        "primary": (0, 188, 212),         # Cyan
        "secondary": (20, 20, 30),
        "accent": (255, 82, 82),          # Red energy
        "bg_light": (240, 255, 255),
        "text_dark": (10, 30, 40),
        "icon_color": (0, 150, 170),
        "cover_bg": (10, 20, 35),
        "pattern": "geometric",
        "thematic_pages": [
            {
                "title": "Dziennik Treningowy",
                "fields": ["Data:", "Rodzaj treningu:", "Czas trwania:", "Intensywność (1-10):", "Tętno spoczynkowe:", "Tętno max:", "Ćwiczenia:"],
                "type": "workout",
                "exercise_rows": 8,
                "icon": "workout"
            },
            {
                "title": "Śledzenie Celów",
                "fields": ["Cel główny:", "Deadline:", "Cel pośredni 1:", "Deadline:", "Cel pośredni 2:", "Deadline:", "Moje motywacje:", "Przeszkody do pokonania:", "Plan działania:"],
                "icon": "goal"
            },
            {
                "title": "Pomiary i Postęp Ciała",
                "type": "measurements",
                "fields": ["Data:", "Waga (kg):", "Tkanka tłuszczowa (%):", "Masa mięśniowa (kg):", "Klatka (cm):", "Talia (cm):", "Biodra (cm):", "Biceps L/P (cm):", "Udo L/P (cm):", "Łydka L/P (cm):", "Uwagi:"],
                "icon": "body"
            },
            {
                "title": "Odżywianie – Dziennik Diety",
                "fields": ["Data:", "Cel kaloryczny:", "Białko (g):", "Tłuszcze (g):", "Węglowodany (g):", "Śniadanie:", "II śniadanie:", "Obiad:", "Kolacja:", "Przekąski:", "Suma kalorii:", "Nawodnienie (L):"],
                "icon": "nutrition"
            },
            {
                "title": "Regeneracja i Sen",
                "fields": ["Data:", "Godziny snu:", "Jakość snu (1-10):", "HRV:", "Samopoczucie ogólne (1-10):", "Ból mięśni (lokalizacja):", "Stretching/Foam rolling:", "Masaż:", "Sauna/Zimny prysznic:", "Suplementacja:", "Uwagi:"],
                "icon": "recovery"
            }
        ]
    },

    "prawnik": {
        "name_pl": "Prawnik",
        "name_en": "Lawyer",
        "emoji": "⚖️",
        "tagline": "Notatnik Prawnika",
        "subtitle": "Sprawy, dokumenty i analizy prawne",
        "primary": (62, 39, 35),          # Dark brown
        "secondary": (245, 240, 230),
        "accent": (212, 175, 55),         # Gold
        "bg_light": (253, 250, 242),
        "text_dark": (30, 20, 10),
        "icon_color": (100, 70, 30),
        "cover_bg": (25, 15, 8),
        "pattern": "legal",
        "thematic_pages": [
            {
                "title": "Karta Sprawy",
                "fields": ["Sygnatura akt:", "Klient:", "Rodzaj sprawy:", "Strony:", "Sąd/Organ:", "Data wpłynięcia:", "Termin przedawnienia:", "Pełnomocnik przeciwny:", "Status:", "Uwagi:"],
                "icon": "case"
            },
            {
                "title": "Notatki z Rozprawy",
                "fields": ["Data:", "Sygnatura:", "Sąd:", "Sędzia:", "Strony obecne:", "Przebieg posiedzenia:", "Wnioski dowodowe:", "Decyzje sądu:", "Termin następny:", "Do przygotowania:"],
                "icon": "court"
            },
            {
                "title": "Analiza Prawna",
                "fields": ["Zagadnienie:", "Stan faktyczny:", "Podstawa prawna:", "Art.:", "Orzecznictwo:", "Doktryna:", "Analiza:", "Wniosek:", "Rekomendacja:"],
                "icon": "analysis"
            },
            {
                "title": "Kontrola Terminów",
                "type": "deadline_tracker",
                "fields": ["Sprawa | Czynność | Termin | Status | Uwagi"],
                "rows": 10,
                "icon": "calendar"
            },
            {
                "title": "Konsultacja z Klientem",
                "fields": ["Data:", "Klient:", "Temat:", "Stan faktyczny wg klienta:", "Dokumenty dostarczone:", "Pytania klienta:", "Udzielone porady:", "Ustalony plan działania:", "Honorarium:", "Następna wizyta:"],
                "icon": "client"
            }
        ]
    },

    "ogrodnik": {
        "name_pl": "Ogrodnik",
        "name_en": "Gardener",
        "emoji": "🌱",
        "tagline": "Notatnik Ogrodnika",
        "subtitle": "Sadzenie, pielęgnacja i plony",
        "primary": (56, 142, 60),         # Green
        "secondary": (255, 253, 245),
        "accent": (255, 160, 0),          # Amber harvest
        "bg_light": (245, 255, 245),
        "text_dark": (15, 40, 15),
        "icon_color": (40, 110, 45),
        "cover_bg": (20, 50, 20),
        "pattern": "leaves",
        "thematic_pages": [
            {
                "title": "Dziennik Ogrodnika",
                "fields": ["Data:", "Pogoda:", "Temperatura min/max:", "Opady:", "Prace wykonane:", "Strefa ogrodu:", "Posadzone/Zasiane:", "Podlane:", "Nawożone (czym?):", "Opryski (czym/dlaczego?):", "Obserwacje chorób/szkodników:", "Plony zebrane:"],
                "icon": "garden"
            },
            {
                "title": "Harmonogram Siewu i Sadzenia",
                "type": "planting_calendar",
                "months": ["Sty", "Lut", "Mar", "Kwi", "Maj", "Cze", "Lip", "Sie", "Wrz", "Paź", "Lis", "Gru"],
                "icon": "calendar"
            },
            {
                "title": "Karta Rośliny",
                "fields": ["Nazwa (polska):", "Nazwa (łacińska):", "Rodzina:", "Stanowisko (słońce/cień):", "Gleba:", "Podlewanie:", "Nawożenie:", "Wymagana przestrzeń:", "Termin siewu:", "Termin sadzenia:", "Zbiory:", "Uwagi pielęgnacyjne:"],
                "icon": "plant"
            },
            {
                "title": "Plan Ogrodu – Strefy",
                "type": "garden_plan",
                "description": "Szkic planu ogrodu z oznaczeniem stref",
                "labels": ["Strefa A:", "Strefa B:", "Strefa C:", "Strefa D:", "Kompostownik:", "Szklarnia:", "Ścieżki:"],
                "icon": "map"
            },
            {
                "title": "Zbiory i Przechowywanie",
                "fields": ["Produkt:", "Data zbioru:", "Ilość (kg):", "Jakość (1-5):", "Metoda przechowywania:", "Miejsce:", "Termin ważności:", "Przeznaczenie:", "Notatki:"],
                "icon": "harvest"
            }
        ]
    },

    "muzyk": {
        "name_pl": "Muzyk",
        "name_en": "Musician",
        "emoji": "🎵",
        "tagline": "Notatnik Muzyka",
        "subtitle": "Kompozycje, akordy i inspiracje muzyczne",
        "primary": (63, 81, 181),         # Indigo
        "secondary": (250, 250, 255),
        "accent": (233, 30, 99),          # Pink
        "bg_light": (248, 248, 255),
        "text_dark": (20, 15, 50),
        "icon_color": (50, 60, 160),
        "cover_bg": (20, 15, 55),
        "pattern": "music",
        "thematic_pages": [
            {
                "title": "Notatki Kompozytorskie",
                "fields": ["Tytuł utworu:", "Gatunek:", "Tonacja:", "Tempo (BPM):", "Metrum:", "Nastrój/Charakter:", "Inspiracja:", "Struktura (intro/zwrotka/chorus):", "Tekst/Motyw:", "Instrumentacja:", "Postęp akordów:"],
                "icon": "compose"
            },
            {
                "title": "Karta Ćwiczeniowa",
                "fields": ["Data:", "Instrument:", "Czas ćwiczenia:", "Rozgrzewka (min):", "Ćwiczone elementy techniczne:", "Repertuar:", "Najtrudniejsze fragmenty:", "Postęp:", "Plan na następną sesję:"],
                "icon": "practice"
            },
            {
                "title": "Pięciolinia – Notatki Muzyczne",
                "type": "staff_lines",
                "staves": 6,
                "description": "Miejsce na zapis nutowy / tabulaturę gitarową",
                "icon": "staff"
            },
            {
                "title": "Setlista / Program Koncertu",
                "fields": ["Koncert:", "Miejsce:", "Data:", "Czas trwania:"],
                "type": "setlist",
                "rows": 15,
                "icon": "setlist"
            },
            {
                "title": "Notatki z Prób",
                "fields": ["Data próby:", "Miejsce:", "Skład:", "Ćwiczone utwory:", "Co poszło dobrze:", "Co wymaga poprawy:", "Techniczne problemy:", "Plan na kolejną próbę:", "Następna próba (data/miejsce):"],
                "icon": "rehearsal"
            }
        ]
    },

    "strazak": {
        "name_pl": "Strażak",
        "name_en": "Firefighter",
        "emoji": "🔥",
        "tagline": "Notatnik Strażaka",
        "subtitle": "Interwencje, szkolenia i bezpieczeństwo",
        "primary": (211, 47, 47),         # Fire red
        "secondary": (30, 30, 30),
        "accent": (255, 193, 7),          # Yellow warning
        "bg_light": (255, 245, 245),
        "text_dark": (40, 10, 10),
        "icon_color": (180, 30, 30),
        "cover_bg": (35, 10, 10),
        "pattern": "flame",
        "thematic_pages": [
            {
                "title": "Raport z Interwencji",
                "fields": ["Nr zdarzenia:", "Data/Godzina alarmowania:", "Godzina przyjazdu:", "Adres zdarzenia:", "Rodzaj zdarzenia:", "Siły i środki:", "Dowódca akcji:", "Opis działań:", "Osoby poszkodowane:", "Straty materialne:", "Godzina zakończenia:", "Wnioski:"],
                "icon": "incident"
            },
            {
                "title": "Przegląd Sprzętu",
                "checks": ["Autopompa – sprawność silnika", "Zabudowa – zbiornik wody (pełny)", "Węże – brak uszkodzeń", "Prądownice – komplet", "Agregat prądotwórczy", "Aparaty powietrzne – ciśnienie OK", "Ubrania bojowe – komplet", "Apteczka – kompletna", "Łączność – radiotelefony naładowane", "GPS/Nawigacja"],
                "icon": "checklist"
            },
            {
                "title": "Notatki ze Szkolenia",
                "fields": ["Temat szkolenia:", "Prowadzący:", "Data:", "Miejsce:", "Uczestnicy:", "Zakres szkolenia:", "Nowe techniki/procedury:", "Ćwiczenia praktyczne:", "Wnioski:", "Następne szkolenie:"],
                "icon": "training"
            },
            {
                "title": "Dyżur – Harmonogram",
                "type": "shift",
                "fields": ["Data dyżuru:", "Zmiana (24h):", "Dowódca:", "Skład:", "Zdarzenia:", "Ćwiczenia:", "Przeglądy:", "Uwagi:"],
                "icon": "shift"
            },
            {
                "title": "Inspekcja Przeciwpożarowa",
                "fields": ["Obiekt:", "Adres:", "Data inspekcji:", "Inspektor:", "Drogi ewakuacyjne:", "Oznakowanie:", "Sprzęt gaśniczy:", "Instalacje ppoż:", "Stwierdzone uchybienia:", "Zalecenia:", "Termin usunięcia:", "Wynik inspekcji:"],
                "icon": "inspection"
            }
        ]
    }
}

# KDP notebook specifications
KDP_SPECS = {
    "trim_width": 6.0,      # inches
    "trim_height": 9.0,     # inches
    "bleed": 0.125,         # inches on each side
    "margin_inner": 0.5,    # inches (spine side)
    "margin_outer": 0.375,  # inches
    "margin_top": 0.5,      # inches
    "margin_bottom": 0.5,   # inches
    "total_pages": 120,     # content pages (must be even)
    "thematic_pages_count": 5,
    "lined_pages_count": 115,
    "dpi": 300,
    "line_spacing": 0.3,    # inches between lines
}

PROFESSION_ORDER = [
    "budowlaniec",
    "informatyk",
    "lekarz",
    "nauczyciel",
    "kucharz",
    "sportowiec",
    "prawnik",
    "ogrodnik",
    "muzyk",
    "strazak",
]
