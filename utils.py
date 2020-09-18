import re
from htmlmin import minify
import lxml.html.clean as clean
from lxml.html.clean import Cleaner
import json


"""

Set of fuctions for analysis and parsering usage.

"""

#Function a clear html leaving only tags and content. Can be changed. Posterior minify.
def clean_and_minify_html(html):
    safe_attrs = clean.defs.safe_attrs
    cleaner = Cleaner(page_structure=True,
                      safe_attrs_only=True, safe_attrs=frozenset())
    html = re.sub(r'\bencoding="[-\w]+"', '', html)
    html = re.sub("<\\?xml.*?\\?>", "", html)
    html = cleaner.clean_html(html)
    html = html.replace("\n", "").replace("\r", "").replace(
        "\t", "").replace("\\n", "").replace("\\\n", "")
    html = minify(html, remove_comments=True, remove_empty_space=True)
    return html

#Return a list of the value of a key in a list of dictionaries.
def extract_value_from_list_of_dicts(list_dicts, key):
    return [y[key] for y in list_dicts if key in y][0]

#Path to access the htmls with and without javascript for analysis.
path_htmls_no_js = "../mastercrawlerTFG/mastercrawler/htmls_no_JS/"
path_htmls_js = "../seleniumCrawler/htmls_js/"

#Get the htmls with and without JS. Extract URL, domain and percentage of change of them.
def extract_tool_from_json_and_parse(filename):
    with open(f"{path_htmls_no_js}{filename}", "r") as fp:
        tool_no_js = json.load(fp)
    with open(f"{path_htmls_js}{filename}", "r") as l:
        tool_js = json.load(l)
    final_url = extract_value_from_list_of_dicts(tool_no_js, 'final_url_tool')
    domain = final_url.split('//')[-1].split("/")[0].replace("www.", "")
    html_no_js = clean_and_minify_html(
        extract_value_from_list_of_dicts(tool_no_js, 'html_no_js'))
    html_js = clean_and_minify_html(
        extract_value_from_list_of_dicts(tool_js, 'html_js'))
    percentage_of_change = (1-(len(html_no_js)/len(html_js)))*100
    return final_url, domain, percentage_of_change
