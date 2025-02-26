from rich import print
import ytpy
x , y = ytpy.filter_json("https://music.youtube.com/watch?v=q5go1dovoeM&si=XBTW8eUYrBD8bjpV")

print(x)
print(y)    