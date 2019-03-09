from json import JSONDecoder


class ATJSONObjectParser:
    def __init__(self, text, *args, **kwargs):
        self.text = text.decode()
        self._JSONObjectPresent = False
        self._JSONObject = []
        self.JSONObjectExreact(self.text)
        # self.get_data(text)

    @property
    def JSONObjectPresent(self):
        return self._JSONObjectPresent

    @property
    def JSONObject(self):
        return self._JSONObject

    def JSONObjectExreact(self, text):
        for object in self._extract_json_objects(text):
            self._JSONObject.append(object)
        if self._JSONObject:
            self._JSONObjectPresent = True

    def _extract_json_objects(self, text, decoder=JSONDecoder()):
        """Find JSON objects in text, and yield the decoded JSON data """

        processText = "".join(text.split())
        pos = 0
        while True:
            match_c = processText.find('{', pos)
            match_s = processText.find('[', pos)
            dif = abs(match_c-match_s)
            if dif == 1:
                match = text.find('[', pos)
            else:
                match = text.find('{', pos)
            if match == -1:
                break
            try:
                result, index = decoder.raw_decode(text[match:])
                yield result
                pos = match + index
            except ValueError:
                pos = match + 1

