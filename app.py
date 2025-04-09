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

    try:
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
        return f"""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
          <meta charset="UTF-8" />
          <title>Erro ao Baixar</title>
          <style>
            body {{
              background: linear-gradient(to right, #ff0000, #ffe600);
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
              color: #fff700;
              border-radius: 30px;
              text-decoration: none;
            }}
          </style>
        </head>
        <body>
          <div class="msg">
            <h2>❌ Erro ao baixar o vídeo</h2>
            <p>Verifique se o link é válido, público e não exige login ou confirmação de idade.</p>
            <a href="/">Voltar para a página inicial</a>
          </div>
        </body>
        </html>
        """
