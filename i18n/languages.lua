-- STEMwerk Internationalization (i18n)
-- Language files for EN/NL/DE

local LANGUAGES = {
    en = {
        -- General
        help = "Help",
        close = "Close",
        back = "Back",
        cancel = "Cancel",
        yes = "Yes",
        no = "No",

        -- Start screen
        select_audio = "Select audio in REAPER",
        select_audio_tooltip = "Select tracks, media items, or make a time selection",
        help_tooltip = "View Help & Art Gallery (F1)",
        exit_tooltip = "Exit STEMwerk",

        -- Main dialog
        presets = "Presets:",
        stems = "Stems (1-4):",
        stems_6 = "Stems (1-6):",
        model = "Model:",
        output = "Output:",
        after = "After:",
        selected = "Selected:",
        target = "Location:",

        -- Footer info (main dialog)
        footer_track = "track",
        footer_tracks = "tracks",
        footer_item = "item",
        footer_items = "items",
        footer_take = "take",
        footer_takes = "takes",
        footer_time_selection = "time selection",
        footer_location_new_folder = "New folder with stem tracks",
        footer_location_new_tracks = "New tracks below source",
        footer_location_in_place = "In-place (as %d takes on source tracks)",

        -- Stems
        vocals = "Vocals",
        drums = "Drums",
        bass = "Bass",
        other = "Other",
        guitar = "Guitar",
        piano = "Piano",

        -- Presets
        karaoke = "Karaoke",
        all_stems = "All",
        instrumental = "Instrumental",

        -- Output options
        new_tracks = "New tracks",
        new_track = "New track",
        in_place = "In-place",
        keep_takes = "Keep takes",
        explode_to_new_tracks = "Explode → tracks",
        explode_in_place = "Explode in-place",
        explode_in_order = "Explode in-order",
        create_folder = "Folder",
        mute_original = "Mute orig",
        delete_original = "Delete orig",
        delete_track = "Del track",
        mute_selection = "Mute sel",
        delete_selection = "Del sel",

        -- Processing
        parallel = "Parallel",
        sequential = "Sequential",
        processing = "Processing...",
        starting = "Starting...",
        cancelled = "Cancelled",
        timeout = "Timeout",
        elapsed = "Elapsed:",

        -- Tooltips
        switch_dark = "Switch to dark mode",
        switch_light = "Switch to light mode",
        tooltip_quick_settings = "Quick settings",
        click_to_stemperate = "Click to STEMwerk",
        double_click_reset = "Double-click to reset",
        tooltip_change_language = "Click to change language",
        tooltip_logo_help = "Click for help - Select tracks/items, choose stems, click STEMwerk!",
        tooltip_new_tracks = "Create separate tracks for each stem",
        tooltip_in_place = "Replace original with stems as takes",
        tooltip_keep_takes = "Keep stems as takes on one item",
        tooltip_explode_to_new_tracks = "After processing, explode takes to new tracks",
        tooltip_explode_in_place = "After processing, explode takes to separate items on the same track",
        tooltip_explode_in_order = "After processing, lay out takes sequentially in time",
        tooltip_create_folder = "Group stem tracks in a track folder",
        tooltip_mute_original = "Mute original items after separation",
        tooltip_delete_original = "Delete original items after separation",
        tooltip_delete_track = "Delete original tracks after separation",
        tooltip_mute_selection = "Mute only the time selection part",
        tooltip_delete_selection = "Delete only the time selection part",
        tooltip_close = "Close STEMwerk (ESC)",
        tooltip_parallel = "Process multiple tracks simultaneously (uses more GPU memory)",
        tooltip_sequential = "Process tracks one at a time (slower but uses less memory)",

        -- Quick settings menu
        menu_dark_mode = "Dark mode",
        menu_visual_fx = "Visual FX",
        menu_tooltips = "Tooltips",

        -- Model descriptions
        model_fast_desc = "htdemucs - Fastest model, good quality (4 stems)",
        model_quality_desc = "htdemucs_ft - Best quality, slower (4 stems)",
        model_6stem_desc = "htdemucs_6s - Adds Guitar & Piano separation",

        -- Preset tooltips
        tooltip_preset_karaoke = "Everything except vocals",
        tooltip_preset_all = "Select all available stems",
        tooltip_preset_vocals = "Select only Vocals stem",
        tooltip_preset_drums = "Select only Drums stem",
        tooltip_preset_bass = "Select only Bass stem",
        tooltip_preset_other = "Select only Other stem",
        tooltip_preset_piano = "Select only Piano stem",
        tooltip_preset_guitar = "Select only Guitar stem",

        -- Stem content tooltips
        tooltip_stem_vocals = "Voice, lead vocals, backing vocals",
        tooltip_stem_drums = "Drums, percussion, cymbals",
        tooltip_stem_bass = "Bass guitar, synth bass",
        tooltip_stem_other = "Synths, strings, keys, effects",
        tooltip_stem_guitar = "Electric and acoustic guitars",
        tooltip_stem_piano = "Piano, keys, Rhodes",

        -- Messages
        no_stems_selected = "No Stems Selected",
        please_select_stem = "Please select at least one stem.",
        separation_cancelled = "Separation cancelled.",
        separation_timeout = "Separation timed out after 10 minutes.",

        -- Help hints
        hint_keys = "Enter / Space / ESC",
        hint_monitor = "F1 = Help | ESC = Close",
        hint_nav = "< > Navigate | Scroll to zoom | Right-drag to pan | ESC to close",
        hint_cancel = "Press ESC or close window to cancel",
        click_new_art = "Click for new art",

        -- Help tabs
        help_welcome = "Welcome",
        help_quickstart = "Quick Start",
        help_stems = "Stems",
        help_gallery = "Gallery",
        help_about = "About",
        help_gallery_hint = "< > Navigate | Scroll to zoom | ESC to close",

        -- About tab
        about_title = "About STEMwerk",
        about_subtitle = "AI-Powered Stem Separation for REAPER",
        about_version = "Version",
        about_author = "Created with",
        about_claude = "Claude AI",
        about_powered_by = "Powered by",
        about_demucs = "Meta's Demucs",
        about_conceived = "Conceived by",
        about_features_title = "Features",
        about_feature_1 = "4 or 6 stem separation (Vocals, Drums, Bass, Other, Guitar, Piano)",
        about_feature_2 = "Multiple quality modes (Fast, Quality, 6-Stem)",
        about_feature_3 = "In-place or new tracks output",
        about_feature_4 = "Multi-track parallel processing",
        about_feature_5 = "Beautiful procedural art animations",
        about_shortcuts_title = "Keyboard Shortcuts",
        about_tip = "Tip: Press R to reset camera, Space for new art",

        -- Welcome tab
        help_welcome_title = "Welcome to STEMwerk",
        help_welcome_sub = "AI-powered stem separation for REAPER",
        help_feature_vocals = "Extract vocals for remixes or karaoke",
        help_feature_drums = "Isolate drums for sampling or practice",
        help_feature_bass = "Separate bass for mixing or transcription",
        help_feature_other = "Get other instruments cleanly",

        -- Quick Start tab
        help_quickstart_title = "Getting Started",
        help_quickstart_sub = "Follow these simple steps to separate your audio",
        help_step1_title = "Select Audio",
        help_step1_desc = "Select tracks, items, or make a time selection",
        help_step1_detail = "Select one or more tracks, or media items, or make a time/loop selection",
        help_step2_title = "Choose Model & Stems",
        help_step2_desc = "Pick a preset or select individual stems",
        help_step2_detail = "Choose Karaoke (vocals only), All Stems (4 tracks), or select individual stems",
        help_step3_title = "Click STEMwerk",
        help_step3_desc = "Wait for AI to separate your audio",
        help_step3_detail = "Click the STEMwerk button and watch the AI work its magic!",
        help_pro_tip = "Pro Tip: Use the 6-stem model (htdemucs_6s) for guitar and piano separation!",
        tips_hints = "Tips",
        open_help = "Open Help",
        close_cancel = "Close / Cancel",
        start_stemwerk = "Start STEMwerk",

        -- mouse_options removed (not shown)

        -- Stems tab
        help_stems_title = "About Stems",
        help_stems_sub = "Understanding what each stem contains",
        help_stem_vocals_desc = "Lead vocals, backing vocals, speech",
        help_stem_drums_desc = "Kick, snare, hi-hats, cymbals, percussion",
        help_stem_bass_desc = "Bass guitar, synth bass, low frequencies",
        help_stem_other_desc = "Guitar, keys, strings, synths, effects",
        help_stem_vocals_uses = "Perfect for karaoke, vocal isolation, remix, or studying vocal techniques",
        help_stem_drums_uses = "Great for drummers, sampling, practice tracks, or groove analysis",
        help_stem_bass_uses = "Ideal for bass transcription, low-end mixing, or learning bass lines",
        help_stem_other_uses = "Captures everything else: guitars, keys, strings, synths, pads, effects",
        help_6stem_title = "6-Stem Model (htdemucs_6s)",
        help_6stem_desc = "Adds Guitar and Piano as separate stems for even more control!",

        -- Stem names for help
        stem_vocals = "Vocals",
        stem_drums = "Drums",
        stem_bass = "Bass",
        stem_other = "Other",
        stem_guitar = "Guitar",
        stem_piano = "Piano",

        -- FX toggle
        fx_enable = "Enable visual effects",
        fx_disable = "Disable visual effects",
    },

    nl = {
        -- General
        help = "Help",
        close = "Sluiten",
        back = "Terug",
        cancel = "Annuleren",
        yes = "Ja",
        no = "Nee",

        -- Start screen
        select_audio = "Selecteer audio in REAPER",
        select_audio_tooltip = "Selecteer tracks, media-items of maak een tijdselectie",
        help_tooltip = "Bekijk Help & Art Gallery (F1)",
        exit_tooltip = "Sluit STEMwerk",

        -- Main dialog
        presets = "Presets:",
        stems = "Stems (1-4):",
        stems_6 = "Stems (1-6):",
        model = "Model:",
        output = "Uitvoer:",
        after = "Daarna:",
        selected = "Geselecteerd:",
        target = "Locatie:",

        -- Footer info (main dialog)
        footer_track = "track",
        footer_tracks = "tracks",
        footer_item = "item",
        footer_items = "items",
        footer_take = "take",
        footer_takes = "takes",
        footer_time_selection = "tijdselectie",
        footer_location_new_folder = "Nieuwe folder met stem tracks",
        footer_location_new_tracks = "Nieuwe tracks onder bron",
        footer_location_in_place = "In-place (als %d takes op brontracks)",

        -- Stems
        vocals = "Zang",
        drums = "Drums",
        bass = "Bas",
        other = "Overig",
        guitar = "Gitaar",
        piano = "Piano",

        -- Presets
        karaoke = "Karaoke",
        all_stems = "Alles",
        instrumental = "Instrumentaal",

        -- Output options
        new_tracks = "Nieuwe tracks",
        new_track = "Nieuwe track",
        in_place = "Op plek",
        keep_takes = "Takes houden",
        explode_to_new_tracks = "Explodeer → tracks",
        explode_in_place = "Explodeer op plek",
        explode_in_order = "Explodeer op volgorde",
        create_folder = "Map",
        mute_original = "Mute orig",
        delete_original = "Wis orig",
        delete_track = "Wis track",
        mute_selection = "Mute sel",
        delete_selection = "Wis sel",

        -- Processing
        parallel = "Parallel",
        sequential = "Sequentieel",
        processing = "Verwerken...",
        starting = "Starten...",
        cancelled = "Geannuleerd",
        timeout = "Time-out",
        elapsed = "Verstreken:",

        -- Tooltips
        switch_dark = "Schakel naar donkere modus",
        switch_light = "Schakel naar lichte modus",
        tooltip_quick_settings = "Snelle instellingen",
        click_to_stemperate = "Klik om STEMwerk te starten",
        double_click_reset = "Dubbelklik om te resetten",
        tooltip_change_language = "Klik om taal te wijzigen",
        tooltip_logo_help = "Klik voor help - Selecteer tracks/items, kies stems, klik STEMwerk!",
        tooltip_new_tracks = "Maak aparte tracks voor elke stem",
        tooltip_in_place = "Vervang origineel met stems als takes",
        tooltip_keep_takes = "Houd stems als takes op één item",
        tooltip_explode_to_new_tracks = "Na verwerking: explodeer takes naar nieuwe tracks",
        tooltip_explode_in_place = "Na verwerking: explodeer takes naar losse items op dezelfde track",
        tooltip_explode_in_order = "Na verwerking: plaats takes achter elkaar in de tijd",
        tooltip_create_folder = "Groepeer stem tracks in een folder track",
        tooltip_mute_original = "Mute originele items na separatie",
        tooltip_delete_original = "Verwijder originele items na separatie",
        tooltip_delete_track = "Verwijder originele tracks na separatie",
        tooltip_mute_selection = "Mute alleen het tijdselectie deel",
        tooltip_delete_selection = "Verwijder alleen het tijdselectie deel",
        tooltip_close = "Sluit STEMwerk (ESC)",
        tooltip_parallel = "Verwerk meerdere tracks tegelijk (gebruikt meer GPU geheugen)",
        tooltip_sequential = "Verwerk tracks een voor een (langzamer maar minder geheugen)",

        -- Quick settings menu
        menu_dark_mode = "Donkere modus",
        menu_visual_fx = "Visuele FX",
        menu_tooltips = "Tooltips",

        -- Model descriptions
        model_fast_desc = "htdemucs - Snelste model, goede kwaliteit (4 stems)",
        model_quality_desc = "htdemucs_ft - Beste kwaliteit, langzamer (4 stems)",
        model_6stem_desc = "htdemucs_6s - Voegt Gitaar & Piano separatie toe",

        -- Preset tooltips
        tooltip_preset_karaoke = "Alles behalve zang",
        tooltip_preset_all = "Selecteer alle beschikbare stems",
        tooltip_preset_vocals = "Selecteer alleen Zang stem",
        tooltip_preset_drums = "Selecteer alleen Drums stem",
        tooltip_preset_bass = "Selecteer alleen Bas stem",
        tooltip_preset_other = "Selecteer alleen Overig stem",
        tooltip_preset_piano = "Selecteer alleen Piano stem",
        tooltip_preset_guitar = "Selecteer alleen Gitaar stem",

        -- Stem content tooltips
        tooltip_stem_vocals = "Stem, leadzang, achtergrondzang",
        tooltip_stem_drums = "Drums, percussie, bekkens",
        tooltip_stem_bass = "Basgitaar, synthbas",
        tooltip_stem_other = "Synths, strijkers, keys, effecten",
        tooltip_stem_guitar = "Elektrische en akoestische gitaren",
        tooltip_stem_piano = "Piano, keys, Rhodes",

        -- Messages
        no_stems_selected = "Geen stems geselecteerd",
        please_select_stem = "Selecteer minimaal een stem.",
        separation_cancelled = "Separatie geannuleerd.",
        separation_timeout = "Separatie time-out na 10 minuten.",

        -- Help hints
        hint_keys = "Enter / Spatie / ESC",
        hint_monitor = "F1 = Help | ESC = Sluiten",
        hint_nav = "< > Navigeer | Scroll om te zoomen | Rechts-slepen om te pannen | ESC om te sluiten",
        hint_cancel = "Druk ESC of sluit venster om te annuleren",
        click_new_art = "Klik voor nieuwe kunst",

        -- Help tabs
        help_welcome = "Welkom",
        help_quickstart = "Snel Starten",
        help_stems = "Stems",
        help_gallery = "Galerie",
        help_about = "Over",
        help_gallery_hint = "< > Navigeer | Scroll om te zoomen | ESC om te sluiten",

        -- About tab
        about_title = "Over STEMwerk",
        about_subtitle = "AI-Gestuurde Stem Separatie voor REAPER",
        about_version = "Versie",
        about_author = "Gemaakt met",
        about_claude = "Claude AI",
        about_powered_by = "Aangedreven door",
        about_demucs = "Meta's Demucs",
        about_conceived = "Bedacht door",
        about_features_title = "Functies",
        about_feature_1 = "4 of 6 stem separatie (Vocals, Drums, Bass, Other, Guitar, Piano)",
        about_feature_2 = "Meerdere kwaliteitsmodi (Fast, Quality, 6-Stem)",
        about_feature_3 = "In-place of nieuwe tracks output",
        about_feature_4 = "Multi-track parallelle verwerking",
        about_feature_5 = "Prachtige procedurele kunst animaties",
        about_shortcuts_title = "Sneltoetsen",
        about_tip = "Tip: Druk R om camera te resetten, Spatie voor nieuwe kunst",

        -- Welcome tab
        help_welcome_title = "Welkom bij STEMwerk",
        help_welcome_sub = "AI-gestuurde stem-separatie voor REAPER",
        help_feature_vocals = "Haal zang eruit voor remixes of karaoke",
        help_feature_drums = "Isoleer drums voor sampling of oefenen",
        help_feature_bass = "Separeer bas voor mixen of transcriptie",
        help_feature_other = "Krijg andere instrumenten schoon",

        -- Quick Start tab
        help_quickstart_title = "Aan de Slag",
        help_quickstart_sub = "Volg deze simpele stappen om je audio te scheiden",
        help_step1_title = "Selecteer Audio",
        help_step1_desc = "Selecteer tracks, items of maak een tijdselectie",
        help_step1_detail = "Selecteer een of meer tracks, media-items, of maak een tijd/loop selectie",
        help_step2_title = "Kies Model & Stems",
        help_step2_desc = "Kies een preset of selecteer losse stems",
        help_step2_detail = "Kies Karaoke (alleen zang), Alle Stems (4 tracks), of selecteer losse stems",
        help_step3_title = "Klik STEMwerk",
        help_step3_desc = "Wacht tot AI je audio separeert",
        help_step3_detail = "Klik op de STEMwerk knop en kijk hoe de AI zijn magie doet!",
        help_pro_tip = "Pro Tip: Gebruik het 6-stem model (htdemucs_6s) voor gitaar en piano separatie!",
        keyboard_shortcuts = "Sneltoetsen:",
        open_help = "Open Help",
        close_cancel = "Sluiten / Annuleren",
        start_stemwerk = "Start STEMwerk",

        -- Stems tab
        help_stems_title = "Over Stems",
        help_stems_sub = "Wat elke stem bevat",
        help_stem_vocals_desc = "Leadzang, achtergrondzang, spraak",
        help_stem_drums_desc = "Kick, snare, hi-hats, bekkens, percussie",
        help_stem_bass_desc = "Basgitaar, synthbas, lage frequenties",
        help_stem_other_desc = "Gitaar, keys, strijkers, synths, effecten",
        help_stem_vocals_uses = "Perfect voor karaoke, zang isolatie, remix, of zangtechnieken studeren",
        help_stem_drums_uses = "Geweldig voor drummers, sampling, oefentracks, of groove analyse",
        help_stem_bass_uses = "Ideaal voor bas transcriptie, low-end mixen, of baslijnen leren",
        help_stem_other_uses = "Vangt al het andere: gitaren, keys, strijkers, synths, pads, effecten",
        help_6stem_title = "6-Stem Model (htdemucs_6s)",
        help_6stem_desc = "Voegt Gitaar en Piano toe als aparte stems voor nog meer controle!",

        -- Stem names for help
        stem_vocals = "Zang",
        stem_drums = "Drums",
        stem_bass = "Bas",
        stem_other = "Overig",
        stem_guitar = "Gitaar",
        stem_piano = "Piano",

        -- FX toggle
        fx_enable = "Visuele effecten inschakelen",
        fx_disable = "Visuele effecten uitschakelen",
    },

    de = {
        -- General
        help = "Hilfe",
        close = "Schliessen",
        back = "Zurueck",
        cancel = "Abbrechen",
        yes = "Ja",
        no = "Nein",

        -- Start screen
        select_audio = "Audio in REAPER auswaehlen",
        select_audio_tooltip = "Tracks, Medien-Items oder Zeitauswahl waehlen",
        help_tooltip = "Hilfe & Art Gallery anzeigen (F1)",
        exit_tooltip = "STEMwerk beenden",

        -- Main dialog
        presets = "Presets:",
        stems = "Stems (1-4):",
        stems_6 = "Stems (1-6):",
        model = "Modell:",
        output = "Ausgabe:",
        after = "Danach:",
        selected = "Ausgewaehlt:",
        target = "Ort:",

        -- Footer info (main dialog)
        footer_track = "Track",
        footer_tracks = "Tracks",
        footer_item = "Item",
        footer_items = "Items",
        footer_take = "Take",
        footer_takes = "Takes",
        footer_time_selection = "Zeitauswahl",
        footer_location_new_folder = "Neuer Ordner mit Stem-Tracks",
        footer_location_new_tracks = "Neue Tracks unter Quelle",
        footer_location_in_place = "In-place (als %d Takes auf Quell-Tracks)",

        -- Stems
        vocals = "Gesang",
        drums = "Schlagzeug",
        bass = "Bass",
        other = "Sonstige",
        guitar = "Gitarre",
        piano = "Klavier",

        -- Presets
        karaoke = "Karaoke",
        all_stems = "Alle",
        instrumental = "Instrumental",

        -- Output options
        new_tracks = "Neue Tracks",
        new_track = "Neuer Track",
        in_place = "An Ort",
        keep_takes = "Takes behalten",
        explode_to_new_tracks = "Explode → Tracks",
        explode_in_place = "Explode an Ort",
        explode_in_order = "Explode in Reihenfolge",
        create_folder = "Ordner",
        mute_original = "Mute orig",
        delete_original = "Loesch orig",
        delete_track = "Loesch Trk",
        mute_selection = "Mute sel",
        delete_selection = "Loesch sel",

        -- Processing
        parallel = "Parallel",
        sequential = "Sequentiell",
        processing = "Verarbeitung...",
        starting = "Starten...",
        cancelled = "Abgebrochen",
        timeout = "Zeitueberschreitung",
        elapsed = "Vergangen:",

        -- Tooltips
        switch_dark = "Zum Dunkelmodus wechseln",
        switch_light = "Zum Hellmodus wechseln",
        tooltip_quick_settings = "Schnelle Einstellungen",
        click_to_stemperate = "Klicken zum STEMwerk",
        double_click_reset = "Doppelklick zum Zuruecksetzen",
        tooltip_change_language = "Klicken um Sprache zu aendern",
        tooltip_logo_help = "Klicken fuer Hilfe - Tracks/Items waehlen, Stems waehlen, STEMwerk klicken!",
        tooltip_new_tracks = "Separate Tracks fuer jeden Stem erstellen",
        tooltip_in_place = "Original durch Stems als Takes ersetzen",
        tooltip_keep_takes = "Stems als Takes auf einem Item behalten",
        tooltip_explode_to_new_tracks = "Nach der Verarbeitung: Takes in neue Tracks explodieren",
        tooltip_explode_in_place = "Nach der Verarbeitung: Takes in einzelne Items auf derselben Spur explodieren",
        tooltip_explode_in_order = "Nach der Verarbeitung: Takes nacheinander in der Zeit anordnen",
        tooltip_create_folder = "Stem Tracks in einem Ordner gruppieren",
        tooltip_mute_original = "Originale Items nach Trennung stumm schalten",
        tooltip_delete_original = "Originale Items nach Trennung loeschen",
        tooltip_delete_track = "Originale Tracks nach Trennung loeschen",
        tooltip_mute_selection = "Nur den Zeitauswahl-Teil stumm schalten",
        tooltip_delete_selection = "Nur den Zeitauswahl-Teil loeschen",
        tooltip_close = "STEMwerk schliessen (ESC)",
        tooltip_parallel = "Mehrere Tracks gleichzeitig verarbeiten (braucht mehr GPU Speicher)",
        tooltip_sequential = "Tracks einzeln verarbeiten (langsamer aber weniger Speicher)",

        -- Quick settings menu
        menu_dark_mode = "Dunkelmodus",
        menu_visual_fx = "Visuelle FX",
        menu_tooltips = "Tooltips",

        -- Model descriptions
        model_fast_desc = "htdemucs - Schnellstes Modell, gute Qualitaet (4 Stems)",
        model_quality_desc = "htdemucs_ft - Beste Qualitaet, langsamer (4 Stems)",
        model_6stem_desc = "htdemucs_6s - Fuegt Gitarre & Klavier Trennung hinzu",

        -- Preset tooltips
        tooltip_preset_karaoke = "Alles ausser Gesang",
        tooltip_preset_all = "Alle verfuegbaren Stems auswaehlen",
        tooltip_preset_vocals = "Nur Gesang Stem auswaehlen",
        tooltip_preset_drums = "Nur Schlagzeug Stem auswaehlen",
        tooltip_preset_bass = "Nur Bass Stem auswaehlen",
        tooltip_preset_other = "Nur Sonstige Stem auswaehlen",
        tooltip_preset_piano = "Nur Klavier Stem auswaehlen",
        tooltip_preset_guitar = "Nur Gitarre Stem auswaehlen",

        -- Stem content tooltips
        tooltip_stem_vocals = "Stimme, Hauptgesang, Hintergrundgesang",
        tooltip_stem_drums = "Schlagzeug, Perkussion, Becken",
        tooltip_stem_bass = "Bassgitarre, Synthbass",
        tooltip_stem_other = "Synths, Streicher, Keys, Effekte",
        tooltip_stem_guitar = "Elektrische und akustische Gitarren",
        tooltip_stem_piano = "Klavier, Keys, Rhodes",

        -- Messages
        no_stems_selected = "Keine Stems ausgewaehlt",
        please_select_stem = "Bitte mindestens einen Stem auswaehlen.",
        separation_cancelled = "Trennung abgebrochen.",
        separation_timeout = "Trennung nach 10 Minuten abgebrochen.",

        -- Help hints
        hint_keys = "Enter / Leertaste / ESC",
        hint_monitor = "F1 = Hilfe | ESC = Schliessen",
        hint_nav = "< > Navigieren | Scrollen zum Zoomen | Rechts ziehen zum Schwenken | ESC zum Schliessen",
        hint_cancel = "ESC druecken oder Fenster schliessen zum Abbrechen",
        click_new_art = "Klicken fuer neue Kunst",

        -- Help tabs
        help_welcome = "Willkommen",
        help_quickstart = "Schnellstart",
        help_stems = "Stems",
        help_gallery = "Galerie",
        help_about = "Info",
        help_gallery_hint = "< > Navigieren | Scrollen zum Zoomen | ESC zum Schliessen",

        -- About tab
        about_title = "Ueber STEMwerk",
        about_subtitle = "KI-Gesteuerte Stem-Trennung fuer REAPER",
        about_version = "Version",
        about_author = "Erstellt mit",
        about_claude = "Claude AI",
        about_powered_by = "Angetrieben von",
        about_demucs = "Meta's Demucs",
        about_conceived = "Konzipiert von",
        about_features_title = "Funktionen",
        about_feature_1 = "4 oder 6 Stem Trennung (Vocals, Drums, Bass, Other, Guitar, Piano)",
        about_feature_2 = "Mehrere Qualitaetsmodi (Fast, Quality, 6-Stem)",
        about_feature_3 = "In-place oder neue Tracks Ausgabe",
        about_feature_4 = "Multi-Track parallele Verarbeitung",
        about_feature_5 = "Wunderschoene prozedurale Kunst Animationen",
        about_shortcuts_title = "Tastaturkuerzel",
        about_tip = "Tipp: Druecke R zum Kamera-Reset, Leertaste fuer neue Kunst",

        -- Welcome tab
        help_welcome_title = "Willkommen bei STEMwerk",
        help_welcome_sub = "KI-gesteuerte Stem-Trennung fuer REAPER",
        help_feature_vocals = "Gesang fuer Remixes oder Karaoke extrahieren",
        help_feature_drums = "Schlagzeug zum Samplen oder Ueben isolieren",
        help_feature_bass = "Bass zum Mischen oder Transkribieren trennen",
        help_feature_other = "Andere Instrumente sauber erhalten",

        -- Quick Start tab
        help_quickstart_title = "Erste Schritte",
        help_quickstart_sub = "Folgen Sie diesen einfachen Schritten um Ihr Audio zu trennen",
        help_step1_title = "Audio auswaehlen",
        help_step1_desc = "Tracks, Items oder Zeitauswahl waehlen",
        help_step1_detail = "Waehlen Sie einen oder mehrere Tracks, Media-Items, oder machen Sie eine Zeit/Loop-Auswahl",
        help_step2_title = "Modell & Stems waehlen",
        help_step2_desc = "Preset waehlen oder einzelne Stems auswaehlen",
        help_step2_detail = "Waehlen Sie Karaoke (nur Gesang), Alle Stems (4 Tracks), oder einzelne Stems",
        help_step3_title = "STEMwerk klicken",
        help_step3_desc = "Warten bis KI Ihr Audio trennt",
        help_step3_detail = "Klicken Sie auf STEMwerk und schauen Sie zu wie die KI ihre Magie wirkt!",
        help_pro_tip = "Pro Tipp: Nutzen Sie das 6-Stem Modell (htdemucs_6s) fuer Gitarre und Klavier Trennung!",
        keyboard_shortcuts = "Tastaturkuerzel:",
        open_help = "Hilfe oeffnen",
        close_cancel = "Schliessen / Abbrechen",
        start_stemwerk = "STEMwerk starten",

        -- Stems tab
        help_stems_title = "Ueber Stems",
        help_stems_sub = "Was jeder Stem enthaelt",
        help_stem_vocals_desc = "Hauptgesang, Hintergrundgesang, Sprache",
        help_stem_drums_desc = "Kick, Snare, Hi-Hats, Becken, Perkussion",
        help_stem_bass_desc = "Bassgitarre, Synthbass, tiefe Frequenzen",
        help_stem_other_desc = "Gitarre, Keys, Streicher, Synths, Effekte",
        help_stem_vocals_uses = "Perfekt fuer Karaoke, Gesangsisolierung, Remix, oder Gesangstechniken studieren",
        help_stem_drums_uses = "Toll fuer Schlagzeuger, Sampling, Uebungstracks, oder Groove-Analyse",
        help_stem_bass_uses = "Ideal fuer Bass-Transkription, Low-End Mischen, oder Basslinien lernen",
        help_stem_other_uses = "Erfasst alles andere: Gitarren, Keys, Streicher, Synths, Pads, Effekte",
        help_6stem_title = "6-Stem Modell (htdemucs_6s)",
        help_6stem_desc = "Fuegt Gitarre und Klavier als separate Stems hinzu fuer noch mehr Kontrolle!",

        -- Stem names for help
        stem_vocals = "Gesang",
        stem_drums = "Schlagzeug",
        stem_bass = "Bass",
        stem_other = "Sonstige",
        stem_guitar = "Gitarre",
        stem_piano = "Klavier",

        -- FX toggle
        fx_enable = "Visuelle Effekte aktivieren",
        fx_disable = "Visuelle Effekte deaktivieren",
    },
}

return LANGUAGES
