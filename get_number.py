from flask_restful import Resource, reqparse
from preprocessing_1 import find_array as find_array_1
from preprocessing import find_array
from preprocessing_1 import find_array as find_array_1
from flask_restful import request
from PIL import Image


class GetNumber(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("image")
    def get(self):

        data = self.parser.parse_args()
        im =Image.open(request.files["image"])
        im = im.convert("RGB")

        a = len(find_array(im))
        b = len(find_array_1(im))
        mean = (a + b) / 2
        return int(mean)
