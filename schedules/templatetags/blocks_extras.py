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

    return 0

@register.filter
def block_percentage(quantity, total):
    if total == 0:
        return 0

    return quantity * 100 / total
