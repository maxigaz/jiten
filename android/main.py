import sys
if isinstance(getattr(sys.stdout, "buffer", None), str):
  print("Fixing stdout/stderr...")
  import androidembed
  class LogFile:
    def __init__(self):
      self.__buf = ""
    def write(self, s):
      s = self.__buf + s
      lines = s.split("\n")
      for l in lines[:-1]:
        androidembed.log(l)
      self.__buf = lines[-1]
    def flush(self):
      return
  sys.stdout = sys.stderr = LogFile()

import os
if os.path.exists(os.path.join(os.environ["ANDROID_PRIVATE"], "__debug__")):
  print("*** DEBUG MODE ***")
  os.environ["FLASK_ENV"] = "development"

  from jiten.app import app
  @app.route("/__debug__")
  def r_debug(): raise RuntimeError

from jiten.cli import serve_app
serve_app(True, "localhost", 29483, use_reloader = False)
