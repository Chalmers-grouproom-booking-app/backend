import urllib.parse
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
        "objects=192429.186,192430.186,192372.186,214726.186,192373.186,214727.186,221390.186,221391.186,192376.186,221392.186,192431.186,192432.186,192433.186,192434.186,192421.186,192422.186,192381.186,221425.186,192382.186,221426.186,192383.186,221427.186,192384.186,221428.186,192385.186,221429.186,192386.186,221430.186,192387.186,221431.186,192388.186,221432.186,192393.186,221393.186,192394.186,221394.186,205247.186,205248.186,205249.186,205250.186,205251.186,205252.186,205253.186,205254.186,205260.186,205261.186,205262.186,192564.186,192565.186,192566.186,192567.186,192493.186,192526.186,192527.186,206066.186,206067.186,192528.186,192529.186,206064.186,192530.186,192531.186,204726.186,204727.186,204728.186,204729.186,204730.186,204722.186,204723.186,204724.186,204725.186,204678.186,204721.186,204679.186,204731.186,204732.186,204733.186,204734.186,204735.186,204736.186,204741.186,204742.186,204738.186,204739.186,204737.186,204740.186,204743.186,204744.186,207120.186,207121.186,207122.186,207123.186,207124.186,207125.186,207126.186,207127.186,207128.186,207129.186,207012.186,207013.186,207019.186,207020.186,207017.186,207016.186,207015.186,207014.186,204178.186,192601.186,192604.186,192605.186,204181.186,221361.186,221362.186,221363.186,221364.186,222122.186,221288.186,221290.186,221291.186,221292.186,221282.186,221281.186,221283.186,221289.186,221279.186,221286.186,221294.186,221285.186,221287.186,221293.186,221284.186,221280.186,458092.186,460544.186,524166.186,230530.186,651106.186,81226.186,213839.186,87127.186,982085.186,689143.186,448670.186,989622.186,399891.186,736122.186,344873.186,650288.186,799780.186,184112.186,270918.186,681473.186,443635.186,852706.186,550177.186,574192.186,406172.186,795722.186,848008.186,907160.186,254158.186,979908.186,244962.186,494260.186,856490.186,846052.186,512531.186,868802.186,225446.186,255301.186,475010.186,644693.186,442088.186,249753.186,146511.186,323583.186,377636.186,148974.186,639783.186,225110.186,731833.186,531416.186,326970.186,154962.186,475347.186,884101.186,83586.186,96819.186,867707.186,140553.186,625171.186,128140.186,614170.186,391773.186,693384.186,978863.186,715582.186,290203.186,182873.186,791627.186,904327.186,20560.186,666122.186,452612.186,238643.186,876231.186,24153.186,292429.186,88951.186,731554.186,2186.186,247604.186,616876.186,742169.186,284448.186,76076.186,109703.186,348224.186,90172.186,890735.186,621011.186,83120.186,93445.186,300633.186,242266.186,262570.186,577199.186,513457.186,50571.186,149570.186,115136.186,303191.186,106603.186,345494.186,262780.186,767893.186,259181.186,616747.186,653161.186,952390.186,710535.186,628914.186,29116.186,79441.186,579468.186,846325.186,970268.186,540179.186,667957.186,282966.186,874240.186,412779.186,175902.186,151144.186,86429.186,785996.186,788870.186,560904.186,803069.186,254003.186,274744.186,614481.186,318161.186,676993.186,518958.186,754685.186,786348.186,618799.186,526721.186,443804.186,868882.186,448726.186,914231.186,370424.186,431565.186,469833.186,498282.186,653575.186,273577.186,561177.186,417332.186,700168.186,228193.186,424191.186,860037.186,210207.186,472630.186,35173.186,509710.186,759506.186,336219.186,232567.186,210332.186,800494.186,351696.186,136870.186,176753.186,5354.186,658898.186,875425.186,960011.186,817070.186,115863.186,725078.186,473468.186,491835.186,102156.186,750304.186,491500.186,103318.186,310308.186,710899.186,469271.186,763744.186,134221.186,311630.186,377871.186,164675.186,674615.186,557475.186,",
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
    def as_url(self, from_date: datetime = None, to_date: datetime = None):
        # Convert string to datetime, example: "20240411" -> datetime(2024, 4, 11)
        if from_date is None and to_date is None:
            today = datetime.now().strftime('%Y%m%d')
            date_range = f"p={today}-{today}"
        elif from_date and to_date:
            # Check if from_date is greater than to_date
            if from_date > to_date:
                raise ValueError("The from_date cannot be later than the to_date.")
            date_range = f"p={from_date.strftime('%Y%m%d')}-{to_date.strftime('%Y%m%d')}"
        elif from_date:
            # Only from_date is provided, use the same date for to_date
            date_range = f"p={from_date.strftime('%Y%m%d')}-{from_date.strftime('%Y%m%d')}"
        else:  # Only to_date is provided
            date_range = f"p={to_date.strftime('%Y%m%d')}-{to_date.strftime('%Y%m%d')}"

        # Set the URL parameter
        self.key_values[2] = date_range
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
