import json
from flask import Flask, send_file, request
from spiegelen import mirror_filter
from zwart_wit import zwart_wit_filter
from binary_hackerman import binary_filter
from contrast import contrast_filter
from colorshift import color_shifter_filter
from neon import neon_filter
from driehoeken import driehoekFilter
from cirkel import cirkelFilter

app = Flask(__name__)


@app.route('/cirkel', methods=['POST'])
def cirkel_page():
    cirkel_filter_image = image_getter("cirkel")
    return cirkel_filter_image


@app.route('/driehoek', methods=['POST'])
def driehoek_page():
    print('test')
    driehoek_filter_image = image_getter("driehoek")
    return driehoek_filter_image


@app.route('/neon', methods=['POST'])
def neon_page():
    neon_filter_image = image_getter("neon")
    return neon_filter_image


@app.route('/mirror', methods=['POST'])
def mirror_page():
    mirror_filter_image = image_getter("mirror")
    return mirror_filter_image


@app.route('/zwart_wit', methods=['POST'])
def zwart_wit_page():
    zwart_wit_filter_image = image_getter("zwart_wit")
    return zwart_wit_filter_image


@app.route('/binary', methods=['POST'])
def binary_page():
    binary_filter_image = image_getter("binary")
    return binary_filter_image


@app.route('/contrast', methods=['POST'])
def contrast_page():
    contrast_filter_image = image_getter("contrast")
    return contrast_filter_image


@app.route('/color_shift', methods=['POST'])
def color_shift_page():
    color_shift_filter_image = image_getter("color_shift")
    return color_shift_filter_image


def image_getter(filter_selector):
    my_json = request.data.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    image = data['data'].replace('\n', '').encode('ascii')

    returned_image = ''

    if filter_selector == "mirror":
        returned_image = mirror_filter(image)
    if filter_selector == "zwart_wit":
        returned_image = zwart_wit_filter(image)
    if filter_selector == "binary":
        returned_image = binary_filter(image)
    if filter_selector == "contrast":
        returned_image = contrast_filter(image)
    if filter_selector == "color_shift":
        returned_image = color_shifter_filter(image)
    if filter_selector == "neon":
        returned_image = neon_filter(image)
    if filter_selector == "driehoek":
        returned_image = driehoekFilter(image)
    if filter_selector == "cirkel":
        returned_image = cirkelFilter(image, 100)
    return returned_image


#hier komen meer filters zodra ze af zijn
if __name__ == '__main__':
    app.run(host='192.168.2.10', port=5000, debug=True)
