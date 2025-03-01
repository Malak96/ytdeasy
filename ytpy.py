from rich import print  
from rich.console import Console
from rich.table import Table
import subprocess
import json
console = Console()

def read_link (url):
    
    command = ["C:/Users/angel/OneDrive/Documentos/ytdeasy/yt-dlp.exe", "--no-warnings","--no-playlist", "--cookies","./cookies.txt", "-q", "-j", url]
    #command = ["./yt-dlp.exe", "--no-warnings","--no-playlist", "-q", "-j", url]
    salida = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        resultado_json = json.loads(salida.stdout)
    except json.JSONDecodeError:
        print("Error al decodificar el JSON.")
        return []

    formatos_filtrados = [
        {
            "format_id": f.get("format_id", None),
            "ext": f.get("ext", None),
            "resolution": f.get("resolution", None),
            "filesize": f.get("filesize", None),
            "fps": f.get("fps", None),
            "vcodec": f.get("vcodec", None),
            "acodec": f.get("acodec", None),
            "format_note": f.get("format_note",None),
            "vbr": f.get("vbr",None),
            "abr": f.get("abr",None)
        }
        for f in resultado_json.get('formats', [])
    ]
    return formatos_filtrados
    
    
def filter_json(url):
    a_table=[]
    v_table=[]
    formatos = read_link(url)
    if not formatos:
        print("No se encontraron formatos disponibles.")
        return
    
    for f in formatos:
        if f["filesize"] is not None:
            try:
                size=["B","KB","MB","GB","?"]
                count_size=0
                filesize_kb = f['filesize']
                while True:
                    if filesize_kb >= 1024:
                        count_size=count_size+1
                        filesize_kb = int(filesize_kb) / 1024
                    else:
                        break
                if count_size < 5: 
                    filesize_kb = f"{filesize_kb:.2f}{size[count_size]}"
                else: 
                    filesize_kb = f"{filesize_kb:.2f}{size[4]}"
            except (ValueError, TypeError):
                filesize_kb = None
        else:
            filesize_kb = None
        
        vcodec = f.get("vcodec", None)
        try:
            if vcodec != None:
                if vcodec=="none"or vcodec=="None":vcodec=None
                if "avc" in vcodec: vcodec = f"{vcodec}(x264)"
        except(ValueError,TypeError):
            vcodec = None
            
        try:
            acodec = (f["acodec"])
            if acodec == "None" or acodec == "none": acodec=None
        except(ValueError,TypeError):
            acodec = None
            
        try:
            fps = str(f["fps"]) + "FPS"
            if fps == "None" or fps == "none": fps=""
            
        except(ValueError,TypeError):
            fps = ""
        # if vcodec == None and acodec != None:
        #     #a_table.add_row(f["format_id"], f["ext"], filesize_kb, str(f["abr"]), acodec, f["format_note"])
        #     a_table.append(f"{f["format_id"]} - {f["ext"]} - {filesize_kb} - {str(f["abr"])}kbps - {acodec} - {f["format_note"]}")
            
        # elif vcodec != None:
        #     #v_table.add_row(f["format_id"], f["ext"], f["resolution"], filesize_kb, fps, str(f["vbr"]), vcodec, f["format_note"])
        #     v_table.append(f"{f["format_id"]} - {f["ext"]} - {f["resolution"]} - {filesize_kb} - {fps} - {str(f["vbr"])}kbps - {vcodec} - {f["format_note"]}")

        if vcodec is None and acodec is not None:
            a_table.append((
                f"{f['ext']}|{filesize_kb}|{str(f['abr'])}kbps|{acodec}|{f['format_note']}",
                f["format_id"]
            ))

        elif vcodec is not None:
            v_table.append(( 
                f"{f['ext']}|{f['resolution']}|{filesize_kb}|{fps}|{str(f['vbr'])}kbps|{vcodec}|{f['format_note']}",
                f["format_id"]
            ))

    return a_table, v_table

    """
    command =["./yt-dlp.exe", "--no-warnings","-q", "-j", url]
    #salida = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    salida = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        resultado_json = json.loads(salida.stdout)
    except json.JSONDecodeError:
        print("Error al decodificar el JSON.")
        return []
    formatos_filtrados = [formato for formato in resultado_json.get('formats', []) if 'format_id' in formato]

    return formatos_filtrados
    """


if __name__ == "__main__":
    print(None)
