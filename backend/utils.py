def normalize(text):
    words = text.lower().replace(",", " ").split()
    return set([w.rstrip('s') for w in words])