import ipywidgets as ipw

def get_start_widget(appbase, jupbase):
    #http://fontawesome.io/icons/
    template = """
    <table>
    <tr>
    
    <td valign="top"><ul>
    <li><a href="{appbase}/mfh.ipynb" target="_blank">MFH TB</a>
    </ul></td>
    
    </tr>
    </table>
"""
    
    html = template.format(appbase=appbase, jupbase=jupbase)
    return ipw.HTML(html)
    
#EOF
