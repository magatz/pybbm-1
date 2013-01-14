import bleach

TZ_CHOICES = [(float(x[0]), x[1]) for x in (
    (-12, '-12'), (-11, '-11'), (-10, '-10'), (-9.5, '-09.5'), (-9, '-09'),
    (-8.5, '-08.5'), (-8, '-08 PST'), (-7, '-07 MST'), (-6, '-06 CST'),
    (-5, '-05 EST'), (-4, '-04 AST'), (-3.5, '-03.5'), (-3, '-03 ADT'),
    (-2, '-02'), (-1, '-01'), (0, '00 GMT'), (1, '+01 CET'), (2, '+02'),
    (3, '+03'), (3.5, '+03.5'), (4, '+04'), (4.5, '+04.5'), (5, '+05'),
    (5.5, '+05.5'), (6, '+06'), (6.5, '+06.5'), (7, '+07'), (8, '+08'),
    (9, '+09'), (9.5, '+09.5'), (10, '+10'), (10.5, '+10.5'), (11, '+11'),
    (11.5, '+11.5'), (12, '+12'), (13, '+13'), (14, '+14'),
)]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title', 'class', 'target', 'rel'],
    'div': ['class', 'id', 'style'],
    'span': ['class', 'style'],
    'img': ['class', 'src', 'alt', 'title'],
    'input': ['type', 'class', 'value'],
    'iframe': ['width', 'height', 'frameborder', 'src', 'data-youtube-id', 'allowfullscreen'],
}

ALLOWED_TAGS = bleach.ALLOWED_TAGS + [
    'input',
    'div',
    'span',
    'img',
    'strike',
    'u',
    'code',
    'blockquote',
    'iframe',
    'br',
]

ALLOWED_STYLES = bleach.ALLOWED_STYLES + [
    'font-size',
    'font-family',
    'text-align',
    'list-style-type',
    'color',
]
