from analyzer import analyze, trace


stack = []


@trace(stack)
def mystery(x):
    if x > 0:
        return mystery(x - 1) * x
    else:
        return 1


mystery(5)


analyze(mystery, stack)
