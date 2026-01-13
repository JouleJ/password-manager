import secrets
import string


def shuffle_list(xs):
    size = len(xs)
    if size > 1:
        for idx in range(1, size):
            other = secrets.randbelow(idx + 1)
            if other != idx:
                xs[idx], xs[other] = xs[other], xs[idx]
            

def generate_password(n_uppercase=10, n_lowercase=5, n_digits=5, n_other=3):
    char_list = [secrets.choice(string.ascii_uppercase) for _ in range(n_uppercase)]
    char_list.extend([secrets.choice(string.ascii_lowercase) for _ in range(n_lowercase)])
    char_list.extend([secrets.choice(string.digits) for _ in range(n_digits)])
    char_list.extend([secrets.choice(string.punctuation) for _ in range(n_other)])

    shuffle_list(char_list)
    return ''.join(char_list)
