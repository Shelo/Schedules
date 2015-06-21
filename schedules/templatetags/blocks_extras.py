from django.templatetags.tz import register

@register.filter
def day(blocks, index):
    if index in blocks:
        return blocks[index]

    return {}

@register.filter
def block(blocks, index):
    if index in blocks:
        return blocks[index]

    return []

@register.filter
def existblock(blocks, index):
    if index in blocks:
        return True

    return False

@register.filter
def rawblock(blocks, index):
    if index in blocks:
        return blocks[index]

    return None

@register.filter
def percentage(quantity, total):
    if total == 0:
        return 0

    if quantity is None:
        return 100

    return len(quantity) * 100 / total

@register.filter
def tooltip(block):
    if len(block) == 0:
        return u'No members.'
    else:
        return ", ".join(block)