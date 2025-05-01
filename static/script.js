$(document).ready(function () {
    $('#generateKeys').click(function () {
        $.ajax({
            url: '/key_gen',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({}),
            success: function (response) {
                $('#publicKeyDisplay').val(response.public_key);
                $('#privateKeyDisplay').val(response.private_key);
            },
            error: function () {
                alert('Failed to generate keys.');
            }
        });
    });

    $('#encryptBtn').click(function () {
        const message = $('#messageInput').val();
        if (!message) {
            alert('Please enter a message to encrypt.');
            return;
        }

        $.ajax({
            url: '/encryption',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ message: message }),
            success: function (response) {
                $('#encryptResult').html(`
                    <p><strong>Encrypted Message:</strong></p>
                    <textarea readonly rows="4" style="width:100%;">${response.encrypted_msg}</textarea>
                    <p><strong>Encapsulated Ciphertext (Base64):</strong></p>
                    <textarea readonly rows="4" style="width:100%;">${response.ciphertext}</textarea>
                `);
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.error || 'Encryption failed.');
            }
        });
    });

    $('#decryptBtn').click(function () {
        const encryptedMsg = $('#encryptedInput').val();
        if (!encryptedMsg) {
            alert('Please enter an encrypted message to decrypt.');
            return;
        }

        $.ajax({
            url: '/decryption',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ encrypted_msg: encryptedMsg }),
            success: function (response) {
                $('#decryptResult').html(`
                    <p><strong>Decrypted Message:</strong></p>
                    <textarea readonly rows="4" style="width:100%;">${response.decrypted_msg}</textarea>
                `);
            },
            error: function (xhr) {
                alert(xhr.responseJSON?.error || 'Decryption failed.');
            }
        });
    });
});