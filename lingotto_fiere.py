class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = prezzo_base
        self.disponibile = True
        self.espositore = None

    def prezzo_finale(self):
        return self.prezzo_base

    def tipo(self):
        return "Standard"

    def extra(self):
        return ""

    def __eq__(self, other):
        return isinstance(other, Stand) and self.codice == other.codice

    def __hash__(self):
        return hash(self.codice)

    def __lt__(self, other):
        return self.prezzo_finale() < other.prezzo_finale()

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Non disponibile"
        return (f"{self.codice}: {self.tipo()} | {self.superficie} mq - "
                f"Padiglione: {self.padiglione} - Prezzo {self.prezzo_finale():.2f}€"
                f"{self.extra()} - {stato}")

    __repr__ = __str__

class StandPrese(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese_extra = prese_extra

    def prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 * self.prese_extra)

    def tipo(self):
        return "Prese Extra"

    def extra(self):
        return f" - Prese extra: {self.prese_extra}"

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def prezzo_finale(self):
        return self.prezzo_base * 1.30

    def tipo(self):
        return "Premium"

    def extra(self):
        return f" - Posizione: {self.posizione}"

class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        return isinstance(other, Espositore) and self.codice == other.codice

    def __hash__(self):
        return hash(self.codice)

    def __str__(self):
        base = f"{self.codice}: {self.nome} {self.cognome}"
        if self.stand is not None:
            base += f" - Stand assegnato: {self.stand.codice}"
        return base

    __repr__ = __str__

class LingottoFiere:
    def __init__(self, nome):
        self._nome = nome
        self.stand = []
        self.espositori = []

    def get_nome(self):
        return self._nome

    def set_nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        self.stand = []
        self.espositori = []

        with open(file_path, "r", encoding="utf-8") as f:
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue
                campi = [c.strip() for c in riga.split(",")]
                while campi and campi[-1] == "":
                    campi.pop()
                codice = campi[0]

                if codice.startswith("ST"):
                    superficie = int(campi[1])
                    padiglione = int(campi[2])
                    prezzo = float(campi[3])
                    if len(campi) == 4:
                        s = Stand(codice, superficie, padiglione, prezzo)
                    else:
                        extra = campi[4]
                        if extra.isdigit():
                            s = StandPrese(codice, superficie, padiglione, prezzo, int(extra))
                        else:
                            s = StandPremium(codice, superficie, padiglione, prezzo, extra)
                    self.stand.append(s)

                elif codice.startswith("ES"):
                    self.espositori.append(Espositore(codice, campi[1], campi[2]))

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        stand = None
        for s in self.stand:
            if s.codice == codice_stand:
                stand = s
                break
        if stand is None:
            raise ValueError(f"Stand {codice_stand} non trovato.")

        espositore = None
        for e in self.espositori:
            if e.codice == codice_espositore:
                espositore = e
                break
        if espositore is None:
            raise ValueError(f"Espositore {codice_espositore} non trovato.")

        if not stand.disponibile:
            raise ValueError(f"Stand {codice_stand} non disponibile.")
        if espositore.stand is not None:
            raise ValueError(f"Espositore {codice_espositore} ha già uno stand.")

        stand.disponibile = False
        stand.espositore = espositore
        espositore.stand = stand

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for e in self.espositori:
            print(e)

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand)


