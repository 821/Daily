FOR /D %%I IN (*) DO CD %%I&"C:\Program Files\WinRAR\winrar" u -afzip -IBCK -m5 "%%I" *.*&MOVE /Y "%%I".zip ..\&CD ..