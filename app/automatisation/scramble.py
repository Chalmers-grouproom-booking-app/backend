import urllib.parse
from typing import Union
from datetime import datetime

# Magic scramble class for TimeEdit
class TimeEditScramble:
    # Initial data setup
    tabledata = [
        ("h=t&sid=", "6="),
        ("objects=", "1="),
        ("sid=", "2="),
        ("&ox=0&types=0&fe=0", "3=3"),
        ("&types=0&fe=0", "5=5"),
        ("&h=t&p=", "4="),
    ]

    tabledataspecial = [
        ("=", "ZZZX1"),
        ("&", "ZZZX2"),
        (",", "ZZZX3"),
        (".", "ZZZX4"),
        (" ", "ZZZX5"),
        ("-", "ZZZX6"),
        ("/", "ZZZX7"),
        ("%", "ZZZX8"),
    ]

    pairs = [
        ("=", "Q"),
        ("&", "Z"),
        (",", "X"),
        (".", "Y"),
        (" ", "V"),
        ("-", "W"),
    ]

    pattern = [4, 22, 5, 37, 26, 17, 33, 15, 39, 11, 45, 20, 2, 40, 19, 36, 28, 38, 30, 41, 44, 42, 7, 24, 14, 27, 35, 25, 12, 1, 43, 23, 6, 16, 3, 9, 47, 46, 48, 50, 21, 10, 49, 32, 18, 31, 29, 34, 13, 8]
    
    # Default data
    urls = [
        "https://cloud.timeedit.net/chalmers/web/b1/ri.json",
    ]
    key_values = [
        "h=t",
        "sid=1004",
        "p=20240411-20240510",
        "objects=192429.186,192430.186,192372.186,214726.186,192373.186,214727.186,221390.186,221391.186,192376.186,221392.186,192431.186,192432.186,192433.186,192434.186,192421.186,192422.186,192381.186,221425.186,192382.186,221426.186,192383.186,221427.186,192384.186,221428.186,192385.186,221429.186,192386.186,221430.186,192387.186,221431.186,192388.186,221432.186,192393.186,221393.186,192394.186,221394.186,205247.186,205248.186,205249.186,205250.186,205251.186,205252.186,205253.186,205254.186,205260.186,205261.186,205262.186,192564.186,192565.186,192566.186,",
        "ox=0",
        "types=0",
        "fe=0",
        "part=t",
        "tg=-1",
        "se=f",
        "exw=t"
    ]
    extra = ""
    def __init__(self, url = None, key_values = None, extra = None):
        if (url is not None):
            self.urls = [url]
        if (key_values is not None):
            self.key_values = key_values
        if (extra is not None):
            self.extra = extra

    def table_short(self, result):
        for key, value in TimeEditScramble.tabledata:
            result = result.replace(key, value)
        return result

    def table_special(self, result):
        for key, value in TimeEditScramble.tabledataspecial:
            result = result.replace(key, value)
        return result

    def mod_key(self, ch):
        if 'a' <= ch <= 'z':
            return chr(97 + ((ord(ch) - 88) % 26))
        if '1' <= ch <= '9':
            return chr(49 + ((ord(ch) - 45) % 9))
        return ch

    def scramble_char(self, ch):
        for pair in TimeEditScramble.pairs:
            if ch == pair[0]:
                return pair[1]
            if ch == pair[1]:
                return pair[0]
        return self.mod_key(ch)

    def swap_pattern(self,chars):
        steps = (len(chars) + max(TimeEditScramble.pattern) - 1) // max(TimeEditScramble.pattern)
        for step in range(steps):
            for index in range(1, len(TimeEditScramble.pattern), 2):
                from_index = TimeEditScramble.pattern[index - 1] + step * len(TimeEditScramble.pattern)
                to_index = TimeEditScramble.pattern[index] + step * len(TimeEditScramble.pattern)
                if from_index < len(chars) and to_index < len(chars):
                    chars[from_index], chars[to_index] = chars[to_index], chars[from_index]

    def swap_char(self, result):
        chars = list(result)
        for index in range(len(chars)):
            chars[index] = self.scramble_char(chars[index])
        self.swap_pattern(chars)
        return ''.join(chars)

    def scramble(self,query):
        if not query or len(query) < 2 or query.startswith('i='):
            return query
        result = urllib.parse.unquote(query)
        result = self.table_short(result)
        result = self.swap_char(result)
        result = self.table_special(result)
        return urllib.parse.quote(result)
    def add_object(self, object_id: str):
        self.key_values[3] += f"{object_id},"
    def edit_all_objects(self, object_ids: list):
        self.key_values[3] = "objects=" + ",".join(object_ids) + ","
    def as_url(self, from_date: Union[str, datetime] = None, to_date: Union[str, datetime] = None):
        # Convert string to datetime, example: "20240411" -> datetime(2024, 4, 11)
        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, "%Y%m%d")
        if isinstance(to_date, str):
            to_date = datetime.strptime(to_date, "%Y%m%d")
        if (from_date is not None and to_date is not None and from_date > to_date):
            self.key_values[2] = f"p={from_date.strftime('%Y%m%d')}-{to_date.strftime('%Y%m%d')}"
        elif (from_date is not None):
            self.key_values[2] = f"p={from_date.strftime('%Y%m%d')}-{from_date.strftime('%Y%m%d')}"
        elif (to_date is not None):
            self.key_values[2] = f"p={to_date.strftime('%Y%m%d')}-{to_date.strftime('%Y%m%d')}"
        else:
            # Todays date
            self.key_values[2] = f"p={datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%Y%m%d')}"

        url = self.urls[0]
        key_values = [str(k).replace('+', ' ') for k in self.key_values]
        last_slash = str(url).rfind("/")
        page = url[last_slash + 1:]

        dot = ".json"  # Default extension
        last_dot = str(url).rfind(".")
        if last_dot != -1:
            dot = url[last_dot:]
            url = url[:last_dot]  # Remove the existing extension before adding scrambled part

        if last_slash != -1:
            url = url[:last_slash + 1]  # Ensure the base path is correctly set

        scrambled = self.scramble("&".join(key_values) + str(self.extra))
        final_url = f"{url}ri{scrambled}{dot}"
        return final_url


if __name__ == "__main__":
    # Test scramble today
    scramble_data = TimeEditScramble()
    print(scramble_data.as_url(datetime.now()))
