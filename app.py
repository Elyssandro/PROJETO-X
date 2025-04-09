from flask import Flask, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <title>Gelado</title>
      <style>
        * {
          box-sizing: border-box;
        }
        body {
          margin: 0;
          padding: 0;
          font-family: Arial, sans-serif;
          background: linear-gradient(to right, #ff00a2, #e0ff4f);
          display: flex;
          justify-content: center;
          align-items: center;
          min-height: 100vh;
        }
        .container {
          width: 100%;
          max-width: 500px;
          padding: 20px;
          text-align: center;
        }
        .titulo {
          width: 100%;
          max-width: 100%;
          height: auto;
          margin-bottom: 30px;
        }
        .input-link, select {
          width: 100%;
          padding: 15px;
          margin: 10px 0;
          border: none;
          border-radius: 30px;
          background-color: #d4ff1e;
          font-size: 16px;
        }
        .btn-baixar {
          width: 100%;
          padding: 15px;
          margin-top: 15px;
          border: none;
          border-radius: 30px;
          background-color: #000;
          color: #d4ff1e;
          font-size: 16px;
          cursor: pointer;
        }
        .logo {
          margin-top: 30px;
          width: 80px;
        }
        @media (max-width: 400px) {
          .btn-baixar, .input-link, select {
            font-size: 14px;
            padding: 12px;
          }
        }
      </style>
    </head>
    <body>
      <div class="container">
        <img src="/BAIXE.png" alt="Baixe Suas Músicas e Vídeos" class="titulo"/>
        <form action="/baixar" method="POST">
          <input type="text" name="link" placeholder="COLE O LINK AQUI" class="input-link" required />
          <select name="formato" class="input-link">
            <option value="mp3">MP3</option>
            <option value="mp4">MP4</option>
          </select>
          <button type="submit" class="btn-baixar">BAIXAR</button>
        </form>
        <img src="/logo.png" alt="Logo Gelado" class="logo"/>
      </div>
    </body>
    </html>
    '''

@app.route("/BAIXE.png")
def get_baixe():
    return send_from_directory(".", "BAIXE.png")

@app.route("/logo.png")
def get_logo():
    return send_from_directory(".", "logo.png")

@app.route("/baixar", methods=["POST"])
def baixar():
    link = request.form["link"]
    formato = request.form["formato"]

    pasta = "GELADO"
    os.makedirs(pasta, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best" if formato == "mp3" else "best",
        "outtmpl": os.path.join(pasta, "%(title)s.%(ext)s"),
    }

    if formato == "mp3":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=True)
        filename = ydl.prepare_filename(info)
        if formato == "mp3":
            filename = filename.rsplit(".", 1)[0] + ".mp3"
        filename = os.path.join(pasta, os.path.basename(filename))
        nome_exibido = os.path.basename(filename)

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8" />
      <title>Download Concluído</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
      <style>
        body {{
          background: linear-gradient(to right, #d4ff1e, #ff00a2);
          font-family: Arial, sans-serif;
          text-align: center;
          padding: 30px;
        }}
        .msg {{
          background: white;
          padding: 20px;
          border-radius: 20px;
          display: inline-block;
          box-shadow: 0 0 10px rgba(0,0,0,0.2);
          max-width: 90%;
        }}
        a {{
          display: inline-block;
          margin-top: 20px;
          padding: 10px 20px;
          background: #000;
          color: #d4ff1e;
          border-radius: 30px;
          text-decoration: none;
        }}
      </style>
    </head>
    <body>
      <div class="msg">
        <h2>✅ Baixado com sucesso!</h2>
        <p>O arquivo <strong>{nome_exibido}</strong> foi salvo na pasta <strong>GELADO</strong>.</p>
        <a href="/download/{nome_exibido}" download>Clique aqui para baixar agora</a>
      </div>
    </body>
    </html>
    """

@app.route("/download/<path:nome_arquivo>")
def baixar_arquivo(nome_arquivo):
    return send_from_directory("GELADO", nome_arquivo, as_attachment=True)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
