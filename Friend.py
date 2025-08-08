from Birthday import Birthday

class Friend:
    def __init__(self, first_name, last_name):
        """A person/friend is defined by a first and last name, a birthday in the
        form (month, day), and a city they live in. Additional fields may
        be added here later. A new object requires only a first and last
        name to instantiate. The remaining fields can be set later using
        the corresponding mutator methods."""
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = None
        self.email_address = None
        self.nickname = None
        self.street_address = None
        self.city = None
        self.state = None
        self.zip = None
        self.phone = None

    # simple way for a friend object to introduce itself
    def introduce(self):
        msg = f"Hello, my name is {self.first_name}"
        if self.birthday:
            msg += f" and my birthday is on {self.birthday_str()}"
        print(msg)

    # Mutator for birthday. Uses our very own Birthday class.
    def set_birthday(self, month, day):
        self.birthday = Birthday(month, day)

    # Mutator for city.
    def set_city(self, city):
        self.city = city

    # Accessor for first name
    def get_first_name(self):
        return self.first_name

    # Accessor for last name
    def get_last_name(self):
        return self.last_name

    # Small helper to format a conversational date like '29th of June'
    # (I reused the ordinal-suffix trick from week08).
    def birthday_str(self) -> str:
        if not self.birthday:
            return "unknown"
        day = self.birthday.get_day()
        if 11 <= day % 100 <= 13:
            suffix = "th"
        elif day % 10 == 1:
            suffix = "st"
        elif day % 10 == 2:
            suffix = "nd"
        elif day % 10 == 3:
            suffix = "rd"
        else:
            suffix = "th"
        month_names = [
            None, "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return f"{day}{suffix} of {month_names[self.birthday.get_month()]}"

    # Convenience for printing lists/labels
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # --- CSV helpers (kept simple; no extra imports) ---
    # Order: first,last,email,phone,street,city,state,zip,month,day
    def to_csv_line(self) -> str:
        m = self.birthday.get_month() if self.birthday else ""
        d = self.birthday.get_day() if self.birthday else ""
        fields = [
            self.first_name or "",
            self.last_name or "",
            self.email_address or "",
            self.phone or "",
            self.street_address or "",
            self.city or "",
            self.state or "",
            self.zip or "",
            str(m),
            str(d),
        ]
        # quick note to self: replace commas inside fields so CSV stays simple
        return ",".join(x.replace(",", " ") for x in fields)

    @staticmethod
    def from_csv_line(line: str):
        parts = [p.strip() for p in line.strip().split(",")]
        # pad if shorter than expected
        parts += [""] * (10 - len(parts))
        first, last, email, phone, street, city, state, zip_code, m, d = parts[:10]
        fr = Friend(first, last)
        fr.email_address = email or None
        fr.phone = phone or None
        fr.street_address = street or None
        fr.city = city or None
        fr.state = state or None
        fr.zip = zip_code or None
        if m and d:
            try:
                fr.birthday = Birthday(int(m), int(d))
            except:
                fr.birthday = None
        return fr

    def __str__(self):
        """String representation for the object"""
        return f"[ {self.full_name()} ]"
