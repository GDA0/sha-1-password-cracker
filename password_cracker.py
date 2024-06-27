import hashlib


def crack_sha1_hash(hash_value, use_salts=False):
    salts = []
    
    if use_salts:
        # Get all known salts from file if use salts is true
        with open("known-salts.txt") as salt_file:
            salts = salt_file.readlines()
            salts = [salt.strip() for salt in salts]

    with open("top-10000-passwords.txt", mode="r") as password_file:
        # Get all passwords to check
        passwords = password_file.readlines()
        passwords = [p.strip() for p in passwords]
        
        for password in passwords:
            if not use_salts:
                # Password check without salts
                p_crack = hashlib.sha1()
                p_crack.update(password.encode("utf-8"))
                cracked_password_hash = p_crack.hexdigest().lower()
                if cracked_password_hash == hash_value:
                    return password
            else:
                # Password check with salts
                for salt in salts:
                    append_pass = salt + password
                    prepend_pass = password + salt
                    for current_pass in [append_pass, prepend_pass]:
                        p_crack = hashlib.sha1()
                        p_crack.update(current_pass.encode("utf-8"))
                        cracked_password_hash = p_crack.hexdigest().lower()
                        if cracked_password_hash == hash_value:
                            return password

    return "PASSWORD NOT IN DATABASE"
