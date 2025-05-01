from flask import Flask, render_template, request, jsonify
import utils  

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/key_gen', methods=['POST'])
def create_public_and_private_key():
    try:
        publi_key, privat_key = utils.key_creation()
        return jsonify({
            'message': 'Keys generated successfully.',
            'private_key': privat_key,
            'public_key': publi_key
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/encryption', methods=['POST'])
def encryption():
    msg = request.json.get('message')
    if not msg:
        return jsonify({'error': 'Message is required.'}), 400
    try:
        encrypted_msg, cipher = utils.mes_enc(msg)
        return jsonify({'encrypted_msg': encrypted_msg, 'ciphertext': cipher})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decryption', methods=['POST'])
def decryption():
    enc_msg = request.json.get('encrypted_msg')
    if not enc_msg:
        return jsonify({'error': 'Encrypted message required.'}), 400
    try:
        decrypted_msg = utils.mes_dry(enc_msg)
        return jsonify({'decrypted_msg': decrypted_msg})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
