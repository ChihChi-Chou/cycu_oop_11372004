lyrics = '''
When you're weary
Feeling small
When tears are in your eyes
I will dry them all
I'm on your side
Oh, when times get rough
And friends just can't be found
Like a bridge over troubled water
I will lay me down
Like a bridge over troubled water
I will lay me down
When you're down and out
When you're on the street
When evening falls so hard
I will comfort you
I'll take your part
Oh, when darkness comes
And pain is all around
Like a bridge over troubled water
I will lay me down
Like a bridge over troubled water
I will lay me down
Sail on, silver girl
Sail on by
Your time has come to shine
All your dreams are on their way
See how they shine
Oh, if you need a friend
I'm sailing right behind
Like a bridge over troubled water
I will ease your mind
Like a bridge over troubled water
I will ease your mind
'''

def count_silence(lyrics, word= 'bridge'):
    count = 0
    words = lyrics.lower().split()
    for word in words:
        if word == 'bridge':
            count += 1
    return count

print(count_silence(lyrics))