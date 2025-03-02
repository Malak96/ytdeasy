from rich import print
import ytpy
x , y,t ,z = ytpy.filter_json("https://music.youtube.com/watch?v=q5go1dovoeM&si=XBTW8eUYrBD8bjpV")

print(x)
print(y) 
print(t)
# Suponiendo que buscas un ID específico
buscado_id = "160"
resultado = [f for f in z if f["format_id"] == buscado_id]

# Mostrar los resultados
if resultado:
    print("Formato encontrado:", resultado[0]['resolution'])
else:
    print("No se encontró el formato con ese ID.")

