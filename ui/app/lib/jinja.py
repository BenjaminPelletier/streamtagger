import jinja2

env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('app/templates'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)
env.globals.update(zip=zip)
env.globals.update(len=len)