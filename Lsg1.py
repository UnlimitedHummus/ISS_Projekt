import komm
import numpy as np
from PIL import Image


def load_image_bits(image_path, verbose=True):
    if verbose:
        print("Loading", image_path, "and converting to bits")
    with Image.open(image_path) as image:
        image_array = np.asarray(image)
        reshaped_array = image_array.reshape((1, -1))
        image_bits = np.unpackbits(reshaped_array)
    return image_bits


def modulate(psk, image_path, verbose=True):
    if verbose:
        print("Modulating image data from:", image_path)
    data = load_image_bits(image_path)
    modulated_data = psk.modulate(data)  # modulate digital data (multiple of 2 bits)
    return modulated_data


def send_data(modulated_data, snr, verbose=True):
    if verbose:
        print("Sending data over AWGN-Channel")
    channel = komm.AWGNChannel(snr=snr, signal_power=1)  # creating new AWGNChannel
    received_data = channel(modulated_data)  # sending data over channel
    return received_data


def save_image(image_bits, image_path, verbose=True):
    if verbose:
        print("Saving image to:", image_path)
    image_bytes = np.packbits(image_bits)
    reshaped_array = image_bytes.reshape((40, 40, 4))
    Image.fromarray(reshaped_array).save(image_path)


def show_image(image_bits, verbose=True):
    if verbose:
        print("Showing image")
    image_bytes = np.packbits(image_bits)
    reshaped_array = image_bytes.reshape((40, 40, 4))
    Image.fromarray(reshaped_array).show()


def demodulate(psk, received_data, verbose=True):
    if verbose:
        print("Transmission demodulated")
    demodulated_bits = psk.demodulate(received_data)  # demodulate bits
    return demodulated_bits


def test_pipeline(image_path, show=True, verbose=True):
    psk = komm.PSKModulation(4, phase_offset=np.pi / 4)  # defining QPSK modulation

    modulated_data = modulate(psk, image_path=image_path, verbose=verbose)  # loads image from file and uses QPSK on it
    received_data = send_data(modulated_data, snr=0.99, verbose=verbose)  # simulates data transfer with loss
    demodulated_data = demodulate(psk, received_data, verbose=verbose)  # demodulates the data
    save_image(demodulated_data, "transmission.png", verbose=verbose)  # saves the transmitted image to a file

    if show:
        show_image(demodulated_data, verbose=verbose)


test_pipeline("test_image.png")
