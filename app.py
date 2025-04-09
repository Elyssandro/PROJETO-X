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
        body {
          margin: 0;
          padding: 0;
          font-family: Arial, sans-serif;
          background: linear-gradient(to right, #ff00a2, #e0ff4f);
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
        }
        .container {
          text-align: center;
        }
        .titulo {
          max-width: 90%;
          height: auto;
          margin-bottom: 40px;
        }
        .input-link {
          display: block;
          width: 80%;
          max-width: 500px;
          margin: 10px auto;
          padding: 15px;
          border: none;
          border-radius: 30px;
          background-color: #d4ff1e;
          color: #000;
          font-size: 16px;
        }
        .btn-baixar {
          margin-top: 20px;
          padding: 15px 30px;
          border: none;
          border-radius: 30px;
          background-color: #000;
          color: #d4ff1e;
          font-size: 16px;
          cursor: pointer;
        }
        .logo {
          position: absolute;
          bottom: 10px;
          left: 10px;
          width: 100px;
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
        "noplaylist": True,
    }

    if formato == "mp3":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)
            if formato == "mp3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            nome_exibido = os.path.basename(filename)

        return f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
          <meta charset="UTF-8" />
          <title>Download Concluído</title>
          <style>
            body {{
              background: linear-gradient(to right, #d4ff1e, #ff00a2);
              font-family: Arial, sans-serif;
              text-align: center;
              padding: 50px;
            }}
            .msg {{
              background: white;
              padding: 30px;
              border-radius: 20px;
              display: inline-block;
              box-shadow: 0 0 10px rgba(0,0,0,0.2);
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

    except Exception as e:
        return f"Erro ao baixar: {str(e)}", 500

@app.route("/download/<path:nome_arquivo>")
def baixar_arquivo(nome_arquivo):
    return send_from_directory("GELADO", nome_arquivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
