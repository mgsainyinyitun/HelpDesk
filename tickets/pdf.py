from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa;

def render_to_pdf(template_src,content_dict = {}):
    template = get_template(template_src);
    html = template.render(content_dict);
    result = BytesIO();

    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result);
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type = 'application/pdf')
    return None;

    